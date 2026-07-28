<!-- 本文件基于上游仓库重新编写；修改与署名见 NOTICE。 -->

# Nature Skills

[![License](https://img.shields.io/badge/license-Apache--2.0-2ea44f)](LICENSE)
![Skills](https://img.shields.io/badge/skills-18-0ea5e9)
[![Validate](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml)
[English](README_EN.md)

一组面向高水平科研写作、证据审计、论文阅读、图表、投稿与研究工作流的
Agent Skills。每个技能都是可独立安装的轻量路由器，详细规范、rubric、模板与
确定性脚本只在任务需要时加载。

本仓库源于
[`Yuan1z0825/nature-skills`](https://github.com/Yuan1z0825/nature-skills)
的 Apache-2.0 内容，但采用全新的独立 Git 历史，不是 GitHub fork。基线与主要
修改见 [NOTICE](NOTICE)。

## 这版优化了什么

设计结合：

- [OpenAI GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)：
  精简且不重复的提示、结果导向契约、清晰的自主/批准边界，以及先验证最终质量；
- [Anthropic Claude 5 context-engineering guidance](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)：
  减少过度约束、使用 progressive disclosure、让接口和高保真参考承担细节；
- [OpenAI Codex skill documentation](https://developers.openai.com/plugins/build/skills)：
  清晰触发描述、聚焦单一用户目标、按需 references/scripts/assets。

相对采用的上游 HEAD：

| 指标 | 上游 | 本仓库 | 变化 |
|---|---:|---:|---:|
| 18 个触发描述总字符 | 11,021 | 6,510 | -41% |
| 18 个 `SKILL.md` 总行数 | 2,384 | 1,294 | -46% |
| `nature-downloader/SKILL.md` | 623 行 | 78 行 | -87% |
| `nature-figure` 目录 | 约 34 MB | 约 5.8 MB | 移除无明确许可证的第三方快照 |

同时完成：

- 全部 frontmatter 仅保留 `name` 与 `description`；
- 目录名、技能名、manifest 与 UI 元数据一致；
- 18/18 个技能包含 `agents/openai.yaml`；
- 每个技能均有 direct / indirect / incomplete / negative / English implicit
  触发样例，另有套件级负例与多技能组合；
- 写作/润色、预审/回复、检索/配引文/书目核验等相邻边界显式化；
- 下载器不再尝试自动绕过 CAPTCHA、滑块、OTP 或访问控制；
- 图表后端优先从项目上下文推断，仅在选择会实质影响实现时询问；
- 技能自包含，不依赖必须同时安装的跨目录 `nature-shared`。

完整设计见 [上下文工程说明](docs/context-engineering.md)。

## 技能索引

### 文献与阅读

| 技能 | 用途 | 不负责 |
|---|---|---|
| [`nature-academic-search`](skills/nature-academic-search/README.md) | 多源检索、检索式、文献图谱、引文网络审计 | 给具体句子补引用 |
| [`nature-citation`](skills/nature-citation/README.md) | claim-to-source 支撑核验与引文导出 | 书目字段清洗 |
| [`nature-ref-verifier`](skills/nature-ref-verifier/README.md) | 核对作者、题名、卷期页、DOI 与版本冲突 | 判断来源是否支持论断 |
| [`nature-downloader`](skills/nature-downloader/README.md) | 合法 OA/API/CNKI/机构全文与 SI 获取 | 搜索未知论文或绕过访问控制 |
| [`nature-literature-pipeline`](skills/nature-literature-pipeline/README.md) | 定时/批量检索、去重、摘要、投递和归档 | 单次检索 |
| [`nature-reader`](skills/nature-reader/README.md) | 全文中英文对照、图表就近、稳定源定位 | summary-only 或正式审稿 |
| [`nature-paper-card`](skills/nature-paper-card/README.md) | 单篇论文结构化证据链与批判性精读卡 | 全文双语重建 |

### 写作、投稿与评审

| 技能 | 用途 | 不负责 |
|---|---|---|
| [`nature-writing`](skills/nature-writing/README.md) | 从证据与笔记起草/重构论文和首次投稿材料 | 仅语言润色 |
| [`nature-polishing`](skills/nature-polishing/README.md) | 润色、翻译、proofread 与 LaTeX 排版 | 发明缺失科学内容 |
| [`nature-proposal-writer`](skills/nature-proposal-writer/README.md) | 基金、开题、研究方案与 proposal QA | 普通 manuscript section |
| [`nature-reviewer`](skills/nature-reviewer/README.md) | 投稿前模拟同行评审与综合 | 真实意见的作者回复 |
| [`nature-response`](skills/nature-response/README.md) | 编辑决定后的逐点回复、rebuttal 与修回包 | 投稿前 mock review |
| [`nature-data`](skills/nature-data/README.md) | Data/Code Availability、仓库、FAIR 与受限数据声明 | 上传数据或统计审计 |
| [`nature-statistics`](skills/nature-statistics/README.md) | 统计设计/报告、`n`、效应、CI、多重比较和图注 | 无设计信息的正式重分析 |

### 科研产物与记录

| 技能 | 用途 | 不负责 |
|---|---|---|
| [`nature-figure`](skills/nature-figure/README.md) | 投稿级科研图、多面板、示意图与最终尺寸 QA | 幻灯片或纯统计推断 |
| [`nature-paper2ppt`](skills/nature-paper2ppt/README.md) | 从论文生成完整 PPTX、讲稿与视觉 QA | 单张论文图 |
| [`nature-paper-to-patent`](skills/nature-paper-to-patent/README.md) | 论文/代码到中文交底书、权利要求和证据台账 | 法律、FTO 或可专利性意见 |
| [`nature-experiment-log`](skills/nature-experiment-log/README.md) | 文字/图像/转录到可追溯实验日志 | 统计分析或论文 Methods |

## 安装

查看可安装技能：

```bash
npx skills add Mubuky/nature-skills --list
```

安装单个技能：

```bash
npx skills add Mubuky/nature-skills --global --agent codex \
  --skill nature-writing --yes --copy
```

安装全部 18 个技能：

```bash
npx skills add Mubuky/nature-skills --global --agent codex \
  --skill '*' --yes --copy
```

若保留一个本地 clone，可使用仓库脚本。默认 `core` profile 只同步本项目原先
使用的 11 个核心技能；`--profile all` 同步全部 18 个：

```bash
scripts/update-codex-skills.sh --profile core
scripts/update-codex-skills.sh --check --profile core
```

安装或更新后重启 Codex/Agent，让宿主重新载入技能元数据。Python、R、浏览器、
MCP 与出版商 API 凭据是按工作流选择的可选运行依赖，不会由安装器静默安装。

## 验证与开发

```bash
python3 scripts/generate_openai_metadata.py
git diff --exit-code -- skills
python3 scripts/validate_context_engineering.py
python3 scripts/validate_trigger_cases.py
python3 scripts/validate-repository.py
python3 scripts/validate-skill-metadata.py
python3 scripts/validate-workflows.py
bash -n scripts/update-codex-skills.sh
python3 scripts/test_update_codex_skills.py
python3 -m unittest discover -s skills/nature-citation/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-paper-to-patent/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-downloader/tests/python -p 'test_*.py'
node --test skills/nature-downloader/tests/unit/*.test.mjs
python3 skills/nature-figure/scripts/validate_figure.py --self-test
```

`evals/trigger_cases.jsonl` 是 104 条带标签的静态路由覆盖集：90 条逐技能样例、
6 条期望不触发本套件的负例，以及 8 条多技能组合。它只验证 schema、标签和
覆盖，不测模型激活准确率；重大修改仍应在相同真实任务上做 forward test。质量、
证据完整性与最终产物正确性通过后，再比较上下文、token、延迟或调用次数。

## 许可证与来源

根项目使用 [Apache License 2.0](LICENSE)。部分组件保留自己的 MIT 许可证或
署名文件。来源 commit、独立派生关系、修改范围和第三方素材处理见
[NOTICE](NOTICE)。

本仓库不重新分发上游曾打包的 `figures4papers` 快照，因为该快照中未发现对应
许可证。公开可见不等于允许再分发。
