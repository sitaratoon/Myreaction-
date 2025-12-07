import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNELS, PICS
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

async def get_fsub(bot: Client, message: Message) -> bool:
    tb = await bot.get_me()
    user_id = message.from_user.id

    # PICS se image select
    FSUB_IMAGE = random.choice(PICS) if PICS else None

    not_joined_channels = []

    # CHECK MEMBERSHIP
    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)

        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)

            # ✅ JOIN-REQUEST INVITE LINK (CORRECT!)
            inv = await bot.create_chat_invite_link(
                channel_id,
                creates_join_request=True
            )
            invite_link = inv.invite_link

            not_joined_channels.append((chat.title, invite_link))

    # IF NOT JOINED ANY CHANNEL
    if not_joined_channels:

        join_buttons = []

        # 2 buttons per row
        for i in range(0, len(not_joined_channels), 2):
            row = []
            for j in range(2):
                if i + j < len(not_joined_channels):
                    title, link = not_joined_channels[i + j]
                    row.append(InlineKeyboardButton(title, url=link))
            join_buttons.append(row)

        # Try Again button
        join_buttons.append([
            InlineKeyboardButton("🔄 Try Again", callback_data="check_fsub")
        ])

        # SEND IMAGE MESSAGE
        if FSUB_IMAGE:
            await message.reply_photo(
                photo=FSUB_IMAGE,
                caption=(
                    f"**🎭 {message.from_user.mention}, You must join all channels first!**\n\n"
                    "**👇 Join all channels to continue your request.**"
                ),
                reply_markup=InlineKeyboardMarkup(join_buttons)
            )
        else:
            await message.reply(
                f"**🎭 {message.from_user.mention}, You must join all required channels!**",
                reply_markup=InlineKeyboardMarkup(join_buttons)
            )

        return False

    return True
