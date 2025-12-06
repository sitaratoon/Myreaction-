from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNELS
from pyrogram import Client
from pyrogram.types import Message
from typing import List
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden

async def get_fsub(bot: Client, message: Message) -> bool:
    tb = await bot.get_me()
    user_id = message.from_user.id
    not_joined_channels = []

    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)

        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)

            # Try getting invite link safely
            try:
                invite_link = chat.invite_link or await bot.export_chat_invite_link(channel_id)
            except ChatAdminRequired:
                invite_link = None  # Bot not admin
            except Exception:
                invite_link = None

            not_joined_channels.append((chat.title, invite_link))

    if not_joined_channels:
        join_buttons = []

        # Multi-channel 2-button rows
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    row.append(
                        InlineKeyboardButton(
                            f"{title}",
                            url=link if link else "https://t.me/"
                        )
                    )
            join_buttons.append(row)

        # Try Again button (better UX)
        join_buttons.append(
            [InlineKeyboardButton("🔄 Try Again", callback_data="check_fsub")]
        )

        try:
            await message.reply(
                f"**🎭 {message.from_user.mention}, You must join our channel(s) first.**",
                reply_markup=InlineKeyboardMarkup(join_buttons)
            )
        except ChatWriteForbidden:
            pass

        return False

    return True
