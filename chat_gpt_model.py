import config

import time

import usesless
import theb

gpt_model = config.gpt_model
send_message_prompt = open("v_prompt\send_message_prompt.txt", "r", encoding="utf-8")
send_message_prompt = send_message_prompt.read()
get_random_fact_prompt = open("v_prompt\get_random_fact_prompt.txt", "r", encoding="utf-8")
get_random_fact_prompt = get_random_fact_prompt.read()
dialogue = []
us_message_id = ''


def theb_gen(prompt):
    response = theb.Completion.create(prompt)
    response = ''.join(token for token in response)
    if response == '':
        time.sleep(2)  # Ожидаем 2 секунды
        response = theb_gen(prompt)  # Рекурсивно вызываем функцию send_message()
    return response


def usesless_gen(prompt):
    global us_message_id
    api_response = usesless.Completion.create(prompt=prompt, parentMessageId=us_message_id)
    response = api_response['text']  # получаем текст
    us_message_id = api_response["id"]  # для сохранения лога
    return response


def generate_text(mode, message_id):
    prompt = 0
    user = 0
    # проверяем в первую очередь по моду
    if mode == 'twitch_message': # если мод twitch_message проверяем prompt и берем стандартный прессет для этого режима
        print('Генерим сообщение в режиме twitch_message')
        if not prompt:
            return "Игнор"
        prompt_base = send_message_prompt  # базовый prompt
        # запишем немного контекста из нашего dialogue[]
        context = "\n".join([f"(Вопрос пользователя: {p}\nВасилиса: {r})" for p, r in dialogue[-3:]])
        # сформируем гига чад вопрос с добавлением пользователя
        prompt_dev = ("\nВопрос от " + user + ":" + prompt)
        # а вот это уже реально гига чад prompt
        giga_prompt = prompt_base + context + prompt_dev
        print('отправил запрос')
        if gpt_model == 'theb':
            response = theb_gen(giga_prompt)
        else:
            response = usesless_gen(giga_prompt)
        print('получил запрос')
        lines = response.splitlines()  # нам нужно разобрать некоторое дерьмо
        for line in lines:
            try:  # пытаемся сделать более менее красивый текст
                name, content = line.split(":", maxsplit=1)
                if name.strip() == "Василиса":
                    response = content.strip()
            except ValueError:  # тут по классике, видим ошибку - даем игнор
                response = 'Игнор'
        return response
        dialogue.append((prompt, response))  # сохраняем для контекста
    elif mode == 'day_fact':  # если мод day_fact берем стандартный прессет для этого режима
        print('Генерим day_fact')
        prompt = get_random_fact_prompt
        print('отправил запрос')
        if gpt_model == 'theb':
            response = theb_gen(prompt)
        else:
            response = usesless_gen(prompt)
        print('получил запрос')
        response = response.splitlines()  # разбиваем сразу
        return response
    else:
        return 'Игнор'







#print(generate_text('day_fact', '', ''))