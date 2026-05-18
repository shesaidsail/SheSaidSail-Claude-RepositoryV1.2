/**
 * She Said Sail — Rose Day Club
 * Page-specific JavaScript
 * Version: 1.0
 *
 * Features:
 * - UTM parameter capture and hidden field population
 * - Sticky mobile CTA bar
 * - FAQ accordion
 * - Scroll reveal animations
 * - Form analytics events
 */

(function () {
  'use strict';

  /* ===================================
     UTM CAPTURE
     =================================== */

  function getParam(name) {
    var url = new URLSearchParams(window.location.search);
    return url.get(name) || '';
  }

  function getOrSetSession(key, value) {
    if (value) {
      try { sessionStorage.setItem(key, value); } catch (e) {}
      return value;
    }
    try { return sessionStorage.getItem(key) || ''; } catch (e) { return ''; }
  }

  function populateHiddenFields() {
    var utmSource   = getOrSetSession('utm_source',   getParam('utm_source'));
    var utmMedium   = getOrSetSession('utm_medium',   getParam('utm_medium'));
    var utmCampaign = getOrSetSession('utm_campaign', getParam('utm_campaign'));
    var utmContent  = getOrSetSession('utm_content',  getParam('utm_content'));
    var utmTerm     = getOrSetSession('utm_term',     getParam('utm_term'));

    var fields = {
      'source_url':    window.location.href,
      'utm_source':    utmSource,
      'utm_medium':    utmMedium,
      'utm_campaign':  utmCampaign,
      'utm_content':   utmContent,
      'utm_term':      utmTerm,
      'page_name':     'rose-day-club',
      'brand':         'SSS',
      'city':          'Fort Lauderdale'
    };

    Object.keys(fields).forEach(function (name) {
      var el = document.querySelector('input[name="' + name + '"]');
      if (el) el.value = fields[name];
    });
  }

  /* ===================================
     STICKY MOBILE CTA
     =================================== */

  function initStickyCTA() {
    var bar = document.querySelector('.rdc-sticky-cta');
    if (!bar) return;

    var shown = false;
    var threshold = 0.3;

    function check() {
      var scrolled = window.scrollY / (document.body.scrollHeight - window.innerHeight);
      if (!shown && scrolled > threshold) {
        bar.classList.add('is-visible');
        shown = true;
      }
    }

    window.addEventListener('scroll', check, { passive: true });
    check();
  }

  /* ===================================
     FAQ ACCORDION
     =================================== */

  function initAccordion() {
    var items = document.querySelectorAll('.rdc-accordion__item');
    if (!items.length) return;

    items.forEach(function (item) {
      var trigger = item.querySelector('.rdc-accordion__trigger');
      if (!trigger) return;

      trigger.addEventListener('click', function () {
        var isOpen = item.classList.contains('is-open');

        items.forEach(function (i) {
          i.classList.remove('is-open');
        });

        if (!isOpen) {
          item.classList.add('is-open');
        }
      });
    });
  }

  /* ===================================
     SCROLL REVEAL
     =================================== */

  function initScrollReveal() {
    var elements = document.querySelectorAll('.rdc-reveal');
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
      elements.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(function (el) { observer.observe(el); });
  }

  /* ===================================
     SMOOTH SCROLL TO FORM
     =================================== */

  function initSmoothScroll() {
    document.querySelectorAll('a[href="#rdc-inquiry"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var target = document.getElementById('rdc-inquiry');
        if (!target) return;
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        var first = target.querySelector('input, select, textarea');
        if (first) setTimeout(function () { first.focus(); }, 600);
      });
    });
  }

  /* ===================================
     GTM EVENTS
     =================================== */

  function pushEvent(eventName, params) {
    if (!window.dataLayer) return;
    window.dataLayer.push(Object.assign({ event: eventName }, params));
  }

  function initAnalytics() {
    var form = document.getElementById('rdc-inquiry-form');
    if (!form) return;

    form.addEventListener('submit', function () {
      pushEvent('sss_form_submit', {
        page_name:  'rose-day-club',
        experience: 'Rose Day Club',
        form_id:    'rdc-inquiry-form'
      });
    });

    document.querySelectorAll('.rdc-btn--primary, .rdc-btn--ghost').forEach(function (btn) {
      btn.addEventListener('click', function () {
        pushEvent('sss_cta_click', {
          page_name:  'rose-day-club',
          cta_text:   btn.textContent.trim(),
          cta_location: btn.closest('section') ? btn.closest('section').className : 'unknown'
        });
      });
    });
  }

  /* ===================================
     FORM VALIDATION ENHANCEMENT
     =================================== */

  function initFormValidation() {
    var form = document.getElementById('rdc-inquiry-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      var valid = true;

      form.querySelectorAll('[required]').forEach(function (field) {
        var fieldGroup = field.closest('.rdc-form__field');
        var existing = fieldGroup && fieldGroup.querySelector('.rdc-form__error');
        if (existing) existing.remove();

        if (!field.value.trim()) {
          valid = false;
          if (fieldGroup) {
            var err = document.createElement('span');
            err.className = 'rdc-form__error';
            err.textContent = 'This field is required.';
            err.style.cssText = 'display:block;font-size:12px;color:#cc4444;margin-top:4px;';
            fieldGroup.appendChild(err);
          }
        }
      });

      if (!valid) {
        e.preventDefault();
        var firstError = form.querySelector('.rdc-form__error');
        if (firstError) {
          firstError.closest('.rdc-form__field').querySelector('input, select, textarea').focus();
        }
      }
    });
  }

  /* ===================================
     INIT
     =================================== */

  function init() {
    populateHiddenFields();
    initStickyCTA();
    initAccordion();
    initScrollReveal();
    initSmoothScroll();
    initAnalytics();
    initFormValidation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
