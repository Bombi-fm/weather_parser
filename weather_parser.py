import re
import datetime
import requests
from bs4 import BeautifulSoup


def month_converter(date):
    mtn = {' января': '01',
           ' февраля': '02',
           ' марта': '03',
           ' апреля': '04',
           ' мая': '05',
           ' июня': '06',
           ' июля': '07',
           ' августа': '08',
           ' сентября': '01',
           ' октября': '10',
           ' ноября': '11',
           ' декаря': '12'}
    for key in mtn:
        if key in date:
            date = date.replace(key, mtn[key])
            date = datetime.date(year=datetime.date.today().year, month=int(date[-2:]), day=int(date[:-2]))
            return str(date)


class WeatherMaker:

    def __init__(self):
        pass

    def get_weater(self):
        response = requests.get("https://meteoinfo.ru/forecasts5000/russia/arkhangelsk-area/severodvinsk")

        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            ###даты
            list_of_alldates = html_doc.find_all('nobr')
            list_of_dates = []
            re_date = r'\d{1,2}\s(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'
            for date in list_of_alldates:
                if re.search(re_date, str(date)):
                    date = str(date)
                    date = date.replace('<nobr>', '')
                    date = date.replace('</nobr>', '')
                    date = month_converter(date)
                    list_of_dates.append(date)



            ### температура днем
            list_of_values = html_doc.find_all('span', {'class': 'fc_temp_short'})
            list_of_values = list_of_values[::2]
            list_of_temperatures = []

            for temperature in list_of_values:
                result = re.findall('[-]*\d\d*', str(temperature))
                list_of_temperatures.append(result[0])

            ### типы погоды
            list_of_types = html_doc.find_all('div', {'class': 'fc_small_gorizont_ww'})
            types_of_weather = []

            re_weather_type = r'title=".*"[/]'
            for type_of_weather in list_of_types:
                if re.search(re_weather_type, str(type_of_weather)):
                    type_of_weather = str(type_of_weather)
                    result = re.findall(re_weather_type, type_of_weather)
                    type_of_weather = result[0][:-2]
                    type_of_weather = type_of_weather.replace('title="', '')
                    types_of_weather.append(type_of_weather)

            types_of_weather = types_of_weather[0:7]

            forecast = []
            for type_of_weather, date, temperature in zip(types_of_weather, list_of_dates, list_of_temperatures):
                forecast.append({'weather': type_of_weather, 'temperature': temperature, 'date': date})

            return forecast

    def run(self):
        return self.get_weater()
