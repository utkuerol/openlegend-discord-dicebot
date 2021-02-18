from typing import Pattern
import discord
import utils
import os

client = discord.Client()
TOKEN = os.environ['DISCORD_OPENLEGEND_BOT_TOKEN']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/r") or message.content.startswith("/roll"):
        check_err = utils.parse_msg(
            message.content)
        if check_err == -1:
            await message.channel.send("Ooops...Wrong arguments!")
        else:
            vicious, destructive, attr_score, adv, repeat_factor = utils.parse_msg(
                message.content)
            results, info = utils.calculate_result(
                vicious, destructive, attr_score, adv, repeat_factor)
            msg = "{} rolled: ".format(message.author)
            for result in results:
                msg += "\n\n**Roll {}**".format(results.index(result)+1)

                total_base = sum(sum(result[0][0], []))
                total_attr = sum(sum(result[1][0], []))
                separator = " "
                table = str.maketrans('[]', '()')

                base_kept = separator.join(
                    map(str, result[0][0])).translate(table)

                base_dropped = separator.join(
                    map(str, result[0][1])).translate(table)
                if base_dropped == "":
                    base_dropped = "-"

                base_dropped_vs = separator.join(
                    map(str, result[0][2])).translate(table)
                if base_dropped_vs == "":
                    base_dropped_vs = "-"

                attr_kept = separator.join(
                    map(str, result[1][0])).translate(table)
                if attr_kept == "":
                    attr_kept = "-"

                attr_dropped = separator.join(
                    map(str, result[1][1])).translate(table)
                if attr_dropped == "":
                    attr_dropped = "-"

                msg += "\n----------\nTotal: {} \nBase (1d20 = {}): \t {} \t *dropped: {} \t dropped (vicious strike): {}* \nAttribute ({} = {}): \t {} \t *dropped: {}*".format((total_base + total_attr), total_base,
                                                                                                                                                                                 base_kept, base_dropped, base_dropped_vs, total_attr, info, attr_kept, attr_dropped)

            await message.channel.send(msg)

    elif message.content.startswith("/r!") or message.content.startswith("/roll!"):
        args = message.content.split(" ")[1:]
        result = utils.roll_raw(args[0])
        await message.channel.send("{} rolled: {}".format(message.author), result)


client.run(TOKEN)
