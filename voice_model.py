import pyaudio
from speechkit import Session, SpeechSynthesis
import os
import config

# default audio rate
sample_rate = 48000

# yandex speechkit
oauth_token = config.yandex_oauth_token
catalog_id = config.yandex_catalog_id
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
synthesizeAudio = SpeechSynthesis(session)


# с помощью танцев с бубном воспроизводим звук
def play_audio(audio_data, num_channels=1,
                                sample_rate=sample_rate, chunk_size=6000) -> None:
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=sample_rate,
        output=True,
        frames_per_buffer=chunk_size
    )

    try:
        for i in range(0, len(audio_data), chunk_size):
            stream.write(audio_data[i:i + chunk_size])
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def yandex_tts(response):
    # получаем и записываем respone в текстовой файл для вывода в obs
    print('AI VOICE: ' + response)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text_path = os.path.join(script_dir, 'v_for_stream', 'response_vasilis.txt')
    os.makedirs(os.path.dirname(text_path), exist_ok=True)
    # Wrap the response text to multiple lines
    with open(text_path, 'w', encoding='utf-8') as file:
        file.write(response)

    if config.enable_voice:
        # синтезируем голос в speechkit
        audio_data = synthesizeAudio.synthesize_stream(
            text=response,
            voice='alena',
            format='lpcm',
            sampleRateHertz=sample_rate
        )

        # Воспроизводим синтезированный файл если в конфиге стоит true
        play_audio(audio_data, sample_rate=sample_rate)
