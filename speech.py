import speech_recognition,pyttsx3

class Speech:
    def __init__(self,recognition_language):
        self.recognition_language = recognition_language
        self.ttsEngine = pyttsx3.init()

    def speak(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.voice_input = self.record_and_recognize_audio()
        self.setup_assistant_voice()
        return self.voice_input

    def setup_assistant_voice(self):
        voices = self.ttsEngine.getProperty("voices")
        self.ttsEngine.setProperty("voice",voices[0].id)

    def play_voice_assisstant_speech(self,text_to_speech):
        self.ttsEngine.say(str(text_to_speech))
        self.ttsEngine.runAndWait()
    
    def record_and_recognize_audio(self,*args:tuple):
        with self.microphone:
            self.recognized_data = ""
            #* регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone,duration=2)
            try:
                print("Listening ...")
                audio = self.recognizer.listen(self.microphone,5,5)

            except speech_recognition.WaitTimeoutError:
                print("Проверьте пожалуста что у вас включен микрофон")
                return
            
            #* Использование online-распознание речи Google
            try:
                print("Started recognizing ")
                self.recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()


            except speech_recognition.UnknownValueError:
                pass
            except speech_recognition.RequestError:
                print("Проверьте подключение к интернету")
                
            return self.recognized_data

