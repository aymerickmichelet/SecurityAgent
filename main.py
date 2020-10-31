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

import discord
from discord.ext import commands
from user import User

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
token = open('token.txt', 'r').read()

new_user = None
text_timeout = "Bon, à bientôt j'espère...\n**`Vous venez de vous faire kick du serveur`**"
text_wrong_answer = "Désolé, je n'ai pas bien compris... pouvez-vous répéter ?"
text_repeat = "Bon, je vais recommencer le questionnaire..."
text_welcome = "Bienvenue sur le discord **EPSI/WIS** !"
text_42 = "T'as tout compris !\n**`Vous venez de vous faire kick du serveur`**"
text1 = "Salut, je vais vous demander de répondre à quelques questions" \
        " afin de vous placez correctement dans le discord !\n" \
        "Merci d'y répondre sérieusement."
text2 = "Pourriez-vous me donner votre prénom ?"
text3 = "Pourriez-vous me donner votre nom de famille ?"
text4 = "Etes-vous un étudiant, un professeur ou un administrateur ?\n" \
        "*réponses acceptées: `Etudiant`, `Professeur`, `Administrateur`*"
text5 = "Dans quelle école êtes-vous ?\n" \
        "*réponses acceptées: `EPSI`, `WIS`*"
text6 = "Dans quelle promotion rentrez-vous ? \n" \
        "*réponses acceptées: `B1`, `B2`, `B3`, `I1`, `I2`*"
text7 = "Pour finir, êtes-vous le délégué de votre promotion ?\n" \
        "*réponses acceptées: `Oui`, `Non`*"
text8 = "Ces informations sont correctes ?\n" \
         "*réponses acceptées: `Oui`, `Non`*"


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
    description = new_user.status.capitalize()
    if new_user.status == "ETUDIANT":
        description += " " + new_user.level
    if new_user.delegate == "OUI":
        description += " - Délégué(e)"

    url = "https://user-images.githubusercontent.com/32719398/97791210-2d2cf280-1bd0-11eb-83d4-f6f5aa08ebb0.png"  # epsi
    if new_user.school == "WIS":
        url = "https://user-images.githubusercontent.com/32719398/97790998-1dacaa00-1bce-11eb-8f0f-e6ff185a7ed0.png"  # wis
    elif new_user.school == "42":
        url = "https://user-images.githubusercontent.com/32719398/97790985-08378000-1bce-11eb-9049-a987eed8c176.png" # 42

    embed = discord.Embed(color=0x000000, title=new_user.firstname.capitalize() + " " + new_user.lastname.upper(),
                          description=description)
    embed.set_author(name=new_user.member.name, icon_url=new_user.member.avatar_url)
    embed.set_thumbnail(url=url)
    embed.set_footer(text="(Agent de Sécurité) - Bot by Aymerick MICHELET")

    return embed

async def kick(message: str, reason: str) -> None:
    await new_user.member.send(content=message)
    await new_user.member.kick(reason=reason)
    return None

async def ask_question(question: str, response_type: int) -> str:
    # 0 = free
    # 1 = closed question (Oui / Non)
    # 2 = status (Etudiant / Professeur / Administrateur)
    # 3 = school (Epsi / Wis)
    # 4 = level (B1 / B2 / B3 / I1 / I2)
    # 5 = confirmation (resume info with embed + closed question)

    global new_user
    global text_wrong_answer

    if response_type == 5:
        await new_user.member.send(embed=info_member(new_user))
        response_type = 1

    def check(message):
        return message.author == new_user.member and message.channel == new_user.member.dm_channel

    while True:
        await new_user.member.send(content=question)
        try:
            response = await bot.wait_for("message", timeout=5 * 60, check=check)
        except:
            await kick(text_timeout, "timeout")
            return

        response = response.content.upper()
        correct = False
        if response_type == 0:  # free
            correct = True
        if response_type == 1:  # closed question
            if response == "OUI" or response == "NON":
                correct = True
        elif response_type == 2:  # status
            if response == "ETUDIANT" \
                    or response == "PROFESSEUR" \
                    or response == "ADMINISTRATEUR":
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
            await new_user.member.send(content=text_wrong_answer)
            continue


async def welcome_form():
    global bot
    global new_user
    global text1, text2, text3, text4, text5, text6, text7, text8

    await new_user.member.send(content=text1)
    await asyncio.sleep(5)

    while True:
        new_user = User(member=new_user.member)
        new_user.firstname = await ask_question(text2, 0)
        new_user.lastname = await ask_question(text3, 0)
        new_user.status = await ask_question(text4, 2)
        if new_user.status == "ETUDIANT":
            new_user.school = await ask_question(text5, 3)
            new_user.level = await ask_question(text6, 4)
            new_user.delegate = await ask_question(text7, 1)
            role = discord.utils.get(new_user.member.guild.roles,
                                     name=new_user.school + "-" + new_user.level)
        else:
            role = discord.utils.get(new_user.member.guild.roles, name=new_user.status.capitalize())
        if await ask_question(text8, 5) == "OUI":
            if new_user.school == "42":
                await kick(text_42, "42")
                return
            else:
                await new_user.member.edit(nick=new_user.firstname.lower() + "." + new_user.lastname.lower())
                await new_user.member.edit(roles=[role])
                if new_user.delegate == "OUI":
                    await new_user.member.add_roles(discord.utils.get(new_user.member.guild.roles, name="Délégué"))
                await new_user.member.send(content=text_welcome)
                return
        else:
            await new_user.member.send(content=text_repeat)
            continue


bot.run(token)

# possibilité de liste les etudiants des B3 avec mails envoyé.
# possibilité de lister les admins (epsi.fr + bdd)
# lister professeur ???
# gérer message error (message envoyé quand member kick)
# tester plusieurs user silmutanément