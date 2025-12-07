from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNELS
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

FSUB_IMAGE = "https://graph.org/file/aba068bc8e3bdb42c4594-75a402e8d0fbb84e57.jpg"  # <-- Yaha apni image link daalna

async def get_fsub(bot: Client, message: Message) -> bool:
    tb = await bot.get_me()
    user_id = message.from_user.id
    not_joined_channels = []

    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)

        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)
            invite_link = chat.invite_link or await bot.export_chat_invite_link(channel_id)
            not_joined_channels.append((chat.title, invite_link))

    if not_joined_channels:
        
        join_buttons = []

        # 2 buttons per row
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    button_text = f"{title}"
                    row.append(InlineKeyboardButton(button_text, url=link))
            join_buttons.append(row)

        # Try Again Button
        join_buttons.append([
            InlineKeyboardButton("🔄 Try Again", callback_data="check_fsub")
        ])

        # Image + Caption
        await message.reply_photo(
            photo=FSUB_IMAGE,
            caption=(
                f"**🎭 {message.from_user.mention}, You must join all channels first!**\n\n"
                "**👇 Join all channels to continue your request.**"
            ),
            reply_markup=InlineKeyboardMarkup(join_buttons)
        )
        return False

    return True
