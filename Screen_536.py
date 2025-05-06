from kivymd.uix.button import MDRectangleFlatButton, MDRectangleFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock

import matplotlib.pyplot as plt
import logging
from datetime import datetime
import json

from ccolor import *
from data import data_549_mean

logger = logging.getLogger(__name__)

class Screen_536(MDScreen):
    '''здесь я создаю второй экран с именем Screen_536'''
    
    def __init__(self, **kwargs):      # на этом экране я делаю все то же самое, что и на главном экране, чтобы иметь возможность переключаться вперед и назад
        super(Screen_536, self).__init__(**kwargs)

        """Логика POST запроса на сервер с помощью асинхронного UrlRequest"""
        def on_confirm(self):

            def success(req, result):
                logger.info(f'Данные отправленны!!. Result: {result}. Поздравляю!!')
                checkbox1.state = 'normal'  #  Реакция смайла 

            def failure(req, result):
                logger.info(f'Данные обработаны. Но есть нюанс: {result}')

            def post_progress(req, current_size, total_size):
                #  current_size текущий размер
                #  total_size общий размер
                progress.value = (total_size - current_size) / total_size
                logger.info(f'полоса прогресса: {progress.value}')     


            data = {"humidity": humidity_text.text, "temperature": temperature_text.text, "creation_date": str(datetime.now())}
            data = json.dumps(data)

            logger.info(f'Попытка отправить запрос на сервер')

            try:
                req = UrlRequest('http://192.168.1.33:8066/setdata/', 
                                 req_body = data, 
                                 on_success=success, 
                                 on_failure=failure,
                                 on_progress=post_progress)
            except:
                logger.error(f'Ошибка. Что-то не так')

        """Валидация параметров ввода влажности и смена фокуса на температуру"""
        def on_error_humaditi(self):
            logger.info(f'Попытка ввода данных по влажности')
            try:
                humidity = float(humidity_text.text)
                humidity_text.text_validate_unfocus = True
                humidity_text.error = False
                temperature_text.helper_text = ''
                humidity_text.helper_text = ''
                if humidity <= 20 or humidity >= 60:
                    humidity_text.helper_text = "Влажность находится за пределом уровня тревоги"
                    humidity_text.error = True
                if humidity <= 15 or humidity >= 65:
                    humidity_text.helper_text = "Влажность находится за пределом уровень действия"   
                    humidity_text.error = True
                if humidity_text.focus == True:
                    temperature_text.focus = True
                humidity_text.flag = True
                logger.info(f'Успешная валидация ввода влажности')
            except:
                humidity_text.flag = False
                humidity_text.error = True
                humidity_text.text_validate_unfocus = False
                humidity_text.helper_text = 'Через точку, бро((' if ',' in humidity_text.helper_text else 'Цифры, бро(('
                logger.info(f'Неверный формат данных по влажности')                

        """Валидация параметров ввода температуры"""
        def on_error_temperature(self):
            logger.info(f'Попытка ввода данных по температуре')
            try:
                if humidity_text.flag:
                    temperature = float(temperature_text.text)
                    confirm.disabled = False
                    temperature_text.error = False
                    temperature_text.helper_text = ''
                    if temperature <= 17 or temperature >= 23:
                        temperature_text.helper_text = "Температура находится за пределом уровня тревоги"
                        temperature_text.error = True
                    if temperature <= 15 or temperature >= 25:
                        temperature_text.helper_text = "Температура находится за пределом уровень действия" 
                        temperature_text.error = True     
                    logger.info(f'Успешная валидация ввода температуры')
                else:
                    temperature_text.helper_text = 'Чё там по влажности?' 
            except:
                confirm.disabled = True
                temperature_text.error = True
                temperature_text.helper_text = 'Точка!!!' if ',' in temperature_text.helper_text else 'И тут цифры, бро(('
                logger.info(f'Неверный формат данных по температуре')   

        '''Периодическая проверка на пустые поля температуры и влажности'''
        def exist(self):
            if not humidity_text.text or not temperature_text.text:
                confirm.disabled = True
            if temperature_text.text == '':
                temperature_text.helper_text = ''
            if humidity_text.text == '':
                humidity_text.helper_text = ''   

        """Основной макет скрина
        Без него topbar спустится вниз"""
        second_layout = MDBoxLayout(orientation="vertical")  

        '''Создание панели инструментов в классе Screen'''
        topbar = MDTopAppBar(title=f"№ 536 'Входной материальный шлюз'",
                             left_action_items=[["home", self.to_main_scrn]])

        """Второй макет скрина"""
        content = MDStackLayout(adaptive_height=False,       
                                adaptive_width=False)
                   
        '''Лейбл для ввода влажности'''
        humidity_text = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.62},
                                 mode="rectangle",
                                 hint_text="Влажность",
                                 hint_text_color_normal = blue,
                                 icon_left_color_normal = blue,
                                 text_color_normal = blue,
                                 write_tab = False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="weather-hail",
                                 foreground_color=green,
                                 helper_text_mode = 'on_error',
                                 error = False, 
                                 on_text_validate=on_error_humaditi,
                                 fill_color_normal=green)   
        humidity_text.flag = False  # Флаг для валидации параметров влажности и температуры

        '''Лейбл для ввода температуры'''
        temperature_text = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.49},
                                 mode="rectangle",
                                 hint_text="Температура",
                                 hint_text_color_normal = blue,
                                 icon_left_color_normal = blue,
                                 text_color_normal = blue,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="temperature-celsius",
                                 foreground_color=green,
                                 helper_text_mode = 'on_error',
                                 error = False, 
                                 on_text_validate=on_error_temperature,
                                 fill_color_normal=green)

        '''Кнопка отправить данные'''
        confirm = MDRectangleFlatButton(text="Отправить",
                                 pos_hint={"center_x": 0.5, "center_y": 0.36},
                                 disabled=False,
                                 on_press=on_confirm)
        
        """Строка прогресса"""
        progress = MDProgressBar(value=0.2,
                                 max=1,
                                 back_color=(0, 0.5, 1, 0.2),
                                 color=(0, 0.5, 1, 1),
                                 orientation="vertical",
                                 reversed=False)
        
        """Смайл реагирующий на строку прогресса"""
        checkbox1 = CheckBox(size_hint=(0.1, 0.16), 
                             disabled=True, 
                             state = 'down',
                             background_checkbox_disabled_down="images/()().png",
                             background_checkbox_disabled_normal="images/Троль.png")

        second_layout.add_widget(topbar)
        second_layout.add_widget(content)
        content.add_widget(progress)
        content.add_widget(checkbox1)
        self.add_widget(humidity_text)
        self.add_widget(temperature_text)
        self.add_widget(confirm)
        self.add_widget(second_layout) 

        """Периодическая активация exist"""
        Clock.schedule_interval(exist, 1/60)
        
    def graf(self, *args):
        plt.plot(data_549_mean) # Построим простой график температур
        plt.ylabel('humidity_549')
        plt.legend(['humidity_549','temperature_549'], loc='upper left')
        plt.show()
        return

    def to_main_scrn(self, *args):  # Вместе с нажатием кнопки он передает информацию о себе.
        # Чтобы не выдать ошибку, я добавляю в функцию *args
        self.manager.current = 'Main'  # Выбор экрана по имени (в данном случае по имени "Main")
        return 0