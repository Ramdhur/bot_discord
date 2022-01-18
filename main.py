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
            
            
            if message.content.startswith("!removeTableProduit"):
                
                cur.execute("DROP TABLE produit")
                conn.commit()
                
                await message.delete()                
                embed=discord.Embed(
                    title="Destruction table produit",
                    description = "",
                    color=0x000000
                )
                await message.channel.send(embed=embed)
                               
            elif message.content.startswith('!addTableProduit'):
                
                cur.execute("CREATE TABLE produit (nom TEXT PRIMARY KEY NOT NULL, stock_actuel INT NOT NULL, stock_voulu INT NOT NULL, prix_particulier INT NOT NULL, prix_entreprise INT NOT NULL)")
                conn.commit()
                
                await message.delete()                
                embed=discord.Embed(
                    title="Création table produit",
                    description = "",
                    color=0x000000
                )
                await message.channel.send(embed=embed)
               
            else:
                await message.delete()

            
                
        #--------------------------------------------#                  
        elif message.channel.name == "vente-tournée":
            
            if message.content.startswith("!export"):
                await message.delete()
                if message.content[8:].isnumeric():
                    date = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=0)
                    embed=discord.Embed(
                        title="Système PBSC - Comptabilité - " + date.strftime("%Hh%M"),
                        description = "Export enregister par " + message.author.display_name + " pour une quantité de : " + message.content[8:] + " !",
                        color=0x0BD33B
                        )
                    await message.channel.send(embed=embed)
            else:
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
