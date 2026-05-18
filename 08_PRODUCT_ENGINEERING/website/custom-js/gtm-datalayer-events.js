/**
 * She Said Sail: GTM DataLayer Events
 * Version: 1.0
 * Branch: feature/luxury-conversion-overhaul
 *
 * Load via GTM > Tags > Custom HTML, trigger: All Pages
 * OR via Insert Headers and Footers plugin (Scripts in Footer, deferred).
 *
 * Pushes custom events to window.dataLayer for GTM to consume.
 * Safe for WordPress/Elementor: no conflicts with existing scripts.
 * All selectors are prefixed or scoped to avoid false positives.
 */

(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  function push(event, params) {
    var payload = { event: event };
    if (params && typeof params === 'object') {
      Object.keys(params).forEach(function (k) {
        payload[k] = params[k];
      });
    }
    window.dataLayer.push(payload);
  }


  /* ----------------------------------------------------------
     VIEW_HOMEPAGE
     Fires on homepage load only.
  ---------------------------------------------------------- */
  var path = window.location.pathname;
  var isHomepage = path === '/' || path === '/home/' || path === '/index.html';

  if (isHomepage) {
    push('view_homepage', {
      page_location: window.location.href
    });
  }


  /* ----------------------------------------------------------
     CLICK_REQUEST_TO_BOOK
     Fires on any CTA that links to /request-to-book/
     Captures which section the click came from.
  ---------------------------------------------------------- */
  document.querySelectorAll('a[href*="request-to-book"]').forEach(function (el) {
    el.addEventListener('click', function () {
      var location = 'unknown';

      if (el.closest('.elementor-location-header')) {
        location = 'nav';
      } else if (el.closest('.sss-hero') || el.closest('.elementor-section-hero')) {
        location = 'hero';
      } else if (el.closest('.sss-email-capture')) {
        location = 'email-capture';
      } else if (el.closest('.elementor-section-bottom-cta') || el.closest('.sss-bottom-cta')) {
        location = 'bottom-cta';
      }

      push('click_request_to_book', {
        cta_location:  location,
        page_location: window.location.href
      });
    });
  });


  /* ----------------------------------------------------------
     CLICK_EXPLORE_EXPERIENCES
     Fires on any CTA that links to /experiences/
  ---------------------------------------------------------- */
  document.querySelectorAll('a[href*="/experiences/"]').forEach(function (el) {
    el.addEventListener('click', function () {
      push('click_explore_experiences', {
        cta_location:  'hero',
        page_location: window.location.href
      });
    });
  });


  /* ----------------------------------------------------------
     CLICK_EXPERIENCE_CARD
     Fires when a user clicks into an experience detail card.
     Captures which experience was clicked and its position.
  ---------------------------------------------------------- */
  document.querySelectorAll('.e-loop-item').forEach(function (card, index) {
    var link = card.querySelector('a');
    if (!link) return;

    link.addEventListener('click', function () {
      var nameEl = card.querySelector('.elementor-heading-title');
      var name   = nameEl ? nameEl.textContent.trim() : 'unknown';

      push('click_experience_card', {
        experience_name: name,
        card_position:   index + 1,
        page_location:   window.location.href
      });
    });
  });


  /* ----------------------------------------------------------
     CLICK_PHONE
     Fires when the user taps the phone number.
  ---------------------------------------------------------- */
  document.querySelectorAll('a[href^="tel:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      push('click_phone', {
        page_location: window.location.href
      });
    });
  });


  /* ----------------------------------------------------------
     OPEN_CHAT
     Fires when Tidio chat is opened.
     Uses Tidio's public API callback.
  ---------------------------------------------------------- */
  if (typeof tidioChatApi !== 'undefined') {
    tidioChatApi.on('open', function () {
      push('open_chat', {
        page_location: window.location.href
      });
    });
  } else {
    document.addEventListener('tidioChat-open', function () {
      push('open_chat', {
        page_location: window.location.href
      });
    });
  }


  /* ----------------------------------------------------------
     START_BOOKING_FORM
     Fires on first interaction with the booking form.
     Uses a one-shot listener to avoid repeated fires.
  ---------------------------------------------------------- */
  var bookingForm = document.querySelector('.mf-form-body, form.wpcf7-form, #booking-form, [action*="request-to-book"]');

  if (bookingForm) {
    var bookingStarted = false;

    var startEvents = ['focus', 'change'];
    startEvents.forEach(function (eventType) {
      bookingForm.addEventListener(eventType, function () {
        if (bookingStarted) return;
        bookingStarted = true;

        push('start_booking_form', {
          form_name: 'request-to-book'
        });
      }, { once: false });
    });
  }


  /* ----------------------------------------------------------
     SUBMIT_BOOKING_FORM
     Fires on confirmed form submission.
     Captures occasion and group size from form fields.
  ---------------------------------------------------------- */
  if (bookingForm) {
    bookingForm.addEventListener('submit', function () {
      var occasionEl   = bookingForm.querySelector('[name="occasion"]');
      var groupSizeEl  = bookingForm.querySelector('[name="group_size"]');

      push('submit_booking_form', {
        form_name:  'request-to-book',
        occasion:   occasionEl   ? occasionEl.value   : '',
        group_size: groupSizeEl  ? parseInt(groupSizeEl.value, 10) || 0 : 0
      });
    });
  }


  /* ----------------------------------------------------------
     SUBMIT_EMAIL_CAPTURE
     Fires when the homepage email form is submitted.
     Integrates with the sss-email-form in email-capture-section.html.
  ---------------------------------------------------------- */
  var emailForm = document.querySelector('.sss-email-form');

  if (emailForm) {
    emailForm.addEventListener('submit', function () {
      push('submit_email_capture', {
        form_location: 'homepage'
      });
    });
  }


  /* ----------------------------------------------------------
     VIEW_THANK_YOU_PAGE
     Fires on /thank-you/ page or any confirmation URL.
  ---------------------------------------------------------- */
  if (window.location.pathname.indexOf('/thank-you') !== -1 ||
      window.location.pathname.indexOf('/confirmation') !== -1) {
    push('view_thank_you_page', {
      page_location: window.location.href
    });
  }

})();
