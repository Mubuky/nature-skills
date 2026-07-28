<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# `nature-citation` 技能

[English](README_EN.md)

`nature-citation` 用于把论文段落、手稿片段或单条科学判断拆成可引用的 claim，并为每个 claim 寻找 Nature Portfolio、Science family 和 Cell Press 范围内的支撑文献。

## 适合用它做什么

- 给 introduction、discussion 或 reviewer response 中的关键判断补引用。
- 将长段落拆成稳定编号的 claim 单元，例如 `S001`、`S002`。
- 限定只查 Nature、Science、Cell 及其子刊，或只保留旗舰刊。
- 为每个候选文献说明待核验的匹配关系；核验后记录证据位置和支撑强度。
- 仅将经过语义筛选、带证据定位的选择导出为 Zotero、EndNote 或其他文献管理器可用的文件。

## 典型请求

- “把这段 introduction 分段补 Nature 系列引用。”
- “只用 CNS 及子刊，为这些 claim 找近五年的支撑文献。”
- “这些 DOI 已逐条核验并映射到对应 claim，帮我校验筛选记录后导出 Zotero 文件。”

## 你需要提供

- 待引用的段落或 claim 列表；已知 DOI 可作为每条 claim 的候选输入。
- 期刊范围、时间范围、是否允许综述、是否只要旗舰刊。
- 目标引用格式和导出格式，例如 `RIS`、`ENW` 或 Zotero `RDF`。

## 产出

- claim 分段表和候选文献表；候选发现阶段只产生 JSON/TSV/Markdown 审查材料。
- 经人工或代理阅读摘要/全文后形成的 claim–source 映射、证据定位、核验时间和支撑等级。
- 只有通过 screened-selection 门的记录才会生成可导入文献管理器的引用文件及筛选审计记录。

## 边界

- 标题或元数据匹配只会进入候选池，不会产生插入标记或最终引用文件。
- 只把论文作为候选支撑，不会替作者保证其必然适合最终引用。
- 不会使用博客、新闻稿或搜索摘要作为唯一依据。
- 当文献只能支撑相邻但不完全相同的 claim 时，会明确标注证据偏差。

## 相关技能

- `nature-academic-search`：更宽范围的文献搜索和引用指标审计。
- `nature-ref-verifier`：校验已选参考文献的元数据。
- `nature-writing`：把引用选择整合回手稿论证。
