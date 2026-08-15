/* ============================================================
   Vivarcus Website — analytics (Baidu Tongji) + event tracking.

   Site: vivarcus.com (百度统计站点 ID 23445211，免费版)
   管理入口: tongji.baidu.com → 使用设置 → 代码管理 → 代码获取
   事件说明: 工具下载(tool/download)、试用点击(conversion/trial-click)、
            按钮点击(tool/button-click) — 报表在「事件分析」中查看。
   ============================================================ */

(function () {
  'use strict';

  var BAIDU_TONGJI_ID = 'e97e9ad8fc1bb660c9ebc1edb38d270e';
  if (!BAIDU_TONGJI_ID) return;

  window._hmt = window._hmt || [];
  var hm = document.createElement('script');
  hm.async = true;
  hm.src = 'https://hm.baidu.com/hm.js?' + BAIDU_TONGJI_ID;
  document.head.appendChild(hm);

  function track(category, action, label) {
    try { window._hmt.push(['_trackEvent', category, action, label || '']); }
    catch (e) { /* analytics must never break the page */ }
  }

  document.addEventListener('click', function (e) {
    var el = e.target;
    if (!el || !el.closest) return;
    var a = el.closest('a');
    if (a) {
      var href = a.getAttribute('href') || '';
      if (a.hasAttribute('download')) {
        track('tool', 'download', href);
        return;
      }
      var page = href.split('#')[0].split('?')[0].replace(/^\.?\//, '');
      if (page === 'trial.html') track('conversion', 'trial-click', location.pathname);
      return;
    }
    var btn = el.closest('button');
    if (btn && btn.id && btn.id.indexOf('csv') === -1) {
      track('tool', 'button-click', btn.id);
    }
  });
})();
