#!/usr/bin/env python3
"""EDL 生成器 static page builder (zh-only).

Zero-dependency (Python 3 stdlib only) build script:
  source data:  release-payloads/desired/clinical-operations/etmf/data/templates/*.zh.csv
                via shared edl_data.py（与 tmf-checker / tmf-reference 同源，禁止复制）
generates:
  website/edl-generator.html   (static page, committed to git)

Run: cd website && python3 tools/build_edl_generator.py

页面约定：zh-only 正文；EDL 数据以 JSON 嵌入页面；研究类型/阶段/检查范围/
部门筛选 + 只读预览；导出 CSV（UTF-8 BOM，Excel/WPS 直接打开，无门控）。
不做条目按研究类型过滤——数据源无类型字段，阶段仅编者提示（与 tmf-checker 同原则）。
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
    var EDL_DATA = JSON.parse(document.getElementById('edl-data').textContent);

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function isEn() { return !!(window.I18N && I18N.getLang() === 'en'); }

    function currentControls() {
      var type = document.getElementById('edl-type').value;
      var phase = document.getElementById('edl-phase').value;
      var levels = [];
      document.querySelectorAll('input[name="edl-level"]:checked').forEach(function (c) { levels.push(c.value); });
      levels.sort();
      return {
        type: type, phase: phase, levels: levels,
        dept: document.getElementById('edl-dept').value,
      };
    }

    function renderPhaseOptions(type) {
      var sel = document.getElementById('edl-phase');
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
      var sel = document.getElementById('edl-dept');
      var en = isEn();
      var html = '<option value="all" selected>' + (en ? 'All Departments' : '全部部门') + '</option>';
      EDL_DATA.depts.forEach(function (d) {
        html += '<option value="' + d.key + '">' + esc(en ? d.label_en : d.label) + '</option>';
      });
      sel.innerHTML = html;
    }

    function phaseNote(c) {
      var notes = isEn() ? EDL_DATA.phase_notes_en : EDL_DATA.phase_notes;
      return notes[c.type + ':' + c.phase] || '';
    }

    function inScope(item, c) {
      return c.levels.indexOf(item.level) !== -1;
    }

    // 过滤后的行（部门顺序），同时供预览与 CSV 导出使用
    function filteredRows(c) {
      var rows = [];
      EDL_DATA.depts.forEach(function (d) {
        if (c.dept !== 'all' && d.key !== c.dept) return;
        EDL_DATA.items.forEach(function (item) {
          if (item.dept !== d.key || !inScope(item, c)) return;
          rows.push({ item: item, dept: d });
        });
      });
      return rows;
    }

    function renderPreview() {
      var c = currentControls();
      var en = isEn();
      document.getElementById('edl-phase-note').textContent = phaseNote(c);
      var rows = filteredRows(c);
      var nReq = rows.filter(function (r) { return r.item.requiredness === 'required__v'; }).length;
      var deptN = {};
      rows.forEach(function (r) { deptN[r.dept.key] = (deptN[r.dept.key] || 0) + 1; });
      var html = '', idx = 0, curDept = null;
      var head = en
        ? '<th>#</th><th>Item Name</th><th>Requirement</th><th>Level</th><th>Count</th><th>Milestone</th>'
        : '<th>#</th><th>条目名称</th><th>要求</th><th>层级</th><th>数量</th><th>里程碑</th>';
      rows.forEach(function (r) {
        if (curDept !== r.dept.key) {
          if (curDept !== null) html += '</tbody></table>';
          curDept = r.dept.key;
          html += '<h3 class="edl-dept-head">' + esc(en ? r.dept.label_en : r.dept.label) +
                  ' <span class="edl-dept-count">' + deptN[r.dept.key] + (en ? ' items' : ' 条') + '</span></h3>';
          html += '<div class="edl-scroll"><table class="edl-table"><thead><tr>' + head +
            '</tr></thead><tbody>';
        }
        idx++;
        var item = r.item;
        var reqCls = item.requiredness === 'required__v' ? 'edl-req' : (item.requiredness === 'pending_decision__v' ? 'edl-pending' : '');
        html += '<tr>' +
          '<td class="edl-idx">' + idx + '</td>' +
          '<td class="edl-name">' + esc(en ? item.name_en : item.name) + '</td>' +
          '<td><span class="edl-badge ' + reqCls + '">' + esc((en ? EDL_DATA.req_en : EDL_DATA.req)[item.requiredness] || '—') + '</span></td>' +
          '<td class="edl-level">' + esc((en ? EDL_DATA.level_en : EDL_DATA.level)[item.level] || '—') + '</td>' +
          '<td class="edl-count">' + (item.count && item.count !== '0' ? esc(item.count) : '') + '</td>' +
          '<td class="edl-ms">' + esc(en ? (item.milestone_en || item.milestone) : item.milestone) + '</td>' +
          '</tr>';
      });
      html += '</tbody></table></div>';
      var list = document.getElementById('edl-preview');
      list.innerHTML = html || ('<p class="edl-empty">' + (en
        ? 'No items under the current filters. Please select at least one scope.'
        : '当前筛选条件下没有条目。请勾选至少一个检查范围。') + '</p>');
      document.getElementById('edl-stats').textContent = en
        ? 'Total ' + rows.length + ' items · Required ' + nReq
        : '共 ' + rows.length + ' 条 · 其中必需 ' + nReq + ' 条';
    }

    function csvCell(s) {
      s = String(s == null ? '' : s);
      if (/[",\\n\\r]/.test(s)) s = '"' + s.replace(/"/g, '""') + '"';
      return s;
    }

    function downloadCsv() {
      var c = currentControls();
      var en = isEn();
      var rows = filteredRows(c);
      if (!rows.length) { renderPreview(); return; }
      var header = en
        ? '\\uFEFFNo.,Department,Item Name,Requirement,Level,Expected Count,Milestone'
        : '\\uFEFF序号,部门,条目名称,要求,层级,预期数量,里程碑';
      var lines = [header];
      rows.forEach(function (r, i) {
        lines.push([
          i + 1,
          en ? r.dept.label_en : r.dept.label,
          en ? r.item.name_en : r.item.name,
          (en ? EDL_DATA.req_en : EDL_DATA.req)[r.item.requiredness] || '',
          (en ? EDL_DATA.level_en : EDL_DATA.level)[r.item.level] || '',
          r.item.count || '',
          en ? (r.item.milestone_en || r.item.milestone) : r.item.milestone || '',
        ].map(csvCell).join(','));
      });
      var typeLabel = { drug: 'drug', device: 'device', be: 'be' }[c.type];
      var phaseTag = c.type === 'drug' ? '-' + c.phase.replace('phase_', '') : '';
      var now = new Date();
      var dateStr = now.getFullYear() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
      var fname = 'vivarcus-tmf-index-' + typeLabel + phaseTag + '-' + dateStr + '.csv';
      var blob = new Blob([lines.join('\\r\\n')], { type: 'text/csv;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = fname;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    }

    document.addEventListener('DOMContentLoaded', function () {
      renderPhaseOptions('drug');
      renderDeptOptions();
      renderPreview();
    });

    window.addEventListener('langchange', function () {
      renderPhaseOptions(document.getElementById('edl-type').value);
      renderDeptOptions();
      renderPreview();
    });

    document.addEventListener('change', function (e) {
      if (!e.target) return;
      if (e.target.id === 'edl-type') { renderPhaseOptions(e.target.value); renderPreview(); return; }
      if (e.target.id === 'edl-phase' || e.target.id === 'edl-dept' || e.target.name === 'edl-level') { renderPreview(); return; }
    });

    document.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'edl-csv-btn') downloadCsv();
      if (e.target && e.target.id === 'edl-print-btn') Tools.printReport();
    });
  </script>"""

EXTRA_STYLE = """
    .edl-controls { display: flex; flex-wrap: wrap; gap: 1rem 1.4rem; margin-bottom: 0.9rem; }
    .edl-field { display: flex; flex-direction: column; gap: 0.35rem; }
    .edl-field > label, .edl-field > .edl-field-label { font-size: 0.82rem; opacity: 0.65; font-weight: 600; }
    .edl-field select {
      padding: 0.5rem 0.8rem; font-size: 0.92rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 8px; outline: none;
      background: var(--bg, #fff); color: inherit; min-width: 10rem;
    }
    .edl-field select:focus { border-color: var(--accent, #2563eb); }
    .edl-levels { display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; padding: 0.45rem 0; }
    .edl-levels label { display: inline-flex; align-items: center; gap: 0.3rem; cursor: pointer; }
    .edl-phase-note { width: 100%; font-size: 0.86rem; opacity: 0.8; line-height: 1.7; margin: 0; }
    .edl-toolbar {
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.9rem 1.2rem;
      margin: 1rem 0 1.4rem; padding: 0.8rem 1rem; border: 1px solid var(--border, #d8dde4);
      border-radius: 10px; background: var(--bg-soft, #f6f8fa); font-size: 0.9rem;
    }
    .edl-stats { margin-left: auto; opacity: 0.85; white-space: nowrap; }
    .edl-dept-head { margin: 1.6rem 0 0.5rem; font-size: 1.02rem; }
    .edl-dept-count { font-weight: 400; font-size: 0.78rem; opacity: 0.6; margin-left: 0.4rem; }
    .edl-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .edl-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 0 0 0.6rem; }
    .edl-table th, .edl-table td { text-align: left; padding: 0.5rem 0.7rem; border-top: 1px solid var(--border, #d8dde4); vertical-align: top; }
    .edl-table th { font-size: 0.78rem; opacity: 0.6; font-weight: 600; white-space: nowrap; }
    .edl-idx { opacity: 0.55; font-family: ui-monospace, monospace; white-space: nowrap; }
    .edl-name { line-height: 1.55; }
    .edl-badge {
      font-size: 0.7rem; line-height: 1.4; padding: 0 0.4rem; border-radius: 4px;
      border: 1px solid var(--border, #d8dde4); opacity: 0.8; white-space: nowrap;
    }
    .edl-badge.edl-req { color: #1d4ed8; border-color: rgba(37, 99, 235, 0.4); }
    .edl-badge.edl-pending { color: #b45309; border-color: rgba(217, 119, 6, 0.4); }
    .edl-level, .edl-count, .edl-ms { opacity: 0.75; white-space: nowrap; }
    .edl-count { font-family: ui-monospace, monospace; }
    .edl-empty { padding: 1.5rem 0; opacity: 0.7; }
    .edl-preview { margin-top: 1rem; }
    @media print {
      body.tools-print-mode .site-header, body.tools-print-mode .page-hero,
      body.tools-print-mode .cta-section, body.tools-print-mode .site-footer,
      body.tools-print-mode .no-print { display: none !important; }
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
        "req": REQ_LABEL,
        "req_en": REQ_LABEL_EN,
        "level": LEVEL_LABEL,
        "level_en": LEVEL_LABEL_EN,
        "phase_notes": PHASE_NOTES,
        "phase_notes_en": PHASE_NOTES_EN,
    }

    body = f"""
        <aside class="content-note">
          <p data-i18n-html="edl.note.source"><strong>数据来源：</strong>本清单与 <a href="tmf-reference.html">TMF 分类参考</a>、<a href="tmf-checker.html">TMF 完整性自查器</a>同源（TMF 参考模型 v3.0 / Vivarcus 标准 EDL 模板，{n_items} 条，其中必需 {n_req} 条）。</p>
          <p data-i18n-html="edl.note.disclaimer"><strong>免责声明：</strong>研究类型与阶段为编者整理参考，不改变清单条目；正式项目请以申办方 EDL 与方案为准。本工具为参考，不构成合规结论。</p>
        </aside>

        <div class="edl-controls no-print" id="edl-controls">
          <div class="edl-field">
            <label for="edl-type" data-i18n="edl.field.type">研究类型</label>
            <select id="edl-type">
              <option value="drug" selected data-i18n="edl.opt.drug">药物临床试验</option>
              <option value="device" data-i18n="edl.opt.device">医疗器械试验</option>
              <option value="be" data-i18n="edl.opt.be">BE 试验</option>
            </select>
          </div>
          <div class="edl-field">
            <label for="edl-phase" data-i18n="edl.field.phase">阶段</label>
            <select id="edl-phase"></select>
          </div>
          <div class="edl-field">
            <span class="edl-field-label" data-i18n="edl.field.scope">检查范围</span>
            <div class="edl-levels">
              <label><input type="checkbox" name="edl-level" value="study_level__v" checked /> <span data-i18n="edl.level.study">研究</span></label>
              <label><input type="checkbox" name="edl-level" value="country_level__v" checked /> <span data-i18n="edl.level.country">国家/地区</span></label>
              <label><input type="checkbox" name="edl-level" value="site_level__v" checked /> <span data-i18n="edl.level.site">中心</span></label>
            </div>
          </div>
          <div class="edl-field">
            <label for="edl-dept" data-i18n="edl.field.dept">部门</label>
            <select id="edl-dept">
              <option value="all" selected>全部部门</option>
              {{dept_options}}
            </select>
          </div>
          <p class="edl-phase-note" id="edl-phase-note"></p>
        </div>

        <div class="edl-toolbar no-print">
          <span class="edl-stats" id="edl-stats"></span>
          <button type="button" class="btn btn-primary" id="edl-csv-btn" data-i18n="edl.btn.csv">下载 TMF Index（CSV）</button>
          <button type="button" class="btn btn-outline" id="edl-print-btn" data-i18n="edl.btn.print">打印 / 导出 PDF</button>
        </div>

        <div id="edl-preview" class="edl-preview"></div>

        <p class="ctcae-related" style="margin-top:2.4rem;font-size:0.9rem;">
          <span data-i18n="edl.related">相关资源：</span><a href="tmf-reference.html" data-i18n="edl.related.tmfref">TMF 分类参考</a> ·
          <a href="tmf-checker.html" data-i18n="edl.related.checker">TMF 完整性自查器</a> ·
          <a href="template-tmf-index.html" data-i18n="edl.related.tmfindex">TMF 文件清单模板</a> ·
          <a href="glossary.html" data-i18n="edl.related.glossary">术语词典</a>
        </p>
        <script type="application/json" id="edl-data">{{edl_data_json}}</script>
"""
    dept_options = "\n".join(
        f'              <option value="{d["key"]}">{d["label"]}</option>' for d in depts)
    body = body.replace("{dept_options}", dept_options)
    body = body.replace("{edl_data_json}", json.dumps(data, ensure_ascii=False))

    meta = {
        "title": "EDL 生成器：按研究类型生成 TMF Index（Excel 下载）| Vivarcus",
        "desc": (f"EDL 生成器：选择研究类型与检查范围，生成预期文件清单 TMF Index（与 TMF 分类参考同源，{n_items} 条 EDL，"
                 f"其中必需 {n_req} 条），导出 CSV 在 Excel/WPS 中直接使用，公开下载无需注册。"),
        "file": "edl-generator.html",
        "eyebrow": "行业资源 · TMF 工具",
        "hero": "EDL 生成器",
        "subtitle": f"与 TMF 分类参考同源：按研究类型生成 TMF Index（预期文件清单，{n_items} 条），导出 CSV 在 Excel/WPS 里直接使用。",
    }
    html = sitegen.render_page(
        meta, body,
        cta_title="这张清单，Vivarcus eTMF 里自动生成并实时追踪",
        cta_desc="EDL 自动生成、文件自动归位、完整性指标实时可见——下载的清单在系统里直接可用。",
        cta_secondary_href="tmf-checker.html",
        cta_secondary_label="TMF 完整性自查器",
        extra_style=EXTRA_STYLE,
        i18n="edl",
    )
    html = html.replace("</body>",
                        '  <script src="js/tools.js"></script>\n' + PAGE_JS + "</body>")
    out = ROOT / "edl-generator.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({n_items} EDL items, {n_req} required)")


if __name__ == "__main__":
    build_page()
