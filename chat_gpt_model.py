import config
import asyncio
import time
import evagpt4
import ai_respone


gpt_model = config.gpt_model
send_message_prompt = open("v_prompt\send_message_prompt.txt", "r", encoding="utf-8")
send_message_prompt = send_message_prompt.read()
get_random_fact_prompt = open("v_prompt\get_random_fact_prompt.txt", "r", encoding="utf-8")
get_random_fact_prompt = get_random_fact_prompt.read()


async def eva_get(prompt_base, prompt_user):
    model = evagpt4.Model()
    messages = [
            {"role": "system", "content": prompt_base},
            {"role": "user", "content": prompt_user}
        ]
    full_text = await model.ChatCompletion(messages)
    return full_text


def generate_text(mode, obj_message):
    if mode == 'twitch':
        obj_message.set_await_response()
        prompt_base = send_message_prompt  # базовый prompt
        prompt_user = ("\nВопрос от " + obj_message.user + ":" + obj_message.text)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(eva_get(prompt_base, prompt_user))
        obj_message.set_ai_response(result)
    elif mode == 'day_fact':
        obj_message.set_await_response()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(eva_get(get_random_fact_prompt, 'придумай какой-нибдб факт дня или расскажи историю о себе'))
        obj_message.set_text(result)