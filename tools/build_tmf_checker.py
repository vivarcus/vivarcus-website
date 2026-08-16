#!/usr/bin/env python3
"""TMF 完整性自查器 static page builder (zh-only).

Zero-dependency (Python 3 stdlib only) build script:
  source data in  release-payloads/desired/clinical-operations/etmf/data/templates/*.zh.csv
  (same EDL data source as tmf-reference.html — 数据与分类页同源，禁止复制)
generates:
  website/tmf-checker.html   (static page, committed to git)

Run: cd website && python3 tools/build_tmf_checker.py

页面约定：zh-only 正文；EDL 数据以 JSON 嵌入页面；研究类型/阶段/检查范围/
部门筛选 + 逐项勾选（localStorage 持久化，按 类型:阶段:范围 分键）；生成
缺口报告后用 window.print() 打印（js/tools.js 的 Tools.printReport()）。
"""

import json
from pathlib import Path

import sitegen
from edl_data import (
    DEPT_LABEL, DEPT_LABEL_EN, LEVEL_LABEL, LEVEL_LABEL_EN, OTHER_DEPT,
    OTHER_DEPT_EN, PHASE_NOTES, PHASE_NOTES_EN, REQ_LABEL, REQ_LABEL_EN,
    read_edl,
)

ROOT = Path(__file__).resolve().parent.parent  # website/


PAGE_JS = """<script>
    var CHK_DATA = JSON.parse(document.getElementById('chk-data').textContent);

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function isEn() { return !!(window.I18N && I18N.getLang() === 'en'); }

    function currentControls() {
      var type = document.getElementById('chk-type').value;
      var phase = document.getElementById('chk-phase').value;
      var levels = [];
      document.querySelectorAll('input[name="chk-level"]:checked').forEach(function (c) { levels.push(c.value); });
      levels.sort();
      return {
        type: type, phase: phase, levels: levels,
        dept: document.getElementById('chk-dept').value,
        onlyReq: document.getElementById('chk-only-req').checked,
        onlyTodo: document.getElementById('chk-only-todo').checked,
      };
    }

    function storageKey(c) {
      return 'vivarcus-tmf-checker:v1:' + c.type + ':' + c.phase + ':' + c.levels.join('.');
    }

    function loadChecked(c) {
      try {
        var raw = localStorage.getItem(storageKey(c));
        if (raw) { var d = JSON.parse(raw); if (d && Array.isArray(d.checked)) return d.checked; }
      } catch (e) {}
      return [];
    }

    function saveChecked(c, checked) {
      try { localStorage.setItem(storageKey(c), JSON.stringify({ checked: checked, date: new Date().toISOString() })); } catch (e) {}
    }

    function renderPhaseOptions(type) {
      var sel = document.getElementById('chk-phase');
      var en = isEn();
      var opts = type === 'drug'
        ? [['phase_i', en ? 'Phase I' : 'I 期'], ['phase_ii', en ? 'Phase II' : 'II 期'],
           ['phase_iii', en ? 'Phase III' : 'III 期'], ['phase_iv', en ? 'Phase IV' : 'IV 期']]
        : [['none', '—']];
      sel.innerHTML = opts.map(function (o) {
        return '<option value="' + o[0] + '">' + o[1] + '</option>';
      }).join('');
      sel.disabled = type !== 'drug';
    }

    function renderDeptOptions() {
      var sel = document.getElementById('chk-dept');
      var en = isEn();
      var html = '<option value="all" selected>' + (en ? 'All Departments' : '全部部门') + '</option>';
      CHK_DATA.depts.forEach(function (d) {
        html += '<option value="' + d.key + '">' + esc(en ? d.label_en : d.label) + '</option>';
      });
      sel.innerHTML = html;
    }

    function phaseNote(c) {
      var notes = isEn() ? CHK_DATA.phase_notes_en : CHK_DATA.phase_notes;
      return notes[c.type + ':' + c.phase] || '';
    }

    function updateProgress() {
      var done = document.querySelectorAll('.chk-box:checked').length;
      var total = document.querySelectorAll('.chk-box').length;
      var reqDone = document.querySelectorAll('.chk-item.is-checked .chk-badge.chk-req').length;
      var reqTotal = document.querySelectorAll('.chk-badge.chk-req').length;
      document.getElementById('chk-progress').textContent = isEn()
        ? 'Checked ' + done + ' / ' + total + ' · Required done ' + reqDone + ' / ' + reqTotal
        : '已勾选 ' + done + ' / ' + total + ' · 必需已完成 ' + reqDone + ' / ' + reqTotal;
    }

    function inScope(item, c) {
      return c.levels.indexOf(item.level) !== -1;
    }

    function renderList() {
      var c = currentControls();
      var en = isEn();
      document.getElementById('chk-phase-note').textContent = phaseNote(c);
      var checked = loadChecked(c);
      var checkedSet = {};
      checked.forEach(function (id) { checkedSet[id] = true; });
      var list = document.getElementById('chk-list');
      var html = '';
      var total = 0, done = 0, reqTotal = 0, reqDone = 0;
      CHK_DATA.depts.forEach(function (d) {
        if (c.dept !== 'all' && d.key !== c.dept) return;
        var rows = '', nRows = 0;
        CHK_DATA.items.forEach(function (item) {
          if (item.dept !== d.key || !inScope(item, c)) return;
          var isReq = item.requiredness === 'required__v';
          if (c.onlyReq && !isReq) return;
          if (c.onlyTodo && checkedSet[item.id]) return;
          total++; if (checkedSet[item.id]) done++;
          if (isReq) { reqTotal++; if (checkedSet[item.id]) reqDone++; }
          var reqCls = item.requiredness === 'required__v' ? 'chk-req' : (item.requiredness === 'pending_decision__v' ? 'chk-pending' : '');
          var name = en ? item.name_en : item.name;
          var ms = en ? (item.milestone_en || item.milestone) : item.milestone;
          var badges = '<span class="chk-badge ' + reqCls + '">' + esc((en ? CHK_DATA.req_en : CHK_DATA.req)[item.requiredness] || '—') + '</span>' +
                       '<span class="chk-badge chk-level">' + esc((en ? CHK_DATA.level_en : CHK_DATA.level)[item.level] || '—') + '</span>' +
                       (item.count && item.count !== '0' ? '<span class="chk-count">×' + esc(item.count) + '</span>' : '') +
                       (ms ? '<span class="chk-ms">' + esc(ms) + '</span>' : '');
          rows += '<label class="chk-item' + (checkedSet[item.id] ? ' is-checked' : '') + '">' +
                  '<input type="checkbox" class="chk-box" value="' + esc(item.id) + '"' +
                  (checkedSet[item.id] ? ' checked' : '') + ' />' +
                  '<span class="chk-name">' + esc(name) + '</span>' + badges + '</label>';
          nRows++;
        });
        if (!rows) return;
        html += '<details class="chk-dept"' + (c.dept !== 'all' ? ' open' : '') + '><summary>' +
                esc(en ? d.label_en : d.label) + ' <span class="chk-dept-count">' + nRows + (en ? ' items' : ' 条') + '</span></summary>' +
                '<div class="chk-dept-body">' + rows + '</div></details>';
      });
      list.innerHTML = html || ('<p class="chk-empty">' + (en
        ? 'No items under the current filters. Please select at least one scope.'
        : '当前筛选条件下没有条目。请勾选至少一个检查范围。') + '</p>');
      updateProgress();
    }

    function renderReport() {
      var c = currentControls();
      var en = isEn();
      var checked = loadChecked(c);
      var checkedSet = {};
      checked.forEach(function (id) { checkedSet[id] = true; });
      var total = 0, done = 0, reqTotal = 0, reqDone = 0;
      var missing = {};  // dept -> [items]
      CHK_DATA.items.forEach(function (item) {
        if (!inScope(item, c)) return;
        if (c.dept !== 'all' && item.dept !== c.dept) return;
        total++; if (checkedSet[item.id]) done++;
        if (item.requiredness === 'required__v') {
          reqTotal++;
          if (checkedSet[item.id]) reqDone++;
          else (missing[item.dept] = missing[item.dept] || []).push(item);
        }
      });
      var now = new Date();
      var dateStr = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
      var typeLabel = en
        ? { drug: 'Drug Trial', device: 'Device Trial', be: 'BE Study' }[c.type] || c.type
        : { drug: '药物临床试验', device: '医疗器械试验', be: 'BE 试验' }[c.type] || c.type;
      var phaseLabel = c.phase === 'none' ? '—'
        : (en
          ? { phase_i: 'Phase I', phase_ii: 'Phase II', phase_iii: 'Phase III', phase_iv: 'Phase IV' }[c.phase]
          : { phase_i: 'I 期', phase_ii: 'II 期', phase_iii: 'III 期', phase_iv: 'IV 期' }[c.phase]);
      var levelDict = en ? CHK_DATA.level_en : CHK_DATA.level;
      var levelLabel = c.levels.map(function (l) { return levelDict[l] || l; }).join(en ? ', ' : '、');
      var deptLabel = c.dept === 'all' ? (en ? 'All' : '全部') : (en ? CHK_DATA.dept_en : CHK_DATA.dept)[c.dept];
      var rate = total ? Math.round(done / total * 100) : 0;
      var html = '<div class="chk-report-head">' +
        '<h2>' + (en ? 'TMF Completeness Self-Check Report' : 'TMF 完整性自查报告') + '</h2>' +
        '<p class="chk-report-meta">' + (en ? 'Study name: ____________  Generated: ' : '研究名称：______________　生成日期：') + dateStr + '</p>' +
        '<p class="chk-report-meta">' + (en
          ? 'Study type: ' + typeLabel + '　Phase: ' + phaseLabel + '　Scope: ' + levelLabel + '　Department: ' + deptLabel
          : '研究类型：' + typeLabel + '　阶段：' + phaseLabel + '　检查范围：' + levelLabel + '　部门：' + deptLabel) + '</p>' +
        '</div>' +
        '<div class="chk-report-stats">' +
        '<div class="chk-stat"><strong>' + total + '</strong><span>' + (en ? 'Total items' : '总条目') + '</span></div>' +
        '<div class="chk-stat"><strong>' + reqTotal + '</strong><span>' + (en ? 'Required items' : '必需条目') + '</span></div>' +
        '<div class="chk-stat"><strong>' + done + '</strong><span>' + (en ? 'Completed' : '已完成') + '</span></div>' +
        '<div class="chk-stat chk-stat-warn"><strong>' + (reqTotal - reqDone) + '</strong><span>' + (en ? 'Required not done' : '未完成必需') + '</span></div>' +
        '<div class="chk-stat"><strong>' + rate + '%</strong><span>' + (en ? 'Completion rate' : '完成率') + '</span></div>' +
        '</div>';
      html += '<h3>' + (en ? 'Required Items Not Done (by Department)' : '未完成必需项（按部门）') + '</h3>';
      var anyMissing = false;
      Object.keys(missing).sort().forEach(function (dk) {
        if (!missing[dk].length) return;
        anyMissing = true;
        html += '<h4>' + esc((en ? CHK_DATA.dept_en : CHK_DATA.dept)[dk] || dk) + '</h4><ul>';
        missing[dk].forEach(function (item) {
          html += '<li>' + esc(en ? item.name_en : item.name) + (item.milestone ? '<span class="chk-report-ms">' + esc(en ? (item.milestone_en || item.milestone) : item.milestone) + '</span>' : '') + '</li>';
        });
        html += '</ul>';
      });
      if (!anyMissing) html += '<p>' + (en
        ? 'Required items not done: none. All required items in the current scope (' + levelLabel + ') are complete.'
        : '未完成必需项：无。当前范围（' + levelLabel + '）下所有必需条目均已完成。') + '</p>';
      html += '<p class="chk-report-note">' + (en
        ? 'This report is generated from the same data source as the <a href="tmf-reference.html">TMF Reference</a> (TMF Reference Model v3.0 / Vivarcus standard EDL), for self-check reference only and does not constitute a compliance conclusion. Study-type/phase differences follow the sponsor EDL and protocol; "Pending decision" items are not treated as required. Data source: Vivarcus eTMF built-in standard EDL template.'
        : '本报告基于 <a href="tmf-reference.html">TMF 分类参考</a>同源数据（TMF 参考模型 v3.0 / Vivarcus 标准 EDL）生成，为自查参考，不构成合规结论。各研究类型/阶段的差异以申办方 EDL 与方案为准；「待定」条目未按必需对待。数据来源：Vivarcus eTMF 预置标准 EDL 模板。') + '</p>'
            + '<div class="chk-report-actions no-print"><button type="button" class="btn btn-primary" id="chk-print-btn">' + (en ? 'Print / Export PDF' : '打印 / 导出 PDF') + '</button></div>';
      var report = document.getElementById('gap-report');
      report.innerHTML = html;
      report.hidden = false;
      report.scrollIntoView({ behavior: 'smooth' });
    }

    document.addEventListener('DOMContentLoaded', function () {
      renderPhaseOptions('drug');
      renderDeptOptions();
      renderList();
    });

    window.addEventListener('langchange', function () {
      renderPhaseOptions(document.getElementById('chk-type').value);
      renderDeptOptions();
      renderList();
      var report = document.getElementById('gap-report');
      if (report && !report.hidden) renderReport();
    });

    // 控件变化 → 重新渲染（事件委托）
    document.addEventListener('change', function (e) {
      if (!e.target) return;
      if (e.target.id === 'chk-type') { renderPhaseOptions(e.target.value); renderList(); return; }
      if (e.target.id === 'chk-phase' || e.target.id === 'chk-dept' ||
          e.target.id === 'chk-only-req' || e.target.id === 'chk-only-todo') { renderList(); return; }
      if (e.target.name === 'chk-level') { renderList(); return; }
      if (e.target.classList && e.target.classList.contains('chk-box')) {
        var c = currentControls();
        var checked = loadChecked(c);
        var idx = checked.indexOf(e.target.value);
        if (e.target.checked && idx === -1) checked.push(e.target.value);
        if (!e.target.checked && idx !== -1) checked.splice(idx, 1);
        saveChecked(c, checked);
        var row = e.target.closest('.chk-item');
        if (row) row.classList.toggle('is-checked', e.target.checked);
        // 更新进度，不整表重渲染以免打断浏览位置
        updateProgress();
        if (document.getElementById('chk-only-todo').checked) renderList();
      }
    });

    document.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'chk-report-btn') renderReport();
      if (e.target && e.target.id === 'chk-print-btn') Tools.printReport();
    });
  </script>"""

EXTRA_STYLE = """
    .chk-controls { display: flex; flex-wrap: wrap; gap: 1rem 1.4rem; margin-bottom: 0.9rem; }
    .chk-field { display: flex; flex-direction: column; gap: 0.35rem; }
    .chk-field > label, .chk-field > .chk-field-label { font-size: 0.82rem; opacity: 0.65; font-weight: 600; }
    .chk-field select, .chk-field input[type="date"] {
      padding: 0.5rem 0.8rem; font-size: 0.92rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 8px; outline: none;
      background: var(--bg, #fff); color: inherit; min-width: 10rem;
    }
    .chk-field select:focus { border-color: var(--accent, #2563eb); }
    .chk-levels { display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; padding: 0.45rem 0; }
    .chk-levels label { display: inline-flex; align-items: center; gap: 0.3rem; cursor: pointer; }
    .chk-phase-note { width: 100%; font-size: 0.86rem; opacity: 0.8; line-height: 1.7; margin: 0; }
    .chk-toolbar {
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.9rem 1.2rem;
      margin: 1rem 0 1.4rem; padding: 0.8rem 1rem; border: 1px solid var(--border, #d8dde4);
      border-radius: 10px; background: var(--bg-soft, #f6f8fa); font-size: 0.9rem;
    }
    .chk-toolbar label { display: inline-flex; align-items: center; gap: 0.3rem; cursor: pointer; }
    .chk-progress { margin-left: auto; opacity: 0.85; white-space: nowrap; }
    .chk-dept { margin-bottom: 0.9rem; border: 1px solid var(--border, #d8dde4); border-radius: 10px; overflow: hidden; }
    .chk-dept > summary { padding: 0.85rem 1.1rem; font-weight: 600; cursor: pointer; }
    .chk-dept-count { font-weight: 400; font-size: 0.8rem; opacity: 0.65; margin-left: 0.4rem; }
    .chk-dept-body { padding: 0 1.1rem 0.6rem; }
    .chk-item {
      display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.35rem 0.7rem;
      padding: 0.5rem 0.3rem; border-bottom: 1px dashed var(--border, #d8dde4); cursor: pointer;
    }
    .chk-item:last-child { border-bottom: none; }
    .chk-item.is-checked .chk-name { opacity: 0.55; text-decoration: line-through; }
    .chk-box { margin: 0 0.2rem; flex: none; }
    .chk-name { flex: 1 1 16rem; line-height: 1.5; }
    .chk-badge {
      font-size: 0.7rem; line-height: 1.4; padding: 0 0.4rem; border-radius: 4px;
      border: 1px solid var(--border, #d8dde4); opacity: 0.8; white-space: nowrap;
    }
    .chk-badge.chk-req { color: #1d4ed8; border-color: rgba(37, 99, 235, 0.4); }
    .chk-badge.chk-pending { color: #b45309; border-color: rgba(217, 119, 6, 0.4); }
    .chk-badge.chk-level { opacity: 0.6; }
    .chk-count { font-size: 0.78rem; opacity: 0.65; font-family: ui-monospace, monospace; }
    .chk-ms { font-size: 0.78rem; opacity: 0.65; }
    .chk-empty { padding: 1.5rem 0; opacity: 0.7; }
    .chk-report { margin-top: 2.6rem; border-top: 2px solid var(--accent, #2563eb); padding-top: 1.4rem; }
    .chk-report h2 { margin: 0 0 0.6rem; }
    .chk-report-meta { font-size: 0.88rem; opacity: 0.85; margin: 0.2rem 0; }
    .chk-report-stats { display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 1.2rem 0 1.6rem; }
    .chk-stat {
      flex: 1 1 7rem; text-align: center; padding: 0.8rem 0.6rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 10px; background: var(--bg-soft, #f6f8fa);
    }
    .chk-stat strong { display: block; font-size: 1.4rem; }
    .chk-stat span { font-size: 0.78rem; opacity: 0.7; }
    .chk-stat-warn strong { color: #b91c1c; }
    .chk-report h3 { margin: 1.4rem 0 0.5rem; }
    .chk-report h4 { margin: 0.9rem 0 0.3rem; font-size: 0.95rem; }
    .chk-report ul { margin: 0.2rem 0 0.8rem; padding-left: 1.3rem; }
    .chk-report li { line-height: 1.7; }
    .chk-report-ms { font-size: 0.78rem; opacity: 0.6; margin-left: 0.6rem; }
    .chk-report-note { font-size: 0.82rem; opacity: 0.7; line-height: 1.7; margin-top: 1.4rem; }
    .chk-report-actions { display: flex; gap: 0.8rem; margin: 1rem 0 0; }
    .print-only { display: none; }
    @media print {
      .print-only { display: block; }
      body.tools-print-mode .site-header, body.tools-print-mode .page-hero,
      body.tools-print-mode .cta-section, body.tools-print-mode .site-footer,
      body.tools-print-mode .no-print { display: none !important; }
      body.tools-print-mode .chk-dept { border: none; }
      body.tools-print-mode .chk-report { border-top: none; }
    }
  """


def build_page():
    items = read_edl()
    n_req = sum(1 for it in items if it["requiredness"] == "required__v")
    n_items = len(items)

    dept_labels = dict(DEPT_LABEL)
    dept_labels[OTHER_DEPT] = "其他"
    dept_labels_en = dict(DEPT_LABEL_EN)
    dept_labels_en[OTHER_DEPT] = OTHER_DEPT_EN
    dept_counts = {d: 0 for d in dept_labels}
    for it in items:
        dept_counts[it["dept"]] = dept_counts.get(it["dept"], 0) + 1
    depts = [{"key": d, "label": dept_labels[d], "label_en": dept_labels_en[d], "count": dept_counts[d]}
             for d in dept_labels if dept_counts[d]]

    data = {
        "items": items,
        "depts": depts,
        "dept": dept_labels,
        "dept_en": dept_labels_en,
        "req": REQ_LABEL,
        "req_en": REQ_LABEL_EN,
        "level": LEVEL_LABEL,
        "level_en": LEVEL_LABEL_EN,
        "phase_notes": PHASE_NOTES,
        "phase_notes_en": PHASE_NOTES_EN,
    }

    body = f"""
        <aside class="content-note">
          <p data-i18n-html="chk.note.source"><strong>数据来源：</strong>本清单与 <a href="tmf-reference.html">TMF 分类参考</a>同源（TMF 参考模型 v3.0 / Vivarcus 标准 EDL 模板，{n_items} 条，其中必需 {n_req} 条）。</p>
          <p data-i18n-html="chk.note.disclaimer"><strong>免责声明：</strong>各研究类型/阶段的差异为编者整理参考，不改变清单条目；正式项目请以申办方 EDL 与方案为准。本工具为自查参考，不构成合规结论。</p>
        </aside>

        <div class="chk-controls no-print" id="chk-controls">
          <div class="chk-field">
            <label for="chk-type" data-i18n="chk.field.type">研究类型</label>
            <select id="chk-type">
              <option value="drug" selected data-i18n="chk.opt.drug">药物临床试验</option>
              <option value="device" data-i18n="chk.opt.device">医疗器械试验</option>
              <option value="be" data-i18n="chk.opt.be">BE 试验</option>
            </select>
          </div>
          <div class="chk-field">
            <label for="chk-phase" data-i18n="chk.field.phase">阶段</label>
            <select id="chk-phase"></select>
          </div>
          <div class="chk-field">
            <span class="chk-field-label" data-i18n="chk.field.scope">检查范围</span>
            <div class="chk-levels">
              <label><input type="checkbox" name="chk-level" value="study_level__v" checked /> <span data-i18n="chk.level.study">研究</span></label>
              <label><input type="checkbox" name="chk-level" value="country_level__v" checked /> <span data-i18n="chk.level.country">国家/地区</span></label>
              <label><input type="checkbox" name="chk-level" value="site_level__v" checked /> <span data-i18n="chk.level.site">中心</span></label>
            </div>
          </div>
          <div class="chk-field">
            <label for="chk-dept" data-i18n="chk.field.dept">部门</label>
            <select id="chk-dept">
              <option value="all" selected>全部部门</option>
              {{dept_options}}
            </select>
          </div>
          <p class="chk-phase-note" id="chk-phase-note"></p>
        </div>

        <div class="chk-toolbar no-print">
          <label><input type="checkbox" id="chk-only-req" /> <span data-i18n="chk.filter.req">只看必需</span></label>
          <label><input type="checkbox" id="chk-only-todo" /> <span data-i18n="chk.filter.todo">只看未完成</span></label>
          <span class="chk-progress" id="chk-progress"></span>
          <button type="button" class="btn btn-primary" id="chk-report-btn" data-i18n="chk.btn.report">生成缺口报告</button>
        </div>

        <div id="chk-list" class="no-print"></div>

        <div id="gap-report" class="chk-report" hidden></div>
        <p class="print-only" data-i18n="chk.print.note">本页由 Vivarcus TMF 完整性自查器生成，仅作自查参考。</p>

        <p class="ctcae-related" style="margin-top:2.4rem;font-size:0.9rem;">
          <span data-i18n="chk.related">相关资源：</span><a href="tmf-reference.html" data-i18n="chk.related.tmfref">TMF 分类参考</a> ·
          <a href="template-tmf-index.html" data-i18n="chk.related.tmfindex">TMF 文件清单模板</a> ·
          <a href="template-audit-readiness-checklist.html" data-i18n="chk.related.audit">稽查准备清单</a> ·
          <a href="glossary.html" data-i18n="chk.related.glossary">术语词典</a>
        </p>
        <script type="application/json" id="chk-data">{{chk_data_json}}</script>
"""
    dept_options = "\n".join(
        f'              <option value="{d["key"]}">{d["label"]}</option>' for d in depts)
    body = body.replace("{dept_options}", dept_options)
    body = body.replace("{chk_data_json}", json.dumps(data, ensure_ascii=False))

    meta = {
        "title": "TMF 完整性自查器：按研究类型生成必备文件清单 | Vivarcus",
        "desc": (f"TMF 完整性自查：选择研究类型与阶段，生成预期文档清单（与 TMF 分类参考同源，{n_items} 条 EDL，"
                 f"其中必需 {n_req} 条），逐项勾选自查、进度实时可见，导出可打印的缺口报告。"),
        "file": "tmf-checker.html",
        "eyebrow": "行业资源 · TMF 自查",
        "hero": "TMF 完整性自查器",
        "subtitle": f"与 TMF 分类参考同源：{n_items} 条预期文档（EDL）按部门逐项勾选，一键生成可打印的缺口报告。",
    }
    html = sitegen.render_page(
        meta, body,
        cta_title="这份清单，Vivarcus eTMF 里已经内置",
        cta_desc="EDL 自动生成、文件自动归位、完整性指标实时可见——自查器的数据在系统里直接可用。",
        cta_secondary_href="tmf-reference.html",
        cta_secondary_label="TMF 分类参考",
        extra_style=EXTRA_STYLE,
        i18n="chk",
    )
    html = html.replace("</body>",
                        '  <script src="js/tools.js"></script>\n' + PAGE_JS + "</body>")
    out = ROOT / "tmf-checker.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({n_items} EDL items, {n_req} required)")


if __name__ == "__main__":
    build_page()
