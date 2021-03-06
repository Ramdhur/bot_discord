"""
Traces :
ESA01   31/01/22    Ajout sauvegarde message id

-----
Code couleur :
    - vert : 0x0BD33B
    - orange : 0xF67B00
    - rouge : 0xF40000
"""    

import discord
import os
import datetime
import psycopg2


HOST = "ec2-52-49-56-163.eu-west-1.compute.amazonaws.com"
USER = "ofcugccjnydpcc"
PASSWORD = "daa547f1bfedd106c2817e9f616c5f9d86208128ee5002de86741b34857f16cf"
DATABASE = "d4op586jpca06q"

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
            
            if message.content.startswith("!addTable"):   
                cur.execute("CREATE TABLE save (id_msg INT NOT NULL, chan_msg TEXT NOT NULL, descr_msg TEXT NOT NULL)")
                conn.commit()
                embed=discord.Embed(
                                title="Ajout Table",
                                description = "save",
                                color=0x000000
                        )
                await message.channel.send(embed=embed)
            
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
                    text_query = ""
                    await message.channel.send(embed=embed)
                    
            await message.delete()
            
        #--------------------------------------------#                  
        
        elif message.channel.name == "stock":
            
            if message.content.startswith("!stock"):                
                cur.execute("SELECT nom, stock_actuel, stock_voulu FROM produit ORDER BY nom")
                selectedLignes = cur.fetchall()
                messageG = ""
                messageD = ""
                
                for raw in selectedLignes:
                    if raw[1] < raw[2]:
                        messageG += ":red_circle: - "
                    else:
                        messageG += ":green_circle: - "
                    messageG += raw[0] + "\n"
                    messageD += str(raw[1]) + " / " + str(raw[2]) + "\n"
                
                
                embed=discord.Embed(
                    title="Système PBSC - Comptabilité - Stock",
                    description = "",
                    color=0x0BD33B
                )
                embed.add_field(name = "Nom", value = messageG, inline = True)
                embed.add_field(name = "Quantité", value = messageD, inline = True)
                                
                #ESA01 await message.channel.send(embed=embed)
                #ESA01...                
                msg = await message.channel.send(embed=embed)
                addIDmsg(msg.id, message.channel, "stock")                
                #...ESA01
            
            
            elif message.content.startswith("!addProduit"):
                contenu = message.content[12:].split(", ")
                
                if len(contenu) == 5:
                    cur.execute("SELECT * FROM produit WHERE nom = '" + contenu[0] + "'")
                    
                    if len(cur.fetchall()) == 0: 
                        
                        text_query = "INSERT INTO produit VALUES ('"
                        text_query += contenu[0] + "',"
                        text_query += contenu[1] + ","
                        text_query += contenu[2] + ","
                        text_query += contenu[3] + ","
                        text_query += contenu[4] + ")"
                        cur.execute(text_query)
                        conn.commit()
                        text_query = ""
                        
                        embed=discord.Embed(
                            title="Ajout produit",
                            description = contenu[0],
                            color=0x000000
                        )
                        await message.channel.send(embed=embed)
                        
                        
            elif message.content.startswith("!removeProduit"):
                cur.execute("SELECT * FROM produit WHERE nom = '" + message.content[15:] + "'")
                if len(cur.fetchall()) != 0:
                    cur.execute("DELETE FROM produit WHERE nom = '" + message.content[15:] + "'")
                    conn.commit()
                    
                    embed=discord.Embed(
                            title="Supression produit",
                            description = message.content[15:],
                            color=0x000000
                    )
                    await message.channel.send(embed=embed)
                
            await message.delete()
        
        
# ESA01...
def addIDmsg(pId_msg, pChannel_msg, pDescr_msg):    
    text_query = "INSERT INTO save VALUES ("
    text_query += str(pId_msg) + ",'"
    text_query += pChannel_msg + "',"
    text_query += pDescr_msg + "')"
    cur.execute("")
    conn.commit()
    text_query = ""
#...ESA01        

        
client = MyClient()
client.run(os.environ.get('TOKEN'))

cur.close()
conn.close()
