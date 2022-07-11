from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.prompt import Prompt, Confirm
from time import perf_counter, sleep
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number
from functions.flood import FloodChat
from settings.config import time_captcha

console = Console(theme=Theme({"repr.number": color_number}))

class Joined(FloodChat):
	"""join to chat"""
	
	def __init__(self, connect_sessions, initialize):
		self.initialize = initialize
		self.connect_sessions = connect_sessions

		self.account_count(self.connect_sessions)

		console.print(
			'[1] joining a chat/channel',
			'[2] joining a chat via a channel',
			sep='\n',
			style='bold'
		)

		self.mode = console.input(
			'[bold white]>> [/]'
			)

		link = console.input(f'[bold red]link:[/] ')

		if '/+' in link:
			self.link = link.replace('/+', '/joinchat/') #/+ криво работает в pyrogram
		elif '/joinchat' in link:
			self.link = link
		else:
			self.link = link.split('/')[3]

		self.settings_join = Prompt.ask(
			'[bold red]speed[bold magenta]',
			choices=["norm", "fast"]
		)

		asyncio.get_event_loop().run_until_complete(self.start_joined())

	async def start_joined(self):
		if self.settings_join == 'fast':

			joined = 0
			start = perf_counter()

			with console.status("[bold]JOIN", spinner='aesthetic'):
				tasks = await asyncio.gather(*[
					self.join_chat(session)
					for session in self.connect_sessions
				])

				for result in tasks:
					joined += 1

				join_time = round(perf_counter() - start, 2)
				console.print(f"[+] {joined} bots joined [yellow]{join_time}[/]s")

		elif self.settings_join == 'norm':

			self.captcha = Confirm.ask('[bold red]captcha?')
			time_normal = int(console.input('[bold blue]delay>[/] '))

			for session in track(
				self.connect_sessions,
				description='[bold]JOIN'
			):

				await self.join_chat(session)
				await asyncio.sleep(time_normal)

				if self.captcha:
					await self.solve_captcha(session, self.link)

	async def solve_captcha(self, session, link):
		sleep(time_captcha)

		chat = await session.get_chat(link)
		message = session.get_chat_history(chat.id, limit=5)

		async for msg in message:
			try:
				callback = msg.reply_markup \
					.inline_keyboard[0][0].callback_data

				await session.request_callback_answer(
					chat.id,
					msg.id,
					callback
				)
			except:
				pass

	async def join_chat(self, session):
		if not self.initialize:
			await session.connect()

		me = await session.get_me()

		try:
			if self.mode == '1':
				await session.join_chat(self.link)

			elif self.mode == '2':
				channel = await session.get_chat(self.link)
				await session.join_chat(channel.linked_chat.id)

		except Exception as error:
			console.print(f'[bold red]did not join[/]: {error}')
