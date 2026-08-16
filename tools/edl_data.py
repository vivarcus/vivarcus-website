#!/usr/bin/env python3
"""Shared EDL data source for tmf-checker / tmf-reference / edl-generator.

Single source of truth: release-payloads/desired/clinical-operations/etmf/data/templates/*.zh.csv
数据与分类页同源，禁止复制（build_tmf_checker.py / build_edl_generator.py 共用本模块）。

英文名（name__v / 里程碑名）从同目录 *.csv（非 .zh）按 external_id__v 对齐读取，
即产品数据自身的英文原文，不做二次翻译。
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # website/
PAYLOAD = ROOT.parent / "release-payloads/desired/clinical-operations/etmf/data/templates"

# 与 build_tmf_reference.py 相同的产品 picklist 语义标签
DEPT_LABEL = {
    "clinical_operations__c": "临床运营",
    "supplies__c": "试验供应",
    "data_management__c": "数据管理",
    "biostatistics__c": "生物统计",
    "regulatory_affairs__c": "法规事务",
    "safety__c": "药物安全",
    "medical_writing__c": "医学写作",
    "quality_assurance__c": "质量保证",
    "project_management__c": "项目管理",
    "medical_affairs__c": "医学事务",
}
DEPT_LABEL_EN = {
    "clinical_operations__c": "Clinical Operations",
    "supplies__c": "Trial Supplies",
    "data_management__c": "Data Management",
    "biostatistics__c": "Biostatistics",
    "regulatory_affairs__c": "Regulatory Affairs",
    "safety__c": "Drug Safety",
    "medical_writing__c": "Medical Writing",
    "quality_assurance__c": "Quality Assurance",
    "project_management__c": "Project Management",
    "medical_affairs__c": "Medical Affairs",
}
REQ_LABEL = {"required__v": "必需", "notrequired__v": "不要求", "pending_decision__v": "待定"}
REQ_LABEL_EN = {"required__v": "Required", "notrequired__v": "Not required", "pending_decision__v": "Pending decision"}
LEVEL_LABEL = {"study_level__v": "研究", "country_level__v": "国家/地区", "site_level__v": "中心"}
LEVEL_LABEL_EN = {"study_level__v": "Study", "country_level__v": "Country/Region", "site_level__v": "Site"}
OTHER_DEPT = "other"  # 未归属部门的条目归入「其他」
OTHER_DEPT_EN = "Other"

# 研究类型 × 阶段的编者提示（数据源无阶段字段，提示仅作参考，不做条目过滤）
PHASE_NOTES = {
    "drug:phase_i": "I 期多为单中心、剂量探索设计：重点核对中心层级启动文件、安全性报告（SAE/SUSAR）与剂量递增相关记录。",
    "drug:phase_ii": "II 期聚焦疗效与安全性探索：重点核对方案、知情同意、安全性报告与研究层级管理文件。",
    "drug:phase_iii": "III 期多中心确证性试验，国家/地区与中心层级文件量最大：重点核对多中心一致性文件与稽查准备记录。",
    "drug:phase_iv": "IV 期上市后研究：重点核对上市后安全性监测、研究者发起的相关记录与注册事务文件。",
    "device:none": "器械试验涉及注册检验与器械相关不良事件路径：文件范围以器械注册申报要求为准，本清单按 TMF 参考模型通用条目整理。",
    "be:none": "BE 试验周期短、中心少：重点核对生物样本管理、分析报告与一致性评价相关文件。",
}
PHASE_NOTES_EN = {
    "drug:phase_i": "Phase I is mostly single-center, dose-escalation design: focus on site-level startup documents, safety reports (SAE/SUSAR) and dose-escalation records.",
    "drug:phase_ii": "Phase II focuses on efficacy and safety exploration: focus on the protocol, informed consent, safety reports and study-level management documents.",
    "drug:phase_iii": "Phase III multicenter confirmatory trials carry the largest country/region- and site-level document volume: focus on multicenter consistency documents and audit readiness records.",
    "drug:phase_iv": "Phase IV post-marketing studies: focus on post-marketing safety monitoring, investigator-initiated records and regulatory affairs documents.",
    "device:none": "Device trials involve registration testing and device-specific adverse event pathways: the document scope follows device registration filing requirements; this checklist is organized per TMF Reference Model generic items.",
    "be:none": "BE studies are short with few sites: focus on biospecimen management, analysis reports and bioequivalence evaluation documents.",
}


def _load_milestones(path):
    milestones = {}
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            milestones.setdefault(r["milestone_type__v"], r["name__v"])
    return milestones


def _load_names_en():
    """external_id__v -> English name from the non-zh EDL item CSV."""
    names = {}
    with (PAYLOAD / "edl_item_template__v.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            names[r["external_id__v"]] = r["name__v"]
    return names


def read_edl():
    """标准 EDL 条目（zh + en 双名），里程碑名经 milestone_template 映射。"""
    milestones = _load_milestones(PAYLOAD / "milestone_template__v.zh.csv")
    milestones_en = _load_milestones(PAYLOAD / "milestone_template__v.csv")
    names_en = _load_names_en()
    rows = list(csv.DictReader((PAYLOAD / "edl_item_template__v.zh.csv").open(encoding="utf-8")))
    items = []
    for i, r in enumerate(rows):
        dept = r["etmf_department__v"] or ""
        eid = r["external_id__v"] or f"row{i}"
        items.append({
            "id": eid,
            "name": r["name__v"],
            "name_en": names_en.get(eid, r["name__v"]),
            "dept": dept if dept in DEPT_LABEL else OTHER_DEPT,
            "requiredness": r["requiredness__v"] or "",
            "level": r["level__v"] or "",
            "count": r["expected_steady_state_count__v"] or "",
            "milestone": milestones.get(r["milestone_type__v"] or "", ""),
            "milestone_en": milestones_en.get(r["milestone_type__v"] or "", ""),
        })
    return items
