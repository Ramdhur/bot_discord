import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.channel.name == "test-commandes":
                
            if message.content.startswith("!radar"):
                await message.delete()
                if message.content[7:].isnumeric():
                    embed=discord.Embed(
                    title="Compta de Test",
                    description = "Radar : " + message.content[7:] + "$",
                    color=discord.Colour.orange()
                    )
                    await message.channel.send(embed=embed)

            elif message.content.startswith('!salaire'):
                await message.delete()
                embed=discord.Embed(
                    title="Compta de Test",
                    description = "Salaire : 80$",
                    color=discord.Colour.dark_green()
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


client = MyClient()
client.run(os.environ.get('TOKEN'))
