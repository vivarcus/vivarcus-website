/* ============================================================
   Vivarcus Website — Early <head> SEO (runs before body paint)
   Reads ?lang= so crawlers get the correct title/description.
   ============================================================ */

(function () {
  'use strict';

  var STORAGE_KEY = 'vivarcus-lang';
  var SUPPORTED = ['zh', 'en'];

  function detectLang() {
    var params = new URLSearchParams(window.location.search);
    var urlLang = params.get('lang');
    if (urlLang && SUPPORTED.indexOf(urlLang) !== -1) return urlLang;

    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored && SUPPORTED.indexOf(stored) !== -1) return stored;

    var browser = (navigator.language || '').split('-')[0];
    if (browser && SUPPORTED.indexOf(browser) !== -1) return browser;

    return 'zh';
  }

  function applyHeadMeta(lang) {
    var dict = (window.I18N_DATA || {})[lang] || {};
    var htmlLang = lang === 'zh' ? 'zh-CN' : 'en-US';
    document.documentElement.lang = htmlLang;

    var titleKey = document.documentElement.getAttribute('data-i18n-title');
    if (titleKey && dict[titleKey] !== undefined) {
      document.title = dict[titleKey];
    }

    var els = document.querySelectorAll('[data-i18n-meta], [data-i18n-og]');
    for (var i = 0; i < els.length; i++) {
      var key = els[i].getAttribute('data-i18n-meta') || els[i].getAttribute('data-i18n-og');
      if (key && dict[key] !== undefined) {
        els[i].setAttribute('content', dict[key]);
      }
    }

    var ogLocale = document.querySelector('meta[property="og:locale"]');
    if (ogLocale) {
      ogLocale.setAttribute('content', lang === 'zh' ? 'zh_CN' : 'en_US');
    }
  }

  window.__VIVARCUS_HEAD_LANG__ = detectLang();
  applyHeadMeta(window.__VIVARCUS_HEAD_LANG__);
})();
