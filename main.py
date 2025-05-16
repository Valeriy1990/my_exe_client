from kivy.app import App
from kivymd.app import MDApp
from kivy.clock import Clock, mainthread
from kivy.app import async_runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem

import asyncio
from asyncio import sleep
import logging.config
from logging_settings import logging_config
from environs import Env
import datetime
import pickle
import requests
import logging
import time

'''Например в main попали кривые коммиты, и мы их запушили в удаленный main. 
Сначала перемещаем указатель на последний стабильный коммит (до того как все пошло не так) по его хешу

git reset --hard mnf3m

и пушим в удаленный репозитарий (для защищенной ветки main должны быть включены --force пуши иначе пуш не пройдет! 
Это настройках ветки устанавливается.)

git push --force origin main'''

from Screen import Screen
from ccolor import *

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

class MainApp(MDApp):
    '''Здесь я добавляю главный и второй экраны в менеджер, больше этот класс ничего не делает'''
    access = True # Поставить на False
    login_active = 'test_login_in_main'
    
    # name_attr = f'room_{537}'
    # scr = Screen(name="Screen_537", room="550")
    # self.__setattr__(name_attr, scr)
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        '''Панель с помещениями'''
        panel = MDNavigationRail(    
                    MDNavigationRailItem(icon="account-cancel",
                                     on_press=self.account_reset,
                                     text="Account Reset"),          
                    MDNavigationRailItem(
                        text=f"Room 536",
                        icon="home-circle-outline",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        badge_icon="exclamation-thick",
                        badge_bg_color=(1, 1, 0, 1),
                        badge_icon_color=(1, 0, 0, 1)),  
                    MDNavigationRailItem(
                        text="Room 537",
                        on_press=self.to_scrn_537,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"), 
                    MDNavigationRailItem(
                        text="Room 538",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),  
                    MDNavigationRailItem(
                        text="Room 539",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),    
                    MDNavigationRailItem(
                        text="Room 540",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),   
                    MDNavigationRailItem(
                        text="Room 541",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),  
                    MDNavigationRailItem(
                        text="Room 542",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),             
                    MDNavigationRailItem(
                        text="Room 543",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),       
                    MDNavigationRailItem(
                        text="Room 544",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),       
                    MDNavigationRailItem(
                        text="Room 545",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),          
                    MDNavigationRailItem(
                        text="Room 546",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),
                    MDNavigationRailItem(
                        text="Room 548",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),
                    MDNavigationRailItem(
                        text="Room 549a",
                        on_press=self.to_scrn_536,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        icon="home-circle-outline"),             
                    md_bg_color=(0.4, 0.4, 0.4, 1),
                    current_selected_item=1,
                    size_hint = (None, None),)
        panel.height = 17 * 56 + 20
    
        '''Лейбл логин'''
        self.text_login = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.8},
                                 mode="rectangle",
                                 hint_text="Никнейм",
                                 hint_text_color_normal = blue,
                                 icon_left_color_normal = blue,
                                 max_text_length=12,
                                 error_color = blue,
                                 text_color_normal = blue,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="account",
                                 foreground_color=green,
                                #  on_text_validate=self.next_field,
                                 fill_color_normal=green)
        
        '''Лейбл пароль'''
        self.text_passrd = MDTextField(size_hint=(0.4, None),
                                  pos_hint={"center_x": 0.5, "center_y": 0.68},
                                  mode="rectangle",
                                  hint_text="Пароль",
                                  icon_left="lock-outline",
                                  hint_text_color_normal = blue,
                                  icon_left_color_normal = blue,
                                  helper_text="Минимальная длина 8 символов.",
                                  helper_text_mode="on_error",
                                  password=True,
                                  password_mask="X")

        '''Текст состояния авторизации'''
        self.text_field0 = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.35, "center_y": 0.93},
                                 mode="line",
                                 hint_text="None",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 max_text_length=16,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="account-cowboy-hat",
                                 readonly=True)

        """Кнопка 'продолжить' после логина и пароля"""
        confirm = MDRectangleFlatButton(text="Продолжить",
                                    on_press=self.on_confirm,
                                    pos_hint={"center_x": 0.5, "center_y": 0.2})

        '''Лейбл связи с сервером'''
        self.text_server = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.1},
                                 mode="line",
                                 hint_text="",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 max_text_length=16,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="",
                                 readonly=True)

        '''Лейбл ввода IP'''
        self.text_ip = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.9, "center_y": 0.4},
                                 size_hint_x=0.15,
                                 mode="line",
                                 hint_text="Введите IP",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 text='192.168.1.33',
                                 icon_left="")
        
        '''Лейбл для порта'''
        self.text_port = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.9, "center_y": 0.3},
                                 size_hint_x=0.15,
                                 mode="line",
                                 hint_text="Введите порт",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 text='8066',
                                 icon_left="")

        '''Кнопка выхода из приложения'''
        exit_button = MDFloatingActionButton(icon="exit-run",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      on_press=self.stop_program,
                                      pos_hint={"center_x": 0.15, "center_y": 0.08})
        
        '''Кнопка подключения к серверу'''
        server_button = MDFloatingActionButton(icon="connection",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      on_press=self.on_server,
                                      pos_hint={"center_x": 0.94, "center_y": 0.08})

        '''Создание пустого макета, не привязанного к экрану'''
        main_layout = MDBoxLayout(orientation="vertical")   

        '''Значок глаза на лейбл пароль'''
        eye_outline = MDIconButton(icon="eye-outline",
                                    on_press=self.show_password,
                                    pos_hint={"center_x": 0.67, "center_y": 0.67})

        '''Ролик на боковую панель'''
        ml = ScrollView(do_scroll_x = False,
                        bar_pos_y = 'left')

        rooms_dict={}

        self.sm = MDScreenManager()  # Необходимо создать переменную manager, которая будет собирать экраны и управлять ими
        main_screen = MDScreen(name='Main')      
        
        for room in list(range(536, 547)) + ['548','549a']:
            self.__dict__[f'screen_{room}'] = Screen(name=f"Screen_{room}", room=room)
        
        # self.screen_536 = Screen(name='Screen_536', room="536")
        # rooms_dict['room_536'] = self.screen_536
        # self.screen_537 = Screen(name="Screen_537", room="537")
        # rooms_dict['room_537'] = self.screen_537
        # self.screen_538 = Screen(name="Screen_538", room="538")
        # rooms_dict['room_538'] = self.screen_538
        # self.screen_539 = Screen(name="Screen_539", room="539")
        # rooms_dict['room_539'] = self.screen_539
        # self.screen_540 = Screen(name="Screen_540", room="540")
        # rooms_dict['room_540'] = self.screen_540
        # self.screen_541 = Screen(name="Screen_541", room="541")
        # rooms_dict['room_541'] = self.screen_541
        # self.screen_542 = Screen(name="Screen_542", room="542")
        # rooms_dict['room_542'] = self.screen_542
        # self.screen_543 = Screen(name="Screen_543", room="543")
        # rooms_dict['room_543'] = self.screen_543
        # self.screen_544 = Screen(name="Screen_544", room="544")
        # rooms_dict['room_544'] = self.screen_544
        # self.screen_545 = Screen(name="Screen_545", room="545")
        # rooms_dict['room_545'] = self.screen_545
        # self.screen_546 = Screen(name="Screen_546", room="546")
        # rooms_dict['room_546'] = self.screen_546
        # self.screen_548 = Screen(name="Screen_548", room="548")
        # rooms_dict['room_548'] = self.screen_548
        # self.screen_549а = Screen(name="Screen_549a", room="549a")
        # rooms_dict['room_549a'] = self.screen_549а
        
        self.sm.add_widget(main_screen)  # Установка значения имени экрана для менеджера экранов
        self.sm.add_widget(self.screen_536)
        self.sm.add_widget(self.screen_537)
       
        self.url = f'{self.text_ip.text}:{self.text_port.text}'

        ml.add_widget(panel)
        main_screen.add_widget(ml)
       
        main_screen.add_widget(self.text_field0)
        main_screen.add_widget(self.text_passrd)
        main_screen.add_widget(self.text_login)
        main_screen.add_widget(self.text_server) 
        main_screen.add_widget(self.text_ip)        
        main_screen.add_widget(self.text_port) 
        
        main_screen.add_widget(confirm)
        main_screen.add_widget(server_button)
        main_screen.add_widget(exit_button)
        main_screen.add_widget(eye_outline)
        main_screen.add_widget(main_layout)
        
        return self.sm  # Тут я возвращаю менедежер, что бы работать с ним
    
    def stop_program(self, instance):
        '''Завершить приложение'''
        logger.info('Успешный выход из программы. Ты великолепен!!')
        App.get_running_app().stop()

    def next_field(self, instance):
        """Если текст логина введён в нужном формате, фокус сменяется на пароль"""
        logger.info('Смена фокуса с логина на пароль')
        if self.text_login.focus == True:
            self.text_passrd.focus = True
   
    def show_password(self, instance):
        '''Скрыть/показать пароль'''
        if self.text_passrd.password == True:
            self.text_passrd.password = False
            instance.icon = "eye-off-outline"
        else:
            self.text_passrd.password = True
            instance.icon = "eye-outline"

    def on_confirm(self, instance):
        '''Авторизация'''

        @mainthread
        def success(req, result):
            """В случае успеха"""
            logger.info(f'Сервер подтвердил запрос')
            self.login_active = self.text_login.text
            self.text_field0.hint_text = self.text_login.text if req._result else "Неверный логин или пароль"
            self.text_passrd.text = ""
            self.text_login.text = ""
            MainApp.access = req._result
            logger.info(f'Процедура авторизации прошла успешно')

        @mainthread
        def on_error(req, error):
            """В случае неудачи"""
            self.text_field0.hint_text = "Ожидание ответа от сервера..."
            MainApp.access = req._result
            load()
            logger.debug(f'Ошибка авторизации') 

        @mainthread
        def failure(req, result):
            """Данные на сервер на сервер переданы, но есть проблема"""
            self.text_field0.hint_text = "Ошибка со стороны сервера"
            MainApp.access = req._result
            logger.debug(f'Ошибак со стороны сервера') 

        def is_network_available():
            """Проверка наличия интернета"""
            logger.info(f'Проверка наличия интернета')
            try:
                response = requests.head("http://www.google.com")
                logger.info(f'Интернет есть')
                return response.status_code == 200
            except:
                return False

        def load():
            """Get запрос с данными пользователя осуществляется здесь"""          
            self.url = f'{self.text_ip.text}:{self.text_port.text}' 
            logger.info(f'Попытка отправить запрос на сервер')    
            if is_network_available():
                logger.error(f'Загрузка на сервер')
                req = UrlRequest(url=f'http://{self.url}/avt/?login={self.text_login.text}&password={self.text_passrd.text}', 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_error=on_error)
            else:
                logger.error(f'Интернета нет')
                self.text_field0.hint_text = "Нет подключения к сети. Попробуем позже..."
                Clock.schedule_once(lambda dt: load(), 5) # Повторная попытка через 5 секунд

        load()  # Вложеная функции load внутри on_confirm        

    def account_reset(self, instance):
        '''Сброс авторизации'''
        logger.info('Успешный сброс авторизации')
        self.text_field0.hint_text = "Введите логин и пароль"
        MainApp.access = False

    def on_server(self, instance):
        """Проверка сервера в сети"""
        self.url = f'{self.text_ip.text}:{self.text_port.text}'   

        def success(req, result):
            logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Cервер на связи'

        def failur(req, result):
            logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Cервер на связи'

        def error(req, result):
            logger.error(result)
            self.text_server.hint_text = 'Нет связи с сервером'

        logger.info(f'Проверка наличия сервера в сети')
        response = UrlRequest(f'http://{self.url}/hello/', 
                                  on_success=success, 
                                  on_failure=failur, 
                                  on_error=error)
        
        Clock.schedule_once(lambda dt: self.on_server(f'http://{self.url}/hello/'), 5) # Повторная попытка через 5 секунд
    
    def to_scrn_536(self, *args):
        """Смена скрина"""
        if MainApp.access == True:
            self.screen_536.set_url(url=self.url, login=self.login_active)
            self.sm.current = 'Screen_536'  # Выбор экрана по имени (в данном случае по имени "Second")
            return 0  # Не обязательно
        
    def to_scrn_536(self, *args):
        """Смена скрина"""
        if MainApp.access == True:
            self.screen_536.set_url(url=self.url, login=self.login_active)
            self.sm.current = "Screen_536"  # Выбор экрана по имени (в данном случае по имени "Second")
            return 0  # Не обязательно
        
    def to_scrn_537(self, *args):
        """Смена скрина"""
        if MainApp.access == True:
            self.screen_537.set_url(url=self.url, login=self.login_active)
            self.sm.current = 'Screen_537'  # Выбор экрана по имени (в данном случае по имени "Second")
            return 0  # Не обязательно
    
if __name__ == '__main__':
    MainApp().run()

