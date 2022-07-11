from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
import random
import os

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))


class ChangePhoto(SettingsFunction):
	"""change profile photo"""

	def __init__(self, connect_sessions, initialize):
		console.print(
			'Photos are taken from the "photo" folder',
			'Press "ENTER"',
			'[bold white]If you change your mind, press CTRL C[/]',
			sep='\n',
			style='bold magenta'
		)

		console.input()

		for session in track(connect_sessions):
			if not initialize:
				session.connect()

			me = session.get_me()

			try:
				file = random.choice(
					os.listdir("resources")
					)
				session.set_profile_photo(photo=f'resources/{file}')

			except Exception as error:
				console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
