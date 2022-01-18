import discord
import os
import datetime
import psycopg2

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

HOST = "ec2-34-255-225-151.eu-west-1.compute.amazonaws.com"
USER = "bwleptnszvvrct"
PASSWORD = "68364d9f99e4bdad10d5c383526d1d271978ba11adbd2b783aaa1faa200221da"
DATABASE = "dc4gsphlfb9d1n"

conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
cur = conn.cursor()

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
            
            await message.delete()
            
                
        #--------------------------------------------#                  
        elif message.channel.name == "vente-tournée":
            
            if message.content.startswith("!export"):                
                if message.content[8:].isnumeric():
                    date = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=0)                                      
                    embed=discord.Embed(
                        title="Système PBSC - Comptabilité - " + date.strftime("%Hh%M"),
                        description = "Export enregister par " + message.author.display_name + " pour une quantité de : " + message.content[8:] + " !",
                        color=0x0BD33B
                    )
                    text_query = "SELECT * FROM resultat WHERE employe = '" + message.author.display_name + "' AND date = '" + date.strftime("%d/%m/%y") + "'"
                    cur.execute(text_query)
                    if len(cur.fetchall()) == 0:
                        # enregistrement non-existant
                        text_query = "INSERT INTO resultat VALUES ('" + message.author.display_name + "','" + date.strftime("%d/%m/%y") + "'," + message.content[8:] +")"
                    else:
                        # enregistrement existant
                        text_query = "UPDATE resultat SET planches = planches + " + message.content[8:] + " WHERE employe = '" + message.author.display_name + "' AND date = '" + date.strftime("%d/%m/%y") + "'"

                    cur.execute(text_query)
                    conn.commit()
                    await message.channel.send(embed=embed)
                    
            await message.delete()
            
        #--------------------------------------------#                  
        """
        elif message.channel.name == "stock":
            
            if message.content.startswith("!stock"):
                await message.delete()
                embed=discord.Embed(
                    title="Système PBSC - Comptabilité - Stock",
                    description = "",
                    color=0x0BD33B
                )
                await message.channel.send(embed=embed)
            else:
                await message.delete()
        """
        
client = MyClient()
client.run(os.environ.get('TOKEN'))

cur.close()
conn.close()
