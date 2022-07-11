from pyrogram import Client
import asyncio
from rich.console import Console, Theme
from rich.prompt import Prompt, Confirm
import random

from settings.function import SettingsFunction
from settings.config import text, message_count
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodComments(SettingsFunction):
	"""flood to channel comments"""
	
	def __init__(self, connect_sessions, initialize):
		self.initialize = initialize
		self.connect_sessions = connect_sessions
		self.text = text

		self.account_count(self.connect_sessions)

		self.link = console.input('[bold red]link to post> [/]')
		self.message = Confirm.ask('[bold red]get text from config?[/]')

		if not self.message:
			self.text = [console.input(
				'[bold red]message:[/] '
				)]

		self.delay = Prompt.ask(
			"[bold red]delay[/]",
			default="0"
			)

		asyncio.get_event_loop().run_until_complete(
			asyncio.gather(*[
					self.flood(session)
					for session in self.connect_sessions
				])
			)

	async def flood(self, session):
		if not self.initialize:
			await session.connect()

		me = await session.get_me()

		try:
			channel = ''.join(self.link.split('/')[-2:-1])
			post_id = int(self.link.split('/')[-1])

			if channel.isdigit():
				channel = int(f'-100{channel}')

			print(channel, post_id)
			post = await session.get_discussion_message(channel, post_id)

		except Exception as error:
			console.print(f'[bold red]ERROR[/]: {error}')

		errors_count = 0
		count = 0

		while count < message_count:
			try:
				await post.reply(random.choice(self.text))
				count += 1

				console.print(
					'[{name}] [bold green]sent[/] COUNT: [{count}]'
					.format(
						name=me.first_name,
						count=count
					)
				)

			except Exception as error:
				errors_count += 1

				console.print(
					'[bold red]ERROR [{}][/]: {name} {error}'
					.format(
							errors_count,
							name=me.first_name,
							error=error
						)
					)

			await asyncio.sleep(int(self.delay))
