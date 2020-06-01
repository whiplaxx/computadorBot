import discord
import tweepy
from asyncio import sleep
from importlib import reload  

from os import path as p
CURRENT_DIR = p.dirname(p.realpath(__file__))
from sys import path
path.append(CURRENT_DIR)

import low_functions
import functions
import read

#🗿
#🖕

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.prefixo = "computador"

        self.BOT_MODS = read.readFile("\\bot_mods", CURRENT_DIR )

        # authenticate twitter
        self.auth_Twitter()

    async def on_message(self, message):
        
        # don't respond to ourselves
        if message.author == self.user:
            return

        if ( message.content.startswith("_computador") 
            and message.content.split(" ")[1].lower() == "reload" 
            and ( [str(message.author.id)] in self.BOT_MODS) ):

            reload_lib(functions)

        if message.author.id in functions.waitingCommand:
            functions.waitingCommand.remove(message.author.id)

            content = ( message.content ).split(" ")

            if message.content.startswith(self.prefixo):
                content = content[1:len(content)]
            await functions.handle(self, message, content)
        
        else:
            if message.content.startswith(self.prefixo):
                
                content = ( ( message.content )[ len(self.prefixo)+1 :len(message.content)] ).split(" ")
                await functions.handle(self, message, content)

    def auth_Twitter(self):

        consumer_key="SdadjbopDSvEHudRyG3ieIM8O"
        consumer_secret="o6Hfj8k6f0zHQUpbi4LqoY8QRwyPvGVMPp1gcVsZClHSjBeEUI"

        access_token="1124008483911872512-jlLOvRTawW1FAqGJxM0FrSUSUHEKZM"
        access_token_secret="xkYHzO1wNxQcuGeST1x6F6cGrbet6zZdLLdATxoPdxSUR"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        self.twitter_api = api

def reload_lib(lib):
    lib = reload(lib)

if __name__ == "__main__":
    tokenFile = open("botToken", 'r')
    token = tokenFile.read().replace('\n', '')
    tokenFile.close()

    client = MyClient()
    client.run(token)
