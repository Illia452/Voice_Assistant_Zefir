import os
import pyaudio
from google.cloud import texttospeech
from dotenv import load_dotenv


load_dotenv("../secret_data/apikey_tts.env")
api_key = os.getenv("API_KEY")
client_options = {"api_key": api_key}
client = texttospeech.TextToSpeechClient(client_options=client_options)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True)


streaming_config = texttospeech.StreamingSynthesizeConfig(
    voice=texttospeech.VoiceSelectionParams(
        name="uk-UA-Chirp3-HD-Charon",
        language_code="uk-UA",
    )
)

config_request = texttospeech.StreamingSynthesizeRequest(streaming_config=streaming_config)

text_iterator = [
    "Привіт усім! ",
    "Я є твій голосовий помічник. ",
    "Я можу говорити під час того як генерується текст. ",
    "Це може зробити нашу розмову більш живою."
]

def request_generator():
    yield config_request
    for text in text_iterator:
        yield texttospeech.StreamingSynthesizeRequest(
            input=texttospeech.StreamingSynthesisInput(text=text)
        )



try:
    streaming_responses = client.streaming_synthesize(request_generator())

    for response in streaming_responses:
        if response.audio_content:
            stream.write(response.audio_content)
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()