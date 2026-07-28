<!-- 本教程基于上游版本重写；来源与修改见 ../NOTICE。 -->

# `nature-paper-card` 快速教程

这个教程演示如何把一篇论文整理成有来源定位、可复核的 01–16 节 Paper Card。
它不是摘要模板；核心验收对象是“论断—证据—定位”能否互相对应。

## 1. 准备输入

优先提供论文 PDF 或 `nature-reader` 生成的 source-map JSON，并说明：

- 输出语言与目录；
- 希望重点审查的方法、实验或结论；
- 是否允许为背景事实进行外部检索。

只有摘要或局部文本也能开始，但输出必须使用 `source-limited` 模式，并把不可判断
内容标为 `Not assessable`。

## 2. 触发技能

```text
使用 nature-paper-card 精读这篇论文，生成中文 Paper Card。
重点检查方法模块、决定性实验、结论边界和可验证的后续研究想法。
```

若输入不在当前工作目录，同时给出准确路径或可访问链接。

## 3. 选择来源定位模式

| 模式 | 何时使用 | 定位要求 |
|---|---|---|
| `page-grounded` | PDF 页码可靠 | 同时记录 PDF 页码与图、表、公式或章节 |
| `structure-grounded` | HTML/XML 或页码不稳定 | 使用章节、段落、图表或公式标识 |
| `source-limited` | 只有摘要或局部材料 | 明确材料边界，不推断不可见内容 |

模式描述的是证据可定位程度，不是论文质量。

## 4. 标准产物

- `paper-card.md`：固定 01–16 节；
- `source_bundle.json`：规范化来源与定位信息；
- `audit-report.json`：结构、定位和证据约束审计；
- `rendered-pages/`：仅在需要视觉核对 PDF 页面时生成。

技能会先建立证据清单与 claim–evidence matrix，再撰写卡片。外部事实、Agent 分析
和研究假设必须与论文作者陈述分开标记。

## 5. 可复现的本地检查

以下路径均相对于仓库根目录；实际调用时也可以让 Agent 根据已安装 Skill 的目录
解析脚本。

```bash
python3 skills/nature-paper-card/scripts/prepare_paper.py paper.pdf \
  --output source_bundle.json

python3 skills/nature-paper-card/scripts/audit_paper_card.py \
  --card paper-card.md \
  --bundle source_bundle.json \
  --locator-mode page-grounded \
  --report audit-report.json
```

若输入不是可靠分页 PDF，应把 `--locator-mode` 改成
`structure-grounded` 或 `source-limited`。

## 6. 验收清单

- 01–16 节齐全且没有自行增加第 17、18 节；
- 核心结论能回到具体图、表、公式、实验或来源片段；
- 论文没有展示的实验、页码和机制没有被补写；
- 作者结论、外部事实、Agent 分析和研究假设区分清楚；
- 后续研究想法可证伪、可执行，并写明其证据起点；
- 审计报告中的失败项已修复，剩余限制已显式说明。
