(function () {
  const config = window.HealthyaaAIConfig;
  if (!config) {
    return;
  }

  const root = document.getElementById('healthyaa-ai-assistant-root');
  if (!root) {
    return;
  }

  const state = {
    open: false,
    loading: false,
    sessionId: getSessionId(),
    nextMessageId: 1,
    scrollTargetId: null,
    scrollMode: 'bottom',
    messages: [
      {
        id: 0,
        role: 'assistant',
        text: config.greeting
      }
    ]
  };

  root.innerHTML = `
    <button class="healthyaa-ai-launcher" type="button" aria-expanded="false" aria-controls="healthyaa-ai-panel">
      <span class="healthyaa-ai-launcher__icon" aria-hidden="true">?</span>
      <span class="healthyaa-ai-launcher__label">${escapeHtml(config.openLabel)}</span>
    </button>
    <section class="healthyaa-ai-panel" id="healthyaa-ai-panel" hidden>
      <header class="healthyaa-ai-panel__header">
        <div>
          <h2>${escapeHtml(config.title)}</h2>
          <p>${escapeHtml(config.subtitle)}</p>
        </div>
        <button class="healthyaa-ai-panel__close" type="button" aria-label="Close assistant">×</button>
      </header>
      <div class="healthyaa-ai-panel__messages" aria-live="polite"></div>
      <form class="healthyaa-ai-panel__form">
        <label class="healthyaa-ai-panel__hint">${escapeHtml(config.privacyNotice)}</label>
        <div class="healthyaa-ai-panel__composer">
          <textarea rows="2" maxlength="${Number(config.maxMessageLen || 1200)}" placeholder="${escapeAttr(config.placeholder)}"></textarea>
          <button type="submit">Send</button>
        </div>
      </form>
    </section>
  `;

  const launcher = root.querySelector('.healthyaa-ai-launcher');
  const panel = root.querySelector('.healthyaa-ai-panel');
  const closeButton = root.querySelector('.healthyaa-ai-panel__close');
  const messagesEl = root.querySelector('.healthyaa-ai-panel__messages');
  const form = root.querySelector('.healthyaa-ai-panel__form');
  const textarea = root.querySelector('textarea');

  launcher.addEventListener('click', function () {
    state.open = !state.open;
    panel.hidden = !state.open;
    root.classList.toggle('healthyaa-ai-assistant-root--open', state.open);
    launcher.setAttribute('aria-expanded', state.open ? 'true' : 'false');
    if (state.open) {
      textarea.focus();
    }
  });

  closeButton.addEventListener('click', function () {
    state.open = false;
    panel.hidden = true;
    root.classList.remove('healthyaa-ai-assistant-root--open');
    launcher.setAttribute('aria-expanded', 'false');
  });

  textarea.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter' || event.shiftKey || event.isComposing) {
      return;
    }

    event.preventDefault();
    if (state.loading || !textarea.value.trim()) {
      return;
    }

    if (typeof form.requestSubmit === 'function') {
      form.requestSubmit();
      return;
    }

    form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  });

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (state.loading) {
      return;
    }

    const value = textarea.value.trim();
    if (!value) {
      return;
    }

    clearLeadPrompts();
    appendMessage('user', value);
    textarea.value = '';
    state.loading = true;
    renderMessages();

    try {
      const payload = await sendRequest({
        message: value,
        session_id: state.sessionId,
        page_context: buildPageContext()
      });

      appendMessage(
        'assistant',
        payload.reply || config.unavailable,
        payload.suggested_products || [],
        payload.sources || [],
        payload.handoff || null,
        payload.lead_capture || null
      );
    } catch (error) {
      appendMessage('assistant', error.message || config.unavailable, [], [], {
        show_whatsapp: true,
        show_contact: true
      });
    } finally {
      state.loading = false;
      renderMessages();
    }
  });

  messagesEl.addEventListener('submit', async function (event) {
    const leadForm = event.target.closest('.healthyaa-ai-lead-form');
    if (!leadForm) {
      return;
    }

    event.preventDefault();
    if (state.loading) {
      return;
    }

    const stageInput = leadForm.querySelector('input[name="lead_stage"]');
    const stage = stageInput ? stageInput.value : '';
    const nameInput = leadForm.querySelector('input[name="lead_name"]');
    const emailInput = leadForm.querySelector('input[name="lead_email"]');
    const name = nameInput ? nameInput.value.trim() : '';
    const email = emailInput ? emailInput.value.trim() : '';

    state.loading = true;
    clearLeadPrompts();
    renderMessages();

    try {
      const payload = await sendRequest({
        message: '',
        session_id: state.sessionId,
        page_context: buildPageContext(),
        lead: {
          action: 'submit',
          stage,
          name,
          email
        }
      });

      appendMessage('assistant', payload.reply || config.unavailable, [], payload.sources || [], payload.handoff || null, payload.lead_capture || null);
    } catch (error) {
      appendMessage('assistant', error.message || config.unavailable, [], [], {
        show_whatsapp: true,
        show_contact: true
      });
    } finally {
      state.loading = false;
      renderMessages();
    }
  });

  messagesEl.addEventListener('click', async function (event) {
    const skipButton = event.target.closest('.healthyaa-ai-lead-skip');
    if (!skipButton) {
      return;
    }

    event.preventDefault();
    if (state.loading) {
      return;
    }

    state.loading = true;
    clearLeadPrompts();
    renderMessages();

    try {
      const payload = await sendRequest({
        message: '',
        session_id: state.sessionId,
        page_context: buildPageContext(),
        lead: {
          action: 'skip',
          stage: skipButton.getAttribute('data-stage') || ''
        }
      });

      appendMessage('assistant', payload.reply || config.unavailable, [], payload.sources || [], payload.handoff || null, payload.lead_capture || null);
    } catch (error) {
      appendMessage('assistant', error.message || config.unavailable, [], [], {
        show_whatsapp: true,
        show_contact: true
      });
    } finally {
      state.loading = false;
      renderMessages();
    }
  });

  renderMessages();

  function buildPageContext() {
    return Object.assign({}, config.pageContext || {}, {
      url: window.location.href
    });
  }

  async function sendRequest(body) {
    const response = await textContentconfig.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.message || config.unavailable);
    }

    if (payload.session_id) {
      state.sessionId = payload.session_id;
      localStorage.setItem('healthyaa-ai-session-id', state.sessionId);
    }

    return payload;
  }

  function clearLeadPrompts() {
    state.messages = state.messages.map(function (message) {
      if (message.leadCapture && message.leadCapture.status === 'prompt') {
        return Object.assign({}, message, { leadCapture: null });
      }

      return message;
    });
  }

  function appendMessage(role, text, suggestions, sources, handoff, leadCapture) {
    const message = {
      id: state.nextMessageId++,
      role,
      text,
      suggestions: Array.isArray(suggestions) ? suggestions : [],
      sources: Array.isArray(sources) ? sources : [],
      handoff: handoff || null,
      leadCapture: leadCapture || null
    };

    state.messages.push(message);
    state.scrollTargetId = message.id;
    state.scrollMode = role === 'assistant' ? 'message-start' : 'bottom';
  }

  function renderMessages() {
    messagesEl.innerHTML = '';

    state.messages.forEach(function (message) {
      const wrapper = document.createElement('div');
      wrapper.className = `healthyaa-ai-message healthyaa-ai-message--${message.role}`;
      wrapper.setAttribute('data-message-id', String(message.id));

      const bubble = document.createElement('div');
      bubble.className = 'healthyaa-ai-message__bubble';
      bubble.textContent = message.text;
      wrapper.appendChild(bubble);

      if (message.suggestions && message.suggestions.length) {
        const heading = document.createElement('div');
        heading.className = 'healthyaa-ai-suggestions__heading';
        heading.textContent = 'Suggested Healthyaa options';
        wrapper.appendChild(heading);

        const cards = document.createElement('div');
        cards.className = 'healthyaa-ai-suggestions';

        message.suggestions.forEach(function (item) {
          const link = document.createElement('a');
          link.className = 'healthyaa-ai-suggestion';
          link.href = item.url || '#';
          link.innerHTML = `
            <div class="healthyaa-ai-suggestion__top">
              <strong>${escapeHtml(item.name || 'Suggested option')}</strong>
              ${item.price_text ? `<span class="healthyaa-ai-suggestion__price">${escapeHtml(item.price_text)}</span>` : ''}
            </div>
            ${item.meta_text ? `<span class="healthyaa-ai-suggestion__meta">${escapeHtml(item.meta_text)}</span>` : ''}
            ${item.summary ? `<small class="healthyaa-ai-suggestion__summary">${escapeHtml(item.summary)}</small>` : ''}
            ${item.reason ? `<small>${escapeHtml(item.reason)}</small>` : ''}
          `;
          cards.appendChild(link);
        });

        wrapper.appendChild(cards);
      }

      if (message.sources && message.sources.length) {
        const heading = document.createElement('div');
        heading.className = 'healthyaa-ai-sources__heading';
        heading.textContent = 'Sources';
        wrapper.appendChild(heading);

        const list = document.createElement('div');
        list.className = 'healthyaa-ai-sources';

        message.sources.forEach(function (item) {
          const link = document.createElement('a');
          link.className = 'healthyaa-ai-source';
          link.href = item.url || '#';
          link.target = '_blank';
          link.rel = 'noopener';
          link.innerHTML = `
            <strong>${escapeHtml(item.label || 'Healthyaa page')}</strong>
            ${item.snippet ? `<small>${escapeHtml(item.snippet)}</small>` : ''}
          `;
          list.appendChild(link);
        });

        wrapper.appendChild(list);
      }

      if (message.leadCapture && message.leadCapture.status === 'prompt') {
        const leadBox = document.createElement('div');
        leadBox.className = 'healthyaa-ai-lead';
        const fieldName = message.leadCapture.field_name || (message.leadCapture.stage === 'email' ? 'lead_email' : 'lead_name');
        const fieldType = message.leadCapture.field_type || (message.leadCapture.stage === 'email' ? 'email' : 'text');
        const fieldLabel = message.leadCapture.field_label || (message.leadCapture.stage === 'email' ? 'Email' : 'First name');
        const fieldValue = message.leadCapture.field_value || '';
        leadBox.innerHTML = `
          <div class="healthyaa-ai-lead__title">${escapeHtml(message.leadCapture.prompt || '')}</div>
          <form class="healthyaa-ai-lead-form">
            <input type="hidden" name="lead_stage" value="${escapeAttr(message.leadCapture.stage || '')}" />
            <input type="${escapeAttr(fieldType)}" name="${escapeAttr(fieldName)}" placeholder="${escapeAttr(fieldLabel)}" value="${escapeAttr(fieldValue)}" />
            <div class="healthyaa-ai-lead__actions">
              <button type="submit">${escapeHtml(message.leadCapture.submit_label || 'Share details')}</button>
              <button type="button" class="healthyaa-ai-lead-skip" data-stage="${escapeAttr(message.leadCapture.stage || '')}">${escapeHtml(message.leadCapture.skip_label || 'Not now')}</button>
            </div>
          </form>
        `;
        wrapper.appendChild(leadBox);
      }

      if (message.handoff && (message.handoff.show_whatsapp || message.handoff.show_contact)) {
        const handoff = document.createElement('div');
        handoff.className = 'healthyaa-ai-handoff';
        if (message.handoff.show_whatsapp) {
          handoff.innerHTML += `<a class="healthyaa-ai-link healthyaa-ai-link--whatsapp" href="${escapeAttr(config.whatsAppUrl)}" target="_blank" rel="noopener">WhatsApp</a>`;
        }
        if (message.handoff.show_contact) {
          handoff.innerHTML += `<a class="healthyaa-ai-link healthyaa-ai-link--contact" href="${escapeAttr(config.contactUrl)}">Contact</a>`;
        }
        wrapper.appendChild(handoff);
      }

      messagesEl.appendChild(wrapper);
    });

    if (state.loading) {
      const loading = document.createElement('div');
      loading.className = 'healthyaa-ai-message healthyaa-ai-message--assistant';
      loading.innerHTML = '<div class="healthyaa-ai-message__bubble healthyaa-ai-message__bubble--loading">Thinking...</div>';
      messagesEl.appendChild(loading);
    }

    applyMessageScroll();
  }

  function applyMessageScroll() {
    if (state.scrollMode === 'message-start' && state.scrollTargetId !== null) {
      const target = messagesEl.querySelector(`[data-message-id="${state.scrollTargetId}"]`);
      if (target) {
        messagesEl.scrollTop = Math.max(0, target.offsetTop - messagesEl.offsetTop - 8);
        return;
      }
    }

    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function getSessionId() {
    const existing = localStorage.getItem('healthyaa-ai-session-id');
    if (existing) {
      return existing;
    }

    const generated = 'haai-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem('healthyaa-ai-session-id', generated);
    return generated;
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function escapeAttr(value) {
    return escapeHtml(value);
  }
})();
