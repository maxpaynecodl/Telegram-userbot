from search_engine_parser import DuckDuckGoSearch

from paimon import Message, paimon


@paimon.on_cmd(
    "ddg",
    about={
        "header": "do a duck duck gosearch",
        "flags": {
            "-p": "page of results to return (default to 1)",
            "-l": "limit the number of returned results (defaults to 5)(max 10)",
        },
        "usage": "{tr}ddc [flags] [query | reply to msg]",
        "examples": "{tr}ddc -p4 -l10 github-paimon",
    },
)
async def ddgsearch(message: Message):
    query = message.filtered_input_str
    await message.edit(f"**searching** for `{query}` ...")
    flags = message.flags
    page = int(flags.get("-p", 1))
    limit = int(flags.get("-l", 5))
    if message.reply_to_message:
        query = message.reply_to_message.text
    if not query:
        await message.err("Give a query or reply to a message to google!")
        return
    try:
        ddg_search = DuckDuckGoSearch()
        ddgresults = await ddg_search.async_search(query, page)
    except Exception as e:
        await message.err(e)
        return
    output = ""
    for i in range(limit):
        try:
            title = ddgresults["titles"][i].replace("\n", " ")
            link = ddgresults["links"][i]
            desc = ddgresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"
        except (IndexError, KeyError):
            break
    output = f"**duck duck go search:**\n`{query}`\n\nResults:\n{output}"
    await message.edit_or_send_as_file(
        text=output, caption=query, disable_web_page_preview=True
    )
