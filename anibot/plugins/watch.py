# credits to @NotThatMF on telegram for chiaki fast api
# well i also borrowed the base code from him

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from .. import BOT_NAME, HELP_DICT, TRIGGERS as trg
from ..utils.data_parser import get_wo, get_wols
from ..utils.helper import check_user


@Client.on_message(filters.command(["watch", f"watch{BOT_NAME}"], prefixes=trg))
async def get_watch_order(client: Client, message: Message):
    """Get List of Scheduled Anime"""
    x = message.text.split(" ", 1)
    if len(x)==1:
        await message.reply_text("Nothing given to search for!!!")
    user = message.from_user.id
    data = get_wols(x[1])
    msg = f"Found related animes for the query {x[1]}"
    buttons = []
    for i in data:
        buttons.append([InlineKeyboardButton(str(i[1]), callback_data=f"watch_{i[0]}_{x[1]}_{user}")])
    await client.send_message(message.chat.id, msg, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(pattern=r"watch_(.*)"))
@check_user
async def watch_(client, cq: CallbackQuery):
    kek, id_, qry, user = cq.data.split("_")
    msg = get_wo(int(id_))
    buttons = [[InlineKeyboardButton("Back", callback_data=f"wol_{qry}_{user}")]]
    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(pattern=r"wol_(.*)"))
@check_user
async def wls(client, cq: CallbackQuery):
    kek, qry, user = cq.data.split("_")
    data = get_wols(qry)
    msg = f"Found related animes for the query {qry}"
    buttons = []
    for i in data:
        buttons.append([InlineKeyboardButton(str(i[1]), callback_data=f"watch_{i[0]}_{qry}_{user}")])
    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


HELP_DICT["watch"] = """Use /watch cmd to get watch order of searched anime

**Usage:**
        `/watch Detective Conan`
        `!watch Naruto`"""