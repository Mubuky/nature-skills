<!-- Modified in the context-engineered edition; see ../../NOTICE. -->

# nature-downloader

<p align="center">
  <img src="assets/banner.jpg" alt="nature-downloader — 合法 OA、出版商 API 与机构授权全文下载" width="100%">
</p>

`nature-downloader` 按文献语言、出版商和可用凭据自动选择合法下载路线：

```text
确认是否下载 SI
→ 中文文献：只走 CNKI / 知网机构授权
→ 英文文献
   ├─ Elsevier / Springer Nature / IEEE 且有可用 Key
   │  ├─ 出版商 API 成功：结束，不强制判断 OA
   │  └─ API 失败：PMC → Unpaywall → 出版商 OA / 合法仓储
   └─ 其他出版商：先查 OA，OA 不可用时走 Web Access 机构授权
```

## 工作方式

1. 先判断文献语言、出版商和 SI 需求，再决定路由。
2. 能走合法 API 就优先走 API；API 不通时再降级到 OA / 仓储 / 机构授权路径。
3. 输出时同时记录访问路径、失败原因和可复用配置，方便后续批量任务。
4. 全程不绕过付费墙、DRM、验证码或双重认证，也不读取或导出浏览器 cookie、密码、localStorage 或 session 文件。

## 下载前必须确认 SI

所有下载命令必须显式选择一次：

```bash
--no-si  # 只下载正文
--si     # 下载正文和可找到的 Supporting Information
```

两者均未提供时，脚本返回 `si_confirmation_required`，且不会创建输出目录或下载文件。两者同时提供时参数校验失败。批量任务的选择作用于整个批次。

## 配置

### 图书馆与 CNKI

优先保存用户实际使用的图书馆资源入口：

```bash
python3 scripts/configure_school.py infer "https://example.edu/library/resources"
python3 scripts/configure_school.py url "https://example.edu/library/resources"
python3 scripts/configure_school.py show
python3 scripts/configure_school.py health --force
```

普通配置保存在 `~/.config/lit-dl/school.json`。

### 出版商 API

非 OA 英文文献命中对应出版商时才需要配置：

- Elsevier：[Developer Portal](https://dev.elsevier.com/)
- Springer Nature：[API Access](https://dev.springernature.com/docs/quick-start/api-access/)
- IEEE：[Developer Registration](https://developer.ieee.org/member/register)

使用隐藏输入保存 API key：

```bash
python3 scripts/configure_credentials.py set elsevier
python3 scripts/configure_credentials.py set springer_nature
python3 scripts/configure_credentials.py set ieee
python3 scripts/configure_credentials.py show
python3 scripts/configure_credentials.py validate elsevier
python3 scripts/configure_credentials.py delete elsevier
```

自动化环境使用结构化标准输入；不要把秘密写进命令参数、回复或 manifest：

```bash
python3 scripts/configure_credentials.py set elsevier --stdin-json \
  < /secure/path/publisher-credentials.json
```

未主动提供时仍优先使用本地隐藏输入。机构密码、OTP、Cookie 和会话令牌不适用此规则。

Elsevier 的可选机构 token 和 IEEE Full-Text endpoint 模板也通过隐藏提示或
标准输入 JSON 提供，不进入 argv。
IEEE 普通 Metadata API key 不代表收费全文权限；只有获得 Full-Text Access API
产品后，才配置由 IEEE 提供的 endpoint 模板。秘密保存在
`~/.config/lit-dl/credentials.json`，文件权限为 `0600`；短秘密会完全遮蔽，
较长秘密仅显示末四位。

Unpaywall 需要合规联系邮箱：

```bash
python3 scripts/configure_credentials.py contact-email researcher@example.org
```

该邮箱保存在非秘密配置 `~/.config/lit-dl/settings.json`。

## 下载示例

按 DOI 下载正文：

```bash
node scripts/batch_download.mjs \
  --dois "10.1007/s00122-021-03957-1,10.1111/pbi.14066" \
  --no-si \
  --out "./文献自动下载"
```

中文题名只走知网：

```bash
node scripts/batch_download.mjs \
  --title "乡村振兴背景下数字治理研究" \
  --no-si \
  --out "./文献自动下载"
```

默认 PDF 优先、允许 CAJ；只接受 PDF 时增加 `--cnki-format pdf`。学校提供专用知网入口时增加 `--cnki-url URL`。

英文 OA 精确题名：

```bash
node scripts/batch_download.mjs \
  --title "Attention Is All You Need" \
  --open-access \
  --no-si \
  --out "./文献自动下载"
```

主题检索并下载 SI：

```bash
node scripts/batch_download.mjs \
  --topic "rice blast resistance gene" \
  --count 10 \
  --si \
  --out "./文献自动下载"
```

已知合法全文 URL：

```bash
node scripts/batch_download.mjs \
  --pdf-url "https://arxiv.org/pdf/1706.03762" \
  --title "Attention Is All You Need" \
  --no-si \
  --out "./文献自动下载"
```

元数据冲突时可用 `--language zh|en` 或 `--route cnki|open_access|elsevier|springer_nature|ieee|web_access` 覆盖。`--source-url` 指向 CNKI 时强制中文 CNKI 路由。

## API 失败与 Web Access 回退

三家 API 返回无 entitlement 或无全文时，会先自动尝试 PMC、Unpaywall、出版商 OA 和合法仓储。只有 API 与 OA 都未取得全文时，才返回 `api_fallback_confirmation_required`；确认后按出版商重新运行：

```bash
--api-fallback-web-for elsevier
--no-api-fallback-web-for springer_nature
```

全批次统一选择也可使用 `--api-fallback-web` 或 `--no-api-fallback-web`。Web Access 复用用户已登录的 Chrome 机构会话；登录、QR、OTP 和复杂验证仍由用户本人完成。

如果 PMC/Unpaywall 等 OA 检查无法确认文章状态，manifest 会记录 OA assessment 为 `unknown`，但不会把它误标为非 OA；后续仍可使用机构 Web Access 寻找授权全文。

## 输出

- 本地 PDF、HTML、文本或 CNKI 原生全文文件。
- `manifest.json` 记录每篇文献的访问路径、OA/API 回退历史、保存路径、完整性哈希、SI 选择和失败原因。
- 可复用学校入口配置，通常保存在 `~/.config/lit-dl/school.json`。

```text
文献自动下载/
  PDFs/
  FullText/
  CNKI/
  SupportingInformation/
  manifest.json
```

`manifest.json` 记录规范 DOI、语言、出版商、路由、OA 证据、访问模式、正文格式、MIME、大小、SHA-256、SI 选择和失败原因，并递归移除 API key、token、cookie 等秘密字段。

正文成功格式包括：

- PDF：`downloaded` / `open_access_downloaded`
- CNKI CAJ、Springer JATS/XML：`native_fulltext_downloaded`
- 可读 HTML 全文：`full_text_html_available`
- 正文和 SI：`downloaded_with_si`

## 边界

- 不绕过付费墙，不使用镜像站，也不读取或导出 cookie、密码、localStorage 或 session 文件。
- CAPTCHA、滑块、Turnstile/reCAPTCHA、机器人校验、二维码、短信/OTP、
  通行密钥、硬件密钥与双重认证一律立即交由用户本人完成；脚本不得点击、
  拖动、求解或声称绕过这些挑战。
- 没有合法访问权限时，只报告状态、失败原因和可能替代路线。

## 相关技能

- `nature-academic-search`：从题名、DOI 或主题查找目标文献。

## 验证

```bash
python3 -m unittest discover -s tests/python
node --test tests/unit/*.test.mjs
node --check scripts/batch_download.mjs
node --check scripts/browser_pdf_downloader.mjs
```
