from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PERSONALITY_PATH = PROJECT_ROOT / "personality" / "ame.md"


@dataclass(frozen=True, slots=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str
    llm_model: str
    personality_path: Path


def load_settings(env_file: Path | None = None) -> Settings:
    load_dotenv(dotenv_path=env_file or PROJECT_ROOT / ".env")

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    llm_model = os.getenv("LLM_MODEL", "gpt-5.4-mini").strip()
    personality_value = os.getenv("PERSONALITY_PATH", "").strip()
    personality_path = (
        Path(personality_value).expanduser()
        if personality_value
        else DEFAULT_PERSONALITY_PATH
    )

    missing = [
        name
        for name, value in (
            ("TELEGRAM_BOT_TOKEN", telegram_bot_token),
            ("OPENAI_API_KEY", openai_api_key),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Не заданы обязательные переменные: {', '.join(missing)}. "
            "Скопируйте .env.example в .env и вставьте ключи."
        )
    if not personality_path.is_file():
        raise RuntimeError(f"Файл личности Аме не найден: {personality_path}")

    return Settings(
        telegram_bot_token=telegram_bot_token,
        openai_api_key=openai_api_key,
        llm_model=llm_model,
        personality_path=personality_path,
    )
