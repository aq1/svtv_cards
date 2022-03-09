import pytz
from datetime import datetime

def log(some_str_logs, name, level="ERROR"):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')}. {name}: {level}: {some_str_logs}\n")