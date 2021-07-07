from obswebsocket import obsws, requests
import soundcard as sc
import speech_recognition as sr
import numpy
import sounddevice as sd
from func_timeout import func_set_timeout
from scipy.io.wavfile import read
import wave


class Doppelganger:
    def __init__(self, ws_host, ws_port, ws_password):
        self.websocket = obsws(ws_host, ws_port, ws_password)
    def switch_idle(self):
        self.websocket.connect()
        self.websocket.call(requests.SetCurrentScene('doppelganger_idle'))
        self.websocket.disconnect()
    def switch_yes(self):
        self.websocket.connect()
        self.websocket.call(requests.SetCurrentScene('doppelganger_yes'))
        self.websocket.disconnect()
    def switch_hello(self):
        self.websocket.connect()
        self.websocket.call(requests.SetCurrentScene('doppelganger_hello'))
        self.websocket.disconnect()
    def switch_manual(self):
        SAMPLERATE, ALERT = read("alarm.wav")
        with wave.open("alarm.wav", 'rb') as ALARM:
            SAMPLERATE = ALARM.getframerate()
        sc.all_speakers()[0].play(numpy.array(ALERT) / numpy.max(ALERT), samplerate=SAMPLERATE)


@func_set_timeout(5)
def mic_to_text(recognizer:sr.Recognizer, mic:sr.Microphone):
    with mic as src:
        recognizer.adjust_for_ambient_noise(src)
        audio = recognizer.listen(src)
    response = { 
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def list_sound_devices():
    print(sd.query_devices())
