"""基础可用性测试：无需 API Key 也能跑通核心流程。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from storyboard.generator import StoryboardGenerator
from storyboard.exporters import to_markdown, to_csv, to_json


def test_heuristic_runs():
    gen = StoryboardGenerator()  # 无 Key -> 启发式
    sb = gen.generate(
        "夜色中，侦探走进酒吧。\n\n他点了一杯威士忌，环顾四周。",
        title="雨夜侦探",
    )
    assert len(sb.shots) == 2
    assert sb.heuristic is True


def test_exporters():
    gen = StoryboardGenerator()
    sb = gen.generate("场景一。\n\n场景二。")
    md = to_markdown(sb)
    assert "分镜脚本" in md
    csv_text = to_csv(sb)
    assert "序号" in csv_text
    js = to_json(sb)
    assert "shots" in js


if __name__ == "__main__":
    test_heuristic_runs()
    test_exporters()
    print("All tests passed.")
