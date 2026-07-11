"""分镜数据结构定义。"""
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Shot:
    """单个镜头（分镜）。"""

    index: int
    duration: str = ""            # 时长，如 3s
    shot_size: str = ""           # 景别：远/全/中/近/特/极特
    camera_movement: str = ""     # 镜头运动：推/拉/摇/移/跟/升降/旋转/固定
    visual_description: str = ""  # 画面描述（叙事化、具体、无歧义）
    dialogue: str = ""            # 台词 / 旁白
    audio: str = ""               # 音效 / 音乐
    transition: str = ""          # 转场
    notes: str = ""               # 备注：拍摄要点 / 道具 / 灯光
    image_prompt: str = ""        # 为该镜头生成的 AI 绘图提示词

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Storyboard:
    """一整套分镜脚本。"""

    title: str
    shots: List[Shot] = field(default_factory=list)
    heuristic: bool = False  # 是否为启发式降级产物

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "heuristic": self.heuristic,
            "shots": [s.to_dict() for s in self.shots],
        }
