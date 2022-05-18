from pyrogram import Client
from rich.console import Console, Theme
import asyncio
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class ReactionMessage(SettingsFunction):
    """reaction raid"""
    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        
        self.account_count(connect_sessions)

        self.link_message = console.input('[bold red]link message: ')
        self.emoji = console.input('[bold red]emoji> ')

        for app in track(self.connect_sessions,
        description='[bold white]REACTION'):
            self.reaction(app)
        

    def reaction(self, app):
        if not self.initialize:
            app.connect()

        me = app.get_me()
       
        link = self.link_message.split('/')
        if link[3] == 'c':
            link_channel = int('-100'+link[4])
            post_id = int(link[5])
        else:
            link_channel = link[3]
            post_id = int(link[4])
               
        try:
            app.send_reaction(link_channel, post_id, self.emoji)
            
        except Exception as error:
            console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')
