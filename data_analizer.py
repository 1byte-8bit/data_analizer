import sqlite3
from datetime import datetime, timedelta


class DataAnalyzer:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor = None
        self.milliseconds_start = None
        self.milliseconds_current = None

    def connect_to_database(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def disconnect_from_database(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_time_range(self, current_timestamp, time_interval):
        # Вычисление временной метки начала интервала
        start_timestamp = current_timestamp - time_interval

        # Временная метка в миллисекундах
        self.milliseconds_start = int(start_timestamp.timestamp() * 1000)
        self.milliseconds_current = int(current_timestamp.timestamp() * 1000)

        # пустышка
        self.milliseconds_start = 1686242932196

    def analyze_data(self, channel_number: int, start_time: datetime, time_interval: timedelta):

        # Получаем временной диапазон
        self.get_time_range(start_time, time_interval)

        # Подключение к базе данных
        self.connect_to_database()

        self.cursor.execute("""
            SELECT value
            FROM data 
            WHERE channel = ? AND timestamp BETWEEN ? AND ?
            ORDER BY value
            """, (channel_number, self.milliseconds_start, self.milliseconds_current))

        # Извлечение результатов запроса
        result = self.cursor.fetchall()

        # Закрытие соединения с базой данных
        self.disconnect_from_database()

        length = len(result)
        if result:
            if result and length > 2:
                min = float(result[0][0]) if result and result[0] else 0
                max = float(result[-1][0]) if result and result[-1] else 0
                avg = float(result[length // 2][0]) if result and result[length // 2] else 0
                print("Минимальное значение:", min)
                print("Максимальное значение:", max)
                print("Среднее значение:", avg)
            else:
                min = float(result[0][0]) if result and result[0] else 0
                max = float(result[-1][0]) if result and result[-1] else 0
                print("Минимальное значение:", min)
                print("Максимальное значение:", max)
        else:
            print("Пустой результат")


# Использование класса DataAnalyzer
db_path = "data.db"
channel = 39
# Текущая временная метка
current_time = datetime.now()
# Временной интервал
interval = timedelta(minutes=5)

analyzer = DataAnalyzer(db_path)
analyzer.analyze_data(channel, current_time, interval)
