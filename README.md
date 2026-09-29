# File to Markdown

**中文** | [English](#english)

把本地的一个文件上传到转换接口，拿回一个 zip，解压后是 `.md` 文件加上一个
`image/` 图片目录。

仓库地址：

- GitHub：<https://github.com/trampzz/anything2markdown>
- Gitee：<https://gitee.com/zq-168/anything2markdown>

> 仓库名是 `anything2markdown`，skill 名是 `file-to-markdown`，它们指的是同一个
> 东西：仓库叫 `anything2markdown`，安装后 skill 文件夹叫 `file-to-markdown`，
> 这样在对话里用 `$file-to-markdown` 引用最自然。

---

## 中文简介

一个把 **PDF、Office 文档、图片** 一键转成 Markdown 的小工具。

它调用远程转换接口完成转换，服务端会按文件后缀自动选择处理方式：

| 上传的文件 | 转换方式 |
| --- | --- |
| `.pdf` | 普通 PDF 走文本抽取；整篇都是扫描件时自动走 OCR |
| `.doc` `.docx` `.ppt` `.pptx` `.xls` `.xlsx` | Office 文档转换 |
| `.bmp` `.jpeg` `.jpg` `.png` `.tif` `.tiff` `.webp` | OCR 文字识别 |

一次请求只传一个文件，混传不同类型会被拒绝。

### 特点

- **扫描件可用**：只有整篇都是扫描件时才走 OCR，避免在普通 PDF 上浪费时间。
- **图片一起返回**：正文引用到的图片会放在 `image/` 目录里，Markdown 直接可用。
- **零依赖脚本**：调用脚本只用 Python 标准库，CentOS 7 等老系统也能直接跑。
- **计次可控**：接口按 key 计次，次数用光会返回明确状态码。

### 安装

这个 skill 本质就是一个文件夹（核心文件是 `SKILL.md`），**安装 = 把整个文件夹
放到 skills 目录里**。下面按 GitHub / Gitee 两种下载来源、命令行 / 压缩包两种
方式分别说明。

#### 前置条件

- `git`：用命令行 clone 时需要；直接下载 ZIP 可以跳过。
- `Python 3.8+`：运行自带脚本时需要。脚本只用标准库，**不需要 `pip install`
  任何依赖包**，所以 CentOS 7 这类老系统也能直接用。

#### 快捷方式：一条命令或让 agent 代装

只是想快点装上的话，克隆到 skills 目录其实只有一条命令（自动建目录、自动
放到正确位置）：

```bash
# macOS / Linux（Codex 全局）
mkdir -p ~/.codex/skills && \
  git clone --depth 1 https://github.com/trampzz/anything2markdown.git \
  ~/.codex/skills/file-to-markdown
```

```powershell
# Windows PowerShell（Codex 全局）
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone --depth 1 https://github.com/trampzz/anything2markdown.git "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

换成 Gitee 只要把域名替换成 `gitee.com/zq-168`；改用 Claude Code 就把
`.codex` 换成 `.claude`。

**让 AI 助手帮你装**：在 Codex / Claude Code 里新建一个对话，把下面这段原样
发过去即可，助手会自己完成下载、摆放和验证：

```text
请帮我安装 file-to-markdown skill：
1. 从 https://github.com/trampzz/anything2markdown 克隆（如果访问不了就用 Gitee：https://gitee.com/zq-168/anything2markdown）
2. 放到 Codex 的 ~/.codex/skills/file-to-markdown/；如果我用的是 Claude Code，就放到 ~/.claude/skills/file-to-markdown/
3. 确保 SKILL.md 直接位于 file-to-markdown 文件夹内，不要多套一层
4. 运行 python scripts/convert_to_markdown.py --help 验证能正常启动，并把结果告诉我
```

在 Codex 里如果已经装了 skill 安装器，也可以直接用一句：

```text
用 $skill-installer 安装 https://github.com/trampzz/anything2markdown
```

下面的「第一步」到「第四步」是手动安装的完整流程，按需选用即可。

#### 第一步：下载

命令行 clone：

```bash
# GitHub
git clone https://github.com/trampzz/anything2markdown.git

# Gitee
git clone https://gitee.com/zq-168/anything2markdown.git
```

或者下载 ZIP：

- GitHub：仓库页面 → `Code` → `Download ZIP`
- Gitee：仓库页面 → `克隆/下载` → `下载 ZIP`

解压后会得到一个 `file-to-markdown` 文件夹。

#### 第二步：放到 skills 目录

按你用的工具选择目录，`~` 在 Windows 上就是 `C:\Users\<你的用户名>`：

| 使用场景 | 安装目录 |
| --- | --- |
| Codex（全局） | `~/.codex/skills/file-to-markdown/` |
| Claude Code（全局） | `~/.claude/skills/file-to-markdown/` |
| 只给某个项目用 | `<项目>/.codex/skills/file-to-markdown/` 或 `<项目>/.claude/skills/file-to-markdown/` |

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/trampzz/anything2markdown.git \
  ~/.codex/skills/file-to-markdown
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/trampzz/anything2markdown.git `
  "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

Windows CMD：

```cmd
mkdir "%USERPROFILE%\.codex\skills"
git clone https://github.com/trampzz/anything2markdown.git "%USERPROFILE%\.codex\skills\file-to-markdown"
```

如果你下载的是 ZIP，就把解压出来的 `file-to-markdown` 文件夹**整体**拷进上面的
skills 目录即可。用 Claude Code 或项目级安装时，把命令里的 `.codex` 换成
`.claude`，或把路径换成项目目录。

#### 第三步：检查目录结构

放好之后目录应该长这样，`SKILL.md` 必须**直接**在 `file-to-markdown` 里：

```text
file-to-markdown/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── convert_to_markdown.py
```

常见的错误是解压后多套了一层，变成
`skills/file-to-markdown/file-to-markdown/SKILL.md`。这时要把**内层**文件夹挪
出来，保证只有一层 `file-to-markdown`。

#### 第四步：重开并验证

重启或刷新 Codex / Claude Code，让它重新扫描 skills 目录，然后跑一次脚本确认
能启动：

```bash
python ~/.codex/skills/file-to-markdown/scripts/convert_to_markdown.py --help
```

能打印出参数帮助就说明文件到位了。此时还没配地址和 key，真正转换前请先看下面的
「配置接口地址和 key」。

#### 更新

命令行安装的：

```bash
cd ~/.codex/skills/file-to-markdown
git pull
```

ZIP 安装的：重新下载最新 ZIP，覆盖原来的 `file-to-markdown` 文件夹。

#### 卸载

直接把 `file-to-markdown` 文件夹删掉即可：

```bash
# macOS / Linux
rm -rf ~/.codex/skills/file-to-markdown
```

```powershell
# Windows PowerShell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

### 快速开始

```bash
python scripts/convert_to_markdown.py 待转换文件.pdf \
  --url http://<接口地址>/api/charts/generata/ \
  --token <你的 key>
```

默认输出到 `原文件名_markdown/`，也可以用 `-o` 指定目录。

### 配置接口地址和 key

接口地址和 key **不内置在 skill 里**，需要通过微信获取：

- 微信号：`smkynet`
- 添加时请写：**转markdown**

拿到后可以用命令行参数（`--url`、`--token`），或环境变量
`CONVERT_MARKDOWN_URL`、`CONVERT_MARKDOWN_TOKEN` 传入，命令行参数优先。

---

## English

A small tool that turns **PDFs, Office documents, and images** into Markdown in
one step.

Repository:

- GitHub: <https://github.com/trampzz/anything2markdown>
- Gitee: <https://gitee.com/zq-168/anything2markdown>

> The repository is named `anything2markdown` while the skill is named
> `file-to-markdown`. They are the same thing: the repo is
> `anything2markdown`, and once installed the skill folder is `file-to-markdown`
> so you can reference it as `$file-to-markdown`.

It uploads your file to a remote conversion service, which picks the right
handler by file extension:

| Uploaded file | Conversion |
| --- | --- |
| `.pdf` | Text extraction for normal PDFs; automatic OCR when the whole document is scanned |
| `.doc` `.docx` `.ppt` `.pptx` `.xls` `.xlsx` | Office document conversion |
| `.bmp` `.jpeg` `.jpg` `.png` `.tif` `.tiff` `.webp` | OCR |

One file per request. Mixing different file types is rejected.

### Features

- **Scanned documents supported** — OCR only kicks in when the entire document
  is scanned, so normal PDFs stay fast.
- **Images included** — pictures referenced by the Markdown are returned in an
  `image/` folder, ready to use.
- **Dependency-free script** — the client uses only the Python standard library
  and runs on older systems such as CentOS 7.
- **Metered access** — the API is billed per call through a key, and returns a
  clear status code when the quota runs out.

### Installation

This skill is just a folder (the key file is `SKILL.md`), so **installing it
means dropping the whole folder into your skills directory**. Below are both
download sources (GitHub / Gitee) and both methods (git clone / ZIP).

#### Prerequisites

- `git` — only needed for the clone method. Skip it if you download the ZIP.
- `Python 3.8+` — needed to run the bundled script. The script uses only the
  standard library, so **no `pip install` is required** and it runs fine on
  older systems such as CentOS 7.

#### Shortcut: one command, or let your agent do it

If you just want it installed quickly, cloning into the skills directory is a
single command:

```bash
# macOS / Linux (Codex, global)
mkdir -p ~/.codex/skills && \
  git clone --depth 1 https://github.com/trampzz/anything2markdown.git \
  ~/.codex/skills/file-to-markdown
```

```powershell
# Windows PowerShell (Codex, global)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone --depth 1 https://github.com/trampzz/anything2markdown.git "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

For Gitee, swap the host for `gitee.com/zq-168`; for Claude Code,
swap `.codex` for `.claude`.

**Let your AI assistant install it**: open a new chat in Codex / Claude Code and
paste this prompt. The agent will download, place, and verify everything for you.

```text
Please install the file-to-markdown skill for me:
1. Clone https://github.com/trampzz/anything2markdown (if it is unreachable, use Gitee: https://gitee.com/zq-168/anything2markdown)
2. Put it in ~/.codex/skills/file-to-markdown/ for Codex; if I am using Claude Code, use ~/.claude/skills/file-to-markdown/
3. Make sure SKILL.md sits directly inside the file-to-markdown folder, with no extra nesting
4. Run python scripts/convert_to_markdown.py --help to verify it starts, and report the result back to me
```

In Codex, if the skill installer is available, this one line is enough:

```text
Use $skill-installer to install https://github.com/trampzz/anything2markdown
```

Steps 1-4 below cover the full manual path; use whichever you prefer.

#### Step 1: Download

Clone:

```bash
# GitHub
git clone https://github.com/trampzz/anything2markdown.git

# Gitee
git clone https://gitee.com/zq-168/anything2markdown.git
```

Or download a ZIP:

- GitHub: repo page → `Code` → `Download ZIP`
- Gitee: repo page → `克隆/下载` → `下载 ZIP`

You will get a `file-to-markdown` folder either way.

#### Step 2: Put it in your skills directory

Pick the directory that matches your tool. On Windows, `~` is
`C:\Users\<your-name>`.

| Use case | Install directory |
| --- | --- |
| Codex (global) | `~/.codex/skills/file-to-markdown/` |
| Claude Code (global) | `~/.claude/skills/file-to-markdown/` |
| Single project only | `<project>/.codex/skills/file-to-markdown/` or `<project>/.claude/skills/file-to-markdown/` |

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/trampzz/anything2markdown.git \
  ~/.codex/skills/file-to-markdown
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/trampzz/anything2markdown.git `
  "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

Windows CMD:

```cmd
mkdir "%USERPROFILE%\.codex\skills"
git clone https://github.com/trampzz/anything2markdown.git "%USERPROFILE%\.codex\skills\file-to-markdown"
```

For the ZIP method, copy the extracted `file-to-markdown` folder into the skills
directory. For Claude Code or a project-level install, swap `.codex` for
`.claude` or use the project path.

#### Step 3: Check the layout

The structure should look like this, with `SKILL.md` **directly** inside
`file-to-markdown`:

```text
file-to-markdown/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── convert_to_markdown.py
```

A common mistake is an extra nested folder, e.g.
`skills/file-to-markdown/file-to-markdown/SKILL.md`. In that case move the
**inner** folder up so there is only one `file-to-markdown` level.

#### Step 4: Restart and verify

Restart or refresh Codex / Claude Code so it rescans the skills directory, then
run the script to confirm it starts:

```bash
python ~/.codex/skills/file-to-markdown/scripts/convert_to_markdown.py --help
```

If it prints the argument help, the files are in place. The endpoint and key are
still missing at this point — see "Configure the endpoint and key" below before
your first real conversion.

#### Updating

For a clone install:

```bash
cd ~/.codex/skills/file-to-markdown
git pull
```

For a ZIP install, download the latest ZIP and overwrite the folder.

#### Uninstall

Just delete the `file-to-markdown` folder:

```bash
# macOS / Linux
rm -rf ~/.codex/skills/file-to-markdown
```

```powershell
# Windows PowerShell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\file-to-markdown"
```

### Quick start

```bash
python scripts/convert_to_markdown.py report.pdf \
  --url http://<your-endpoint>/api/charts/generata/ \
  --token <your-key>
```

Output goes to `report_markdown/` by default; use `-o` to change it.

### Configure the endpoint and key

The endpoint and key are **not bundled with this skill**. Get them via WeChat:

- WeChat ID: `smkynet`
- When adding, please write: **转markdown**

Then pass them with `--url` / `--token`, or via the `CONVERT_MARKDOWN_URL` and
`CONVERT_MARKDOWN_TOKEN` environment variables. Command-line arguments win.

### API

```text
POST <endpoint>/api/charts/generata/
Headers: token: <your-key>, Content-Type: multipart/form-data
Form field: file
Returns: application/zip  ->  <name>.md + image/
```

Status codes: `401` invalid or missing key, `409` quota exhausted, `413` file
too large, `502` gateway could not reach the converter, `503` converter could
not reach its database. Do not retry on `401` or `409`.

---

## License

Add your preferred license here.
