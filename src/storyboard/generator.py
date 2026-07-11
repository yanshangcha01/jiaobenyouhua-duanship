"""分镜脚本生成核心逻辑（支持 LLM 与启发式降级）。"""
import json
import os
import re
from typing import Optional

from .models import Shot, Storyboard
from .prompts import SYSTEM_PROMPT, build_user_prompt


class StoryboardGenerator:
    """将剧本/故事描述转化为结构化分镜脚本。

    优先调用 OpenAI 兼容大模型；未配置 API Key 时降级为启发式结构骨架生成。
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = (
            base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = model or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
        self.timeout = timeout

    @property
    def is_ai_enabled(self) -> bool:
        return bool(self.api_key)

    def generate(self, script: str, **kwargs) -> Storyboard:
        if self.is_ai_enabled:
            try:
                return self._generate_with_llm(script, **kwargs)
            except Exception:
                # 任何调用异常都安全降级，不阻断交付
                sb = self._generate_heuristic(script, **kwargs)
                sb.heuristic = True
                return sb
        return self._generate_heuristic(script, **kwargs)

    def _generate_with_llm(self, script: str, **kwargs) -> Storyboard:
        import requests  # 延迟导入，未用 AI 时不依赖网络库

        user_prompt = build_user_prompt(script, **kwargs)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(self._extract_json(content))
        return self._parse_storyboard(data)

    @staticmethod
    def _extract_json(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            text = text[s : e + 1]
        return text.strip()

    @staticmethod
    def _parse_storyboard(data: dict) -> Storyboard:
        title = data.get("title") or "未命名分镜"
        shots: list[Shot] = []
        for i, raw in enumerate(data.get("shots", []), start=1):
            shots.append(
                Shot(
                    index=int(raw.get("index", i)),
                    duration=str(raw.get("duration", "") or ""),
                    shot_size=str(raw.get("shot_size", "") or ""),
                    camera_movement=str(raw.get("camera_movement", "") or ""),
                    visual_description=str(raw.get("visual_description", "") or ""),
                    dialogue=str(raw.get("dialogue", "") or ""),
                    audio=str(raw.get("audio", "") or ""),
                    transition=str(raw.get("transition", "") or ""),
                    notes=str(raw.get("notes", "") or ""),
                    image_prompt=str(raw.get("image_prompt", "") or ""),
                )
            )
        return Storyboard(title=title, shots=shots)

    def _generate_heuristic(self, script: str, **kwargs) -> Storyboard:
        """无 API Key 时的启发式降级：按段落切分并生成结构骨架。"""
        title = kwargs.get("title") or "未命名分镜（启发式模式，未接入AI）"
        blocks = [b.strip() for b in re.split(r"\n\s*\n", script) if b.strip()]
        if not blocks:
            blocks = [script.strip()]
        shots: list[Shot] = []
        for i, block in enumerate(blocks, start=1):
            first_line = block.split("\n", 1)[0][:40]
            shots.append(
                Shot(
                    index=i,
                    duration="",
                    shot_size="",
                    camera_movement="",
                    visual_description=block[:200],
                    dialogue="",
                    audio="",
                    transition="",
                    notes="启发式模式：接入 AI 后重新生成可获得完整分镜与绘图提示词",
                    image_prompt=f"Cinematic storyboard frame, {first_line}, detailed, film lighting",
                )
            )
        return Storyboard(title=title, shots=shots, heuristic=True)
