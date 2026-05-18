/**
 * SHE SAID SAIL
 * Pink Palm Club Experience Page
 * JavaScript: Analytics, Attribution, Form, UX
 * Version: 1.0 | May 2026
 *
 * Apply in Webflow: Page Settings > Custom Code > Body (before </body>)
 */

(function () {
  'use strict';

  /* ============================================================
     CONFIGURATION
     ============================================================ */

  var CONFIG = {
    EXPERIENCE_NAME: 'Pink Palm Club',
    EXPERIENCE_CITY: 'Fort Lauderdale',
    EXPERIENCE_YACHT: 'Lucky Star',
    EXPERIENCE_DURATION: '4 hours',
    EXPERIENCE_BOARDING: 'Fort Lauderdale Beach Marina',
    FORM_SELECTOR: '#ppc-inquiry-form',
    FORM_SECTION_SELECTOR: '#ppc-form-section',
    HERO_SELECTOR: '.ppc-hero',
    FLOATING_CTA_SELECTOR: '.ppc-floating-cta',
    SCROLL_DEPTH_MILESTONES: [25, 50, 75, 100]
  };

  /* ============================================================
     UTILITY: GET URL PARAMETER
     ============================================================ */

  function getUrlParam(name) {
    var url = window.location.search;
    var regex = new RegExp('[?&]' + name + '=([^&#]*)');
    var match = regex.exec(url);
    return match ? decodeURIComponent(match[1].replace(/\+/g, ' ')) : '';
  }

  /* ============================================================
     UTILITY: PUSH TO GTM DATA LAYER
     ============================================================ */

  function pushEvent(eventName, eventData) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: eventName };
    if (eventData) {
      Object.keys(eventData).forEach(function (key) {
        payload[key] = eventData[key];
      });
    }
    window.dataLayer.push(payload);
  }

  /* ============================================================
     ATTRIBUTION: CAPTURE UTM PARAMS
     ============================================================ */

  function captureAttribution() {
    var utmSource   = getUrlParam('utm_source');
    var utmMedium   = getUrlParam('utm_medium');
    var utmCampaign = getUrlParam('utm_campaign');
    var utmContent  = getUrlParam('utm_content');
    var utmTerm     = getUrlParam('utm_term');

    if (utmSource) {
      sessionStorage.setItem('sss_utm_source',   utmSource);
      sessionStorage.setItem('sss_utm_medium',   utmMedium);
      sessionStorage.setItem('sss_utm_campaign', utmCampaign);
      sessionStorage.setItem('sss_utm_content',  utmContent);
      sessionStorage.setItem('sss_utm_term',     utmTerm);
    }

    return {
      utm_source:   sessionStorage.getItem('sss_utm_source')   || '',
      utm_medium:   sessionStorage.getItem('sss_utm_medium')   || '',
      utm_campaign: sessionStorage.getItem('sss_utm_campaign') || '',
      utm_content:  sessionStorage.getItem('sss_utm_content')  || '',
      utm_term:     sessionStorage.getItem('sss_utm_term')     || ''
    };
  }

  /* ============================================================
     FORM: POPULATE HIDDEN FIELDS
     ============================================================ */

  function populateHiddenFields(form) {
    var attribution = captureAttribution();

    var fields = {
      'experience':        CONFIG.EXPERIENCE_NAME,
      'yacht':             CONFIG.EXPERIENCE_YACHT,
      'city':              CONFIG.EXPERIENCE_CITY,
      'duration':          CONFIG.EXPERIENCE_DURATION,
      'boarding_location': CONFIG.EXPERIENCE_BOARDING,
      'source_url':        window.location.href,
      'page_slug':         window.location.pathname,
      'utm_source':        attribution.utm_source,
      'utm_medium':        attribution.utm_medium,
      'utm_campaign':      attribution.utm_campaign,
      'utm_content':       attribution.utm_content,
      'utm_term':          attribution.utm_term
    };

    Object.keys(fields).forEach(function (fieldName) {
      var input = form.querySelector('input[name="' + fieldName + '"]');
      if (input && !input.value) {
        input.value = fields[fieldName];
      }
    });
  }

  /* ============================================================
     FORM: TRACK FORM START
     ============================================================ */

  var formStarted = false;

  function trackFormStart() {
    if (!formStarted) {
      formStarted = true;
      pushEvent('sss_form_start', {
        experience_name: CONFIG.EXPERIENCE_NAME,
        page_url:        window.location.href
      });
    }
  }

  /* ============================================================
     FORM: VALIDATE REQUIRED FIELDS
     ============================================================ */

  function validateForm(form) {
    var valid = true;
    var requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(function (field) {
      var errorEl = form.querySelector('[data-error-for="' + field.name + '"]');

      if (!field.value.trim()) {
        valid = false;
        field.style.borderColor = '#c0392b';
        if (errorEl) errorEl.style.display = 'block';
      } else {
        field.style.borderColor = '';
        if (errorEl) errorEl.style.display = 'none';
      }
    });

    return valid;
  }

  /* ============================================================
     FORM: HANDLE SUBMISSION
     ============================================================ */

  function initForm() {
    var form = document.querySelector(CONFIG.FORM_SELECTOR);
    if (!form) return;

    populateHiddenFields(form);

    var inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(function (input) {
      input.addEventListener('focus', trackFormStart, { once: true });
    });

    form.addEventListener('submit', function (e) {
      if (!validateForm(form)) {
        e.preventDefault();
        var firstError = form.querySelector('[style*="c0392b"]');
        if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      pushEvent('sss_lead_submitted', {
        experience_name: CONFIG.EXPERIENCE_NAME,
        city:            CONFIG.EXPERIENCE_CITY,
        utm_source:      sessionStorage.getItem('sss_utm_source') || 'direct',
        utm_campaign:    sessionStorage.getItem('sss_utm_campaign') || ''
      });
    });

    if (typeof Webflow !== 'undefined' && Webflow.push) {
      Webflow.push(function () {
        $(CONFIG.FORM_SELECTOR).on('success.webflow', function () {
          showFormSuccess(form);

          pushEvent('sss_lead_submitted_confirmed', {
            experience_name: CONFIG.EXPERIENCE_NAME,
            city:            CONFIG.EXPERIENCE_CITY
          });

          if (typeof gtag === 'function') {
            gtag('event', 'conversion', {
              send_to: 'AW-CONVERSION_ID/CONVERSION_LABEL'
            });
          }
        });
      });
    }
  }

  /* ============================================================
     FORM: SHOW SUCCESS STATE
     ============================================================ */

  function showFormSuccess(form) {
    var formInner = form.querySelector('.ppc-form__inner');
    var successEl = form.querySelector('.ppc-form__success');

    if (formInner) formInner.style.display = 'none';
    if (successEl) {
      successEl.classList.add('is-visible');
      successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    var floatingCta = document.querySelector(CONFIG.FLOATING_CTA_SELECTOR);
    if (floatingCta) floatingCta.classList.add('is-hidden');
  }

  /* ============================================================
     ANALYTICS: PAGE VIEW
     ============================================================ */

  function trackPageView() {
    var attribution = captureAttribution();

    pushEvent('sss_page_view', {
      page_type:       'experience',
      experience_name: CONFIG.EXPERIENCE_NAME,
      page_url:        window.location.href,
      utm_source:      attribution.utm_source,
      utm_medium:      attribution.utm_medium,
      utm_campaign:    attribution.utm_campaign
    });
  }

  /* ============================================================
     ANALYTICS: SCROLL DEPTH
     ============================================================ */

  function initScrollDepth() {
    var milestones = CONFIG.SCROLL_DEPTH_MILESTONES.slice();
    var fired = [];

    function checkScrollDepth() {
      var scrollTop    = window.scrollY || document.documentElement.scrollTop;
      var docHeight    = document.documentElement.scrollHeight - window.innerHeight;
      var scrollPct    = Math.round((scrollTop / docHeight) * 100);

      milestones.forEach(function (pct) {
        if (scrollPct >= pct && fired.indexOf(pct) === -1) {
          fired.push(pct);
          pushEvent('sss_scroll_depth', {
            depth_pct:       pct,
            experience_name: CONFIG.EXPERIENCE_NAME
          });
        }
      });
    }

    window.addEventListener('scroll', checkScrollDepth, { passive: true });
  }

  /* ============================================================
     ANALYTICS: CTA CLICK TRACKING
     ============================================================ */

  function initCtaTracking() {
    document.addEventListener('click', function (e) {
      var target = e.target.closest('.ppc-btn, [data-cta]');
      if (!target) return;

      pushEvent('sss_cta_click', {
        cta_text:        target.textContent.trim(),
        cta_location:    target.getAttribute('data-cta-location') || 'unknown',
        experience_name: CONFIG.EXPERIENCE_NAME
      });
    });
  }

  /* ============================================================
     UX: FLOATING MOBILE CTA
     ============================================================ */

  function initFloatingCta() {
    var floatingCta = document.querySelector(CONFIG.FLOATING_CTA_SELECTOR);
    var hero        = document.querySelector(CONFIG.HERO_SELECTOR);
    if (!floatingCta || !hero) return;

    floatingCta.classList.add('is-hidden');

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            floatingCta.classList.remove('is-hidden');
          } else {
            floatingCta.classList.add('is-hidden');
          }
        });
      },
      { threshold: 0.1 }
    );

    observer.observe(hero);
  }

  /* ============================================================
     UX: SMOOTH SCROLL TO FORM
     ============================================================ */

  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var anchor = e.target.closest('[href="#ppc-form-section"], [data-scroll-to="form"]');
      if (!anchor) return;

      e.preventDefault();
      var target = document.querySelector(CONFIG.FORM_SECTION_SELECTOR);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(function () {
          var firstInput = target.querySelector('input:not([type="hidden"])');
          if (firstInput) firstInput.focus();
        }, 600);
      }
    });
  }

  /* ============================================================
     UX: ADD-ON SELECTION (checkbox visual enhancement)
     ============================================================ */

  function initAddonSelection() {
    var addonCards = document.querySelectorAll('.ppc-addon-card[data-addon]');

    addonCards.forEach(function (card) {
      card.addEventListener('click', function () {
        var addonName = card.getAttribute('data-addon');
        card.classList.toggle('is-selected');

        if (card.classList.contains('is-selected')) {
          card.style.borderColor = 'var(--sss-gold)';
          card.style.background  = 'rgba(201, 168, 76, 0.05)';
        } else {
          card.style.borderColor = '';
          card.style.background  = '';
        }

        updateAddonHiddenField();
      });
    });

    function updateAddonHiddenField() {
      var form = document.querySelector(CONFIG.FORM_SELECTOR);
      if (!form) return;

      var selected = [];
      document.querySelectorAll('.ppc-addon-card.is-selected').forEach(function (card) {
        selected.push(card.getAttribute('data-addon'));
      });

      var addonsInput = form.querySelector('input[name="add_ons"]');
      if (addonsInput) addonsInput.value = selected.join(', ');
    }
  }

  /* ============================================================
     INIT
     ============================================================ */

  function init() {
    trackPageView();
    initForm();
    initScrollDepth();
    initCtaTracking();
    initFloatingCta();
    initSmoothScroll();
    initAddonSelection();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
