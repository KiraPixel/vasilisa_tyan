import time
import os
import threading

import chat_gpt_model
import config
from twitch_model import Bot
import voice_model
import asyncio
from ai_respone import twitch_message_1, twitch_message_2, day_fact_message


''' Ранеры. '''
def run_voice_model(text):
    voice_model.yandex_tts(text)


def run_chat_dpt_model(mode, message_id):
    text = chat_gpt_model.generate_text(mode, message_id)
    send_to_voice_model(text)


''' хранение потоков '''


# заранее прописываем потоки
voice_thread = None
chat_gpt_thread = None

''' API '''


def send_to_voice_model(text):
    global voice_thread
    voice_thread = threading.Thread(target=run_voice_model, args=(text,))  # Создаем поток с аргументом text
    voice_thread.start()  # Запускаем поток
    voice_thread.join()  # Ожидаем завершения потока


def send_to_chat_gpt_model(mode, prompt, user):
    global chat_gpt_thread
    chat_gpt_thread = threading.Thread(target=run_chat_dpt_model, args=(mode, prompt, user))  # Создаем поток с аргументом prompt
    chat_gpt_thread.start()  # Запускаем поток
    chat_gpt_thread.join()  # Ожидаем завершения потока


''' основной код '''
if __name__ == '__main__':
    print('start')

    # Создание корутины для запуска бота
    async def run_bot():
        bot = Bot()
        await bot.start()

    # Функция, которая будет выполняться в отдельном потоке
    def do_something():
        loop = asyncio.get_event_loop()
        ''' задаем всякое первичное '''
        day_fact_interval = 10
        interval = 3  # Интервал времени в секундах
        start_time = time.time()
        while True:
            def skip():
                # Пауза на интервал времени
                time.sleep(interval)

            elapsed_time = time.time() - start_time
            print(f'el_time = {elapsed_time} day_time = {day_fact_interval}' )
            if day_fact_message.done and not day_fact_message.await_response:
                chat_gpt_model.generate_text('day_fact', day_fact_message)
                start_time = time.time()
                skip()
                continue
            elif day_fact_message.await_response:
                start_time = time.time()
            elif day_fact_message.ai_done and elapsed_time >= day_fact_interval:
                voice_model.yandex_tts(day_fact_message.text)
                day_fact_message.ready()
                start_time = time.time()

            if not twitch_message_1.done:
                if twitch_message_1.ai_response is None and not twitch_message_1.await_response:
                    chat_gpt_model.generate_text('twitch', twitch_message_1)
                elif twitch_message_1.ai_response is not None:
                    voice_model.yandex_tts(twitch_message_1.ai_response)
                    twitch_message_1.message_complete()
            if not twitch_message_2.done:
                if twitch_message_2.ai_response is None and not twitch_message_2.await_response:
                    chat_gpt_model.generate_text('twitch', twitch_message_2)
                elif twitch_message_2.ai_response is not None:
                    voice_model.yandex_tts(twitch_message_2.ai_response)
                    twitch_message_2.message_complete()





    # Создание событийного цикла (event loop)
    loop = asyncio.get_event_loop()
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=asyncio.run, args=(run_bot(),))
    bot_thread.start()
    # Запуск функции do_something() в основном потоке
    do_something()
    # Ожидание завершения потока с ботом
    bot_thread.join()
