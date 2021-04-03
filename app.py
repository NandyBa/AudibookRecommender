import discord
from discord.ext import commands
from wit import Wit
import os
import bot
from persona import *

from dotenv import load_dotenv
load_dotenv('.env')


app = commands.Bot(command_prefix = "!", description = "Chatbot & recommendation system bot project")

@app.event
async def on_ready():
	print("Ready !")

@app.event
async def on_message(message):
	if message.author.dm_channel is not None and message.channel.id == message.author.dm_channel.id:
		# private message
		client = Wit(os.environ['Wit_server_token'])
		persona = Persona.get(message.channel.id)
		intent, entitie = None, None
		kind, category = None, None
		try:
			res  = client.message(message.content)
		except Exception as e:
			raise e
		print("res:", res)
		try:
			intent = res['intents'][0]['name']
			print(intent)
		except:
			print('No intent')


		try:
			kind = res['entities']['kind:kind'][0]['value']
		except:
			pass
		try:
			category = res['entities']['category:category'][0]['value']
		except:
			pass

		print("kind:", kind)
		print('category', category)

		try:
			method_to_call = getattr(bot, intent)
			response = method_to_call(persona, kind, category)
		except:
			try:
				method_to_call = getattr(bot, persona.lastIntent)
				response = method_to_call(persona, kind, category)
				intent = persona.lastIntent
			except:
				response = "Sorry but I didn't understand."
		
		try:
			p2 = pickle.load(open('data/personna-id-'+str(message.channel.id)+'.pkl','rb'))
			print(p2.FavoriteCategories)
		except:
			pass
	
		persona.setLastIntent(intent)
	
		await message.author.send( response )


app.run(os.environ['Discord_bot_token'])
