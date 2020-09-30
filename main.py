#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
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
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

import asyncio
import discord
import time
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "!")
tocken = "NzU5ODc2NTU5Nzc5MTM1NTI5.X3D4MQ.vNF_4CtAIKqb16yih5AxA4uzy_8"

logs_channel = client.get_channel(760878352658726912)

@client.event
async def on_ready():
    print("Botzoula is ready.")

@client.event
async def on_member_join(member):
    print(str(member) + " vient de rejoindre le serveur.")

    role = get(member.guild.roles, name = "EPSI-B3")
    print(member.guild_permissions)
    print(member.guild_permissions.manage_roles)
    
    await member.edit(roles=[role])

    await formWelcome(member)

@client.event
async def on_member_remove(member):
    print(str(member) + " vient de quitter le serveur.")


async def formWelcome(member):

    global client

    text_timeout = "Bon, à bientôt je l'espère...\n**`Tu viens de te faire kick du serveur`**"
    text_wrong_answer = "Désolé, je n'ai pas bien compris... tu peux répéter ?"
    text_alert = "Hey ne m'oublie pas !"
    text1 = "Salut bienvenue sur le discord de l'**EPSI/WIS Paris** !"
    text2 = "Pour te placer correctement dans le discord, je vais te demander quelques informations..."
    text3 = "Merci de bien y répondre car en cas d'erreur, *seul un administrateur pourra corriger le tire*."
    text4 = "Pourrais-tu me donner ton prénom ?"
    text5 = "Pourrais-tu me donner ton nom de famille ?"
    text6 = "... ton école ? \n*réponses acceptées: `EPSI`, `WIS`*"
    text7 = "Dans quelle promotion rentres-tu ? \n*réponses acceptées: `B1`, `B2`, `B3`, `I1`, `I2`*"
    text8 = "Pour finir, es-tu délégué de ta promotion ?\n*réponses acceptées: `Oui`, `Non`*"
    
    questions = [text4, text5, text6, text7, text8]
    values = ["", "", "", "", False]

    await member.send(content=text1+"\n"+text2+"\n"+text3)

    # time.sleep(5)
    await asyncio.sleep(5)
    
    def check(message):
        return message.author == member and message.channel == member.dm_channel

    for i in range(0, len(questions)):
        count_limit = 10
        count = 0
        await member.send(content=questions[i])
        while True:
            try:
                values[i] = await client.wait_for("message", timeout = 30, check = check)
            except:
                count+=1
                if count < count_limit:
                    await member.send(content=text_alert)
                    continue
                else:
                    await member.send(content=text_timeout)
                    await member.kick(reason="No response during the welcome form")
                    return
            msg = values[i].content.upper()
            values[i] = values[i].content
            if i == 2:
                result = msg == "EPSI" or msg == "WIS"
            elif i == 3:
                result = msg == "B1" or msg == "B2" or msg == "B3" or msg == "I1" or msg == "I2"
            elif i == 4:
                result = msg == "OUI" or msg == "NON"
            else:
                result = True
            if result:
                count = 0
                break
            else:
                await member.send(content=text_wrong_answer)

    embed=discord.Embed(color=0x000000)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/619567457123958813/3d33b155ee4c990c7d89b394fee4bbdd.webp?size=128")
    embed.add_field(name="prénom:", value=values[0], inline=True)
    embed.add_field(name="nom:", value=values[1], inline=True)
    embed.add_field(name="école:", value=values[2], inline=False)
    embed.add_field(name="level:", value=values[3], inline=True)
    embed.add_field(name="delegate:", value=values[4], inline=True)
    embed.set_footer(text="(Agent de Sécurité) - Bot by Aymerick MICHELET")
    await member.send(embed=embed)

    # role = discord.utils.get(member.server.roles, name=values[2].upper()+"-"+values[3].upper())

    await member.edit(nick=values[0].lower()+"."+values[1].lower())


client.run(tocken)



