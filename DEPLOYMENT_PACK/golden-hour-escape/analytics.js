/**
 * GOLDEN HOUR ESCAPE — ANALYTICS + TRACKING
 * FILE: DEPLOYMENT_PACK/golden-hour-escape/analytics.js
 * VERSION: 1.0 | DATE: May 2026
 *
 * IMPLEMENTATION:
 * 1. Ensure GTM container tag is in the <head> (GTM loads dataLayer)
 * 2. Paste this script in Webflow: Pages > Golden Hour Escape > Custom Code > Footer Code
 * 3. All events push to dataLayer and are read by GTM triggers
 *
 * GTM TRIGGERS TO CREATE (see analytics-gtm-config.md):
 * - sss_page_view
 * - sss_form_start
 * - sss_form_submit
 * - sss_cta_click
 * - sss_scroll_depth_50
 * - sss_scroll_depth_75
 * - sss_section_view_[name]
 */

(function() {
  'use strict';

  // Initialize dataLayer
  window.dataLayer = window.dataLayer || [];

  var PAGE_CONTEXT = {
    experience_name: 'Golden Hour Escape',
    page_slug: '/experience/golden-hour-escape/',
    page_category: 'experience',
    brand: 'SSS'
  };

  // ===========================
  // UTM CAPTURE + HIDDEN FIELDS
  // ===========================

  function getParam(key) {
    return new URLSearchParams(window.location.search).get(key) || '';
  }

  function populateHiddenFields() {
    var fieldMap = {
      'source_url':    window.location.href,
      'utm_source':    getParam('utm_source'),
      'utm_medium':    getParam('utm_medium'),
      'utm_campaign':  getParam('utm_campaign'),
      'utm_content':   getParam('utm_content'),
      'utm_term':      getParam('utm_term'),
      'page_slug':     window.location.pathname,
      'referrer':      document.referrer
    };

    Object.keys(fieldMap).forEach(function(key) {
      var el = document.querySelector('[name="' + key + '"]');
      if (el) el.value = fieldMap[key];
    });
  }

  // ===========================
  // PAGE VIEW EVENT
  // ===========================

  function firePageView() {
    window.dataLayer.push({
      event: 'sss_page_view',
      event_category: 'experience',
      experience_name: PAGE_CONTEXT.experience_name,
      page_slug: PAGE_CONTEXT.page_slug,
      utm_source: getParam('utm_source'),
      utm_medium: getParam('utm_medium'),
      utm_campaign: getParam('utm_campaign')
    });
  }

  // ===========================
  // CTA CLICK TRACKING
  // ===========================

  function bindCtaClicks() {
    var ctaSelectors = [
      '.ghe-hero .ghe-btn-primary',
      '.ghe-btn-primary[href*="form"]',
      '.ghe-sticky-cta a',
      'a[href="#reserve"]',
      'a[href="#inquiry"]',
      'a[href="#form"]'
    ];

    var ctaElements = document.querySelectorAll(ctaSelectors.join(','));

    ctaElements.forEach(function(el) {
      el.addEventListener('click', function() {
        window.dataLayer.push({
          event: 'sss_cta_click',
          event_category: 'experience',
          event_label: el.textContent.trim() || 'hero_cta',
          experience_name: PAGE_CONTEXT.experience_name,
          cta_location: el.closest('[class]') ? el.closest('[class]').className.split(' ')[0] : 'unknown'
        });
      });
    });
  }

  // ===========================
  // FORM TRACKING
  // ===========================

  var formStarted = false;

  function bindFormTracking() {
    var form = document.querySelector('form[id*="golden"], form[id*="ghe"], .ghe-form, form.w-form-form');

    if (!form) {
      // Fallback: find the first form in the form section
      var formSection = document.querySelector('.ghe-form-section, #reserve, #inquiry');
      if (formSection) form = formSection.querySelector('form');
    }

    if (!form) return;

    // Form start (first interaction)
    form.addEventListener('focusin', function() {
      if (formStarted) return;
      formStarted = true;
      window.dataLayer.push({
        event: 'sss_form_start',
        event_category: 'experience',
        experience_name: PAGE_CONTEXT.experience_name,
        form_id: form.id || 'golden-hour-inquiry'
      });
    }, { once: false });

    // Form submit
    form.addEventListener('submit', function() {
      var guestCount = form.querySelector('[name="guest_count"]');
      var occasion = form.querySelector('[name="occasion"]');
      var preferredDate = form.querySelector('[name="preferred_date"]');

      window.dataLayer.push({
        event: 'sss_form_submit',
        event_category: 'experience',
        experience_name: PAGE_CONTEXT.experience_name,
        form_id: form.id || 'golden-hour-inquiry',
        guest_count: guestCount ? guestCount.value : '',
        occasion: occasion ? occasion.value : '',
        has_date: preferredDate ? (preferredDate.value ? 'yes' : 'no') : 'unknown',
        utm_source: getParam('utm_source'),
        utm_medium: getParam('utm_medium'),
        utm_campaign: getParam('utm_campaign')
      });
    });
  }

  // ===========================
  // SCROLL DEPTH TRACKING
  // ===========================

  var scrollFired = { 25: false, 50: false, 75: false, 90: false };

  function bindScrollDepth() {
    window.addEventListener('scroll', function() {
      var scrollPct = Math.round(
        (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
      );

      [25, 50, 75, 90].forEach(function(depth) {
        if (!scrollFired[depth] && scrollPct >= depth) {
          scrollFired[depth] = true;
          window.dataLayer.push({
            event: 'sss_scroll_depth_' + depth,
            event_category: 'experience',
            experience_name: PAGE_CONTEXT.experience_name,
            scroll_depth: depth
          });
        }
      });
    }, { passive: true });
  }

  // ===========================
  // SECTION VIEW TRACKING (Intersection Observer)
  // ===========================

  function bindSectionViews() {
    if (!window.IntersectionObserver) return;

    var sections = [
      { selector: '.ghe-experience', name: 'experience_copy' },
      { selector: '.ghe-includes', name: 'what_included' },
      { selector: '.ghe-addons', name: 'add_ons' },
      { selector: '.ghe-reviews', name: 'social_proof' },
      { selector: '.ghe-form-section', name: 'inquiry_form' }
    ];

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var sectionName = entry.target.dataset.sectionName;
          window.dataLayer.push({
            event: 'sss_section_view',
            event_category: 'experience',
            event_label: sectionName,
            experience_name: PAGE_CONTEXT.experience_name
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    sections.forEach(function(item) {
      var el = document.querySelector(item.selector);
      if (el) {
        el.dataset.sectionName = item.name;
        observer.observe(el);
      }
    });
  }

  // ===========================
  // STICKY CTA VISIBILITY
  // ===========================

  function manageStickyCtaVisibility() {
    var stickyCta = document.querySelector('.ghe-sticky-cta');
    if (!stickyCta) return;

    var formSection = document.querySelector('.ghe-form-section, #reserve, #inquiry');

    if (!formSection) return;

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          stickyCta.classList.add('is-hidden');
        } else {
          stickyCta.classList.remove('is-hidden');
        }
      });
    }, { threshold: 0.1 });

    observer.observe(formSection);
  }

  // ===========================
  // INIT
  // ===========================

  function init() {
    populateHiddenFields();
    firePageView();
    bindCtaClicks();
    bindFormTracking();
    bindScrollDepth();
    bindSectionViews();
    manageStickyCtaVisibility();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
