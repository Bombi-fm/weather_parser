import peewee
from datetime import timedelta, datetime

database = peewee.SqliteDatabase('weather_database.db')


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Date(BaseTable):
    name = peewee.DateTimeField()


class Day(BaseTable):
    date = peewee.ForeignKeyField(Date)
    type_of_weather = peewee.CharField()
    temperature = peewee.CharField()


database.create_tables([Date, Day])


class DataBaseHolder:

    def collect_weather(self, weather_list):
        for weather_day in weather_list:
            weather, created = Day.get_or_create(date=weather_day['date'],
                                                 defaults=dict(type_of_weather=weather_day['weather'],
                                                               temperature=weather_day['temperature']))
            if not created:
                weather.type_of_weather = weather_day['weather']
                weather.temperature = weather_day['temperature']
                weather.save()

    def gave_data_from_to(self, from_date, to_date):

        weather_list = []
        for day in Day.select().where(Day.date.between(from_date, to_date)):
            weather_list.append({'weather': day.type_of_weather, 'temperature': day.temperature, 'date': day.date_id})
        return weather_list

    def day_chek_in_range(self, from_date, to_date):

        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')

        for result in perdelta(from_date, to_date, timedelta(days=1)):
            if not self.day_chek(str(result.date())):
                return False

    def day_chek(self, date):

        if Day.select().where(Day.date_id == date):
            return True
        else:
            return False
