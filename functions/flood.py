from rich.console import Console, Theme
from pyrogram import Client, idle
import asyncio
from rich.prompt import Prompt, Confirm
from rich.progress import track
from multiprocessing import Process, Manager
import sys
import random
import time
import os

from pyrogram.raw import functions, types

from settings.config import *
from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodChat(SettingsFunction):

    def __init__(self, connect_sessions, initialize):
        self.connect_sessions = connect_sessions
        self.initialize = initialize

        if initialize:
            console.print('[bold red]this may not work correctly during initialization')

        self.flood_menu = (
            ('raid text', self.flood_text),
            ('raid media', self.flood_media)
        )

    def ask(self):
        for number, function in enumerate(self.flood_menu, 1):
            console.print(
                '[{number}] {name}'
                .format(
                    number=number,
                    name=function[0]
                )
            )

        choice = int(
            console.input(
            '[bold white]>> [/]'
            )
        )-1

        self.function = self.flood_menu[choice][1]

        self.notify = Confirm.ask('[bold red]notify users?')

        if self.notify:
            self.notify_admins = Confirm.ask('[bold red]notify_admins?')

        self.delay = Prompt.ask("[bold red]delay[/]", default="0")

    async def flood(self, session, peer, reply_msg_id):
        self.peer = peer
        self.reply_msg_id = reply_msg_id

        try:
            if type(self.peer) == str:
                link = await session.get_chat(self.peer)
                self.peer = link.id

            if self.notify:
                self.users_id = []

                async for member in session.get_chat_members(self.peer):
                    if member.status in ["creator", "administrator"] \
                        and not self.notify_admins:
                        continue

                    self.users_id.append(str(member.user.id))

        except Exception as error:
            console.print(error)

        me = await session.get_me()

        errors_count = 0
        count = 0

        while count < message_count:
            try:
                if not self.notify:
                    self.text = random.choice(text)
                else:
                    self.text = '<a href=\"tg://user?id={user_id}\"> </a>{message}' \
                    .format(
                        user_id=random.choice(self.users_id),
                        message=random.choice(text)
                    )

                await self.function(
                        session,
                        self.peer,
                        self.reply_msg_id
                    )

                count += 1

                console.print(
                    f'[{me.first_name}] [bold green]sent[/] COUNT: [{count}]'
                    )

            except Exception as error:
                console.print(
                        '[bold red]not sent [{}][/]:{name} {error}'
                        .format(
                            errors_count,
                            name=me.first_name,
                            error=error
                        )
                    )

                errors_count += 1

            if errors_count >= 3:
                break

            await asyncio.sleep(int(self.delay))

    async def flood_text(self, session, peer, reply_msg_id):
        await session.send_message(
                peer,
                self.text,
                reply_to_message_id=reply_msg_id
            )

    async def flood_media(self, session, peer, reply_msg_id):
        file = random.choice(os.listdir('media'))

        await session.send_document(
                self.peer,
                f'media/{file}',
                reply_to_message_id=reply_msg_id
            )

    def handler(self, session, num_accs):
        try:

            session.start()
            console.log(f'initialized/{num_accs}')
            @session.on_message()
            async def main(client, message):
                reply_msg_id = False
                
                if message.reply_to_message:
                    reply_msg_id = message.reply_to_message_id

                if message.text == trigger \
                        and message.from_user.id == my_id:
                    await self.flood(
                            session,
                            message.chat.id,
                            reply_msg_id
                        )

            idle()

        except Exception as error:
            console.print(f'[bold red]ERROR[/]: {error}')

    def start_process_flood(self):
        self.account_count(self.connect_sessions)

        processes = []

        for num_accs, session in enumerate(self.connect_sessions):
            process = Process(
                    target=self.handler,
                    args=(session, num_accs)
                )

            process.start()
            processes.append(process)

        console.print(
            f'[*][bold white]SEND "[yellow]{trigger}[/]" to chat[/]'
            )

        for process in processes:
            process.join()
