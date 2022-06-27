from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code, region_code_for_number, country_code_for_region

from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Checkingnumber:
    """country of the number"""
    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        self.connect_sessions = connect_sessions

        self.code = []
        self.country_list = {}
        self.list_number = {}

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.checkng_start(app)
                for app in self.connect_sessions
            ])
        )

        self.number_output = console.input('[bold red]output of phone numbers?(y/n)<n>: [/]')
        if self.number_output == 'y':
            console.print('[bold red]the code of the countries that are located here:[/]\n<',
            ', '.join(
                map(str, list(
                        set(self.code)
                        )
                    )
                ), '>\n')

            for name, number in self.list_number.items():
                console.print(f'{name} - {number}')

    async def checkng_start(self, app):
        if not self.initialize:
            await app.connect()

        me = await app.get_me()

        self.list_number[me.first_name, me.id]=me.phone_number

        country = phonenumbers.parse(f'+{me.phone_number}')

        string_country = region_code_for_country_code(country.country_code)
        code_country = country_code_for_region(string_country)

        self.country_list[string_country]=code_country
        self.code.append(code_country)

        if len(self.code) == len(self.connect_sessions):
            for name, code in self.country_list.items():
                if code in self.code:
                    console.print(name, self.code.count(code))
