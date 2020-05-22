import discord

from asyncio import sleep

from os import path as p
CURRENT_DIR = p.dirname(p.realpath(__file__))
from sys import path
path.append(CURRENT_DIR)

import low_functions
import functions

#🗿
#🖕

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.prefixo = "computador"


    async def on_message(self, message):
        
        # don't respond to ourselves
        if message.author == self.user:
            return

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

if __name__ == "__main__":
    tokenFile = open("botToken", 'r')
    token = tokenFile.read().replace('\n', '')
    tokenFile.close()

    client = MyClient()
    client.run(token)
