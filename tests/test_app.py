from pathlib import Path

import pytest

from app.bot import split_message
from app.config import load_settings


def test_split_message_keeps_every_chunk_within_telegram_limit() -> None:
    source = (("строка " * 800) + "\n") * 2

    chunks = split_message(source)

    assert len(chunks) > 1
    assert all(0 < len(chunk) <= 4096 for chunk in chunks)
    assert "".join(chunks).replace("\n", "").replace(" ", "") == source.replace(
        "\n", ""
    ).replace(" ", "")


def test_load_settings_reads_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "TELEGRAM_BOT_TOKEN=1234567890:test_token\n"
        "OPENAI_API_KEY=sk-test\n"
        "LLM_MODEL=gpt-5.4-mini\n",
        encoding="utf-8",
    )

    settings = load_settings(env_file)

    assert settings.telegram_bot_token == "1234567890:test_token"
    assert settings.openai_api_key == "sk-test"
    assert settings.llm_model == "gpt-5.4-mini"
    assert settings.personality_path.name == "ame.md"


def test_load_settings_rejects_missing_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("LLM_MODEL=gpt-5.4-mini\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN"):
        load_settings(env_file)
