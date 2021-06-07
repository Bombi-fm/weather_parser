import db_of_weather
import image_maker
import weather_parser
from datetime import date, datetime, timedelta


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


class WeatherForecast:

    def __init__(self):
        pass

    def run(self):
        print('Добрый день!')
        self.dialog()

    def load_week(self):
        week_forecast_data = weather_parser.WeatherMaker().run()
        data_baser = db_of_weather.DataBaseHolder()
        data_baser.collect_weather(week_forecast_data)

    def dialog(self):
        print('*' * 50)
        print('Что я могу для вас сделать?')
        print('>>> 1. Добавить прогнозы погоды в баззу данных.(В пределах одной недели вперед) \n'
              '>>> 2. Получить прогнозы погоды за диапозон дат.(Если даты нет в базе и она за пределами недели '
              'вперед, то получить по ней прогноз не получится) \n')
        answer = input('>>> ')

        if answer == '1':
            self.adding_forecast()
        elif answer == '2':
            self.getting_forecast()

    def adding_forecast(self):
        from_date = input('Укажите диапозон дат в формате Y-m-d .\nОт>>> ')
        to_date = input('До>>> ')
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        db = db_of_weather.DataBaseHolder()

        for result in perdelta(from_date, to_date, timedelta(days=1)):
            answer = db.day_chek(date=str(result.date()))
            if not answer:
                self.load_week()
                print('Данные обновлены.')
                break

    def getting_forecast(self):

        from_date = input('Укажите диапозон дат в формате Y-m-d.\nОт>>> ')
        to_date = input('До>>> ')
        weather = db_of_weather.DataBaseHolder()
        if not weather.day_chek_in_range(from_date, to_date):
            self.load_week()
            print('*' * 50, '\nНе все нужные записи были в базе данных.\nБаза была обновлена на неделю вперед.\n',
                  '*' * 49)
        weather_list = weather.gave_data_from_to(from_date, to_date)
        self.work_with_forecast(weather_list)

    def work_with_forecast(self, weather_list):
        answer = input('Что будем делать с этими прогнозами?\n'
                       '>>> 1. Выведем на консоль.\n'
                       '>>> 2. Создадим карточки по этим прогнозам.\n'
                       '>>> 3. И то и другое.\n'
                       '>>> ')
        if answer == '1':
            self.print_weather_list(weather_list)
        elif answer == '2':
            self.make_weather_cards(weather_list)
        elif answer == '3':
            self.print_weather_list(weather_list)
            self.make_weather_cards(weather_list)
        else:
            pass

    def print_weather_list(self, weather_list):

        for day in weather_list:
            print(day['date'], day['weather'], day['temperature'])

    def make_weather_cards(self, weather_list):
        painter = image_maker.ImageMaker(weather_list)
        painter.run()
