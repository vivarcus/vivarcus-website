/* ============================================================
   Vivarcus Help Center — sidebar, scrollspy, client-side search
   ============================================================ */

(function () {
  'use strict';

  var lang = (document.documentElement.lang || 'zh-CN').indexOf('zh') === 0 ? 'zh' : 'en';

  /* ---------- derive lang + help base dir from location ---------- */
  var m = location.pathname.match(/^\/help\/(zh|en)\//);
  if (m) lang = m[1];
  var BASE = '/help/';

  /* ---------- mobile sidebar toggle ---------- */
  var toggle = document.querySelector('.help-sidebar-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('sidebar-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---------- scrollspy for the right mini-TOC ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.help-toc__nav a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var activeId = null;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          activeId = entry.target.id;
        }
      });
      tocLinks.forEach(function (link) {
        var isActive = link.getAttribute('href') === '#' + activeId;
        link.classList.toggle('active', isActive);
      });
    }, { rootMargin: '-64px 0px -70% 0px', threshold: 0 });
    tocLinks.forEach(function (link) {
      var id = link.getAttribute('href').slice(1);
      var target = document.getElementById(id);
      if (target) observer.observe(target);
    });
  }

  /* ---------- client-side search ---------- */
  var inputs = document.querySelectorAll('.help-search');
  if (!inputs.length) return;

  var index = null;

  function loadIndex(cb) {
    if (index) { cb(index); return; }
    fetch(BASE + 'search-index.' + lang + '.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; cb(data); })
      .catch(function () { /* search unavailable — stay silent */ });
  }

  function norm(s) { return (s || '').toLowerCase(); }

  function matchScore(article, q) {
    var score = 0;
    if (norm(article.title).indexOf(q) !== -1) score += 10;
    if (norm(article.description).indexOf(q) !== -1) score += 4;
    (article.headings || []).forEach(function (h) {
      if (norm(h).indexOf(q) !== -1) score += 3;
    });
    return score;
  }

  function articleUrl(a) {
    return BASE + lang + '/' + a.app + '/' + a.slug + '.html';
  }

  inputs.forEach(function (input) {
    var wrap = input.parentElement;
    var resultsBox = wrap.querySelector('.help-search-results');

    function render(results, q) {
      if (!results.length) {
        var noResults = lang === 'zh' ? '未找到相关文章，换个关键词试试。' : 'No articles found. Try different keywords.';
        resultsBox.innerHTML = '<p class="help-search-empty">' + noResults + '</p>';
        resultsBox.hidden = false;
        return;
      }
      resultsBox.innerHTML = results.map(function (a) {
        return '<a class="help-search-result" href="' + articleUrl(a) + '">' +
          '<span class="help-search-result__title">' + esc(a.title) + '</span>' +
          '<span class="help-search-result__meta">' +
          '<span class="help-search-result__app">' + esc(a.app_label) + '</span>' +
          esc(a.description || '') + '</span></a>';
      }).join('');
      resultsBox.hidden = false;
    }

    function esc(s) {
      return String(s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    function onInput() {
      var q = norm(input.value.trim());
      if (q.length < 2) { resultsBox.hidden = true; resultsBox.innerHTML = ''; return; }
      loadIndex(function (data) {
        var scored = [];
        data.forEach(function (a) {
          var s = matchScore(a, q);
          if (s > 0) scored.push([s, a]);
        });
        scored.sort(function (x, y) { return y[0] - x[0]; });
        render(scored.slice(0, 10).map(function (p) { return p[1]; }), q);
      });
    }

    input.addEventListener('input', onInput);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { resultsBox.hidden = true; input.blur(); }
    });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) resultsBox.hidden = true;
    });
  });
})();
