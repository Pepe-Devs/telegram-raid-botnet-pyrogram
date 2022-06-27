from rich.console import Console, Theme
from pyrogram import Client, idle
import asyncio
from rich.prompt import Prompt, Confirm
from rich.progress import track
from multiprocessing import Process
import sys
import random
import time


from settings.config import *
from functions.flood import FloodChat
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class FloodChatNoTrigger(FloodChat):
    """flood to chat no trigger(I'm redoing it)"""
