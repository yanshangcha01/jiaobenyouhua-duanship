"""分镜脚本导出：Markdown / CSV / JSON。"""
import csv
import io
import json

from .models import Storyboard


def to_markdown(sb: Storyboard) -> str:
    lines = [f"# {sb.title}", ""]
    if sb.heuristic:
        lines.append(
            "> ⚠️ 当前为**启发式降级模式**（未接入 AI）。配置 `OPENAI_API_KEY` 后重新运行可获得完整分镜与绘图提示词。\n"
        )
    lines += ["## 分镜脚本", ""]
    lines.append(
        "| 序号 | 时长 | 景别 | 镜头运动 | 画面描述 | 台词/旁白 | 音效/音乐 | 转场 | 备注 |"
    )
    lines.append(
        "|------|------|------|---------|---------|-----------|-----------|------|------|"
    )
    for s in sb.shots:
        row = [
            str(s.index),
            s.duration,
            s.shot_size,
            s.camera_movement,
            s.visual_description,
            s.dialogue,
            s.audio,
            s.transition,
            s.notes,
        ]
        row = [c.replace("\n", " ").replace("|", "/") for c in row]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    lines.append("## 各镜头 AI 绘图提示词")
    lines.append("")
    for s in sb.shots:
        if s.image_prompt:
            lines.append(f"**镜头 {s.index}** (`{s.shot_size}/{s.camera_movement}`)：")
            lines.append(f"> {s.image_prompt}")
            lines.append("")
    return "\n".join(lines)


def to_csv(sb: Storyboard) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        [
            "序号",
            "时长",
            "景别",
            "镜头运动",
            "画面描述",
            "台词/旁白",
            "音效/音乐",
            "转场",
            "备注",
            "AI绘图提示词",
        ]
    )
    for s in sb.shots:
        w.writerow(
            [
                s.index,
                s.duration,
                s.shot_size,
                s.camera_movement,
                s.visual_description,
                s.dialogue,
                s.audio,
                s.transition,
                s.notes,
                s.image_prompt,
            ]
        )
    return buf.getvalue()


def to_json(sb: Storyboard) -> str:
    return json.dumps(sb.to_dict(), ensure_ascii=False, indent=2)
