import discord
import os
import time

"""
Code couleur :
    - vert : 0x0BD33B
    - orange : 0xF67B00
    - rouge : 0xF40000

        elif message.channel.name == "":
            
            if message.content.startswith("!"):
                await message.delete()
                embed=discord.Embed(
                    title="",
                    description = "",
                    color=0x000000
                    )
            else:
                await message.delete()

"""

class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

#-------------------------------------------------------#        
        
    async def on_message(self, message):
        # on ne veut pas que le bot se réponde à lui-même
        if message.author.id == self.user.id:
            return
        
        #--------------------------------------------#    
        if message.channel.name == "test-commandes":
                
            if message.content.startswith("!radar"):
                await message.delete()
                if message.content[7:].isnumeric():
                    embed=discord.Embed(
                    title="Compta de Test",
                    description = "Radar : " + message.content[7:] + "$",
                    color=0xF67B00
                    )
                    await message.channel.send(embed=embed)

            elif message.content.startswith('!salaire'):
                await message.delete()
                embed=discord.Embed(
                    title="Compta de Test",
                    description = "Salaire : 80$",
                    color=0x0BD33B
                    )
                await message.channel.send(embed=embed)
            
            elif message.content.startswith('!essence'):
                await message.delete()
                if message.content[9:].isnumeric():
                    embed=discord.Embed(
                        title="Compta de Test",
                        description = "Essence : " + message.content[9:] + "$",
                        color=discord.Colour.orange()
                        )
                    await message.channel.send(embed=embed)
            
            else:
                await message.delete()
                
        #--------------------------------------------#                  
        elif message.channel.name == "vente-tournée":
            
            if message.content.startswith("!export"):
                await message.delete()
                if message.content[8:].isnumeric():
                    embed=discord.Embed(
                        title="Système PBSC - Comptabilité - " + time.strftime('%H:%M', time.localtime()),
                        description = "Export enregister par " + message.author.name + " pour une quantité de : " + message.content[8:] + " !",
                        color=0x0BD33B
                        )
                    await message.channel.send(embed=embed)
            else:
                await message.delete()
            
        
client = MyClient()
client.run(os.environ.get('TOKEN'))
