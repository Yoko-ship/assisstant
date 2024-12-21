import psycopg2
from dotenv import load_dotenv
import os
class Db:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv("USER") 
        self.host = os.getenv("HOST")
        self.database = os.getenv("DATABASE")
        self.password = os.getenv("PASSWORD")
        self.port = os.getenv("PORT")
    
    
        self.connection = psycopg2.connect(
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def connecting(self):
        query = """
                CREATE TABLE IF NOT EXISTS ai(
                ID SERIAL PRIMARY KEY,
                Summary VARCHAR NOT NULL,
                TextId VARCHAR NOT NULL
                )"""
        self.cursor.execute(query)



    def add_table(self,summary,id):
        queryTable = "INSERT INTO ai(Summary,TextId) VALUES(%s,%s)"
        self.cursor.execute(queryTable,[summary,id])
        print("Данные успешно записаны")
    
    def dell_table(self,id):
        queryTable = "DELETE FROM ai WHERE TextId = %s"
        self.cursor.execute(queryTable,[id])

    def show_tables(self):
        queryTable = "SELECT Summary,TextId FROM ai"
        self.cursor.execute(queryTable)
        all_information = self.cursor.fetchall()
        if all_information:
            for information in all_information:
                print(f"Задача: {information[0]} \n Ид: {information[1]} ")

            return all_information
        else:
            return None