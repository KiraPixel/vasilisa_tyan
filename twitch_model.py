from twitchio.ext import commands
import config
from ai_respone import twitch_message_1, twitch_message_2

token = config.twitch_token


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=config.twitch_token, prefix='?', initial_channels=['kirapixel'])

    async def event_ready(self):
        print(f'Авторизация успешна | {self.nick}')
        print(f'ID Пользователя | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        if twitch_message_1.done:
            twitch_message_1.new_message(message.content, message.author.name)
            print(1)
        elif twitch_message_2.done:
            twitch_message_2.new_message(message.content, message.author.name)
            print(2)

#bot = Bot()
#bot.run()