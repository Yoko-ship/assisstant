import os
from dotenv import load_dotenv
from google import genai
import requests,json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from quickstart import GoogleCalendar
from db import Db
from speech import Speech

load_dotenv()
class Helper:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.google_calendar = GoogleCalendar()
        self.db = Db()
        self.speech = Speech('ru')
        self.category = ("Выберите категорию || погода , чат , календарь: ")
        self.speech.play_voice_assisstant_speech(self.category)
        self.voice_input = self.speech.speak()
        self.db.connecting()
        if self.voice_input == "погода":
            self.show_weather()
        elif self.voice_input == "чат":
            self.chat_bot()
        elif self.voice_input == "календарь":
            self.calendar_init()
        # if self.category.lower() == "/weather":
        #     self.show_weather()
        # elif self.category.lower() == "/chat":
        #     self.chat_bot()
        # elif self.category.lower() == "/calendar":
        #     self.calendar_init()

    def chat_bot(self):
        self.running = True
        while self.running:

            self.user_format = self.speech.play_voice_assisstant_speech("Выберите формат, текст или voice: ")
            user_voice = self.speech.speak()
            print(user_voice)
            if user_voice == "voice":
                self.user_input = self.speech.speak()
            else:
                self.user_input = input("Введите запрос: ")
            try:
                self.response = self.client.models.generate_content(model="gemini-2.0-flash-exp",contents=self.user_input)
                print(self.response.text.replace("*",""))
                self.speech.play_voice_assisstant_speech(self.response.text.replace("*",""))

            except ValueError:
                print("Пожалуста введите запрос")
            finally:
                self.leave = input(" Нажмите 'y' если хотите выйти: ")
                if self.leave.lower() == "y":
                    self.running = False
    def show_weather(self):
        self.weather_run = True
        while self.weather_run:

            self.user_city = input("Напишите город: ")
            self.weather_api = os.getenv("WEATHER_API")
            try:

                self.url = f"http://api.weatherapi.com/v1/current.json?key={self.weather_api}&q={self.user_city}&days=1&aqi=no&alerts=no"
                self.request = requests.get(self.url)
                self.weather_data = self.request.json()            
                self.city_name = self.weather_data["location"]["name"]
                self.country = self.weather_data["location"]["country"]
                self.localtime = self.weather_data["location"]["localtime"]
                self.temperature = round(self.weather_data["current"]["temp_c"])
                self.feels_like = round(self.weather_data["current"]["feelslike_c"])
                print(f" Город: {self.city_name} \n Страна {self.country} \n Местное время {self.localtime} \n Температура {self.temperature}°C \n Ощущается как {self.feels_like}°C")

            except KeyError:
                print("Пожалуста напишите правильно город ")
            finally:
                    self.leaving = input(" Нажмите 'y' если хотите выйти: ")
                    if self.leaving.lower() == "y":
                        self.weather_run = False

    def calendar_init(self):
        self.user_info = input("Добавить напоминание - /add || Удалить напоминание - /dell: ")
        if self.user_info.lower() == "/add": 
            self.add_calendar()
        elif self.user_info.lower() == "/dell":
            self.dell_calendar()

    def add_calendar(self):
        running = True
        while running:

            self.summary = input("Текст:")
            self.description = input("Описания: ")
            self.startData = input("Start-Data(год-месяц-день): ")
            self.startTime = input("Start-Time: (hh:mm): ")
            self.endData = input("End-Data(год-месяц-день): ")
            self.endTime = input("End-Time(hh:mm): ")
            self.startCalculated = self.startData + "T" + self.startTime +  ":00+05:00"
            self.endCalculated = self.endData + "T" + self.endTime + ":00+05:00"
            try:
                self.id = self.google_calendar.add_events(self.summary,self.description,self.startCalculated,self.endCalculated,"Asia/Tashkent")
                self.db.add_table(self.summary,self.id)
            except Exception:
                print("Пожалуста заполните все данные правильно")
            finally:
                leaving = input("Нажмите 'y' если хотите выйти || /dell чтобы удалить напоминания: ")
                if leaving.lower() == "y":
                    running = False
                if leaving.lower() == "/dell":
                    self.dell_calendar()
                    running = False

    
    def dell_calendar(self):
        running = True
        while running:

            check_tables = self.db.show_tables()
            if check_tables:
                user_input = input("Введите id задачи: ")
                try:
                    self.db.dell_table(user_input)
                    self.google_calendar.remove_events(user_input)
                except Exception:
                    print("Пожалуста заполните все поле правильно")
                finally:
                    leaving = input("Нажмите y чтобы выйти: ")
                    if leaving.lower() == "y":
                        running = False
            else:
                print("Напоминание отсутствуют,пожалуста добавьте их")
                running = False
gemini = Helper()

