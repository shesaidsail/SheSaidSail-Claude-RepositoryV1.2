/**
 * She Said Sail: Global Production JavaScript | Version 1.0
 * Load via Insert Headers and Footers plugin, Scripts in Footer, wrapped in script defer tags
 *
 * Sections (in execution order):
 *   1. UTM Capture          - runs immediately, before DOM ready
 *   2. Hidden Field Pop.    - runs on DOM ready, form pages only
 *   3. Trust Fixes          - logo alt, phone links, image alts
 *   4. Scroll Reveal        - IntersectionObserver on .sss-reveal
 *   5. Header Scroll State  - adds .sss-header-scrolled after 80px
 *   6. Email Capture        - handles .sss-email-form submission
 *   7. Smooth Scroll        - anchor links with 80px offset
 *   8. Mobile Nav Close     - closes burger menu on link tap
 *   9. Occasion Badges      - injects badge text into experience cards
 *  10. GTM DataLayer Events - all analytics push calls
 *      Page views: view_homepage, view_request_page, view_experiences_page, view_experience_page
 *      CTA clicks: click_request_to_book, click_explore_experiences, click_experience_card
 *      Forms: start_booking_form, submit_booking_form, submit_email_capture
 *      Engagement: click_phone, open_chat, view_about_page, view_contact_page, view_faq_page, view_journal_page, view_thank_you_page, scroll_50_percent, scroll_90_percent
 */

(function () {
  'use strict';

  /* Script-level init guard: prevent double execution */
  if (window.__sssLoaded) return;
  window.__sssLoaded = true;


  /* ==========================================================
     SECTION 1: UTM CAPTURE
     Runs immediately (before DOM ready) on every page.
     Reads UTM params from the URL and stores them in
     sessionStorage under key 'sss_utm' as a JSON object.
     First-touch attribution: does NOT overwrite values already
     stored in sessionStorage from the first landing page.
     Also writes first_seen_at to localStorage on first visit.
  ========================================================== */
  (function captureUtm() {
    try {
      var params = new URLSearchParams(window.location.search);
      var keys   = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'creative_id'];
      var hasAny = false;

      keys.forEach(function (k) {
        if (params.get(k)) hasAny = true;
      });

      if (hasAny) {
        var existing = {};
        try {
          existing = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
        } catch (e) { existing = {}; }

        /* First-touch: only write keys that are not already stored */
        keys.forEach(function (k) {
          if (params.get(k) && !existing[k]) {
            existing[k] = params.get(k);
          }
        });

        sessionStorage.setItem('sss_utm', JSON.stringify(existing));
      }

      /* Write first_seen_at to localStorage only on first ever visit */
      if (!localStorage.getItem('sss_first_seen')) {
        localStorage.setItem('sss_first_seen', new Date().toISOString());
      }
    } catch (e) {
      /* Storage may be blocked in private/restricted contexts - fail silently */
    }
  })();


  /* ==========================================================
     STORAGE HELPERS
     Internal utilities used by multiple sections below.
  ========================================================== */
  function readSession(key) {
    try {
      var data = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
      return data[key] || '';
    } catch (e) {
      return '';
    }
  }

  function readLocal(key) {
    try {
      return localStorage.getItem(key) || '';
    } catch (e) {
      return '';
    }
  }


  /* ==========================================================
     SECTION 2: HIDDEN FIELD POPULATION
     Runs on DOM ready on form pages.
     Reads UTM values from sessionStorage and injects them into
     hidden form inputs so submissions carry attribution data.
     Safe: only runs if at least one matching hidden input exists.
  ========================================================== */
  function populateHiddenFields() {
    var hiddenNames = [
      'utm_source', 'utm_medium', 'utm_campaign', 'utm_content',
      'utm_term', 'creative_id', 'landing_page', 'source_url',
      'referrer_url', 'first_seen_at', 'submission_page', 'brand',
      'service_category'
    ];

    /* Check at least one of our target fields exists before proceeding */
    var hasFields = hiddenNames.some(function (name) {
      return document.querySelector('input[name="' + name + '"]');
    });
    if (!hasFields) return;

    var utm = {};
    try {
      utm = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
    } catch (e) { utm = {}; }

    var fieldValues = {
      utm_source:       utm.utm_source       || '',
      utm_medium:       utm.utm_medium       || '',
      utm_campaign:     utm.utm_campaign     || '',
      utm_content:      utm.utm_content      || '',
      utm_term:         utm.utm_term         || '',
      creative_id:      utm.creative_id      || '',
      landing_page:     window.location.href,
      source_url:       window.location.href,
      referrer_url:     document.referrer    || '',
      first_seen_at:    readLocal('sss_first_seen'),
      submission_page:  window.location.href,
      brand:            'shesaidsail',
      service_category: 'yacht-charter'
    };

    hiddenNames.forEach(function (name) {
      document.querySelectorAll('input[name="' + name + '"]').forEach(function (input) {
        if (fieldValues[name] !== undefined) {
          input.value = fieldValues[name];
        }
      });
    });
  }


  /* ==========================================================
     SECTION 3: TRUST FIXES
     Corrects accessibility and trust signal issues that
     WordPress/Elementor cannot set reliably at the theme level.
  ========================================================== */

  /* Fix missing or empty alt text on logo images in header and footer */
  function fixLogoAlt() {
    var selectors = [
      '.elementor-5919 .elementor-element-0ce6f64 img',
      '.elementor-5924 .elementor-element-6a8350e3 img',
      '.elementor-location-header a[href="/"] img',
      '.elementor-location-footer a[href="/"] img'
    ];

    selectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (img) {
        if (!img.getAttribute('alt') || img.getAttribute('alt') === '') {
          img.setAttribute('alt', 'She Said Sail');
        }
      });
    });
  }

  /* Convert dead href="#" phone entries to tap-to-call links.
     Convert city name entries to Google Maps links. */
  function fixPhoneLink() {
    var containers = document.querySelectorAll(
      '.elementor-5924 .elementor-element-421dcc00 .elementor-icon-list-item, ' +
      '.elementor-location-footer .elementor-icon-list-item'
    );

    containers.forEach(function (item) {
      var textEl = item.querySelector('.elementor-icon-list-text');
      var link   = item.querySelector('a');
      if (!textEl || !link) return;

      var text = textEl.textContent.trim();

      /* Phone number pattern: matches (305) 555-1234 and similar formats */
      if (/^\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}$/.test(text)) {
        link.setAttribute('href', 'tel:' + text.replace(/\D/g, ''));
        link.setAttribute('aria-label', 'Call She Said Sail at ' + text);
      }

      /* Location text: link to Google Maps */
      if (text === 'Miami, FL' || text === 'Fort Lauderdale, FL') {
        link.setAttribute('href', 'https://maps.google.com/?q=' + encodeURIComponent(text));
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        link.setAttribute('aria-label', 'She Said Sail location: ' + text);
      }
    });
  }

  /* Fill empty alt text on hero slideshow images, experience card images,
     and the feature portrait using the nearest heading as context. */
  function fixImageAlts() {
    /* Hero background slideshow images */
    var heroImages = document.querySelectorAll(
      '.elementor-5928 .elementor-element-5345389 .elementor-background-slideshow img'
    );
    heroImages.forEach(function (img) {
      if (!img.getAttribute('alt') || img.getAttribute('alt') === '') {
        img.setAttribute('alt', 'She Said Sail luxury yacht experience on the water');
      }
    });

    /* Experience card images: use card heading as alt text context */
    var cards = document.querySelectorAll('.e-loop-item');
    cards.forEach(function (card) {
      var img     = card.querySelector('img');
      var heading = card.querySelector('.elementor-heading-title');
      if (img && heading && (!img.getAttribute('alt') || img.getAttribute('alt') === '')) {
        img.setAttribute('alt', heading.textContent.trim() + ', She Said Sail experience');
      }
    });

    /* Feature portrait image */
    var featureImg = document.querySelector('.elementor-5928 .elementor-element-bc81594 img');
    if (featureImg && (!featureImg.getAttribute('alt') || featureImg.getAttribute('alt') === '')) {
      featureImg.setAttribute('alt', 'Curated yacht experience, She Said Sail');
    }
  }


  /* ==========================================================
     SECTION 4: SCROLL REVEAL
     Uses IntersectionObserver to add .sss-revealed to elements
     marked with .sss-reveal when they enter the viewport.
     Falls back to immediate class addition if observer unavailable.
  ========================================================== */
  function initScrollReveal() {
    var elements = document.querySelectorAll('.sss-reveal');
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
      /* Fallback: reveal all immediately for older browsers */
      elements.forEach(function (el) { el.classList.add('sss-revealed'); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('sss-revealed');
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -60px 0px', threshold: 0.1 }
    );

    elements.forEach(function (el) { observer.observe(el); });
  }


  /* ==========================================================
     SECTION 5: HEADER SCROLL STATE
     Adds .sss-header-scrolled to the site header after the user
     scrolls past 80px. Uses requestAnimationFrame throttling and
     a passive scroll listener for performance.
  ========================================================== */
  function initHeaderScroll() {
    var header = document.querySelector('.elementor-location-header');
    if (!header) return;

    var threshold = 80;
    var ticking   = false;

    function updateHeader() {
      if (window.scrollY > threshold) {
        header.classList.add('sss-header-scrolled');
      } else {
        header.classList.remove('sss-header-scrolled');
      }
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(updateHeader);
        ticking = true;
      }
    }, { passive: true });

    /* Set initial state in case page loads mid-scroll */
    updateHeader();
  }


  /* ==========================================================
     SECTION 6: EMAIL CAPTURE
     Handles submission of the .sss-email-form snippet.
     Validates email, disables the button during send, and
     replaces the form with a success message on completion.
     Per-form init guard prevents double-binding.
  ========================================================== */
  function initEmailCapture() {
    var forms = document.querySelectorAll('.sss-email-form');
    if (!forms.length) return;

    forms.forEach(function (form) {
      /* Per-form init guard */
      if (form.__sssInit) return;
      form.__sssInit = true;

      var input  = form.querySelector('input[type="email"]');
      var button = form.querySelector('button');

      form.addEventListener('submit', function (e) {
        e.preventDefault();

        var email = input ? input.value.trim() : '';

        /* Validate email format */
        if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          if (input) {
            input.style.borderColor = 'rgba(207, 46, 46, 0.5)';
            input.focus();
          }
          return;
        }

        if (input)  input.style.borderColor = '';
        if (button) { button.textContent = 'Sending'; button.disabled = true; }

        var payload = {
          email:            email,
          utm_source:       readSession('utm_source'),
          utm_medium:       readSession('utm_medium'),
          utm_campaign:     readSession('utm_campaign'),
          landing_page:     window.location.href,
          first_seen_at:    readLocal('sss_first_seen'),
          brand:            'shesaidsail',
          service_category: 'yacht-charter'
        };

        /*
          WIRE THIS to your Make.com webhook before going live.
          See docs/backend/make-webhook-spec.md scenario M-EMAIL-CAPTURE-001.

          fetch('https://hook.us1.make.com/YOUR_EMAIL_CAPTURE_WEBHOOK_ID', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
          }).then(function () {
            showEmailSuccess(form);
          }).catch(function () {
            showEmailSuccess(form);
          });
        */

        /* Remove this setTimeout block once the fetch() above is wired */
        void payload;
        setTimeout(function () { showEmailSuccess(form); }, 600);
      });
    });
  }

  function showEmailSuccess(form) {
    var success = document.createElement('div');
    success.style.cssText = [
      'font-family:"Cormorant Garamond",serif',
      'font-size:22px',
      'font-style:italic',
      'font-weight:400',
      'color:#1A2332',
      'line-height:1.5',
      'padding:8px 0',
      'opacity:0',
      'transition:opacity 0.5s ease'
    ].join(';');
    success.textContent = "You're on the inside. We'll be in touch.";
    if (form.parentNode) form.parentNode.replaceChild(success, form);
    requestAnimationFrame(function () { success.style.opacity = '1'; });
  }


  /* ==========================================================
     SECTION 7: SMOOTH SCROLL
     Intercepts anchor clicks and scrolls to target with an
     80px offset to account for the fixed header height.
  ========================================================== */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href').slice(1);
        if (!targetId) return;
        var target = document.getElementById(targetId);
        if (!target) return;
        e.preventDefault();
        window.scrollTo({
          top:      target.getBoundingClientRect().top + window.scrollY - 80,
          behavior: 'smooth'
        });
      });
    });
  }


  /* ==========================================================
     SECTION 8: MOBILE NAV CLOSE
     Closes the Elementor hamburger menu when the user taps
     a navigation link inside the open dropdown.
  ========================================================== */
  function initMobileNavClose() {
    document.querySelectorAll('.elementor-nav-menu--dropdown a.elementor-item').forEach(function (link) {
      link.addEventListener('click', function () {
        var toggle = document.querySelector('.elementor-menu-toggle[aria-expanded="true"]');
        if (toggle) toggle.click();
      });
    });
  }


  /* ==========================================================
     SECTION 9: OCCASION BADGES
     Injects a small occasion hint badge into each experience
     card on the Experiences page. Matched by card class or by
     slugified heading text. Duplicate guard prevents re-injection
     if init() is called more than once.
  ========================================================== */
  var cardOccasionMap = {
    'monaco-social':      'Birthdays and elevated groups',
    'golden-hour-escape': 'Intimate groups and sunset hosting',
    'rose-day-club':      'Social hosting from water to table',
    'pink-palm-club':     'Social groups who want music and movement'
  };

  function injectOccasionBadges() {
    document.querySelectorAll('.e-loop-item').forEach(function (card) {
      var slug    = '';
      var classes = Array.from(card.classList);

      /* Check card classes first */
      classes.forEach(function (cls) {
        if (cardOccasionMap[cls]) slug = cls;
      });

      /* Fall back to slugifying the heading text */
      if (!slug) {
        var titleEl = card.querySelector('.elementor-heading-title');
        if (titleEl) {
          var titleSlug = titleEl.textContent.trim().toLowerCase().replace(/\s+/g, '-');
          if (cardOccasionMap[titleSlug]) slug = titleSlug;
        }
      }

      if (!slug) return;

      /* Target the text editor or the known Elementor element for badge placement */
      var descContainer = card.querySelector('.elementor-widget-text-editor, .elementor-element-fa493d0');
      if (!descContainer) return;

      /* Duplicate guard: do not inject if badge already exists */
      if (descContainer.querySelector('.sss-occasion-badge')) return;

      var badge = document.createElement('div');
      badge.className   = 'sss-occasion-badge';
      badge.textContent = cardOccasionMap[slug];
      badge.style.cssText = [
        'font-family:"Inter",sans-serif',
        'font-size:10px',
        'letter-spacing:0.16em',
        'text-transform:uppercase',
        'color:#C9A96E',
        'padding:0 10px 8px',
        'display:block'
      ].join(';');

      descContainer.insertBefore(badge, descContainer.firstChild);
    });
  }


  /* ==========================================================
     SECTION 10: GTM DATALAYER EVENTS
     All analytics tracking pushed to window.dataLayer.
     Safe: dataLayer initialized if not already present.
     All selectors checked before use. No throws on missing elements.
  ========================================================== */

  /* Internal push helper - wraps dataLayer.push with safety check */
  function dlPush(event, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      var payload = { event: event };
      if (params && typeof params === 'object') {
        Object.keys(params).forEach(function (k) {
          payload[k] = params[k];
        });
      }
      window.dataLayer.push(payload);
    } catch (e) {
      /* dataLayer push must never break page execution */
    }
  }

  function initGtmEvents() {
    var path = window.location.pathname;

    /* ----------------------------------------------------------
       a. VIEW_HOMEPAGE
       Fires once on page load when user is on the homepage.
    ---------------------------------------------------------- */
    if (path === '/' || path === '/home/' || path === '/index.html') {
      dlPush('view_homepage', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       b. VIEW_REQUEST_PAGE
       Fires on the request-to-book page.
    ---------------------------------------------------------- */
    if (path.indexOf('/request-to-book/') !== -1) {
      dlPush('view_request_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       c. VIEW_EXPERIENCES_PAGE
       Fires on the experiences index page only (not sub-pages).
    ---------------------------------------------------------- */
    if (path === '/experiences/' || path === '/experiences') {
      dlPush('view_experiences_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       d. VIEW_EXPERIENCE_PAGE
       Fires on individual experience pages (/experience/*).
       Captures the experience slug for segmentation.
    ---------------------------------------------------------- */
    if (path.indexOf('/experience/') !== -1) {
      var expSlug = path.replace(/^\/experience\//, '').replace(/\/$/, '') || 'unknown';
      dlPush('view_experience_page', {
        experience_slug: expSlug,
        page_location:   window.location.href
      });
    }

    /* ----------------------------------------------------------
       f. CLICK_REQUEST_TO_BOOK
       Fires on any link that points to /request-to-book/.
       Detects which page section the click originated from.
    ---------------------------------------------------------- */
    document.querySelectorAll('a[href*="request-to-book"]').forEach(function (el) {
      el.addEventListener('click', function () {
        var ctaLocation = 'unknown';

        if (el.closest('.elementor-location-header')) {
          ctaLocation = 'nav';
        } else if (el.closest('.sss-hero') || el.closest('.elementor-section-hero')) {
          ctaLocation = 'hero';
        } else if (el.closest('.sss-email-capture')) {
          ctaLocation = 'email-capture';
        } else if (el.closest('.elementor-section-bottom-cta') || el.closest('.sss-bottom-cta')) {
          ctaLocation = 'bottom-cta';
        }

        dlPush('click_request_to_book', {
          cta_location:  ctaLocation,
          page_location: window.location.href
        });
      });
    });

    /* ----------------------------------------------------------
       g. CLICK_EXPLORE_EXPERIENCES
       Fires on any link to the /experiences/ page.
    ---------------------------------------------------------- */
    document.querySelectorAll('a[href*="/experiences/"]').forEach(function (el) {
      el.addEventListener('click', function () {
        dlPush('click_explore_experiences', {
          page_location: window.location.href
        });
      });
    });

    /* ----------------------------------------------------------
       h. CLICK_EXPERIENCE_CARD
       Fires when a user clicks into a specific experience card.
       Captures the experience name from the card heading and
       the card's 1-indexed position in the loop.
    ---------------------------------------------------------- */
    document.querySelectorAll('.e-loop-item').forEach(function (card, index) {
      var link = card.querySelector('a');
      if (!link) return;

      link.addEventListener('click', function () {
        var nameEl = card.querySelector('.elementor-heading-title');
        var name   = nameEl ? nameEl.textContent.trim() : 'unknown';

        dlPush('click_experience_card', {
          experience_name: name,
          card_position:   index + 1,
          page_location:   window.location.href
        });
      });
    });

    /* ----------------------------------------------------------
       i. START_BOOKING_FORM
       Fires on first focus or change interaction inside the
       booking form. One-shot: uses a flag to prevent repeat fires.
    ---------------------------------------------------------- */
    var bookingForm = document.querySelector(
      '.mf-form-body, form.wpcf7-form, [action*="request-to-book"]'
    );

    if (bookingForm) {
      var bookingStarted = false;

      ['focus', 'change'].forEach(function (eventType) {
        bookingForm.addEventListener(eventType, function () {
          if (bookingStarted) return;
          bookingStarted = true;

          dlPush('start_booking_form', {
            form_name: 'request-to-book'
          });
        });
      });

      /* ----------------------------------------------------------
         h. SUBMIT_BOOKING_FORM
         Fires on booking form submission. Captures occasion type
         and group size from named form fields.
      ---------------------------------------------------------- */
      bookingForm.addEventListener('submit', function () {
        var occasionEl  = bookingForm.querySelector('[name="occasion"]');
        var groupSizeEl = bookingForm.querySelector('[name="group_size"]');

        dlPush('submit_booking_form', {
          form_name:  'request-to-book',
          occasion:   occasionEl  ? occasionEl.value                     : '',
          group_size: groupSizeEl ? (parseInt(groupSizeEl.value, 10) || 0) : 0
        });
      });
    }

    /* ----------------------------------------------------------
       i. SUBMIT_EMAIL_CAPTURE
       Fires when the homepage .sss-email-form is submitted.
    ---------------------------------------------------------- */
    var emailForm = document.querySelector('.sss-email-form');
    if (emailForm) {
      emailForm.addEventListener('submit', function () {
        dlPush('submit_email_capture', {
          form_location: window.location.href
        });
      });
    }

    /* ----------------------------------------------------------
       j. CLICK_PHONE
       Fires when the user taps a tel: link anywhere on the page.
    ---------------------------------------------------------- */
    document.querySelectorAll('a[href^="tel:"]').forEach(function (el) {
      el.addEventListener('click', function () {
        dlPush('click_phone', {
          page_location: window.location.href
        });
      });
    });

    /* ----------------------------------------------------------
       k. OPEN_CHAT
       Fires when the Tidio live chat widget is opened.
       Uses the Tidio public API if loaded; falls back to the
       custom DOM event for async-loaded instances.
    ---------------------------------------------------------- */
    if (typeof tidioChatApi !== 'undefined') {
      tidioChatApi.on('open', function () {
        dlPush('open_chat', { page_location: window.location.href });
      });
    } else {
      document.addEventListener('tidioChat-open', function () {
        dlPush('open_chat', { page_location: window.location.href });
      });
    }

    /* ----------------------------------------------------------
       l. VIEW_ABOUT_PAGE
       Fires on the about page.
    ---------------------------------------------------------- */
    if (path === '/about/' || path === '/about') {
      dlPush('view_about_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       m. VIEW_CONTACT_PAGE
       Fires on the contact page.
    ---------------------------------------------------------- */
    if (path === '/contact/' || path === '/contact') {
      dlPush('view_contact_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       o. VIEW_FAQ_PAGE
       Fires on the FAQ page.
    ---------------------------------------------------------- */
    if (path === '/faq/' || path === '/faq') {
      dlPush('view_faq_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       p. VIEW_JOURNAL_PAGE
       Fires on the journal or blog index page.
    ---------------------------------------------------------- */
    if (path === '/journal/' || path === '/journal' || path === '/blog/' || path === '/blog') {
      dlPush('view_journal_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       n. VIEW_THANK_YOU_PAGE
       Fires on confirmation or thank-you pages.
    ---------------------------------------------------------- */
    if (
      path.indexOf('/thank-you')    !== -1 ||
      path.indexOf('/confirmation') !== -1
    ) {
      dlPush('view_thank_you_page', {
        page_location: window.location.href
      });
    }

    /* ----------------------------------------------------------
       m. SCROLL_50_PERCENT / n. SCROLL_90_PERCENT
       Fires once when the user scrolls to 50% and 90% of the
       total page height respectively. Tracked with per-milestone
       flags to ensure each event fires only once per page load.
    ---------------------------------------------------------- */
    var scroll50Fired = false;
    var scroll90Fired = false;

    window.addEventListener('scroll', function () {
      if (scroll50Fired && scroll90Fired) return;

      var scrollTop    = document.documentElement.scrollTop || document.body.scrollTop || 0;
      var scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (scrollHeight <= 0) return;

      var pct = scrollTop / scrollHeight;

      if (!scroll50Fired && pct >= 0.5) {
        scroll50Fired = true;
        dlPush('scroll_50_percent', { page_location: window.location.href });
      }

      if (!scroll90Fired && pct >= 0.9) {
        scroll90Fired = true;
        dlPush('scroll_90_percent', { page_location: window.location.href });
      }
    }, { passive: true });
  }


  /* ==========================================================
     INIT
     Called on DOMContentLoaded (or immediately if DOM is already
     ready). UTM capture in Section 1 has already run synchronously.
  ========================================================== */
  function init() {
    /* Section 2: Hidden field population */
    populateHiddenFields();

    /* Section 3: Trust fixes */
    fixLogoAlt();
    fixPhoneLink();
    fixImageAlts();

    /* Section 4: Scroll reveal */
    initScrollReveal();

    /* Section 5: Header scroll state */
    initHeaderScroll();

    /* Section 6: Email capture */
    initEmailCapture();

    /* Section 7: Smooth scroll */
    initSmoothScroll();

    /* Section 8: Mobile nav close */
    initMobileNavClose();

    /* Section 9: Occasion badges */
    injectOccasionBadges();

    /* Section 10: GTM DataLayer events */
    initGtmEvents();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
