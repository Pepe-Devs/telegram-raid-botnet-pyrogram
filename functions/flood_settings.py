from functions.flood import FloodChat
from settings.function import SettingsFunction

class FloodSettings(SettingsFunction):
    """flood to chat"""

    def __init__(self, connect_sessions, initialize):
        flood = FloodChat(connect_sessions, initialize)
        flood.ask()

        flood.start_process_flood()
