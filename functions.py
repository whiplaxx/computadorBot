import discord
import asyncio
from time import time, sleep
from random import randint

from os import path as p
CURRENT_DIR = p.dirname(p.realpath(__file__))
from sys import path
path.append(CURRENT_DIR)

import low_functions
import read

DATA_DIR = CURRENT_DIR + "\\data\\"

# BOT'S ID
client_id = 713510650760003697

# LIST ALL COMMANDS
async def sendHelp(f_client, message, content):

    help_msg = ""
    command_keys = commands.keys()

    for i in command_keys:
        help_msg += i + ": " + commands[i][1] + '\n'
    
    await message.channel.send( help_msg )

# SEND BOT'S INVITE LINK
async def invite(f_client, message, content):

    await message.channel.send("https://discord.com/api/oauth2/authorize?client_id=" + str(client_id) + "&permissions=8&scope=bot")

# WAIT N SECONDS
async def wait(f_client, message, content):
    
    time = int( content[1] )
    try:
        await asyncio.sleep( time )
    except:
        pass

    await message.channel.send("esperado " + str( time ) + " segundos")

async def avatar(f_client, message, content):

    mentions = message.mentions

    if len(mentions) == 0:

        try:
            url = low_functions.getAvatarLink(message.author)
            await message.channel.send(url)
        except:
            pass

    else:
        urls = ""
        n = 0
        for i in mentions:
            if n < 3:
                try:
                    urls += low_functions.getAvatarLink(i) + '\n'
                except:
                    break
            else:
                urls += "\nlimite de 3 avatares"

                break
            n += 1 

        await message.channel.send(urls)

async def link(f_client, message, content):

    for i in content:
        if ';' in i:
            await message.channel.send( "sem ponto e virgula" )
            return
    
    try:
        link_key = content[1]

        link_content = read.readFile('links', DATA_DIR, link_key )
        if link_content  != False:
            await message.channel.send( link_content[0][1] )
            return
        else:
            print(read.ERROR_MESSAGE[read.ERROR_LOG])

    except:
        await message.channel.send( "deu n" )
        return
    
    link_content = ""
    for i in range(2, len(content) ):
        link_content += content[i]
    
    if len(link_content) == 0:
        await message.channel.send( "conteudo vazio ou link nao existe" )
        return
    elif len(link_content) >= 100:
        await message.channel.send( "mt gtrande" )
        return

    link_list = [[ link_key, link_content]]

    read.writeFile( link_list, 'links', DATA_DIR, separator=';')

async def tweet(f_client, message, content):

    try:
        user_name = content[1]
    except:
        return

    try:
        tweet = f_client.twitter_api.user_timeline(screen_name=user_name, count=100, include_rts=False, exclude_replies=True)
    except:
        await message.channel.send( "nn existe" )

    len_tweets = len(tweet)
    if len_tweets > 0:
        tweet = tweet[randint(0, len_tweets)]
        link = "https://twitter.com/" + user_name + "/status/" + tweet.id_str

        await message.channel.send( link )
    else: 
        await message.channel.send( "num tweto ")

async def chamada(f_client, message, content):

    author_id = message.author.id

    if author_id not in waitingCommand:
        waitingCommand.append(message.author.id)
    
    if author_id == 277581722357465088:
        await message.channel.send("Sim, mestre?")
    else:
        await message.channel.send("Sim, noob?")

    for i in range(0, 10):
        await asyncio.sleep( 1 )

        if author_id not in waitingCommand:
            break

    try:
        waitingCommand.remove(author_id)
    except:
        pass

# COMMANDS DIC
commands = {
    "ajuda": [sendHelp, "Lista todos os comandos"]
    , "convite": [invite, "Link do convite do cachorro fofo"]
    , "wait": [wait, "espera N segundos"]
    ,"avatar": [avatar, "pega o avatar de alguem"]
    ,"link": [link, "cria link de um texto. link tem que se uma palavra so e nada pode te ponto e virugla. Ex: ?link eae / eae bom"]
    ,"tweet": [tweet, "pega um tweet random do user passado"]
}

waitingCommand = []

# HANDLE MESSAGE CHATS WITH THE BOT PREFIX
async def handle(f_client, message, content):

    command = str(content[0])
    
    if command in commands.keys():
        await commands[ command ][0]( f_client, message, content )
    else:
        if command == '' or command == ' ':
            await chamada( f_client, message, content )
        else:
            await message.channel.send("pane no sistema alguem me desconfiguro")