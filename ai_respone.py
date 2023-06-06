class TwitchMessage:
    def __init__(self):
        self.text = ''
        self.user = ''
        self.ai_response = ''
        self.await_response = False
        self.done = True

    def new_message(self, text, user):
        self.text = text
        self.user = user
        self.ai_response = None
        self.done = False

    def set_ai_response(self, ai_response):
        self.await_response = False
        self.done = False
        self.ai_response = ai_response

    def set_await_response(self):
        self.await_response = True
        self.done = False

    def message_complete(self):
        self.text = ''
        self.ai_response = None
        self.user = ''
        self.done = True


class DayFact:
    def __init__(self):
        self.text = ''
        self.await_response = False
        self.ai_done = False
        self.done = True

    def set_await_response(self):
        self.await_response = True
        self.ai_done = False
        self.done = False

    def set_text(self, text):
        self.text = text
        self.await_response = False
        self.ai_done = True
        self.done = False

    def ready(self):
        self.done = True


twitch_message_1 = TwitchMessage()
twitch_message_2 = TwitchMessage()
day_fact_message = DayFact()