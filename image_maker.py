import os
import re

import cv2


def weather_recognizer(weather_str):
    weather_choice = {'солнечно': {'blue': 0, 'green': 255, 'red': 255,
                                   'weather_img': 'external_data/weather_img/sun.jpg'},
                      'дождь': {'blue': 255, 'green': 0, 'red': 0,
                                'weather_img': 'external_data/weather_img/rain.jpg'},
                      'снег': {'blue': 255, 'green': 255, 'red': 0,
                               'weather_img': 'external_data/weather_img/snow.jpg'},
                      'облачно': {'blue': 105, 'green': 105, 'red': 105,
                                  'weather_img': 'external_data/weather_img/cloud.jpg'}}

    re_clouds = r'(О|о)блачн'
    re_snow = r'(С|с)нег'
    re_sun = r'(С|с)олн'
    re_rain = r'(Д|д)ожд'

    if re.search(re_sun, weather_str):
        return weather_choice['солнечно']['blue'], weather_choice['солнечно']['green'], weather_choice['солнечно'][
            'red'], cv2.imread(weather_choice['солнечно']['weather_img'])
    elif re.search(re_rain, weather_str):
        return weather_choice['дождь']['blue'], weather_choice['дождь']['green'], weather_choice['дождь'][
            'red'], cv2.imread(weather_choice['дождь']['weather_img'])
    elif re.search(re_snow, weather_str):
        return weather_choice['снег']['blue'], weather_choice['снег']['green'], weather_choice['снег'][
            'red'], cv2.imread(weather_choice['снег']['weather_img'])
    elif re.search(re_clouds, weather_str):
        return weather_choice['облачно']['blue'], weather_choice['облачно']['green'], weather_choice['облачно'][
            'red'], cv2.imread(weather_choice['облачно']['weather_img'])
    else:
        print(f"Тип погоды распознать неудалось - {weather_str}")


def gradient(blue, green, red, img, line_number, width, start_point, end_point):
    while line_number < width:
        color = (blue, green, red)
        cv2.line(img, start_point, end_point, color, thickness=3)
        line_number += 3
        start_point = (line_number, 0)
        end_point = (line_number, width)

        if blue < 255:
            blue += 1.5
        if green < 255:
            green += 1.5
        if red < 255:
            red += 1.5


class ImageMaker:

    def __init__(self, weather_list):
        self.img = ''
        self.weather_type = ''
        self.weather_list = weather_list
        self.path = ''

    def run(self):
        folder_name = input('>>> Укажите название папки в которую вы хотите сохранить ваши панели.\n'
                            '>>> ')
        self.path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(self.path, exist_ok=True)
        self.plate_painter()

    def plate_painter(self):
        for weather_day in self.weather_list:
            self.paint_plate(weather_day)

    def paint_plate(self, weather_day):
        img = cv2.imread('external_data/probe.jpg')
        height, width = img.shape[:2]
        line_number = 0
        start_point = (line_number, 0)
        end_point = (line_number, height)
        print(weather_day['weather'])
        blue, green, red, weather_img = weather_recognizer(weather_day['weather'])

        gradient(blue=blue, green=green, red=red, img=img, line_number=line_number, width=width,
                 start_point=start_point, end_point=end_point)

        img[50:50 + weather_img.shape[0], 300:300 + weather_img.shape[1]] = weather_img

        img = cv2.putText(img, weather_day['date'].format('utf-8'), org=(30, 50),
                          fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                          color=(0, 0, 0),
                          thickness=2)
        img = cv2.putText(img, weather_day['weather'].format('utf-8'), org=(30, 100),
                          fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                          color=(0, 0, 0),
                          thickness=2)
        img = cv2.putText(img, weather_day['temperature'].format('utf-8'), org=(30, 150),
                          fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                          color=(0, 0, 0),
                          thickness=2)

        cv2.imwrite(os.path.join(self.path, weather_day['date'] + '.jpg'), img)
