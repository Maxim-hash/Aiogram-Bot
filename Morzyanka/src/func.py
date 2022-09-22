import sqlite3
from random import randint
from config import bot_config, database

def morze_translate(text, lang):
    try:
        sqlite_connection = sqlite3.connect(database)
        cursor = sqlite_connection.cursor()
        result = ""
        items = list(text.lower())

        for item in items:
            sqlite_select_query = f"SELECT morse FROM '{lang}' WHERE word='{item}'"
            cursor.execute(sqlite_select_query)
            temp = cursor.fetchone()

            if(temp):
                result += temp[0] + "\x20"
            else:
                sqlite_select_query = f"SELECT morse FROM spec WHERE word='{item}'"
                cursor.execute(sqlite_select_query)
                temp = cursor.fetchone()
                if(temp):
                    result += temp[0] + "\x20"
                else:
                    lang = get_lang(bot_config.lang)
                    return (f"Язык для кодировки в код морзе установлен {lang[0]}, прошу вас смените раскладку на вашей клавиатуре или смените язык в найтройках используя команду\n/lang")
        cursor.close()
        
        return result
        
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if(sqlite_connection):
            sqlite_connection.close()

def get_words(lang):
    try:
        result = []
        sqlite_connection = sqlite3.connect(database)
        cursor = sqlite_connection.cursor()
        sqlite_length_db_query = f"SELECT COUNT(word) FROM {lang}Words"
        
        cursor.execute(sqlite_length_db_query)
        temp = cursor.fetchone()[0]

        j = randint(0, int(temp))
        sqlite_select_query = f"SELECT word FROM {lang}Words WHERE id='{j}'"
        cursor.execute(sqlite_select_query)
        word = cursor.fetchone()
        result.append(word[0])

        sqlite_connection.close()

        return result

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if(sqlite_connection):
            sqlite_connection.close()


def format(string):
    result = ""
    for i in string:
        if i != '.' and i != " ":
            result += "-"
        else:
            result += i

    return result

def check(expected:str, actual:str):
    word = format(morze_translate(expected, bot_config.lang))
    word = word[:-1]
    return word == actual
    
def get_records():
    try:
        z = 10
        sqlite_connection = sqlite3.connect(database)
        sqlite_get_records_query = f"SELECT * FROM records ORDER BY TOTAL_SCORE/SCORE DESC LIMIT {z};"
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_get_records_query)

        return cursor.fetchall()
    
        sqlite_connection.close()
        
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if(sqlite_connection):
            sqlite_connection.close()

def set_record(nickname:str, score:int, totalScore: int):
    try:
        sqlite_connection = sqlite3.connect(database)
        sqlite_set_record_query = f"INSERT INTO records (NICKNAME, SCORE, LANG, TOTAL_SCORE) VALUES ('{nickname}', '{score}', '{bot_config.lang}', '{totalScore}');"
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_set_record_query)
        sqlite_connection.commit()

        sqlite_connection.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if(sqlite_connection):
            sqlite_connection.close()

def get_lang(langCode):
    try:
        sqlite_connection = sqlite3.connect(database)
        sqlite_get_lang_query = f"SELECT lang FROM language WHERE langCode='{langCode}'"
        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_get_lang_query)

        return cursor.fetchone()

        sqlite_connection.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if(sqlite_connection):
            sqlite_connection.close()
