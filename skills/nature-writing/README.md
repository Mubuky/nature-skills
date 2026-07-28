# `nature-writing` 技能

[English](README_EN.md)

`nature-writing` 用于根据作者提供的 claims、图表、结果、笔记或中文草稿，起草或重建 Nature 风格手稿章节，保真润色已有文本，处理 LaTeX 排版，并准备首次投稿材料包。

## 适合用它做什么

- 构建标题、摘要、引言、结果叙事、讨论、结论或 significance paragraph。
- 根据图表和数据组织 claim-evidence 叙事。
- 将中文研究笔记转成英文手稿段落。
- 为 Introduction 建立背景、缺口、问题和贡献链。
- 对 Results 或 Discussion 做章节级重排，而不是只做句子润色。
- 在不改变 claim、证据、数字、引用和不确定性的前提下润色、校对或翻译已有文本。
- 诊断 LaTeX 浮动体、稀疏页面、悬空标题和多面板排版。
- 准备首次投稿 cover letter、title page、highlights、作者贡献、数据/代码可用性和其他声明。
- 整理推荐审稿人、投稿材料矩阵和提交前完整性检查。

## 典型请求

- “根据这些图和结果写一个 Nature 风格 abstract。”
- “帮我重建 introduction 的逻辑，不要只润色句子。”
- “把这些中文结果整理成英文 Results 叙事。”
- “只润色这段英文，不改变任何科学论断或数值。”
- “修复 Supplementary Information 的空白页和浮动体布局。”
- “根据这篇稿件准备首次投稿 cover letter 和完整 submission package。”

## 你需要提供

- 核心 claim、图表、关键结果、实验事实和目标读者。
- 目标章节、长度、语言和需要保留的术语。
- 润色时提供原文和允许修改的范围；排版时提供 LaTeX 源码及可用编译产物。
- 已确认引用、限制条件和不能新增的结论。

## 产出

- 章节大纲、claim-evidence map 或可粘贴正文。
- 对 novelty、significance、证据链和读者路径的修改建议。
- 保真润色文本及必要的简短修改说明，或 LaTeX 布局诊断与验证状态。
- 需要作者确认的事实、引用或图表说明。
- 首次投稿材料包、可编辑 LaTeX 模板、缺失信息清单和 `ready / ready_with_author_checks / blocked` 状态。

## 边界

- 不会替作者虚构实验结果、统计意义、机制解释或参考文献。
- 润色和排版走按需 special route，不会加载完整 drafting workflow；无法在局部边界内修复的问题只会标记或另行建议结构重写。
- 如果需要先找文献支撑 claim，优先使用 `nature-citation` 或 `nature-academic-search`。
- 首次投稿材料由本技能处理；返修 cover letter、rebuttal 和逐点回复由 `nature-response` 处理。

## 相关技能

- `nature-citation`：为 claim 匹配支撑文献。
- `nature-figure`：把图件结论和面板设计对齐到正文叙事。
- `nature-response`：返修 cover letter、response to reviewers 和返修通信材料。
- `nature-reviewer`：投稿前模拟审稿。
