/**
 * She Said Sail: Luxury UX Enhancements
 * Version: 2.1
 * Branch: feature/luxury-conversion-overhaul
 *
 * Where to load:
 * WordPress > Settings > Insert Headers and Footers > Scripts in Footer
 * Wrap in: <script defer>...</script>
 *
 * Behavior: scroll reveals, mobile nav polish, header scroll state,
 * email capture, accessibility improvements, occasion badges.
 */

(function () {
  'use strict';

  /* Prevent double-execution if script is somehow loaded twice */
  if (window.__sssEnhancementsLoaded) return;
  window.__sssEnhancementsLoaded = true;


  /* ----------------------------------------------------------
     SCROLL REVEAL
     Adds .sss-revealed to elements with .sss-reveal class
     when they enter the viewport.
  ---------------------------------------------------------- */
  function initScrollReveal() {
    var elements = document.querySelectorAll('.sss-reveal');
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
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


  /* ----------------------------------------------------------
     HEADER SCROLL STATE
     Adds .sss-header-scrolled after 80px scroll.
     CSS uses this for a slightly more opaque shadow state.
  ---------------------------------------------------------- */
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

    updateHeader();
  }


  /* ----------------------------------------------------------
     LOGO ALT TEXT FIX
     Sets descriptive alt text on logo images.
     Targets header and footer logo containers by known Elementor IDs,
     with a broad fallback for any logo link image with empty alt.
  ---------------------------------------------------------- */
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


  /* ----------------------------------------------------------
     PHONE LINK FIX
     Turns dead href="#" phone number into a tap-to-call link.
     Primary: targets known footer Elementor container.
     Fallback: scans all icon-list items on the page.
  ---------------------------------------------------------- */
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

      if (/^\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}$/.test(text)) {
        link.setAttribute('href', 'tel:' + text.replace(/\D/g, ''));
        link.setAttribute('aria-label', 'Call She Said Sail at ' + text);
      }

      if (text === 'Miami, FL' || text === 'Fort Lauderdale, FL') {
        link.setAttribute('href', 'https://maps.google.com/?q=' + encodeURIComponent(text));
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        link.setAttribute('aria-label', 'She Said Sail location: ' + text);
      }
    });
  }


  /* ----------------------------------------------------------
     IMAGE ALT TEXT
     Adds meaningful alt text to experience and gallery images
     that have empty alt attributes.
  ---------------------------------------------------------- */
  function fixImageAlts() {
    var heroImages = document.querySelectorAll(
      '.elementor-5928 .elementor-element-5345389 .elementor-background-slideshow img'
    );
    heroImages.forEach(function (img) {
      if (!img.getAttribute('alt') || img.getAttribute('alt') === '') {
        img.setAttribute('alt', 'She Said Sail luxury yacht experience on the water');
      }
    });

    var cards = document.querySelectorAll('.e-loop-item');
    cards.forEach(function (card) {
      var img     = card.querySelector('img');
      var heading = card.querySelector('.elementor-heading-title');
      if (img && heading && (!img.getAttribute('alt') || img.getAttribute('alt') === '')) {
        img.setAttribute('alt', heading.textContent.trim() + ', She Said Sail experience');
      }
    });

    var featureImg = document.querySelector('.elementor-5928 .elementor-element-bc81594 img');
    if (featureImg && (!featureImg.getAttribute('alt') || featureImg.getAttribute('alt') === '')) {
      featureImg.setAttribute('alt', 'Curated yacht experience, She Said Sail');
    }
  }


  /* ----------------------------------------------------------
     EMAIL CAPTURE FORM
     Handles the sss-email-capture snippet submission.
     Replace the setTimeout placeholder with a real fetch() call
     pointing to your Make.com webhook.

     See: docs/backend/make-webhook-spec.md (M-EMAIL-CAPTURE-001)
     See: docs/backend/form-tracking-spec.md (Email Capture Form section)
  ---------------------------------------------------------- */
  function initEmailCapture() {
    var form = document.querySelector('.sss-email-form');
    if (!form) return;

    if (form.__sssEmailCaptureInit) return;
    form.__sssEmailCaptureInit = true;

    var input  = form.querySelector('input[type="email"]');
    var button = form.querySelector('button');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var email = input ? input.value.trim() : '';
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (input) {
          input.style.borderColor = 'rgba(207, 46, 46, 0.5)';
          input.focus();
        }
        return;
      }

      if (input) input.style.borderColor = '';
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
        Wire this fetch() to your Make.com webhook before going live.
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

      /* Remove this setTimeout when the fetch() above is wired */
      void payload;
      setTimeout(function () { showEmailSuccess(form); }, 600);
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
    success.textContent = 'You\'re on the inside. We\'ll be in touch.';
    if (form.parentNode) form.parentNode.replaceChild(success, form);
    requestAnimationFrame(function () { success.style.opacity = '1'; });
  }


  /* ----------------------------------------------------------
     SMOOTH SCROLL
     Handles anchor links with luxury easing.
  ---------------------------------------------------------- */
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


  /* ----------------------------------------------------------
     MOBILE NAV CLOSE ON LINK CLICK
     Closes burger menu when a nav link is tapped.
  ---------------------------------------------------------- */
  function initMobileNavClose() {
    document.querySelectorAll('.elementor-nav-menu--dropdown a.elementor-item').forEach(function (link) {
      link.addEventListener('click', function () {
        var toggle = document.querySelector('.elementor-menu-toggle[aria-expanded="true"]');
        if (toggle) toggle.click();
      });
    });
  }


  /* ----------------------------------------------------------
     EXPERIENCE CARD OCCASION BADGES
     Injects small occasion hint text under each card's image
     without requiring Elementor edits.
     Safe: duplicate guard prevents double injection.
  ---------------------------------------------------------- */
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

      classes.forEach(function (cls) {
        if (cardOccasionMap[cls]) slug = cls;
      });

      if (!slug) {
        var titleEl = card.querySelector('.elementor-heading-title');
        if (titleEl) {
          var title = titleEl.textContent.trim().toLowerCase().replace(/\s+/g, '-');
          if (cardOccasionMap[title]) slug = title;
        }
      }

      if (!slug) return;

      /* Target the description container by class name, not Elementor-generated ID */
      var descContainer = card.querySelector('.elementor-widget-text-editor, .elementor-element-fa493d0');
      if (!descContainer) return;

      /* Duplicate guard */
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


  /* ----------------------------------------------------------
     UTM AND SESSION STORAGE HELPERS
     Used by email capture to read persisted UTM values.
  ---------------------------------------------------------- */
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


  /* ----------------------------------------------------------
     INIT
  ---------------------------------------------------------- */
  function init() {
    fixLogoAlt();
    fixPhoneLink();
    fixImageAlts();
    initScrollReveal();
    initHeaderScroll();
    initEmailCapture();
    initSmoothScroll();
    initMobileNavClose();
    injectOccasionBadges();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
