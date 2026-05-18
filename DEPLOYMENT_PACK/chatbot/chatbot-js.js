/*
  She Said Sail: Luxury Concierge Chat Widget
  chatbot-js.js
  Version: 1.0
  Brand: She Said Sail, Miami

  Pure vanilla JS, no dependencies.
  Full IIFE state machine with conversation flow, GTM events, and Make.com webhook.

  States:
    idle           -> Widget closed, no conversation started
    opener         -> Widget opened, greeting shown
    occasion       -> Detecting occasion type
    energy         -> Detecting energy/vibe preference
    size           -> Guest count collection
    recommendation -> Experience recommendation shown
    date           -> Date preference collected
    name           -> First name collected
    email          -> Email collected
    phone          -> Phone collected (optional)
    handoff        -> Handoff message sent, webhook fired
    closed         -> Conversation complete, input disabled
*/

(function () {
  'use strict';

  // Guard: only load once per page
  if (window.__sssChatLoaded) { return; }
  window.__sssChatLoaded = true;

  // ============================================================
  // CONSTANTS: STATES
  // ============================================================

  var STATE_IDLE           = 'idle';
  var STATE_OPENER         = 'opener';
  var STATE_OCCASION       = 'occasion';
  var STATE_ENERGY         = 'energy';
  var STATE_SIZE           = 'size';
  var STATE_RECOMMENDATION = 'recommendation';
  var STATE_DATE           = 'date';
  var STATE_NAME           = 'name';
  var STATE_EMAIL          = 'email';
  var STATE_PHONE          = 'phone';
  var STATE_HANDOFF        = 'handoff';
  var STATE_CLOSED         = 'closed';

  // ============================================================
  // CONSTANTS: EXPERIENCE DATA
  // ============================================================

  var expNames = {
    'monaco-social':      'Monaco Social',
    'golden-hour-escape': 'Golden Hour Escape',
    'rose-day-club':      'Rose Day Club',
    'pink-palm-club':     'Pink Palm Club'
  };

  var expMessages = {
    'pink-palm-club':
      'Pink Palm Club sounds like it could be exactly right. It is designed for larger groups who want music, movement, and a real Miami energy. High energy, social, and completely private. Up to 22 guests.',
    'monaco-social':
      'Monaco Social is probably the best fit. Think champagne, Riviera energy, and a polished afternoon on the water. It is our most popular choice for bachelorettes and birthday groups who want something memorable without it feeling like a party boat.',
    'golden-hour-escape':
      'The Golden Hour Escape tends to be perfect for that. It is quieter, more personal, and timed around sunset. The kind of afternoon where you slow down and actually feel like you are somewhere special. Up to 12 guests.',
    'rose-day-club':
      'Rose Day Club was basically made for that. A warm afternoon charter with a social, hosted feel. Good rose, good music, everyone together. It tends to be the one groups end up booking every year.'
  };

  var expOverview =
    'Here is a quick overview. Monaco Social: champagne, polished, social. ' +
    'Golden Hour Escape: quiet, sunset, intimate. ' +
    'Rose Day Club: warm afternoon, social, relaxed. ' +
    'Pink Palm Club: high energy, music, larger groups. ' +
    'Which feels closest to what you have in mind?';

  // ============================================================
  // STATE
  // ============================================================

  var currentState = STATE_IDLE;
  var isOpen       = false;

  // Collected conversation data
  var data = {
    occasion:              '',
    occasion_energy:       '',
    guest_count:           '',
    selected_experience:   '',
    preferred_date:        '',
    first_name:            '',
    email:                 '',
    phone:                 '',
    conversation_summary:  '',
    landing_page:          window.location.href,
    utm_source:            '',
    utm_medium:            '',
    utm_campaign:          '',
    utm_content:           '',
    utm_term:              '',
    referrer_url:          document.referrer || '',
    brand:                 'shesaidsail',
    service_category:      'yacht-charter',
    visitor_id:            window.__sssVid || '',
    source_type:           'chatbot'
  };

  // Capture UTM params from sessionStorage (set by global JS)
  try {
    var utm = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
    data.utm_source   = utm.utm_source   || '';
    data.utm_medium   = utm.utm_medium   || '';
    data.utm_campaign = utm.utm_campaign || '';
    data.utm_content  = utm.utm_content  || '';
    data.utm_term     = utm.utm_term     || '';
  } catch (e) {}

  // Conversation tracking
  var exchangeCount       = 0;
  var unrecognizedCount   = 0;
  var silenceTimer        = null;
  var experienceEventFired = false;
  var handoffNotes        = '';

  // Sub-state: awaiting a specific free-text answer
  // Values: null, 'occasion_freetext', 'date_input', 'name', 'email', 'phone', 'handoff_notes'
  var awaitingInput = null;

  // ============================================================
  // WIDGET HTML TEMPLATE
  // ============================================================

  var WIDGET_HTML = [
    '<div id="sss-chat-widget">',

    '  <div id="sss-chat-panel" class="sss-chat-closed" role="dialog"',
    '       aria-label="She Said Sail Concierge Chat" aria-modal="false">',

    '    <div id="sss-chat-header">',
    '      <div class="sss-chat-header-info">',
    '        <span class="sss-chat-header-name">She Said Sail</span>',
    '        <span class="sss-chat-header-status">Concierge</span>',
    '      </div>',
    '      <button id="sss-chat-minimize" aria-label="Minimize chat">',
    '        <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"',
    '             stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
    '          <polyline points="3,6 8,11 13,6"/>',
    '        </svg>',
    '      </button>',
    '    </div>',

    '    <div id="sss-chat-messages" role="log" aria-live="polite" aria-relevant="additions">',
    '    </div>',

    '    <div id="sss-chat-quick-replies" role="group" aria-label="Quick reply options">',
    '    </div>',

    '    <div id="sss-chat-input-area">',
    '      <input type="text" id="sss-chat-input"',
    '             placeholder="Type a message..."',
    '             autocomplete="off"',
    '             aria-label="Your message"',
    '             inputmode="text" />',
    '      <button id="sss-chat-send" aria-label="Send message">',
    '        <svg viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg"',
    '             stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
    '          <line x1="3" y1="9" x2="15" y2="9"/>',
    '          <polyline points="10,4 15,9 10,14"/>',
    '        </svg>',
    '      </button>',
    '    </div>',

    '  </div>',

    '  <button id="sss-chat-toggle" aria-label="Chat with our concierge" aria-expanded="false">',
    '    <span class="sss-chat-toggle-icon">',
    '      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"',
    '           width="24" height="24">',
    '        <path fill="#DAB97E" d="M12 2C6.48 2 2 6.04 2 11c0 2.72 1.23 5.16 3.19 6.84',
    '              L4 22l4.51-2.26C9.6 20.24 10.77 20.5 12 20.5c5.52 0 10-4.04 10-9S17.52 2 12 2z"/>',
    '      </svg>',
    '    </span>',
    '    <span class="sss-chat-toggle-label">Concierge</span>',
    '  </button>',

    '</div>'
  ].join('\n');

  // ============================================================
  // DOM REFERENCES (set after insert)
  // ============================================================

  var widget, panel, toggle, messagesEl, quickRepliesEl, inputEl, sendBtn, minimizeBtn;

  // ============================================================
  // GTM HELPER
  // ============================================================

  function dlPush(eventName, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      var payload = { event: eventName };
      if (params) {
        for (var k in params) {
          if (Object.prototype.hasOwnProperty.call(params, k)) {
            payload[k] = params[k];
          }
        }
      }
      window.dataLayer.push(payload);
    } catch (e) {}
  }

  // ============================================================
  // STATE MACHINE
  // ============================================================

  function setState(newState) {
    currentState = newState;
  }

  // ============================================================
  // TIMING HELPERS
  // ============================================================

  function randomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  // ============================================================
  // TYPING INDICATOR
  // ============================================================

  function showTyping() {
    var wrapper = document.createElement('div');
    wrapper.className = 'sss-msg sss-msg-bot sss-typing';
    var inner = document.createElement('div');
    inner.className = 'sss-typing-inner';
    inner.innerHTML = '<span></span><span></span><span></span>';
    wrapper.appendChild(inner);
    messagesEl.appendChild(wrapper);
    scrollToBottom();
  }

  function hideTyping() {
    var indicators = messagesEl.querySelectorAll('.sss-typing');
    for (var i = 0; i < indicators.length; i++) {
      if (indicators[i] && indicators[i].parentNode) {
        indicators[i].parentNode.removeChild(indicators[i]);
      }
    }
  }

  // ============================================================
  // MESSAGE HELPERS
  // ============================================================

  function addBotMessage(text, callback) {
    var delay = randomDelay(800, 1400);
    showTyping();
    setTimeout(function () {
      hideTyping();
      var wrapper = document.createElement('div');
      wrapper.className = 'sss-msg sss-msg-bot';
      var p = document.createElement('p');
      p.textContent = text;
      wrapper.appendChild(p);
      messagesEl.appendChild(wrapper);
      scrollToBottom();
      setTimeout(function () {
        if (callback) { callback(); }
      }, 300);
    }, delay);
  }

  function addUserMessage(text) {
    var wrapper = document.createElement('div');
    wrapper.className = 'sss-msg sss-msg-user';
    var p = document.createElement('p');
    p.textContent = text;
    wrapper.appendChild(p);
    messagesEl.appendChild(wrapper);
    scrollToBottom();
    exchangeCount++;
    resetSilenceTimer();
  }

  // ============================================================
  // QUICK REPLIES
  // ============================================================

  function showQuickReplies(options) {
    clearQuickReplies();
    for (var i = 0; i < options.length; i++) {
      (function (label) {
        var btn = document.createElement('button');
        btn.className = 'sss-qr-btn';
        btn.textContent = label;
        btn.addEventListener('click', function () {
          clearQuickReplies();
          addUserMessage(label);
          handleUserInput(label);
        });
        quickRepliesEl.appendChild(btn);
      })(options[i]);
    }
  }

  function clearQuickReplies() {
    quickRepliesEl.innerHTML = '';
  }

  // ============================================================
  // SCROLL
  // ============================================================

  function scrollToBottom() {
    try {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    } catch (e) {}
  }

  // ============================================================
  // SILENCE DETECTION
  // ============================================================

  function resetSilenceTimer() {
    if (silenceTimer) { clearTimeout(silenceTimer); }
    if (currentState === STATE_IDLE || currentState === STATE_CLOSED) { return; }
    if (!isOpen) { return; }
    silenceTimer = setTimeout(function () {
      if (currentState !== STATE_IDLE && currentState !== STATE_CLOSED && isOpen) {
        addBotMessage('Still there? No rush.');
      }
    }, 90000);
  }

  // ============================================================
  // KEYWORD DETECTION
  // ============================================================

  function detectOccasion(text) {
    text = text.toLowerCase();
    if (/bach|bride|future mrs|bridal|hen/.test(text))                           { return 'bachelorette'; }
    if (/birthday|bday|turning|celebrat/.test(text))                             { return 'birthday'; }
    if (/girls|getaway|trip|weekend/.test(text))                                 { return 'girls_trip'; }
    if (/annivers|intimate|propos|just us|couple|milestone/.test(text))          { return 'intimate'; }
    return null;
  }

  function detectEnergy(text) {
    text = text.toLowerCase();
    if (/high|music|movement|lively|social|energy|upbeat/.test(text))            { return 'high'; }
    if (/relax|quiet|calm|scenic|slow|intimate|curated|elevated/.test(text))     { return 'relaxed'; }
    return 'mid';
  }

  // ============================================================
  // EXPERIENCE LOGIC
  // ============================================================

  function recommendExperience(occasion, energy, guestCount) {
    var count = parseInt(guestCount, 10) || 0;

    if (occasion === 'bachelorette') {
      if (energy === 'high') { return 'pink-palm-club'; }
      return 'monaco-social';
    }
    if (occasion === 'birthday') {
      if (count >= 16)       { return 'pink-palm-club'; }
      if (count >= 9)        { return 'monaco-social'; }
      return 'golden-hour-escape';
    }
    if (occasion === 'girls_trip') {
      if (energy === 'relaxed') { return 'golden-hour-escape'; }
      return 'rose-day-club';
    }
    if (occasion === 'intimate') { return 'golden-hour-escape'; }
    return 'monaco-social';
  }

  function normalizeGuestCount(text) {
    text = text.toLowerCase();
    if (/under 10|4 to 8|1 to 9|less than 10/.test(text))   { return '8'; }
    if (/10 to 15|9 to 15/.test(text))                        { return '12'; }
    if (/16|more|large/.test(text))                           { return '18'; }
    if (/not sure|unsure|don.t know/.test(text))              { return '0'; }
    // Try to extract a number
    var match = text.match(/\d+/);
    if (match) { return match[0]; }
    return '0';
  }

  // ============================================================
  // ESCALATION
  // ============================================================

  function detectEscalation(text) {
    text = text.toLowerCase();
    return /real person|talk to someone|human|agent|speak to|call me|phone me/.test(text);
  }

  function handleEscalation() {
    addBotMessage(
      'Of course. Let me get a concierge to take over from here. They will reach out to you directly within a few hours. Can I confirm your name and email so they know who to contact?',
      function () {
        awaitingInput = 'name_escalation';
        setState(STATE_NAME);
      }
    );
  }

  // ============================================================
  // EMAIL VALIDATION
  // ============================================================

  function isValidEmail(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val.trim());
  }

  // ============================================================
  // MAKE.COM WEBHOOK
  // ============================================================

  function fireWebhook() {
    try {
      var payload = {};
      for (var k in data) {
        if (Object.prototype.hasOwnProperty.call(data, k)) {
          payload[k] = data[k];
        }
      }
      if (handoffNotes) { payload.conversation_summary = handoffNotes; }

      var xhr = new XMLHttpRequest();
      xhr.open('POST', 'WIRE_THIS_CHATBOT_WEBHOOK_URL', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.timeout = 8000;
      xhr.send(JSON.stringify(payload));
      // Proceed regardless of response
    } catch (e) {
      // Webhook failure must not block the conversation
    }
  }

  // ============================================================
  // STATE TRANSITIONS: FLOW STEPS
  // ============================================================

  function startOpener() {
    setState(STATE_OPENER);
    dlPush('chatbot_open');
    dlPush('chatbot_start_conversation');
    addBotMessage('Hi there. What kind of day are you planning for your group?', function () {
      showQuickReplies([
        'Bachelorette party',
        'Birthday celebration',
        'Girls trip',
        'Something more intimate',
        'Still exploring'
      ]);
      setState(STATE_OCCASION);
    });
  }

  function handleOccasionSelection(text) {
    var occasion = detectOccasion(text);

    // "Still exploring"
    if (!occasion && /still exploring|not sure|exploring|thinking|maybe|don.t know/.test(text.toLowerCase())) {
      data.occasion = 'exploring';
      addBotMessage('That is a good place to start. Can you tell me a little about the occasion? Even just a word or two works.', function () {
        awaitingInput = 'occasion_freetext';
      });
      return;
    }

    // "Something more intimate"
    if (!occasion && /intimate|just us|couple|anniversary|milestone/.test(text.toLowerCase())) {
      occasion = 'intimate';
    }

    if (!occasion) {
      // Unrecognized
      unrecognizedCount++;
      if (unrecognizedCount >= 2) {
        jumpToNameCapture();
        return;
      }
      addBotMessage('That is a bit outside what I can help with here. If it is something specific about an experience or booking, our concierge can answer that directly. Would it help if they reached out?', function () {
        showQuickReplies([
          'Bachelorette party',
          'Birthday celebration',
          'Girls trip',
          'Something more intimate',
          'Still exploring'
        ]);
      });
      return;
    }

    routeOccasion(occasion);
  }

  function routeOccasion(occasion) {
    data.occasion = occasion;
    dlPush('chatbot_select_occasion', { occasion: occasion });
    unrecognizedCount = 0;

    if (occasion === 'bachelorette') {
      addBotMessage(
        'A bachelorette in Miami. Great. Is the group more into a high-energy social day, or something more elevated and curated?',
        function () {
          setState(STATE_ENERGY);
          showQuickReplies([
            'High energy, music, movement',
            'Elevated and curated',
            'Somewhere in between'
          ]);
        }
      );
    } else if (occasion === 'birthday') {
      addBotMessage(
        'A birthday celebration. I love that. How many people are you thinking?',
        function () {
          setState(STATE_SIZE);
          showQuickReplies([
            '4 to 8 guests',
            '9 to 15 guests',
            '16 or more'
          ]);
        }
      );
    } else if (occasion === 'girls_trip') {
      addBotMessage(
        'A girls trip is one of my favorites to help plan. What kind of energy is the group going for?',
        function () {
          setState(STATE_ENERGY);
          showQuickReplies([
            'Social and lively',
            'Relaxed and scenic',
            'Bit of both'
          ]);
        }
      );
    } else if (occasion === 'intimate') {
      data.selected_experience = 'golden-hour-escape';
      addBotMessage(
        'Our Golden Hour Escape was designed for moments like that. It is quieter, more personal, and timed around the light of late afternoon. Can I tell you a bit more about it?',
        function () {
          setState(STATE_RECOMMENDATION);
          showQuickReplies([
            'Yes, tell me more',
            'What other options do you have?'
          ]);
        }
      );
    }
  }

  function handleEnergySelection(text) {
    var energy = detectEnergy(text);
    data.occasion_energy = energy;

    var exp = recommendExperience(data.occasion, energy, data.guest_count);
    data.selected_experience = exp;

    var msg = expMessages[exp];
    addBotMessage(msg, function () {
      addBotMessage('Does that sound like the right direction?', function () {
        setState(STATE_RECOMMENDATION);
        showQuickReplies([
          'Yes, that sounds right',
          'Tell me more',
          'What are the other options?'
        ]);
      });
    });
  }

  function handleSizeSelection(text) {
    data.guest_count = normalizeGuestCount(text);
    var exp = recommendExperience(data.occasion, data.occasion_energy, data.guest_count);
    data.selected_experience = exp;

    var msg = expMessages[exp];
    addBotMessage(msg, function () {
      addBotMessage('Does that sound like the right direction?', function () {
        setState(STATE_RECOMMENDATION);
        showQuickReplies([
          'Yes, that sounds right',
          'Tell me more',
          'What are the other options?'
        ]);
      });
    });
  }

  function handleRecommendationReply(text) {
    var lower = text.toLowerCase();

    if (/other options|other|more options|alternatives|what else/.test(lower)) {
      addBotMessage(expOverview, function () {
        showQuickReplies([
          'Monaco Social',
          'Golden Hour Escape',
          'Rose Day Club',
          'Pink Palm Club'
        ]);
        awaitingInput = 'experience_choice';
      });
      return;
    }

    // "Intimate" initial tell me more
    if (data.occasion === 'intimate' && /tell me more|yes|more detail/.test(lower)) {
      addBotMessage(
        'It runs about 3 to 4 hours, fits up to 12 guests, and the experience is designed to feel slow and intentional. Not a party. Just a beautiful afternoon on the water. Starting from $10,000. Is this for a specific date, or are you still in early planning?',
        function () {
          setState(STATE_DATE);
          showQuickReplies([
            'I have a date',
            'Still planning'
          ]);
        }
      );
      return;
    }

    // Yes or tell me more: collect size if not captured
    if (/yes|sounds right|tell me more|perfect|good|great|love|right direction|sure/.test(lower) || true) {
      if (!data.guest_count) {
        askGroupSize();
      } else {
        askDate();
      }
    }
  }

  function askGroupSize() {
    addBotMessage('How many people are you thinking? An approximate is fine.', function () {
      setState(STATE_SIZE);
      awaitingInput = 'size_after_rec';
      showQuickReplies([
        'Under 10',
        '10 to 15',
        '16 or more',
        'Not sure yet'
      ]);
    });
  }

  function askDate() {
    addBotMessage('Do you have a date in mind, or are you still in the early planning stages?', function () {
      setState(STATE_DATE);
      showQuickReplies([
        'I have a date',
        'Still planning'
      ]);
    });
  }

  function handleDateReply(text) {
    var lower = text.toLowerCase();

    if (/i have a date|specific date|yes.*date|have.*date/.test(lower)) {
      addBotMessage('What date are you looking at?', function () {
        awaitingInput = 'date_input';
      });
      return;
    }

    // Still planning
    data.preferred_date = 'flexible';
    addBotMessage('No problem at all. Our concierge can check availability across several dates once we connect.', function () {
      askName();
    });
  }

  function askName() {
    addBotMessage(
      'Perfect. What is your first name? I would love to make sure a concierge follows up with the right details for you.',
      function () {
        setState(STATE_NAME);
        awaitingInput = 'name';
      }
    );
  }

  function askEmail() {
    addBotMessage(
      'Thanks, ' + data.first_name + '. What is the best email address to reach you?',
      function () {
        setState(STATE_EMAIL);
        awaitingInput = 'email';
      }
    );
  }

  function askPhone() {
    addBotMessage(
      'And a phone number if you would like to hear back by text? Completely optional.',
      function () {
        setState(STATE_PHONE);
        awaitingInput = 'phone';
        showQuickReplies(['Skip for now']);
      }
    );
  }

  function sendHandoff() {
    // Fire experience GTM event if not already done
    if (!experienceEventFired && data.selected_experience) {
      dlPush('chatbot_select_experience', { experience_slug: data.selected_experience });
      experienceEventFired = true;
    }

    var expLabel = data.selected_experience
      ? (expNames[data.selected_experience] || data.selected_experience)
      : 'your group';

    var handoffMsg =
      'You are all set, ' + data.first_name + '. ' +
      'I am going to have a concierge review your details and reach out within 24 hours ' +
      'with the best availability for ' + expLabel + '. ' +
      'Is there anything specific you would like them to know?';

    setState(STATE_HANDOFF);
    addBotMessage(handoffMsg, function () {
      showQuickReplies(['That is everything']);
      awaitingInput = 'handoff_notes';
    });
  }

  function finishHandoff(notes) {
    handoffNotes = notes || '';
    if (handoffNotes) {
      data.conversation_summary = handoffNotes;
    }

    // Fire webhook
    fireWebhook();

    // GTM events
    dlPush('chatbot_handoff', {
      experience_slug: data.selected_experience,
      occasion:        data.occasion,
      has_email:       true
    });

    dlPush('chatbot_complete', {
      experience_slug: data.selected_experience,
      occasion:        data.occasion,
      has_email:       true
    });

    var respondWithClose = function () {
      setState(STATE_CLOSED);
      sendCloseMessage();
    };

    if (handoffNotes && handoffNotes !== 'That is everything') {
      addBotMessage('Got it. I will make sure they see that.', function () {
        respondWithClose();
      });
    } else {
      respondWithClose();
    }
  }

  function sendCloseMessage() {
    addBotMessage(
      'Talk soon. In the meantime, you are welcome to browse the experiences at shesaidsail.com/experiences/ if you would like to see more before we connect.',
      function () {
        // Disable input
        if (inputEl)   { inputEl.disabled = true; inputEl.placeholder = 'Chat ended'; }
        if (sendBtn)   { sendBtn.disabled = true; }
        clearQuickReplies();

        // Visual "ended" state
        var notice = document.createElement('div');
        notice.className = 'sss-chat-ended-notice';
        notice.textContent = 'Chat ended';
        var inputArea = document.getElementById('sss-chat-input-area');
        if (inputArea) {
          inputArea.parentNode.insertBefore(notice, inputArea);
        }
      }
    );
  }

  function jumpToNameCapture() {
    setState(STATE_NAME);
    addBotMessage(
      'I want to make sure I get this right for you. The quickest path is having a concierge reach out directly. Can I get your name and email?',
      function () {
        awaitingInput = 'name';
      }
    );
  }

  // ============================================================
  // MAIN INPUT HANDLER
  // ============================================================

  function handleUserInput(text) {
    text = (text || '').trim();
    if (!text) { return; }

    var lower = text.toLowerCase();

    // Check for escalation at any point
    if (detectEscalation(text) && currentState !== STATE_NAME && currentState !== STATE_EMAIL) {
      clearQuickReplies();
      awaitingInput = null;
      handleEscalation();
      return;
    }

    // Exchange count cap: escalate after 10 exchanges without reaching STATE_NAME
    if (
      exchangeCount >= 10 &&
      currentState !== STATE_NAME &&
      currentState !== STATE_EMAIL &&
      currentState !== STATE_PHONE &&
      currentState !== STATE_HANDOFF &&
      currentState !== STATE_CLOSED
    ) {
      awaitingInput = null;
      jumpToNameCapture();
      return;
    }

    // Handle awaiting free-text inputs first
    if (awaitingInput) {
      var prev = awaitingInput;
      awaitingInput = null;

      if (prev === 'occasion_freetext') {
        // Try to detect occasion from freetext
        var detectedFromFree = detectOccasion(text);
        if (detectedFromFree) {
          routeOccasion(detectedFromFree);
        } else {
          // No match: show overview
          addBotMessage(
            'Got it. We have four experiences that cover different energies, from quiet and intimate to social and lively. What matters more to your group: the atmosphere, the group size, or the timing?',
            function () {
              showQuickReplies([
                'The atmosphere',
                'The group size',
                'The timing'
              ]);
              awaitingInput = 'exploring_pivot';
            }
          );
        }
        return;
      }

      if (prev === 'exploring_pivot') {
        // Route to overview
        addBotMessage(expOverview, function () {
          showQuickReplies([
            'Monaco Social',
            'Golden Hour Escape',
            'Rose Day Club',
            'Pink Palm Club'
          ]);
          awaitingInput = 'experience_choice';
        });
        return;
      }

      if (prev === 'experience_choice') {
        // User picked an experience by name
        var chosenSlug = null;
        for (var slug in expNames) {
          if (
            Object.prototype.hasOwnProperty.call(expNames, slug) &&
            lower.indexOf(expNames[slug].toLowerCase()) !== -1
          ) {
            chosenSlug = slug;
            break;
          }
        }
        if (chosenSlug) {
          data.selected_experience = chosenSlug;
        }
        if (!data.guest_count) {
          askGroupSize();
        } else {
          askDate();
        }
        return;
      }

      if (prev === 'size_after_rec') {
        data.guest_count = normalizeGuestCount(text);
        // Re-run recommendation with updated size
        var reExp = recommendExperience(data.occasion, data.occasion_energy, data.guest_count);
        if (!data.selected_experience) { data.selected_experience = reExp; }
        askDate();
        return;
      }

      if (prev === 'date_input') {
        data.preferred_date = text;
        askName();
        return;
      }

      if (prev === 'name' || prev === 'name_escalation') {
        data.first_name = text.split(' ')[0]; // Use first word only
        // Fire experience GTM if not done
        if (!experienceEventFired && data.selected_experience) {
          dlPush('chatbot_select_experience', { experience_slug: data.selected_experience });
          experienceEventFired = true;
        }
        askEmail();
        return;
      }

      if (prev === 'email') {
        if (!isValidEmail(text)) {
          addBotMessage('That does not look quite right. Can you double-check the email address?', function () {
            awaitingInput = 'email';
          });
          return;
        }
        data.email = text.trim().toLowerCase();
        dlPush('chatbot_capture_email');
        askPhone();
        return;
      }

      if (prev === 'phone') {
        if (/skip|no thanks|not now|maybe later/.test(lower)) {
          data.phone = '';
        } else {
          data.phone = text;
          dlPush('chatbot_capture_phone');
        }
        clearQuickReplies();
        sendHandoff();
        return;
      }

      if (prev === 'handoff_notes') {
        finishHandoff(text);
        return;
      }
    }

    // State-based routing (for quick replies that do not set awaitingInput)
    if (currentState === STATE_OCCASION) {
      handleOccasionSelection(text);
      return;
    }

    if (currentState === STATE_ENERGY) {
      handleEnergySelection(text);
      return;
    }

    if (currentState === STATE_SIZE) {
      // Birthday direct size path
      data.guest_count = normalizeGuestCount(text);
      var bExp = recommendExperience(data.occasion, data.occasion_energy, data.guest_count);
      data.selected_experience = bExp;
      var bMsg = expMessages[bExp];
      addBotMessage(bMsg, function () {
        addBotMessage('Does that sound like the right direction?', function () {
          setState(STATE_RECOMMENDATION);
          showQuickReplies([
            'Yes, that sounds right',
            'Tell me more',
            'What are the other options?'
          ]);
        });
      });
      return;
    }

    if (currentState === STATE_RECOMMENDATION) {
      handleRecommendationReply(text);
      return;
    }

    if (currentState === STATE_DATE) {
      handleDateReply(text);
      return;
    }

    if (currentState === STATE_HANDOFF) {
      // Handoff notes
      finishHandoff(text);
      return;
    }

    if (currentState === STATE_CLOSED) {
      // Conversation over, do nothing
      return;
    }

    // Fallback: unrecognized
    unrecognizedCount++;
    if (unrecognizedCount >= 2) {
      jumpToNameCapture();
    } else {
      addBotMessage(
        'That is a bit outside what I can help with here. If it is something specific about an experience or booking, our concierge can answer that directly. Would it help if they reached out?',
        function () {
          showQuickReplies(['Yes, connect me', 'No, just browsing']);
          awaitingInput = 'out_of_scope';
        }
      );
    }
  }

  // ============================================================
  // WIDGET OPEN / CLOSE
  // ============================================================

  function openWidget() {
    if (isOpen) { return; }
    isOpen = true;

    panel.classList.remove('sss-chat-closed');
    widget.classList.add('sss-widget-open');
    toggle.setAttribute('aria-expanded', 'true');

    // Accessibility: focus the input
    setTimeout(function () {
      if (inputEl && !inputEl.disabled) { inputEl.focus(); }
    }, 350);

    if (currentState === STATE_IDLE) {
      startOpener();
    }

    resetSilenceTimer();
  }

  function closeWidget() {
    if (!isOpen) { return; }
    isOpen = false;

    panel.classList.add('sss-chat-closed');
    widget.classList.remove('sss-widget-open');
    toggle.setAttribute('aria-expanded', 'false');

    if (silenceTimer) { clearTimeout(silenceTimer); }
  }

  // ============================================================
  // SEND ACTION
  // ============================================================

  function sendUserMessage() {
    if (!inputEl) { return; }
    var text = inputEl.value.trim();
    if (!text) { return; }
    inputEl.value = '';
    clearQuickReplies();
    addUserMessage(text);
    handleUserInput(text);
  }

  // ============================================================
  // MOBILE KEYBOARD HANDLING
  // ============================================================

  function setupMobileKeyboard() {
    if (!inputEl) { return; }
    inputEl.addEventListener('focus', function () {
      if (window.innerWidth > 767) { return; }
      // Delay to allow keyboard to appear
      setTimeout(function () {
        scrollToBottom();
      }, 400);
    });

    // iOS: listen for viewport resize (keyboard appearance)
    var lastHeight = window.innerHeight;
    window.addEventListener('resize', function () {
      if (window.innerWidth > 767) { return; }
      var newHeight = window.innerHeight;
      if (newHeight < lastHeight - 100) {
        // Keyboard opened
        scrollToBottom();
      }
      lastHeight = newHeight;
    });
  }

  // ============================================================
  // AUTO-TRIGGER LOGIC
  // ============================================================

  function setupAutoTrigger() {
    // Do not auto-trigger on mobile
    if (window.innerWidth <= 767) { return; }

    // Do not re-trigger if already done this session
    try {
      if (sessionStorage.getItem('sss_chat_triggered')) { return; }
    } catch (e) {}

    // Do not auto-trigger on request-to-book page
    var path = window.location.pathname;
    if (/\/request-to-book/i.test(path)) { return; }

    var delay = 60000; // homepage default
    if (/\/experience/i.test(path)) {
      delay = 45000;
    }

    var triggered = false;
    var triggerTimer = null;

    function onActivity() {
      if (triggered) { return; }
      if (!triggerTimer) {
        triggerTimer = setTimeout(function () {
          if (triggered) { return; }
          triggered = true;
          try { sessionStorage.setItem('sss_chat_triggered', '1'); } catch (e) {}
          window.removeEventListener('scroll', onActivity);
          window.removeEventListener('mousemove', onActivity);
          openWidget();
        }, delay);
      }
    }

    window.addEventListener('scroll', onActivity, { passive: true });
    window.addEventListener('mousemove', onActivity, { passive: true });
  }

  // ============================================================
  // INIT: BUILD AND ATTACH WIDGET
  // ============================================================

  function init() {
    // Insert widget HTML
    var container = document.createElement('div');
    container.innerHTML = WIDGET_HTML;
    document.body.appendChild(container.firstElementChild || container);

    // Cache DOM references
    widget      = document.getElementById('sss-chat-widget');
    panel       = document.getElementById('sss-chat-panel');
    toggle      = document.getElementById('sss-chat-toggle');
    messagesEl  = document.getElementById('sss-chat-messages');
    quickRepliesEl = document.getElementById('sss-chat-quick-replies');
    inputEl     = document.getElementById('sss-chat-input');
    sendBtn     = document.getElementById('sss-chat-send');
    minimizeBtn = document.getElementById('sss-chat-minimize');

    if (!widget || !panel || !toggle || !messagesEl || !inputEl || !sendBtn) {
      return;
    }

    // Toggle open/close
    toggle.addEventListener('click', function () {
      if (isOpen) {
        closeWidget();
      } else {
        openWidget();
      }
    });

    // Minimize button
    if (minimizeBtn) {
      minimizeBtn.addEventListener('click', function () {
        closeWidget();
      });
    }

    // Send button
    sendBtn.addEventListener('click', function () {
      sendUserMessage();
    });

    // Enter key in input
    inputEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        sendUserMessage();
      }
    });

    // Input activity resets silence timer
    inputEl.addEventListener('input', function () {
      resetSilenceTimer();
    });

    // Mobile keyboard
    setupMobileKeyboard();

    // Auto-trigger
    setupAutoTrigger();
  }

  // ============================================================
  // BOOT
  // ============================================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
