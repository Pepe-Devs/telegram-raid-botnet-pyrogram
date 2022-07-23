from rich.prompt import Prompt, Confirm
import asyncio
import sys
from rich.console import Console
import random

console = Console()

class SettingsFunction:
    def add_api(self):
        api_id = int(console.input('[bold red]API ID:[/] '))
        api_hash = console.input('[bold red]API HASH:[/] ')

        my_file = open("sessions/config_api.py", "w+")
        my_file.write(f'api_id = {api_id}\napi_hash = "{api_hash}"')
        my_file.close()
        sys.exit()

    def account_count(self, connect_sessions):
        acc_count = int(Prompt.ask('[bold red]how many accounts to use?',
                            default=str(len(connect_sessions))
                            ))

        self.connect_sessions = random.sample(connect_sessions, acc_count)
