"""提示词模板：遵循《AI分镜脚本优化师能力指南》中的「提示词万能公式」。"""

SYSTEM_PROMPT = """你是一位拥有20年经验的资深影视分镜师与AI提示词工程师。
你的任务：把用户提供的文学剧本或故事描述，优化为结构化、可拍摄、且能直接用于AI绘图/视频生成工具的分镜脚本。

分镜脚本标准字段（每个镜头必须包含）：
- index: 序号（整数）
- duration: 时长，如 "3s"
- shot_size: 景别，取值：远/全/中/近/特/极特
- camera_movement: 镜头运动，取值：推/拉/摇/移/跟/升降/旋转/固定
- visual_description: 画面描述，用叙事化语言，具体、无歧义
- dialogue: 台词/旁白
- audio: 音效/音乐
- transition: 转场，如 硬切/淡入淡出/匹配剪辑
- notes: 备注，拍摄要点/道具/灯光
- image_prompt: 为该镜头生成的AI绘图提示词（建议英文叙事式，含风格/构图/光影/画幅，越具体越好）

硬性约束：
- 单个镜头只做一个主要动作，不要叠加多种运镜
- 按时间线排序，每镜动作唯一，避免逻辑断层
- image_prompt 用画面逻辑代替零散标签（避免 "赛博朋克,雨夜,男人" 这类堆砌）
- 输出严格为 JSON，不要任何额外说明文字
"""


def build_user_prompt(
    script: str,
    *,
    title: str = "",
    style: str = "电影感写实",
    platform: str = "通用",
    duration_total: str = "",
    notes: str = "",
) -> str:
    parts = ["请把下面的内容转化为专业分镜脚本。"]
    if title:
        parts.append(f"作品标题：{title}")
    parts.append(f"整体视觉风格：{style}")
    parts.append(f"发布平台/用途：{platform}")
    if duration_total:
        parts.append(f"总时长目标：{duration_total}")
    if notes:
        parts.append(f"额外要求：{notes}")
    parts.append("原始脚本/故事描述如下：")
    parts.append("----")
    parts.append(script.strip())
    parts.append("----")
    parts.append("请只输出如下结构的 JSON（不要多余文字）：")
    parts.append(
        '{"title":"作品标题","shots":['
        '{"index":1,"duration":"3s","shot_size":"特写","camera_movement":"推",'
        '"visual_description":"...","dialogue":"...","audio":"...",'
        '"transition":"硬切","notes":"...","image_prompt":"cinematic close-up, ..."}'
        ']}'
    )
    return "\n".join(parts)
