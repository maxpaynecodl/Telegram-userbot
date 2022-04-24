import html

from paimon import Config, Message, paimon

LOG = paimon.getLogger(__name__)

PATH = Config.DOWN_PATH + "chat_pic.jpg"


def mention_html(user_id, name):
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))


@paimon.on_cmd(
    "tagall",
    about={
        "header": "Tagall recent 100 members with caption",
        "usage": "{tr}tagall [Text | reply to text Msg]",
    },
    allow_via_bot=True,
    allow_private=False,
)
async def tagall_(message: Message):
    """Tag recent members"""
    replied = message.reply_to_message
    text = message.input_str
    message.chat.title
    c_id = message.chat.id
    await message.edit(f"`@all`")
    text = f"**{text}**\n" if text else ""
    message_id = replied.message_id if replied else None
    try:
        async for members in message.client.iter_chat_members(c_id, filter="recent"):
            if not members.user.is_bot:
                u_id = members.user.id
                u_name = members.user.username or None
                f_name = (await message.client.get_user_dict(u_id))["fname"]
                text += f"@{u_name} " if u_name else f"[{f_name}](tg://user?id={u_id}) "
    except Exception as e:
        text += " " + str(e)
    await message.client.send_message(c_id, text, reply_to_message_id=message_id)
    await message.edit("```Tagged recent Members Successfully...```", del_in=3)


@paimon.on_cmd(
    "tagall",
    about={
        "header": "Tagall recent 100 members with caption",
        "usage": "{tr}tagall [Text | reply to text Msg]",
    },
    allow_via_bot=True,
    allow_private=False,
)
async def tagall_(message: Message):
    """Tag recent members"""
    replied = message.reply_to_message
    text = message.input_str
    message.chat.title
    c_id = message.chat.id
    await message.edit(f"@all")
    text = f"**{text}**\n" if text else ""
    message_id = replied.message_id if replied else None
    try:
        async for members in message.client.iter_chat_members(c_id, filter="recent"):
            if not members.user.is_bot:
                u_id = members.user.id
                u_name = members.user.username or None
                f_name = (await message.client.get_user_dict(u_id))["fname"]
                text += f"@{u_name} " if u_name else f"[{f_name}](tg://user?id={u_id}) "
    except Exception as e:
        text += " " + str(e)
    await message.client.send_message(c_id, text, reply_to_message_id=message_id)
