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
import logging
from datetime import datetime
import json


from ccolor import *

logger = logging.getLogger(__name__)

logger.propagate = False  # Что бы логи root не дублировались

class Screen(MDScreen):
    '''здесь я создаю второй экран с именем Screen'''
        
    def __init__(self, room, **kwargs):      # на этом экране я делаю все то же самое, что и на главном экране, чтобы иметь возможность переключаться вперед и назад
        super(Screen, self).__init__(**kwargs)
        self.room = str(room)
        self.flag_for_main = False

        """Основной макет скрина
        Без него topbar спустится вниз"""
        layout = MDBoxLayout(orientation="vertical")  

        """Второй макет скрина"""
        content = MDStackLayout(adaptive_height=False,       
                                adaptive_width=False)

        '''Создание панели инструментов в классе Screen'''
        self.topbar = MDTopAppBar(title=f"№ {self.room}",
                             left_action_items=[["home", self.to_main_scrn]])
                   
        '''Лейбл для ввода влажности'''
        self.humidity_text = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.62},
                                 size_hint_x=0.6,
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
                                 on_text_validate=self.on_error_humaditi,
                                 fill_color_normal=green)   
        self.humidity_text.flag = False  # Флаг для валидации параметров влажности и температуры

        '''Лейбл для ввода температуры'''
        self.temperature_text = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.49},
                                 size_hint_x=0.6,
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
                                 on_text_validate=self.on_error_temperature,
                                 fill_color_normal=green)

        '''Кнопка отправить данные'''
        self.confirm = MDRectangleFlatButton(text="Отправить",
                                 pos_hint={"center_x": 0.5, "center_y": 0.36},
                                 disabled=True,
                                 on_press=self.on_confirm)
        
        '''Лейбл возврата ошибок'''
        self.error_text = MDTextField(size_hint=(0.4, None),
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
        self.progress = MDProgressBar(value=0.2,
                                 max=1,
                                 back_color=(0, 0.5, 1, 0.2),
                                 color=(0, 0.5, 1, 1),
                                 orientation="vertical",
                                 reversed=False)
        
        """Смайл № 1 реагирующий на строку прогресса"""
        self.checkbox1 = CheckBox(size_hint=(0.1, 0.16), 
                             disabled=True, 
                             state = 'down',
                             background_checkbox_disabled_down="images/()().png",
                             background_checkbox_disabled_normal="images/Троль.png")     

        """Смайл № 2 реагирующий на строку прогресса"""
        self.checkbox2 = CheckBox(size_hint=(0.1, 0.16), 
                             disabled=True, 
                             state = 'down',
                             background_checkbox_disabled_down="images/()().png",
                             background_checkbox_disabled_normal="images/Троль.png")        

        layout.add_widget(self.topbar)
        layout.add_widget(content)
        content.add_widget(self.progress)
        content.add_widget(self.checkbox1)
        content.add_widget(self.checkbox2)
        self.add_widget(self.humidity_text)
        self.add_widget(self.temperature_text)
        self.add_widget(self.error_text)        
        self.add_widget(self.confirm)
        self.add_widget(layout) 

    def load(self, data):
        '''Загрузка данных на сервер'''      
      
        @mainthread
        def success(req, result):
            """В случае успеха создаётся файл pickle с записью даты в виде строки и выполняется функция checkbox1_state"""
            logger.info(f'Данные отправленны!!. Result: {result}. Поздравляю!!')
            self.error_text.hint_text = ''
            self.checkbox_state()

        @mainthread
        def failure(req, result):
            """Данные на сервер переданы, но есть проблема"""
            logger.info(f'Данные обработаны. Результат: {result}')
            self.error_text.hint_text = 'Ошибка со стороны сервера.'

        @mainthread
        def on_error(req, error):
            """В случае неудачной передачи на сервер"""
            logger.info(f"Ошибка: {error}")
            self.error_text.hint_text = 'Нет связи с сервером'
            Clock.schedule_once(lambda dt: self.load(data), 5) # Повторная попытка через 5 секунд
       
        def post_progress(req, current_size, total_size):
            '''Полоса прогресса'''
            #  current_size текущий размер
            #  total_size общий размер
            self.progress.value = (total_size - current_size) / total_size
            logger.info(f'полоса прогресса: {self.progress.value}')  

        def is_network_available():
            """Проверка наличия интернета"""
            logger.info(f'Проверка наличия интернета')
            try:
                response = requests.head("http://www.google.com")
                logger.info(f'Интернет есть')
                self.checkbox_state()
                return response.status_code == 200
            except:
                return False

        logger.info(f'Попытка отправить запрос на сервер')    
        if is_network_available():
            self.error_text.hint_text = 'Идёт загрузка...'
            logger.info(f'Загрузка на сервер')
            req = UrlRequest(f'http://{self.url}/setdata/', 
                                    req_body=data, 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_progress=post_progress,
                                    on_error=on_error)
        else:
            logger.error(f'Интернета нет')
            self.error_text.hint_text = "Нет подключения к сети. Попробуем позже..."
            Clock.schedule_once(lambda dt: self.load(data), 5) # Повторная попытка через 5 секунд

    def on_confirm(self, instance):
        """Подготовка POST запроса на сервер и отправка с помощью асинхронного UrlRequest"""              
        data = {"humidity": self.humidity_text.text, "temperature": self.temperature_text.text, "room": self.room, "login": self.login, "creation_date": str(datetime.now())}
        data = json.dumps(data)  
        self.load(data)      

    def on_error_humaditi(self, instance):
        """Валидация параметров ввода влажности и смена фокуса на температуру"""
        logger.info(f'Попытка ввода данных по влажности')
        try:
            humidity = float(self.humidity_text.text)
            self.humidity_text.text_validate_unfocus = True
            self.humidity_text.error = False
            self.temperature_text.helper_text = ''
            self.humidity_text.helper_text = ''
            if humidity <= 15 or humidity >= 65:
                self.humidity_text.helper_text = "Влажность находится за пределом уровень действия"   
                self.humidity_text.error = True
            elif humidity <= 20 or humidity >= 60:
                self.humidity_text.helper_text = "Влажность находится за пределом уровня тревоги"
                self.humidity_text.error = True
            if self.humidity_text.focus == True:
                self.temperature_text.focus = True
            self.humidity_text.flag = True
            logger.info(f'Успешная валидация ввода влажности')
        except:
            self.humidity_text.flag = False
            self.humidity_text.error = True
            self.humidity_text.text_validate_unfocus = False
            self.humidity_text.helper_text = 'Запишите данные через точку' if ',' in self.humidity_text.helper_text else 'Строчные символы не допускаются'
            logger.info(f'Неверный формат данных по влажности')                

    def on_error_temperature(self, instance):
        """Валидация параметров ввода температуры"""
        logger.info(f'Попытка ввода данных по температуре')
        try:
            if self.humidity_text.flag:
                temperature = float(self.temperature_text.text)
                self.confirm.disabled = False
                self.temperature_text.error = False
                self.temperature_text.helper_text = ''
                if temperature <= 17 or temperature >= 23:
                    self.temperature_text.helper_text = "Температура находится за пределом уровня тревоги"
                    self.temperature_text.error = True
                if temperature <= 15 or temperature >= 25:
                    self.temperature_text.helper_text = "Температура находится за пределом уровень действия" 
                    self.temperature_text.error = True     
                logger.info(f'Успешная валидация ввода температуры')
            else:
                self.temperature_text.helper_text = 'Некорректно введены данные по влажности' 
        except Exception as e:
            self.confirm.disabled = True
            self.temperature_text.error = True
            self.temperature_text.helper_text = 'Запишите данные через точку' if ',' in self.temperature_text.helper_text else 'Строчные символы не допускаются'
            logger.info(f'Ошибка: {e}')   

    def checkbox_state(self):
        '''Реакция смайлов'''
        @mainthread
        def on_success(req, result):
            logger.info(f'Данные обработаны. Результат: {result}')
            if result:
                if datetime.fromisoformat(*result).date() != datetime.now().date():
                    self.checkbox1.state = 'down'    #  Реакция смайла
                    self.checkbox2.state = 'down'  #  Реакция смайла  
                else:
                    if datetime.fromisoformat(*result).hour > 13:
                        self.checkbox2.state = 'normal'    #  Реакция смайла 
                    self.checkbox1.state = 'normal'  #  Реакция смайла             
                    self.manager.__dict__[f'Screen_{self.room}'] = True
        @mainthread
        def failure(req, result):
            logger.info(f'Данные обработаны. Результат: {result}')

        @mainthread
        def on_error(req, error):
            logger.info(f"Ошибка: {error}")

        req2 = UrlRequest(f'http://{self.url}/for_info/?room={self.room}', 
                          on_success=on_success, 
                            on_failure=failure,
                            on_error=on_error)

    def to_main_scrn(self, *args): # Чтобы не выдать ошибку, я добавляю в функцию *args
        self.manager.current = 'Main'  # Выбор экрана по имени (в данном случае по имени "Main")
           
    def set_url(self, url, login,  *args):
        """Принимает данные пользователя и текущий url"""
        logger.info(f'Скрин помещения {self.room} приняло данные от main скрина')
        self.url = url
        self.login = login
        self.checkbox_state()
