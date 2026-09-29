#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upload one local file to the remote conversion API and unpack the zip.

Only relies on the Python standard library, so it runs on a bare Python 3
install (including CentOS 7 with its old glibc).

接口地址和 token 都必须由调用方提供，脚本内不内置任何默认地址或密钥。
地址和 token 可以通过微信 smkynet 获取（添加时请写：转markdown）。

Examples:
    python convert_to_markdown.py report.pdf --url http://<接口地址>/api/charts/generata/ --token <token>
    python convert_to_markdown.py scan.png -o ./out --url <接口地址> --token <token>
    # 也可以用环境变量 CONVERT_MARKDOWN_URL / CONVERT_MARKDOWN_TOKEN 代替
    python convert_to_markdown.py doc.docx
"""

from __future__ import annotations

import argparse
import io
import os
import sys
import uuid
import zipfile
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

DEFAULT_TIMEOUT = 300.0


def build_multipart(file_path: Path, extra_fields):
    """Build a multipart/form-data body and its Content-Type header value."""
    boundary = "----CodexFileToMarkdown" + uuid.uuid4().hex
    buf = io.BytesIO()

    def write_field(name, value):
        buf.write(("--%s\r\n" % boundary).encode("utf-8"))
        buf.write(
            ('Content-Disposition: form-data; name="%s"\r\n\r\n' % name).encode(
                "utf-8"
            )
        )
        buf.write(str(value).encode("utf-8"))
        buf.write(b"\r\n")

    for name, value in (extra_fields or {}).items():
        write_field(name, value)

    data = file_path.read_bytes()
    buf.write(("--%s\r\n" % boundary).encode("utf-8"))
    buf.write(
        (
            'Content-Disposition: form-data; name="file"; filename="%s"\r\n'
            % file_path.name
        ).encode("utf-8")
    )
    buf.write(b"Content-Type: application/octet-stream\r\n\r\n")
    buf.write(data)
    buf.write(b"\r\n")
    buf.write(("--%s--\r\n" % boundary).encode("utf-8"))

    content_type = "multipart/form-data; boundary=%s" % boundary
    return buf.getvalue(), content_type


def describe_http_error(code: int, body: bytes) -> str:
    text = body.decode("utf-8", "replace").strip()
    detail = (" 服务端返回：" + text) if text else ""
    mapping = {
        401: "token 缺失、无效、已禁用或已过期（401），不会重试。请检查 --token 或 CONVERT_MARKDOWN_TOKEN。",
        409: "token 剩余次数已用光（409），不会重试。请更换或充值 token。",
        413: "文件超过服务端大小上限（413）。请压缩或拆分后重试。",
        502: "网关没能连上转换服务（502）。请稍后重试。",
        503: "转换服务连不上它的数据库（503）。请稍后重试。",
    }
    return mapping.get(code, "请求失败，HTTP 状态码 %d。" % code) + detail


def safe_extract(zip_path: Path, dest: Path):
    dest = dest.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            target = (dest / member).resolve()
            if not str(target).startswith(str(dest)):
                raise RuntimeError("zip 内含不安全的路径：%s" % member)
        zf.extractall(dest)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="调用远程接口，把 PDF / Office 文档 / 图片转成 Markdown。"
    )
    parser.add_argument("file", help="要转换的本地文件")
    parser.add_argument("-o", "--output-dir", help="解压输出目录，默认 <文件名>_markdown")
    parser.add_argument(
        "--url",
        help="接口地址（必填）。也可用环境变量 CONVERT_MARKDOWN_URL；"
        "地址可通过微信 smkynet 获取，添加时请写：转markdown",
    )
    parser.add_argument("--token", help="token，覆盖环境变量 CONVERT_MARKDOWN_TOKEN")
    parser.add_argument(
        "--form-token",
        action="store_true",
        help="把 token 放进表单字段而不是请求头（用于不转发请求头的旧版本服务端）",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="读取超时秒数，默认 300",
    )
    args = parser.parse_args(argv)

    file_path = Path(args.file).expanduser()
    if not file_path.is_file():
        print("找不到文件：%s" % file_path, file=sys.stderr)
        return 2

    url = args.url or os.environ.get("CONVERT_MARKDOWN_URL")
    if not url:
        print(
            "缺少接口地址：请用 --url 传入，或设置环境变量 CONVERT_MARKDOWN_URL。\n"
            "接口地址可通过微信 smkynet 获取（添加时请写：转markdown）。",
            file=sys.stderr,
        )
        return 2

    token = args.token or os.environ.get("CONVERT_MARKDOWN_TOKEN")
    if not token:
        print(
            "缺少 token：请用 --token 传入，或设置环境变量 CONVERT_MARKDOWN_TOKEN。\n"
            "token 可通过微信 smkynet 获取（添加时请写：转markdown）。",
            file=sys.stderr,
        )
        return 2

    extra_fields = {"token": token} if args.form_token else None
    body, content_type = build_multipart(file_path, extra_fields)

    headers = {"Content-Type": content_type}
    if not args.form_token:
        headers["token"] = token

    req = urlrequest.Request(url, data=body, headers=headers, method="POST")

    try:
        with urlrequest.urlopen(req, timeout=args.timeout) as resp:
            status = resp.status
            resp_content_type = resp.headers.get("Content-Type", "")
            payload = resp.read()
    except HTTPError as exc:
        try:
            body_bytes = exc.read()
        except Exception:
            body_bytes = b""
        print(describe_http_error(exc.code, body_bytes), file=sys.stderr)
        return 1
    except URLError as exc:
        print("无法连接转换接口：%s" % exc.reason, file=sys.stderr)
        return 1

    if status != 200:
        print("请求失败，HTTP 状态码 %d。" % status, file=sys.stderr)
        return 1

    if "zip" not in resp_content_type.lower():
        print(
            "服务端没有返回 zip（Content-Type=%s）。请确认上传的是受支持的 PDF、Office 文档或图片。"
            % (resp_content_type or "空"),
            file=sys.stderr,
        )
        return 1

    output_dir = (
        Path(args.output_dir).expanduser()
        if args.output_dir
        else file_path.with_name(file_path.stem + "_markdown")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / (file_path.stem + ".zip")
    zip_path.write_bytes(payload)
    safe_extract(zip_path, output_dir)

    md_files = sorted(output_dir.rglob("*.md"))
    image_dir = output_dir / "image"
    image_count = (
        sum(1 for p in image_dir.rglob("*") if p.is_file()) if image_dir.is_dir() else 0
    )

    if md_files:
        print("转换完成。")
        for md in md_files:
            print("Markdown：%s" % md)
    else:
        print("zip 已解压到 %s，但没有找到 .md 文件。" % output_dir)
    print("图片数量：%d" % image_count)
    print("输出目录：%s" % output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
