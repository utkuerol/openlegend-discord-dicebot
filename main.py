"""
An OpenLegend RPG dice bot for Discord servers.
    Copyright (C) 2021  Utku Erol
    Contact: utku.erol@icloud.com
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Pattern
import discord
import utils
import os

client = discord.Client(intents=discord.Intents.all())
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
            msg = "{} rolled: ".format(message.author.display_name)
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

                msg += "\n----------\nTotal: {} \nBase (1d20 -> {}): \t {} \n> \t *Dropped: {}*".format(
                    (total_base + total_attr), total_base, base_kept, base_dropped)
                if vicious == True:  # Only appends Vicious Strike info if the flag returns True
                    msg += "\n> \t _Dropped  **(Vicious Strike)**: {}_".format(
                        base_dropped_vs)
                msg += "\nAttribute ({} -> {}): \t {} \n> \t *Dropped: {}*".format(
                    info, total_attr, attr_kept, attr_dropped)

            await message.channel.send(msg)

    elif message.content.startswith("/!r") or message.content.startswith("/!roll"):
        args = message.content.split(" ")[1:]
        result = utils.roll_raw(args[0])
        if result != -1:
            await message.channel.send("{} rolled: {} -> {}".format(message.author.display_name, args[0], result))

    elif message.content.startswith("/help") or message.content.startswith("/h"):
        file = open("./usage_help_msg", "r")
        msg = file.read()
        file.close()
        await message.channel.send(msg)


client.run(TOKEN)
