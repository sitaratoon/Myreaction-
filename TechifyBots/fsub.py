import random
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import AUTH_CHANNELS, PICS

# ------------------ FSUB Check Function ------------------

async def get_fsub(bot: Client, message: Message) -> bool:
    user_id = message.from_user.id
    FSUB_IMAGE = random.choice(PICS) if PICS else None
    not_joined_channels = []

    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            chat = await bot.get_chat(channel_id)
            inv = await bot.create_chat_invite_link(channel_id, creates_join_request=True)
            not_joined_channels.append((chat.title, inv.invite_link))

    if not_joined_channels:
        join_buttons = [[InlineKeyboardButton(title, url=link)] for title, link in not_joined_channels]
        join_buttons.append([InlineKeyboardButton("🔄 Try Again", callback_data="fsub_check")])

        caption = (
            f"**🫡 {message.from_user.mention}, You must join all channels first!**\n\n"
            "**👇 Pehle channels join karo, phir Try Again dabao.**"
        )

        if FSUB_IMAGE:
            await message.reply_photo(FSUB_IMAGE, caption=caption, reply_markup=InlineKeyboardMarkup(join_buttons))
        else:
            await message.reply(caption, reply_markup=InlineKeyboardMarkup(join_buttons))

        return False

    return True

# ------------------ FSUB Callback Handler ------------------

async def fsub_callback(bot: Client, query: CallbackQuery):
    user_id = query.from_user.id
    not_joined = False

    for channel_id in AUTH_CHANNELS:
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            not_joined = True
            break

    if not_joined:
        await query.answer("❗ Still not approved or not joined!", show_alert=True)
        return

    await query.answer("✅ You are verified!", show_alert=True)
    await query.message.delete()

    # Trigger /start command automatically
    await query.message.chat.send_message("/start")
