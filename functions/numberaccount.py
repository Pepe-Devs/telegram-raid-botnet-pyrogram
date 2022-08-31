from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
from rich.table import Table
from rich import box

import phonenumbers
from phonenumbers.phonenumberutil import (
        region_code_for_country_code,
        region_code_for_number,
        country_code_for_region
    )

from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Checkingnumber:
    """country of the number"""

    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        self.connect_sessions = connect_sessions

        self.code = []
        self.country_list = {}

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.checkng_start(session)
                for session in self.connect_sessions
            ])
        )

    async def checkng_start(self, session):
        if not self.initialize:
            await session.connect()

        me = await session.get_me()

        country = phonenumbers.parse(f'+{me.phone_number}')

        string_country = region_code_for_country_code(country.country_code)
        code_country = country_code_for_region(string_country)

        self.country_list[string_country]=code_country
        self.code.append(code_country)

        if len(self.code) == len(self.connect_sessions):
            for name, code in self.country_list.items():
                if code in self.code:
                    console.print(name, self.code.count(code))
