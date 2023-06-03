import time
import os
import json
import threading

import chat_gpt_model
import config
from twitch_model import Bot
import voice_model
import asyncio


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
        day_fact_interval = 60
        interval = 3  # Интервал времени в секундах
        start_time = time.time()
        while True:
            def skip():
                # Пауза на интервал времени
                time.sleep(interval)

            elapsed_time = time.time() - start_time
            print(elapsed_time)
            with open(config.ai_text_json, 'r', encoding='utf-8') as f:  # открыли файл с данными
                ai_text = json.load(f)  # загнали все, что получилось в переменную
                twitch_message_json = ai_text['twitch_message']
                day_fact_json = ai_text['day_fact']
                ''' проверяем на факт дня '''
                if day_fact_json['done'] == 'true':
                    print('запросила новый факт дня')
                    ''' доработать тут нужно запросить новый day_fact_json '''
                    start_time = day_fact_interval
                    skip()
                    continue
                if elapsed_time >= day_fact_interval:  # если прошло 60 секунд, ебашим факт дня
                    ''' доработать тут нужно вызвать озвучение '''
                    print('выдала новый факт дня')
                    start_time = day_fact_interval  # Сбросить начальное время
                ''' проверяем, что ответы пользователей имеют ответ '''
                if twitch_message_json["message_1"]["done"] == "False":
                    if twitch_message_json["message_1"]["ai_response"] == "":
                        #run_chat_dpt_model("twitch_message", "message_1")  # отправляем в GPT
                        print('запросила ответ на сообщение с твича')
                    else:
                        # озвучим
                        print('Озвучила сообщение с твича 1')
                        skip()
                        continue
                    if twitch_message_json["message_2"]["done"] == "False":
                        if twitch_message_json["message_2"]["ai_response"] == "":
                            print('запросила ответ на сообщение с твича 2')
                            run_chat_dpt_model("twitch_message", "message_2")  # отправляем в GPT
                        else:
                            # озвучим
                            print('Озвучила сообщение с твича 2')
                            skip()
                            continue
            skip()


    # Создание событийного цикла (event loop)
    loop = asyncio.get_event_loop()
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=asyncio.run, args=(run_bot(),))
    bot_thread.start()
    # Запуск функции do_something() в основном потоке
    do_something()
    # Ожидание завершения потока с ботом
    bot_thread.join()
