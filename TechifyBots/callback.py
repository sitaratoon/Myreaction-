from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Script import text
from config import ADMIN
from fsub import fsub_callback

# ------------------ FSUB Callback ------------------

@Client.on_callback_query(filters.regex("fsub_check"))
async def _fsub_check(client: Client, query: CallbackQuery):
    await fsub_callback(client, query)

# ------------------ Main Callback Handler ------------------

@Client.on_callback_query()
async def callback_query_handler(client: Client, query: CallbackQuery):
    # Agar ye FSUB check nahi hai, normal buttons handle karenge

    if query.data == "start":
        await query.message.edit_caption(
            caption=text.START.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    '⇆ Add Me To Your Channel ⇆',
                    url='https://telegram.me/QuickReactRobot?startgroup=botstart')],
                [InlineKeyboardButton('ℹ️ About', callback_data='about'),
                 InlineKeyboardButton('📚 Help', callback_data='help')],
                [InlineKeyboardButton(
                    '⇆ Add Me To Your Channel ⇆',
                    url='https://telegram.me/QuickReactRobot?startchannel=botstart')]
            ])
        )

    elif query.data == "help":
        await query.message.edit_caption(
            caption=text.HELP.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('📢 Updates', url='https://t.me/ST_Rename_Update'),
                 InlineKeyboardButton('💬 Support', url='https://t.me/ST_Bots_Update')],
                [InlineKeyboardButton('↩️ Back', callback_data="start"),
                 InlineKeyboardButton('❌ Close', callback_data="close")]
            ])
        )

    elif query.data == "about":
        await query.message.edit_caption(
            caption=text.ABOUT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('👨‍💻 Developer 👨‍💻', user_id=int(ADMIN))],
                [InlineKeyboardButton('↩️ Back', callback_data="start"),
                 InlineKeyboardButton('❌ Close', callback_data="close")]
            ])
        )

    elif query.data == "close":
        await query.message.delete()
