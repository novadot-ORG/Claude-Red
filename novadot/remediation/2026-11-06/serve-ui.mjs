// Local browser QA only. Build first, then run from the project:
//   npm run build
//   node tests/forms/serve-ui.mjs
// Open http://127.0.0.1:4340/contact/ or /events/ and use synthetic details.
// Scenario emails: success@example.org, invalid@example.org,
// unavailable@example.org, uncertain@example.org, expired@example.org.
// GET /__qa/report gives the same sanitized summary saved under .release/.
// Restart the server to reset its counters and mock request records.
// No real credentials, PHP execution, external requests, or email delivery.

import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { mkdir, readFile, realpath, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { policyFromApache } from '../../scripts/security-policy.mjs';

const project = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const root = await realpath(resolve(project, 'dist'));
const policy = policyFromApache(await readFile(resolve(root, '.htaccess'), 'utf8'));
if ((await readFile(resolve(root, 'index.html'), 'utf8')).includes('data-site=')) {
  throw new Error('Use npm run build (review mode) before local QA; production analytics must not run locally.');
}
const reportPath = resolve(project, '.release/forms-ui-requests.json');
const port = 4340;
const localHosts = new Set([`127.0.0.1:${port}`, `localhost:${port}`]);
const knownFields = new Set(['name', 'email', 'organisation', 'problem', 'consequence', 'system', 'timing', 'phone', 'preference', 'intent', 'room', 'attendees', 'targetDate', 'details', 'privacy']);
const uuidPattern = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const requests = new Map();
const report = { startedAt: new Date().toISOString(), tokenRequests: 0, posts: [], unexpectedNativeRequests: [] };
const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml; charset=utf-8',
};
await mkdir(dirname(reportPath), { recursive: true });
let writeQueue = Promise.resolve();
const save = () => {
  const summary = JSON.stringify(report, null, 2) + '\n';
  writeQueue = writeQueue.then(() => writeFile(reportPath, summary));
  return writeQueue;
};
await save();

const json = (response, status, value) => {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  response.end(JSON.stringify(value));
};
const rejected = (response, status, code, message, fields) => json(response, status, { ok: false, code, message, ...(fields ? { fields } : {}) });
const readBody = async (request, retain) => {
  let bytes = 0;
  const chunks = [];
  for await (const chunk of request) {
    bytes += chunk.length;
    if (bytes > 65536) throw new Error('body_limit');
    if (retain) chunks.push(chunk);
  }
  return { bytes, text: retain ? Buffer.concat(chunks).toString('utf8') : '' };
};

const server = createServer(async (request, response) => {
  response.setHeader('Cache-Control', 'no-store');
  response.setHeader('X-Content-Type-Options', 'nosniff');
  response.setHeader('Content-Security-Policy', policy);
  try {
    if (!localHosts.has(request.headers.host)) return rejected(response, 403, 'local_only', 'Local QA only.');
    if (request.headers.origin && !localHosts.has(new URL(request.headers.origin).host)) return rejected(response, 403, 'local_only', 'Local QA only.');
    const url = new URL(request.url, `http://127.0.0.1:${port}`);
    if (url.pathname === '/api/enquiry.php') {
      if (request.method === 'GET') {
        report.tokenRequests++;
        await save();
        return json(response, 200, { token: `qa-token-${report.tokenRequests}` });
      }
      if (request.method !== 'POST') return rejected(response, 405, 'method', 'Use GET or POST.');
      const { text } = await readBody(request, true);
      let body;
      try { body = JSON.parse(text); } catch { return rejected(response, 400, 'invalid_json', 'Invalid JSON.'); }
      if (!body || typeof body !== 'object' || !body.fields || typeof body.fields !== 'object') return rejected(response, 400, 'invalid', 'Invalid mock request.');
      const requestId = typeof body.request_id === 'string' && uuidPattern.test(body.request_id) ? body.request_id : 'invalid';
      const kind = ['contact', 'event'].includes(body.kind) ? body.kind : 'invalid';
      const keys = Object.keys(body.fields);
      const digest = createHash('sha256').update(JSON.stringify({ kind, fields: body.fields, website: body.website })).digest('hex');
      let stored = requests.get(requestId);
      const conflict = stored && stored.digest !== digest;
      if (!stored && requestId !== 'invalid') {
        stored = { digest, attempts: 0, accepted: false };
        requests.set(requestId, stored);
      }
      if (stored) stored.attempts++;
      let status = 202;
      let code = 'accepted';
      let fieldErrors;
      if (requestId === 'invalid' || kind === 'invalid' || typeof body.token !== 'string' || !body.token.startsWith('qa-token-')) {
        status = 400; code = 'invalid';
      } else if (conflict) {
        status = 409; code = 'request_conflict';
      } else if (stored.accepted) {
        status = 200;
      } else {
        switch (body.fields.email) {
          case 'success@example.org': break;
          case 'invalid@example.org':
            status = 422; code = 'validation'; fieldErrors = { organisation: 'Please check your organisation name.' }; break;
          case 'unavailable@example.org': status = 503; code = 'unavailable'; break;
          case 'uncertain@example.org': status = 502; code = 'delivery_unknown'; break;
          case 'expired@example.org':
            if (stored.attempts === 1) { status = 403; code = 'token_expired'; }
            break;
          default: status = 400; code = 'qa_scenario';
        }
      }
      if (code === 'accepted' && stored) stored.accepted = true;
      report.posts.push({
        kind, request_id: requestId, field_keys: keys.filter((key) => knownFields.has(key)).sort(),
        unknownFieldCount: keys.filter((key) => !knownFields.has(key)).length,
        attempt: stored?.attempts || 1, status, code,
      });
      await save();
      return code === 'accepted'
        ? json(response, status, { ok: true, status: 'accepted', reference: requestId })
        : rejected(response, status, code, 'Synthetic QA response. No email was sent.', fieldErrors);
    }

    // Count unexpected native requests without saving URLs, queries or bodies.
    if (!['GET', 'HEAD'].includes(request.method) || [...url.searchParams.keys()].some((key) => knownFields.has(key))) {
      const { bytes } = await readBody(request, false);
      report.unexpectedNativeRequests.push({ method: request.method, bodyBytes: bytes, queryFieldCount: [...url.searchParams.keys()].length });
      await save();
      return rejected(response, 400, 'unexpected_native_submission', 'Unexpected native submission captured locally.');
    }
    if (url.pathname === '/__qa/report') return json(response, 200, report);
    if (url.pathname === '/__qa/csp') {
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return response.end(`<!doctype html><html><head><title>CSP regression check</title></head><body>
        <h1>CSP regression check</h1><p id="result">Running...</p>
        <button id="probe" onclick="window.unsafeHandler=true">Event handler probe</button>
        <script>window.unsafeInline=true</script><script src="/__qa/csp.js" defer></script>
        </body></html>`);
    }
    if (url.pathname === '/__qa/csp.js') {
      response.writeHead(200, { 'Content-Type': 'text/javascript; charset=utf-8' });
      return response.end(`document.getElementById('probe').click();
        let evalBlocked = false; try { (0, eval)('window.unsafeEval=true'); } catch { evalBlocked = true; }
        const passed = !window.unsafeInline && !window.unsafeHandler && evalBlocked;
        document.getElementById('result').textContent = passed
          ? 'PASS: unapproved inline script, event handler and eval blocked; same-origin script ran.'
          : 'FAIL: CSP regression';`);
    }

    let path;
    try { path = decodeURIComponent(url.pathname); } catch { return rejected(response, 400, 'path', 'Invalid path.'); }
    if (path.split('/').some((segment) => segment.startsWith('.')) || path.includes('\0') || path.includes('\\')) return rejected(response, 404, 'not_found', 'Not found.');
    let file = resolve(root, '.' + path);
    if (file !== root && !file.startsWith(root + sep)) return rejected(response, 404, 'not_found', 'Not found.');
    try {
      if ((await stat(file)).isDirectory()) file = resolve(file, 'index.html');
      file = await realpath(file);
      if (!file.startsWith(root + sep) || !types[extname(file)]) return rejected(response, 404, 'not_found', 'Not found.');
      const bytes = await readFile(file);
      response.writeHead(200, { 'Content-Type': types[extname(file)] });
      response.end(request.method === 'HEAD' ? undefined : bytes);
    } catch {
      rejected(response, 404, 'not_found', 'Not found. Build dist before running this server.');
    }
  } catch (error) {
    rejected(response, error.message === 'body_limit' ? 413 : 400, 'qa_request', 'Invalid local QA request.');
  }
});
server.listen(port, '127.0.0.1', () => {
  console.log(`Mock form QA listening at http://127.0.0.1:${port}/contact/ and /events/ (PID ${process.pid}).`);
  console.log(`Sanitized report: ${reportPath}`);
});
server.on('error', (error) => { console.error(`QA server failed: ${error.code || 'unknown'}`); process.exitCode = 1; });
process.on('SIGINT', () => server.close());
process.on('SIGTERM', () => server.close());
