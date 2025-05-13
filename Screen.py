from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock, mainthread

import requests
import pickle
import logging
from datetime import datetime
import json

from ccolor import *

logger = logging.getLogger(__name__)

class Screen(MDScreen):
    '''здесь я создаю второй экран с именем Screen'''
        
    def __init__(self, room=536, url='192.168.1.33:8066', **kwargs):      # на этом экране я делаю все то же самое, что и на главном экране, чтобы иметь возможность переключаться вперед и назад
        super(Screen, self).__init__(**kwargs)
        self.room = room
        self.url = url
        
        '''Полоса прогресса'''
        def post_progress(req, current_size, total_size):
            #  current_size текущий размер
            #  total_size общий размер
            progress.value = (total_size - current_size) / total_size
            logger.info(f'полоса прогресса: {progress.value}')   

        """В случае успеха создаётся файл pickle с записью даты в виде строки и выполняется функция checkbox1_state"""
        @mainthread
        def success(req, result):
            global room_536
            logger.info(f'Данные отправленны!!. Result: {result}. Поздравляю!!')
            error_text.hint_text = ''
            flag = {f"room_{self.room}": str(datetime.now())}
            with open('my_exe_client/data_states.pickle', 'wb') as f:
                first = pickle.dumps(flag)
                f.write(first)
            logger.info(f'Появился pickle!')
            checkbox1_state(self)

        """Данные на сервер на сервер переданы, но есть проблема"""
        @mainthread
        def failure(req, result):
            logger.info(f'Данные обработаны. Но есть нюанс: {result}')
            error_text.hint_text = str(result)

        def load(data, url=self.url):          
            """В случае неудачной передачи на сервер"""
            @mainthread
            def on_error(req, error):
                logger.info(f"Ошибка: {error}")
                error_text.hint_text = 'Нет связи с сервером'
                Clock.schedule_once(lambda dt: load(data, url), 5) # Повторная попытка через 5 секунд

            logger.info(f'Попытка отправить запрос на сервер')    
            if is_network_available():
                error_text.hint_text = 'Идёт загрузка...'
                logger.error(f'Загрузка на сервер')
                req = UrlRequest(f'http://{url}/setdata/', 
                                    req_body=data, 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_progress=post_progress,
                                    on_error=on_error)
            else:
                logger.error(f'Интернета нет')
                error_text.hint_text = "Нет подключения к сети. Попробуем позже..."
                Clock.schedule_once(lambda dt: load(data, url), 5) # Повторная попытка через 5 секунд


            """Проверка наличия интернета"""
        def is_network_available():
            logger.info(f'Проверка наличия интернета')
            try:
                response = requests.head("http://www.google.com", timeout=5)
                logger.info(f'Интернет есть')
                return response.status_code == 200
            except:
                return False

        """Логика POST запроса на сервер с помощью асинхронного UrlRequest"""
        def on_confirm(self):
            data = {"humidity": humidity_text.text, "temperature": temperature_text.text, "creation_date": str(datetime.now())}
            data = json.dumps(data)    
            load(data)

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

        '''Реакция смайла на pickle'''
        def checkbox1_state(self):
            global room_536
            try:
                with open('my_exe_client/data_states.pickle', 'rb') as f:
                    logger.info(f'Считывание pickle!')
                    first = f.read()
                    flag = pickle.loads(first)
                    tap_flag = flag[f"room_{self.room}"]
            except FileNotFoundError:
                pass
            logger.info(f'Проверка условия для смайла')
            if not tap_flag or datetime.fromisoformat(tap_flag).date() != datetime.now().date():
                checkbox1.state = 'down'    #  Реакция смайла 
            else:
                checkbox1.state = 'normal'  #  Реакция смайла 

        """Основной макет скрина
        Без него topbar спустится вниз"""
        layout = MDBoxLayout(orientation="vertical")  

        '''Создание панели инструментов в классе Screen'''
        topbar = MDTopAppBar(title=f"№ {self.room} 'Входной материальный шлюз'",
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
        
        '''Лейбл возврата ошибок'''
        error_text = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.2},
                                 mode="line",
                                 hint_text="",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 max_text_length=16,
                                 active_line=False,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="",
                                 readonly=True)  
        

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
        
        layout.add_widget(topbar)
        layout.add_widget(content)
        content.add_widget(progress)
        content.add_widget(checkbox1)
        self.add_widget(humidity_text)
        self.add_widget(temperature_text)
        self.add_widget(error_text)        
        self.add_widget(confirm)
        self.add_widget(layout) 


        """Периодическая активация exist"""
        Clock.schedule_interval(exist, 1/60)

    def to_main_scrn(self, *args):  # Вместе с нажатием кнопки он передает информацию о себе.
        # Чтобы не выдать ошибку, я добавляю в функцию *args
        self.manager.current = 'Main'  # Выбор экрана по имени (в данном случае по имени "Main")
        return 0