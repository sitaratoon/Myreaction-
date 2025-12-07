from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNELS, PICS      # ✅ PICS yaha import kiya!
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
import random


async def get_fsub(bot: Client, message: Message) -> bool:
    tb = await bot.get_me()
    user_id = message.from_user.id
    not_joined_channels = []

    # 🔍 Check user joined channels or not
    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)

        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)
            invite_link = chat.invite_link or await bot.export_chat_invite_link(channel_id)
            not_joined_channels.append((chat.title, invite_link))

    # ❗ If user NOT joined channels
    if not_joined_channels:

        join_buttons = []

        # 2-per-row layout
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    button_text = f"{i + j + 1}. {title}"
                    row.append(InlineKeyboardButton(button_text, url=link))
            join_buttons.append(row)

        # TRY AGAIN button → /start trigger
        join_buttons.append([
            InlineKeyboardButton(
                "🔄 Try Again",
                url=f"https://telegram.me/{tb.username}?start=start"
            )
        ])

        caption = (
            f"**🎭 {message.from_user.mention}, you haven’t joined required channels yet.**\n"
            f"**👇 Join channels first then press Try Again!**"
        )

        # 🔥 PHOTO SUPPORT from config.PICS
        if PICS:
            photo = random.choice(PICS)
            await message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(join_buttons)
            )
        else:
            await message.reply(
                caption,
                reply_markup=InlineKeyboardMarkup(join_buttons)
            )

        return False

    return True
