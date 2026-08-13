from __future__ import annotations

from pathlib import Path

from openai import AsyncOpenAI


class AmeLLM:
    def __init__(self, *, api_key: str, model: str, personality_path: Path) -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._personality = personality_path.read_text(encoding="utf-8").strip()
        if not self._personality:
            raise RuntimeError(f"Файл личности пуст: {personality_path}")

    async def reply(self, user_message: str) -> str:
        response = await self._client.responses.create(
            model=self._model,
            instructions=self._personality,
            input=user_message,
            reasoning={"effort": "none"},
            max_output_tokens=1200,
        )
        answer = response.output_text.strip()
        if not answer:
            raise RuntimeError("OpenAI вернул пустой ответ")
        return answer
