// Offline probe: evaluate the actual tracker in a synthetic browser context.
// No browser automation, network, cookies or user data are accessed.
// Run: node analytics-payload-probe.js /path/to/healthyaa-wordpress
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = process.argv[2];
if (!root) throw new Error('Source root required');
let source = fs.readFileSync(path.join(root, 'public_html/wp-content/mu-plugins/healthyaa-analytics/assets/analytics-tracker.js'), 'utf8');
const insertion = "\tif (document.readyState === 'loading') {";
if (source.split(insertion).length !== 2) throw new Error('Unexpected source shape');
source = source.replace(insertion, '\twindow.syntheticPayload = payload;\n' + insertion);
const store = () => ({ getItem: () => null, setItem: () => {}, removeItem: () => {} });
const url = 'https://example.test/checkout/order-received/1/?key=synthetic-order-key&email=visitor%40example.test#synthetic-fragment';
const browser = {
 healthyaaAnalytics: { endpoint: 'https://example.test/admin-ajax.php', action: 'synthetic' },
 location: { href: url, search: '?key=synthetic-order-key&email=visitor%40example.test', protocol: 'https:' },
 localStorage: store(), sessionStorage: store(), screen: {width:100,height:100},
 crypto: { randomUUID: () => 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' },
 fetch: () => { throw new Error('Network must not be invoked'); }
};
vm.runInNewContext(source, {window:browser, navigator:{userAgent:'Synthetic',language:'en'}, document:{title:'Synthetic',referrer:'',readyState:'loading',addEventListener:()=>{}}, URLSearchParams, Intl});
const payload = browser.syntheticPayload('synthetic');
const results = {
 mode: 'actual payload function in synthetic JavaScript context; no requests sent',
 complete_url_retained: payload.page_url === url,
 query_order_key_retained: payload.page_url.includes('key=synthetic-order-key'),
 query_email_retained: payload.page_url.includes('email='),
 fragment_retained: payload.page_url.includes('#synthetic-fragment')
};
console.log(JSON.stringify(results,null,2));
if (Object.values(results).includes(false)) process.exit(1);
