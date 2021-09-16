# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#                                                                       #
#                                                                       #
#   $$$$$$\  $$\   $$\ $$$$$$\$$$$\  $$$$$$$\  $$$$$$\$$$$\   $$$$$$$\  #
#   \____$$\ $$ |  $$ |$$  _$$  _$$\ $$  __$$\ $$  _$$  _$$\ $$  _____| #
#   $$$$$$$ |$$ |  $$ |$$ / $$ / $$ |$$ |  $$ |$$ / $$ / $$ |\$$$$$$\   #
#  $$  __$$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ | $$ | $$ | \____$$\  #
#  \$$$$$$$ |\$$$$$$$ |$$ | $$ | $$ |$$ |  $$ |$$ | $$ | $$ |$$$$$$$  | #
#   \_______| \____$$ |\__| \__| \__|\__|  \__|\__| \__| \__|\_______/  #
#            $$\   $$ |                                                 #
#            \$$$$$$  |                                                 #
#             \______/                                                  #
#                                                                       #
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

import asyncio
import datetime
import discord
from discord.ext import commands

from user import User
from config import Config

intents = discord.Intents.default()
intents.members = True

config = Config()

bot = commands.Bot(command_prefix="!", intents=intents)
token = config.getToken()

new_user = None

@bot.event
async def on_ready():
    print(bot.user.name + " is ready.")


@bot.event
async def on_member_join(member):
    global new_user
    print(str(member) + " vient de rejoindre le serveur.")
    new_user = User(member=member)
    await welcome_form()


@bot.event
async def on_member_remove(member):
    print(str(member) + " vient de quitter le serveur.")


def info_member(user: User):
    global config

    description = "Promotion: "
    description += new_user.level

    if new_user.delegate == "OUI":
        description += " - Délégué: Oui"

    url = config.getUrl("epsi_logo")  # epsi
    if new_user.school == "WIS":
        url = config.getUrl("wis_logo")  # wis
    elif new_user.school == "42":
        url = config.getUrl("42_logo")  # 42

    embed = discord.Embed(color=0x000000, title=new_user.firstname.capitalize() + " " + new_user.lastname.upper(),
                          description=description)
    embed.set_author(name=new_user.member.name, icon_url=new_user.member.avatar_url)
    embed.set_thumbnail(url=url)
    embed.set_footer(text="(SecurityAgent) - Bot by Aymerick MICHELET")

    return embed


# async def kick(message: str, reason: str) -> None:
#     await new_user.member.send(content=message)
#     await new_user.member.kick(reason=reason)
#     return None


async def ask_question(question: str, response_type: int) -> str:
    # 0 = free
    # 1 = closed question (Oui / Non)
    # 3 = school (Epsi / Wis)
    # 4 = level (B1 / B2 / B3 / I1 / I2)
    # 5 = confirmation (resume info with embed + closed question)

    global new_user
    global config

    if response_type == 5:
        await new_user.member.send(embed=info_member(new_user))
        response_type = 1

    def check(message):
        return message.author == new_user.member and message.channel == new_user.member.dm_channel

    while True:
        await new_user.member.send(content=question)
        try:
            response = await bot.wait_for("message", check=check)
        except:
            now = datetime.datetime.now()
            print(now.day + "/" + now.month + "/" + now.year + " - " + now.hour + ":" + now.minute + ":" + now.second +
                  " [ERROR] > '' ne répond pas")
            return

        response = response.content.upper()
        correct = False
        if response_type == 0:  # free
            correct = True
        if response_type == 1:  # closed question
            if response == "OUI" or response == "NON":
                correct = True
        elif response_type == 3:  # school
            if response == "EPSI" \
                    or response == "WIS" \
                    or response == "42":
                correct = True
        elif response_type == 4:  # level
            if response == "B1" \
                    or response == "B2" \
                    or response == "B3" \
                    or response == "I1" \
                    or response == "I2":
                correct = True
        if correct:
            return response
        else:
            await new_user.member.send(content=config.getText("wrong_answer"))
            continue


async def welcome_form():
    global bot
    global new_user
    global config

    await new_user.member.send(content=config.getText("presentation"))
    await asyncio.sleep(5)

    while True:
        new_user = User(member=new_user.member)
        new_user.firstname = await ask_question(config.getText("firstname"), 0)
        new_user.lastname = await ask_question(config.getText("lastname"), 0)
        new_user.school = await ask_question(config.getText("school"), 3)
        new_user.level = await ask_question(config.getText("level"), 4)
        new_user.delegate = await ask_question(config.getText("delegate"), 1)
        role = discord.utils.get(new_user.member.guild.roles,
                                 name=new_user.school + "-" + new_user.level)

        if await ask_question(config.getText("correct"), 5) == "OUI":
            if new_user.school == "42":
                await kick(config.getText("42"), "42")
                return
            else:
                await new_user.member.edit(nick=new_user.firstname.lower() + "." + new_user.lastname.lower())
                await new_user.member.edit(roles=[role])
                if new_user.delegate == "OUI":
                    await new_user.member.add_roles(discord.utils.get(new_user.member.guild.roles, name="Délégué"))
                await new_user.member.send(content=config.getText("welcome"))
                return
        else:
            await new_user.member.send(content=config.getText("repeat"))
            continue


bot.run(token)

# possibilité de liste les etudiants des B3 avec mails envoyé.
# possibilité de lister les admins (epsi.fr + bdd)
# lister professeur ???
# gérer message error (message envoyé quand member kick)
# tester plusieurs user silmutanément
