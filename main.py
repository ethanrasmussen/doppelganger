import functions as f
import speech_recognition as sr
import time


with open('obsws_config.txt', 'r') as config:
    HOST, PORT, PASSWORD = config.read().split('\n')
    DOPPELGANGER = f.Doppelganger(HOST, PORT, PASSWORD)

print("DOPPELGANGER:")
print("To use this program, you will need to have all the installed pre-req's, and the following OBS video scenes:"
      "\n - 'doppelganger_idle'"
      "\n - 'doppelganger_yes'")
input("Press any key when you're ready to continue.")

print("What is your name? This will be used to alert you if your name is called. (Please capitalize first letter)")
your_name = str(input("Name: "))

yes_time = int(input("What is the duration (in seconds) of your 'yes' clip?:"))

hello_time = int(input("What is the duration (in seconds) of your 'hello' clip?:"))

# print("CHOOSE A SPEAKER FOR THE ALERT NOISE:")
# index = 0
# for speaker in sc.all_speakers():
#     print(f"{index} - ")
#     index +=1
# sp_index = int(input("Enter index: "))

print("AUDIO I/O DEVICES:")
f.list_sound_devices()
sd_index = int(input("Please enter the index/number for 'CABLE Output (VB-Audio Virtual , MME (2 in, 0 out)': "))
print("Creating instances...")
rec = sr.Recognizer()
mic = sr.Microphone(sd_index)

print("Initializing Doppelganger...")
DOPPELGANGER.switch_idle()

TIMES_NAME_SAID = 0
NAMES_SAID_TRIGGER = 5
running = True
while running:
    try:
        print("Collecting mic input...")
        transcript = f.mic_to_text(rec, mic)
        if transcript['success'] == False and transcript['error'] == "API unavailable":
            print("API UNAVAILABLE. UNABLE TO CONTINUE. EXITING PROGRAM.")
            running = False
        elif transcript['error'] == 'Unable to recognize speech':
            pass
        elif transcript['success'] == True:
            print(f"OUTPUT: {transcript['transcription']}")
            print("-----------------")
            if your_name in transcript['transcription'] or your_name.lower() in transcript['transcription'] or your_name.upper() in transcript['transcription']:
                TIMES_NAME_SAID += 1
                print(f"Your name has been said {TIMES_NAME_SAID} times...")
                if TIMES_NAME_SAID >= NAMES_SAID_TRIGGER:
                    print("Hey! They're calling your name!!")
                    print("Click any key to interrupt the alert.")
                    alerting = True
                    while alerting:
                        try:
                            DOPPELGANGER.switch_manual()
                        except KeyboardInterrupt:
                            alerting = False
                            break
                    input("Click another key to resume the program idle animation.")
                    DOPPELGANGER.switch_idle()
            elif "can you hear me" in transcript['transcription'] or 'is my audio working' in transcript['transcription']:
                print("Saying 'yes'...")
                DOPPELGANGER.switch_yes()
                time.sleep(yes_time)
                print("Switching back to idle...")
                DOPPELGANGER.switch_idle()
            elif "hi" in transcript['transcription'] or "hello" in transcript['transcription'] or "good morning" in transcript['transcription'] or "hey" in transcript['transcription'] or "what's up" in transcript['transcription'] or "what is up" in transcript['transcription']:
                print("Saying 'hello'...")
                DOPPELGANGER.switch_hello()
                time.sleep(hello_time)
                print("Switching back to idle...")
                DOPPELGANGER.switch_idle()
    except:
        pass