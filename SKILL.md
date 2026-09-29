---
name: file-to-markdown
description: Convert one local PDF, Office document, or image into Markdown by uploading it to the remote conversion API and unpacking the returned zip. Use when the user wants a PDF, scanned document, Word/PPT/Excel file, or photo turned into Markdown text or extracted text.
metadata:
  short-description: 调用远程接口，把 PDF、Office 文档、图片转成 Markdown
---

# File to Markdown

把本地的一个文件发给转换接口，拿回一个 zip，解压后是 `.md` 文件加一个
`image/` 图片目录。

## 先配置接口地址和 key

使用前必须先准备好**接口地址**和**key（token）**，两者都不内置在 skill 里，
也不会随 skill 一起分发。地址和 key 需要通过微信获取：

- 微信号：`smkynet`
- 添加时请写：**转markdown**

拿到之后按下面两种方式之一配置，命令行参数优先于环境变量：

| 配置项 | 命令行参数 | 环境变量 |
| --- | --- | --- |
| 接口地址 | `--url` | `CONVERT_MARKDOWN_URL` |
| key（token） | `--token` | `CONVERT_MARKDOWN_TOKEN` |

接口地址是服务的统一入口，填到 `/api/charts/generata/` 这一层，例如：

```text
http://<接口地址>/api/charts/generata/
```

脚本和示例里的地址都是占位符，运行前请替换成你自己拿到的真实地址。没有拿到
地址或 key 时，先向用户确认，不要凭空编造一个。

## 接口

```text
POST <接口地址>/api/charts/generata/
```

这是统一入口，服务端按文件后缀自动选择转换方式：

| 上传的文件 | 转换方式 |
| --- | --- |
| `.pdf` | 正常 PDF 走文本抽取；整篇都是扫描件时自动走 OCR |
| `.doc` `.docx` `.ppt` `.pptx` `.xls` `.xlsx` | Office 文档转换 |
| `.bmp` `.jpeg` `.jpg` `.png` `.tif` `.tiff` `.webp` | OCR 识别 |

一次请求只传一个文件。混传不同类型的文件会被拒绝（400）。

## 请求格式

- 方法：`POST`
- 请求头 `token`：必填，换成调用方自己的 token
- 请求头 `Content-Type`：`multipart/form-data`，并且必须带 boundary。
  用脚本或 requests、curl 这类客户端时一般由它们自动拼好，不要手写一个
  没有 boundary 的值
- 表单字段 `file`：要转换的文件

curl 形式：

```bash
curl -X POST "$CONVERT_MARKDOWN_URL" \
  -H "token: $CONVERT_MARKDOWN_TOKEN" \
  -F "file=@待转换文件.pdf" \
  -o result.zip
```

## token 配置

token 是计次收费的，**不要写死在文件里，也不要提交到仓库**。运行时按下面
顺序取，取不到就问用户要（微信 `smkynet`，添加时写“转markdown”），不要凭空编一个：

1. 命令行参数 `--token`
2. 环境变量 `CONVERT_MARKDOWN_TOKEN`

如果服务端还是旧版本（没有透传请求头），token 也可以放进表单字段 `token`
里，脚本用 `--form-token` 打开这个方式。

接口地址同样按 `--url` → `CONVERT_MARKDOWN_URL` 的顺序取，取不到直接报错，
不会回退到任何内置地址。

## 返回

成功时 `200` 返回 `application/zip`，解压后结构如下：

```text
<原文件名>.md      转换出的 Markdown
image/             正文引用到的图片，没有图片时可能不存在
```

失败时返回 JSON，按状态码区分：

| 状态码 | 含义 |
| --- | --- |
| 401 | token 缺失、无效、已禁用或已过期 |
| 409 | token 次数用光 |
| 502 | 网关没能连上转换服务 |
| 503 | 转换服务连不上它的数据库 |

遇到 401 和 409 不要重试，直接把原因告诉用户。

## 怎么调用

优先用 `scripts/convert_to_markdown.py`，它只依赖 Python 标准库：

```bash
# 接口地址是必填参数，把 <接口地址> 换成自己拿到的地址
python scripts/convert_to_markdown.py 待转换文件.pdf --url http://<接口地址>/api/charts/generata/ --token <key>
python scripts/convert_to_markdown.py 待转换文件.pdf --url http://<接口地址>/api/charts/generata/ -o ./out --token <key>
```

`--url` 和 `--token` 也可以用环境变量 `CONVERT_MARKDOWN_URL`、
`CONVERT_MARKDOWN_TOKEN` 代替。两者都没有时脚本会直接报错，不会请求任何默认地址。

脚本会把 zip 存下来并解压到输出目录，最后打印出 Markdown 路径和图片数量。
默认输出目录是 `原文件名_markdown/`。

## 注意

- 扫描版 PDF 和图片要走 OCR，明显比普通文档慢，读取超时给足（接口最多
  允许 300 秒），不要因为慢就判定失败。
- 上传体积有上限，超限会返回 413。
- 图片在 Markdown 里是相对于 `image/` 目录引用的，移动文件时要连 `image/`
  一起移动。
