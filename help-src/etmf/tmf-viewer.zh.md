---
title: TMF Viewer 与 Master File Binder
description: 理解 Binder（物理归档）与 TMF Viewer（按参考模型的虚拟浏览）两套能力的分工，学习 Create Study Binders、自动归档与 View Model 切换。
last_updated: 2026-08-15
related:
  - upload-documents
  - review-workflow
  - overview
---

## Binder 与 Viewer 的分工

eTMF 提供两套「按参考模型找文档」的能力，分工不同：

| | Binder（活页夹） | TMF Viewer（查看器） |
|--|------------------|----------------------|
| 定位 | Master File 的**物理归档容器** | 按 DocType → Artifact 映射计算的**虚拟视图** |
| 生成 | 依赖 **Create Study Binders**；支持 Auto-Filing / 手工挂链 | **不依赖** Binder 是否存在 |
| 内容 | Section 树 → 文档链接（含 Filing Origin） | Artifact 树 + 文档列表，按 Study 范围计算 |

手工移入/移出 Binder **不会**改变 Viewer 中的位置；Viewer 的位置只跟文档分类与 Study 范围有关。

## 创建研究活页夹（Create Study Binders）

1. 打开研究 → **All Actions → Create Study Binders**。
2. **Model** 选择参考模型（如 **TMF RM v3.0**）；**Filing Levels** 选择研究级、国家/地区级和研究机构级主文件，确认。
3. 创建后可见 **Study Level File**、**Country Level File**、**Site Level File**（对应已建的国家/中心）。

> 已有同层级 Binder 时重复创建是幂等的（可能计为 skipped）。

## 自动归档（Auto-Filing）

已批准且分类已映射到当前 Model 的文档，会以 **Filing Origin = Auto-filed** 挂到对应 Section 节点：

- 国家/中心级文档只落在对应层级 Binder，**不会**回退到 Study Level。
- 树中暂无文档时，等待几秒后刷新；仍没有则执行 **Refresh Auto-Filing**。
- 重复刷新**不会**产生重复节点。

## 使用 TMF Viewer

1. 顶部导航 → **TMF Viewer**。
2. **Study** 选研究；**View Model** 选参考模型（宜与 Binder 所用 Model 一致）。
3. 左侧 Artifact 树展开定位文档，右侧列表点击进入文档详情。
4. 选择 Study Country / Study Site 可裁剪范围；**Collapse All / Expand All** 控制树展开。

> Viewer 左侧树为空时：确认已选 Study；文档须具备已映射到当前 View Model 的 Classification。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| Binder 树中看不到已批准文档 | 确认已创建对应层级 Binder；Model 与 DocType 的 Artifact 映射一致；等待 Job 或执行 Refresh Auto-Filing |
| Refresh Auto-Filing 无变化 | 确认文档 Study / Country / Site 与 Binder 层级精确匹配；Classification 已映射到该 Binder 的 Model |
| Viewer 看不到刚上传的文档 | 确认 Document Type / Classification 已映射到 TMF RM，且文档 Study 字段正确 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| Tab | TMF Viewer：View | 访问 TMF Viewer |
| 对象 | Document：Read | 浏览并打开文档 |
| 对象动作 | Study：**Create Study Binders** | 生成 Master File Binder |
| 对象动作 | Binder：**Refresh Auto-Filing** | 手动触发自动归档 |

**External Inspector** 等只读角色可完整使用 Viewer（虚拟浏览不依赖 Binder）；创建 Binder 与刷新归档需要编辑类权限。
