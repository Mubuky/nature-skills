<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# `nature-academic-search` 技能

[English](README_EN.md)

`nature-academic-search` 用于多源学术检索、检索策略、引用格式转换、已有书目
逐字段核验、严格他引审计和高影响力引用者分析。

## 适合用它做什么

- 在 CrossRef、PubMed、arXiv、Scopus、ScienceDirect 等来源中检索论文。
- 根据 DOI、PMID 或 arXiv ID 获取结构化文献信息。
- 生成 Nature、APA、IEEE、Vancouver 等引用格式。
- 构建 MeSH 检索式，辅助医学和生命科学主题检索。
- 核对已有参考文献的作者顺序、题名、卷期页、DOI 和版本冲突。
- 审计目标论文的严格他引，排除自引、团队引和明显合作网络引用。
- 识别院士、Fellow、高被引学者、院校领导或领域专家如何引用目标论文。

## 典型请求

- “帮我查这篇论文的严格他引，并列出高影响力引用者。”
- “按这个主题找 20 篇近五年的 Nature/Science/Cell 相关论文。”
- “把这些 DOI 转成 Nature 格式引用，并导出 RIS。”
- “为 PubMed 检索式补 MeSH 词和同义词。”
- “逐条核对这份 BibTeX 的 DOI、作者、年份和页码，列出安全修正。”

## 你需要提供

- 检索主题、关键词、时间范围、期刊范围或目标文献 DOI。
- 书目核验时提供原始参考文献、BibTeX/RIS 或文献管理器导出，并说明允许查询的数据源。
- 如需生成修正后的导出，明确授权可修改的条目和字段。
- 是否允许使用 Scopus / ScienceDirect 等需要本机配置的来源。
- 严格他引的排除口径，例如是否排除同机构、共同作者或课题组网络。

## 产出

- 去重后的文献表，包含标题、作者、年份、期刊、DOI 和来源。
- 引用格式文本或 `.ris`、`.bib`、`.nbib`、`.enw` 等文献管理文件。
- 书目逐字段差异、证据来源、严重性、条目状态及无法核验项。
- 严格他引统计表和引用上下文摘要。
- 查询策略、数据源说明和无法验证的条目列表。

## 运行和依赖

- PubMed 检索需要配置 `PUBMED_EMAIL` 或 `mcp-server/config.toml`。
- Scopus / ScienceDirect 依赖本机 `pybliometrics` 配置，默认读取 `~/.config/pybliometrics.cfg`。
- 不要把 Elsevier API key 写入仓库文件；只在本机安全配置中保存。
- 仓库不包含会静默安装依赖或改写宿主 MCP 配置的安装器；可选
  `config/mcp-snippet.json` 仅供人工审阅后适配。

## 边界

- 二级学术索引只能作为发现线索，关键字段应回到 DOI、PubMed、出版社页面或数据库记录核实。
- 严格他引判断需要明确排除规则；没有作者/机构信息时会标注不确定。
- 书目字段核验不等于论断支撑核验；后者使用 `nature-citation`。
- 无权限数据库不会被绕过，只会报告缺失来源或需要用户登录。

## 相关技能

- `nature-citation`：为手稿 claim 匹配 Nature/CNS/Cell 支撑文献。
