import json
from pyrogram import Client
import asyncio
from rich.console import Console, Theme

console = Console()
	
class ConnectSessions:
	def __init__(self):
		self.initialize = (
			True if console.input('Initialize sessions? [bold while](y/n) ') == 'y'
            else False
        )
		self.connect_sessions = []
		
		with open('sessions/sessions.json', 'r') as json_session:
			sessions = json.load(json_session)['storage_sessions']
			for app in sessions:
				app=Client(app)
				self.connect_sessions.append(app)
		
		if self.initialize:
			with console.status("Initializing"):
				asyncio.get_event_loop().run_until_complete(
					asyncio.wait([
						self.connect_session(number, session)
						for number, session in enumerate(self.connect_sessions)
					])
				)
					
	async def connect_session(self, number, app):
		try:
			console.log(await app.start())
			console.log(f'CONNECTED/{True}/{number}')
			
			self.connect_sessions.append(app)
			self.connect_sessions.remove(app)
			
		except Exception as error:
			console.log(f'NOT CONNECTED/{error}')
			self.connect_sessions.remove(app)
				
		