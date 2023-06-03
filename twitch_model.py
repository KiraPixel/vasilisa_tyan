from twitchio.ext import commands
import json
import config

token = config.twitch_token


def add_message_to_json(text, user):
    with open(config.ai_text_json, 'r', encoding='utf-8') as f:  # открыли файл с данными
        data = json.load(f)

    for message_num, message_data in data['twitch_message'].items():
        if message_data['done'] != 'True':
            continue

        new_message = {
            "text": text,
            "ai_response": "response",
            "user": "@" + user,
            "done": "Response"
        }
        data['twitch_message'][message_num] = new_message
        break

    with open(config.ai_text_json, 'w', encoding='utf-8') as f:  # открыли файл с данными
        json.dump(data, f, ensure_ascii=False, indent=4)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=config.twitch_token, prefix='?', initial_channels=['kirapixel'])

    async def event_ready(self):
        print(f'Авторизация успешна | {self.nick}')
        print(f'ID Пользователя | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        add_message_to_json(message.content, message.author.name)
        return


# bot = Bot()
# bot.run()