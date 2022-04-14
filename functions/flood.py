from rich.console import Console, Theme
from pyrogram import Client, idle
import asyncio
from rich.prompt import Prompt, Confirm
from rich.progress import track
from multiprocessing import Process
import sys
import random	


from settings.config import *
from settings.function import SettingsFunction

console = Console(theme=Theme({"repr.number": "bold purple"}))

class FloodChat(SettingsFunction):
	"""flood to chat"""
	def __init__(self, connect_sessions, initialize):
		self.connect_sessions = connect_sessions
		
		if initialize:
			console.print('[bold red]cannot be used with initialization')
			sys.exit()
			
		self.flood_menu = console.input(
'''[bold]
[1] - flood text
[2] - flood stickers/video
[3] - flood photo
>> ''')
		
		self.notify = Confirm.ask('[bold red]notify admins?')
		
		self.start_process_flood()
		
	async def flood(self, app, chat_id, reply_msg_id):
		self.chat_id = chat_id
		self.reply_msg_id = reply_msg_id

		self.me = await app.get_me()

		self.users_id = []
		self.admins = []


		async for member1 in app.iter_chat_members(self.chat_id, filter="administrators"):
			self.admins_id = member1.user.id
			self.admins.append(str(self.admins_id))

		async for member in app.iter_chat_members(self.chat_id):
			self.user_id = member.user.id
			self.users_id.append(str(self.user_id))
			
		if not self.notify:
			self.users_id = list(set(self.users_id)-set(self.admins))

		count = 0
		for _ in range(range_acc):
			try:
				await self.flood_start(
					app,
					random.choice(self.users_id),
					self.chat_id,
					self.reply_msg_id
					)
				count += 1
				console.print(f'[{self.me.first_name}] [bold green]sent[/] COUNT: [{count}]')

			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{self.me.first_name} {error}')

			await asyncio.sleep(int(self.delay))


	async def flood_text(self,
				app,
				users_id,
				chat_id,
				reply_msg_id
				):
		await app.send_message(
			chat_id,
			(f'<a href=\"tg://user?id={users_id}\">'+notification+'</a>'+random.choice(text)),
			reply_to_message_id=reply_msg_id
			)


	async def flood_stickers(self,
				app,
				chat_id,
				reply_msg_id
				):
		await app.send_document(
			self.chat_id,
			'media/'+random.choice(stickers),
			reply_to_message_id=self.reply_msg_id
			)


	async def flood_photo(self,
				app,
				chat_id,
				reply_msg_id
				):
		await app.send_photo(
			self.chat_id,
			'photo/'+random.choice(photo),
			caption=random.choice(text_photo),
			reply_to_message_id=self.reply_msg_id
			)


	def handler(self, app, num_accs):
		app.start()
		console.log(f'initialized[*]{num_accs}')
		@app.on_message()
		async def main(client, message):
			if message.reply_to_message:
				reply_msg_id = message.reply_to_message.message_id
			else:
				reply_msg_id = False

			if message.text == trigger and message.from_user.id == my_id:
					await self.flood(app, message.chat.id, reply_msg_id)

		idle()

	def start_process_flood(self):
		self.account_count(self.connect_sessions)
		self.delay = console.input('[bold blue]delay[/](0)> ')
		
		if not self.delay:
			self.delay = 0
			
		processes = []

		for num_accs, session in enumerate(
				self.connect_sessions, 
				start=1):
			
			process = Process(
				target=self.handler, args=(session, num_accs,)
				)
			process.start()
			processes.append(process)

		console.print(f'[*][bold white]SEND "[yellow]{trigger}[/]" to chat[/]')

		for process in processes:
			process.join()