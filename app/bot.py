from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message
from openai import APIConnectionError, APIStatusError, RateLimitError

from app.config import Settings
from app.llm import AmeLLM


logger = logging.getLogger(__name__)
router = Router()
TELEGRAM_MESSAGE_LIMIT = 4096


def split_message(text: str, limit: int = TELEGRAM_MESSAGE_LIMIT) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break
        split_at = remaining.rfind("\n", 0, limit + 1)
        if split_at < limit // 2:
            split_at = remaining.rfind(" ", 0, limit + 1)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    return chunks


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "м\nтехнически теперь да\n\nпиши что-нибудь. посмотрим, зачем ты меня сюда поселил"
    )


@router.message(F.text)
async def handle_text(message: Message, ame: AmeLLM) -> None:
    text = (message.text or "").strip()
    if not text:
        return

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    try:
        answer = await ame.reply(text)
    except RateLimitError:
        logger.warning("OpenAI rate limit reached", exc_info=True)
        await message.answer("м\nу меня сейчас лимиты решили устроить забастовку\nпопробуй чуть позже")
        return
    except APIConnectionError:
        logger.warning("Could not connect to OpenAI", exc_info=True)
        await message.answer("я сейчас не могу достучаться до мозга в облаке\nочень символично\nпопробуй ещё раз")
        return
    except APIStatusError:
        logger.exception("OpenAI returned an API error")
        await message.answer("что-то сломалось на стороне модели\nя уже осуждающе смотрю в логи")
        return
    except Exception:
        logger.exception("Unexpected error while generating a reply")
        await message.answer("так\nэто было не по плану\nя упала в ошибку, попробуй ещё раз")
        return

    for chunk in split_message(answer):
        await message.answer(chunk)


@router.message()
async def handle_unsupported(message: Message) -> None:
    await message.answer("я пока понимаю только текст\nда, версия буквально ноль-ноль-один")


async def run_bot(settings: Settings) -> None:
    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    ame = AmeLLM(
        api_key=settings.openai_api_key,
        model=settings.llm_model,
        personality_path=settings.personality_path,
    )

    try:
        await bot.delete_webhook(drop_pending_updates=False)
        await dispatcher.start_polling(bot, ame=ame)
    finally:
        try:
            await ame.close()
        finally:
            await bot.session.close()
