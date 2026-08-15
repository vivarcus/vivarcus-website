/* ============================================================
   Vivarcus Website — i18n Engine
   ============================================================ */

(function () {
  'use strict';

  const STORAGE_KEY = 'vivarcus-lang';
  const DEFAULT_LANG = 'zh';
  const SUPPORTED = ['zh', 'en'];

  /**
   * Resolve the initial language:
   *   1. localStorage preference
   *   2. browser navigator.language (e.g. "en-US" → "en")
   *   3. default (zh)
   */
  function detectLang() {
    if (window.__VIVARCUS_HEAD_LANG__) return window.__VIVARCUS_HEAD_LANG__;

    var params = new URLSearchParams(window.location.search);
    var urlLang = params.get('lang');
    if (urlLang && SUPPORTED.indexOf(urlLang) !== -1) return urlLang;

    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored && SUPPORTED.indexOf(stored) !== -1) return stored;

    var browser = (navigator.language || '').split('-')[0];
    if (browser && SUPPORTED.indexOf(browser) !== -1) return browser;

    return DEFAULT_LANG;
  }

  function syncLangURL(lang) {
    var url = new URL(window.location.href);
    if (lang === 'en') {
      url.searchParams.set('lang', 'en');
    } else {
      url.searchParams.delete('lang');
    }
    var next = url.pathname + url.search + url.hash;
    history.replaceState(null, '', next);
  }

  /**
   * Get the zh/en label key appropriate for the current state.
   * When lang=zh we show "EN" as the target; when lang=en we show "中".
   */
  function targetLang(current) {
    return current === 'zh' ? 'en' : 'zh';
  }

  /**
   * Apply translations for the given language.
   * Walks:
   *   [data-i18n]        → textContent
   *   [data-i18n-html]   → innerHTML
   *   [data-i18n-aria]   → aria-label
   *   [data-i18n-placeholder] → placeholder
   *   [data-i18n-meta]   → meta content
   *   [data-lang-zh] / [data-lang-en] → show/hide (for language switcher label)
   */
  function apply(lang) {
    var dict = (window.I18N_DATA || {})[lang] || {};

    // Update <html lang>
    var htmlLang = lang === 'zh' ? 'zh-CN' : 'en-US';
    document.documentElement.lang = htmlLang;

    // Simple text
    var els = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < els.length; i++) {
      var key = els[i].getAttribute('data-i18n');
      if (dict[key] !== undefined) {
        els[i].textContent = dict[key];
      }
    }

    // HTML content
    els = document.querySelectorAll('[data-i18n-html]');
    for (i = 0; i < els.length; i++) {
      key = els[i].getAttribute('data-i18n-html');
      if (dict[key] !== undefined) {
        els[i].innerHTML = dict[key];
      }
    }

    // Accessible labels (must not touch element children)
    els = document.querySelectorAll('[data-i18n-aria]');
    for (i = 0; i < els.length; i++) {
      key = els[i].getAttribute('data-i18n-aria');
      if (dict[key] !== undefined) {
        els[i].setAttribute('aria-label', dict[key]);
      }
    }

    // Placeholders
    els = document.querySelectorAll('[data-i18n-placeholder]');
    for (i = 0; i < els.length; i++) {
      key = els[i].getAttribute('data-i18n-placeholder');
      if (dict[key] !== undefined) {
        els[i].placeholder = dict[key];
      }
    }

    // Language-specific href targets (e.g. help center zh/en subdirectories)
    els = document.querySelectorAll('[data-lang-href-zh]');
    for (i = 0; i < els.length; i++) {
      var target = lang === 'zh'
        ? els[i].getAttribute('data-lang-href-zh')
        : els[i].getAttribute('data-lang-href-en');
      if (target) els[i].setAttribute('href', target);
    }

    // Meta description & Open Graph / Twitter
    els = document.querySelectorAll('[data-i18n-meta], [data-i18n-og]');
    for (i = 0; i < els.length; i++) {
      key = els[i].getAttribute('data-i18n-meta') || els[i].getAttribute('data-i18n-og');
      if (key && dict[key] !== undefined) {
        els[i].setAttribute('content', dict[key]);
      }
    }

    var ogLocale = document.querySelector('meta[property="og:locale"]');
    if (ogLocale) {
      ogLocale.setAttribute('content', lang === 'zh' ? 'zh_CN' : 'en_US');
    }

    // Document title
    var titleKey = document.documentElement.getAttribute('data-i18n-title');
    if (titleKey && dict[titleKey] !== undefined) {
      document.title = dict[titleKey];
    }

    // Language switcher label: show target language indicator
    var zhLabels = document.querySelectorAll('[data-lang-zh]');
    var enLabels = document.querySelectorAll('[data-lang-en]');
    for (i = 0; i < zhLabels.length; i++) { zhLabels[i].style.display = lang === 'en' ? '' : 'none'; }
    for (i = 0; i < enLabels.length; i++) { enLabels[i].style.display = lang === 'en' ? 'none' : ''; }

    // Update switcher aria-label
    var toggles = document.querySelectorAll('[data-lang-toggle]');
    var target = targetLang(lang);
    var switchLabel = dict['common.lang.switchTo'] || (target === 'zh' ? '切换到中文' : 'Switch to English');
    for (i = 0; i < toggles.length; i++) {
      toggles[i].setAttribute('aria-label', switchLabel);
    }

    // Update form submit _subject hidden input if present
    var subjectInput = document.querySelector('input[name="_subject"]');
    if (subjectInput) {
      var subjectKey = 'trial.form.subject';
      if (dict[subjectKey] !== undefined) {
        subjectInput.value = dict[subjectKey];
      }
    }

    // Dispatch event so inline scripts (like trial form) know language changed
    window.dispatchEvent(new CustomEvent('langchange', { detail: { lang: lang } }));
  }

  var currentLang = detectLang();

  /**
   * Public API
   */
  window.I18N = {
    getLang: function () { return currentLang; },

    setLang: function (lang) {
      if (!lang || SUPPORTED.indexOf(lang) === -1) return;
      currentLang = lang;
      window.__VIVARCUS_HEAD_LANG__ = lang;
      localStorage.setItem(STORAGE_KEY, lang);
      apply(lang);
      syncLangURL(lang);
    },

    toggle: function () {
      window.I18N.setLang(targetLang(currentLang));
    },

    /**
     * Look up a single translation key for the given (or current) language.
     * Useful for inline JS strings (e.g. form validation errors).
     */
    t: function (key, lang) {
      lang = lang || currentLang;
      var dict = (window.I18N_DATA || {})[lang] || {};
      return dict[key] !== undefined ? dict[key] : key;
    },
  };

  // Apply on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      apply(currentLang);
      syncLangURL(currentLang);
    });
  } else {
    apply(currentLang);
    syncLangURL(currentLang);
  }
})();
