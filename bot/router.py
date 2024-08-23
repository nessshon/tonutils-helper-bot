import hashlib

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton, Message, )
from aiogram.utils.markdown import hpre, hbold, hlink, hide_link

from .content import ContentManager

router = Router()


async def create_article(cm: ContentManager, section: str, operation: str, link: str) -> InlineQueryResultArticle:
    message_text = (
        f"{hlink('Tonutils', 'https://github.com/nessshon/tonutils')}\n\n"
        f"🏷 {hbold(operation)}\n"
        f"{section}\n\n"
        f"📦 {hbold('Installation:')}\n"
        "Install the required library using pip:\n"
        f"{hpre('pip install tonutils')}\n\n"
        f"📋 {hbold('Code example:')}\n"
        "Replace the constants with your own:\n"
        f"{hpre(await cm.read_file(link))}"
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Open in GitHub",
                    url="https://github.com/nessshon/tonutils/blob/main/" + link
                )
            ]
        ]
    )
    return InlineQueryResultArticle(
        id=hashlib.sha256(f"{operation}{section}{link}".encode()).hexdigest(),
        title=operation,
        description=section,
        thumbnail_url="https://telegra.ph//file/063ee61e097ee8281b9d3.jpg",
        input_message_content=InputTextMessageContent(
            message_text=message_text,
            disable_web_page_preview=True,
        ),
        reply_markup=reply_markup,
    )


@router.inline_query()
async def search(inline: InlineQuery) -> None:
    items_per_page = 20
    offset = int(inline.offset) if inline.offset else 0

    cm = ContentManager()
    items = await cm.search_items(inline.query)

    if any(items):
        results = []

        for section, operation, link in items[offset:offset + items_per_page]:
            result = await create_article(cm, section, operation, link)
            results.append(result)

        next_offset = str(offset + items_per_page)
        await inline.answer(results=results, next_offset=next_offset, is_personal=False, cache_time=600)


@router.message(Command("start"))
async def start(message: Message) -> None:
    text = (
        f"{hide_link('https://telegra.ph//file/068ea06087c9ce8c6bfed.jpg')}"
        f"👋 Hello, {hbold(message.from_user.full_name)}! "
        f"I'm the {hlink('Tonutils', 'https://github.com/nessshon/tonutils')} helper bot.\n\n"
        "I can assist you in finding code examples on Python for various operations related to the TON blockchain.\n\n"
        "• To get started, simply use inline mode and search for the operations you're interested in."
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔎 Search",
                    switch_inline_query_current_chat=""
                )
            ]
        ]
    )
    await message.answer(text, reply_markup=reply_markup)
