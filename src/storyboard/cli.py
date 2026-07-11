"""命令行入口。"""
import argparse
import sys

from .generator import StoryboardGenerator
from .exporters import to_markdown, to_csv, to_json


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="storyboard",
        description="AI 分镜脚本优化师：把剧本/故事转化为结构化、可拍摄的分镜脚本",
    )
    p.add_argument("input", help="输入脚本文件路径，或传入 '-' 表示从 stdin 读取")
    p.add_argument("-o", "--output", help="输出文件路径（默认打印到 stdout）")
    p.add_argument(
        "-f",
        "--format",
        choices=["md", "csv", "json"],
        default="md",
        help="输出格式，默认 md",
    )
    p.add_argument("-t", "--title", default="", help="作品标题")
    p.add_argument("-s", "--style", default="电影感写实", help="整体视觉风格")
    p.add_argument("--platform", default="通用", help="发布平台/用途")
    p.add_argument("--duration", default="", help="总时长目标，如 60s")
    p.add_argument("--notes", default="", help="额外要求")
    p.add_argument(
        "--api-key",
        default=None,
        help="OpenAI 兼容 API Key（也可设环境变量 OPENAI_API_KEY）",
    )
    p.add_argument(
        "--base-url",
        default=None,
        help="OpenAI 兼容 Base URL（环境变量 OPENAI_BASE_URL）",
    )
    p.add_argument(
        "--model", default=None, help="模型名（环境变量 OPENAI_MODEL）"
    )
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.input == "-":
        script = sys.stdin.read()
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            script = f.read()

    gen = StoryboardGenerator(
        api_key=args.api_key, base_url=args.base_url, model=args.model
    )
    if not gen.is_ai_enabled:
        print(
            "[提示] 未检测到 OPENAI_API_KEY，使用启发式降级模式（仅生成结构骨架）。"
            "设置 API Key 可启用完整 AI 优化。",
            file=sys.stderr,
        )

    sb = gen.generate(
        script,
        title=args.title,
        style=args.style,
        platform=args.platform,
        duration_total=args.duration,
        notes=args.notes,
    )

    if args.format == "json":
        out = to_json(sb)
    elif args.format == "csv":
        out = to_csv(sb)
    else:
        out = to_markdown(sb)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入 {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
