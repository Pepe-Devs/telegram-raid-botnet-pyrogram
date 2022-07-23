from rich.console import Console, Theme
from pyrogram import Client
import sys

from settings.settings import MenuSettings
from settings.settings_session import ConnectSessions
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

console.print(
    """
[bold]idea taken from https://t.me/huis_bn
GitHub botnet on telethon: https://github.com/json1c/telegram-raid-botnet
GitHub botnet on pyrogram: https://github.com/Madara225/telegram-raid-botnet-pyrogram
    """
)

accounts = ConnectSessions()
list_function = MenuSettings()

console.print("Author's channel: https://t.me/Pepe_devs")

def botnet_main():

    console.print(
        '[bold white]botnet accounts >> [{color}]{account_count}'
        .format(
            color=color_number,
            account_count=len(accounts.connect_sessions)
        )
    )

    for num_function, function in enumerate(list_function.menu_botnet, 1):
        console.print(
            '[{color}][{number}][/] {function}'
            .format(
                color=color_number,
                number=num_function,
                function=function.__doc__
            ),
            style="bold white"
            )

    try:
        menu = int(console.input(
                '[bold white]>> [/]'
            ))-1

        function = list_function.menu_botnet[menu]

        function(
            accounts.connect_sessions,
            accounts.initialize
            )

    except KeyboardInterrupt:
        console.print('\n<https://t.me/pepe_devs>')
        sys.exit()

    except Exception as error:
        console.print(error)
        botnet_main()

botnet_main()
