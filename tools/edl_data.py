#!/usr/bin/env python3
"""Shared EDL data source for tmf-checker / tmf-reference / edl-generator.

Single source of truth: release-payloads/desired/clinical-operations/etmf/data/templates/*.zh.csv
数据与分类页同源，禁止复制（build_tmf_checker.py / build_edl_generator.py 共用本模块）。
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
REQ_LABEL = {"required__v": "必需", "notrequired__v": "不要求", "pending_decision__v": "待定"}
LEVEL_LABEL = {"study_level__v": "研究", "country_level__v": "国家/地区", "site_level__v": "中心"}
OTHER_DEPT = "other"  # 未归属部门的条目归入「其他」

# 研究类型 × 阶段的编者提示（数据源无阶段字段，提示仅作参考，不做条目过滤）
PHASE_NOTES = {
    "drug:phase_i": "I 期多为单中心、剂量探索设计：重点核对中心层级启动文件、安全性报告（SAE/SUSAR）与剂量递增相关记录。",
    "drug:phase_ii": "II 期聚焦疗效与安全性探索：重点核对方案、知情同意、安全性报告与研究层级管理文件。",
    "drug:phase_iii": "III 期多中心确证性试验，国家/地区与中心层级文件量最大：重点核对多中心一致性文件与稽查准备记录。",
    "drug:phase_iv": "IV 期上市后研究：重点核对上市后安全性监测、研究者发起的相关记录与注册事务文件。",
    "device:none": "器械试验涉及注册检验与器械相关不良事件路径：文件范围以器械注册申报要求为准，本清单按 TMF 参考模型通用条目整理。",
    "be:none": "BE 试验周期短、中心少：重点核对生物样本管理、分析报告与一致性评价相关文件。",
}


def read_edl():
    """标准 EDL 条目（zh），里程碑名经 milestone_template 映射。"""
    milestones = {}
    with (PAYLOAD / "milestone_template__v.zh.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            milestones.setdefault(r["milestone_type__v"], r["name__v"])
    rows = list(csv.DictReader((PAYLOAD / "edl_item_template__v.zh.csv").open(encoding="utf-8")))
    items = []
    for i, r in enumerate(rows):
        dept = r["etmf_department__v"] or ""
        items.append({
            "id": r["external_id__v"] or f"row{i}",
            "name": r["name__v"],
            "dept": dept if dept in DEPT_LABEL else OTHER_DEPT,
            "requiredness": r["requiredness__v"] or "",
            "level": r["level__v"] or "",
            "count": r["expected_steady_state_count__v"] or "",
            "milestone": milestones.get(r["milestone_type__v"] or "", ""),
        })
    return items
