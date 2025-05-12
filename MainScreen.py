
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem

from environs import Env
import datetime
import pickle
import requests
import logging
from ccolor import *

env = Env()  # Создаем экземпляр класса Env
env.read_env(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\my_exe_client\inter.env') # Методом read_env() читаем файл .env и загружаем из него переменные в окружение
                          
login = env('login')  # Получаем и сохраняем значение переменной окружения в переменную
Password = env('Password')  

# login = {'Valeriy': '1111'}

logger = logging.getLogger(__name__)

class MainScreen(MDScreen):
    '''здесь я создаю первый экран с именем MainScreen'''
    access = False # Поставить на False
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)     

        """Проверка сервера в сети"""
        def on_server(self):

            logger.info(f'Проверка наличия сервера в сети')
            try:
                response = requests.head('http://192.168.1.33:8066/hello/',
                                    timeout=5)
                logger.info(response.status_code)
                text_server.hint_text = 'Cервер на связи'
            except:
                text_server.hint_text = 'Нет связи с сервером'

        '''Завершить приложение'''
        def stop_program(self):
            logger.info('Успешный выход из программы. Ты великолепен!!')
            App.get_running_app().stop()

        """Если текст логина введён в нужном формате, фокус сменяется на пароль"""
        def next_field(self):
            logger.info('Смена фокуса с логина на пароль')
            if text_login.focus == True:
                text_passrd.focus = True

        '''Скрыть/показать пароль'''
        def show_password(self):
            if text_passrd.password == True:
                text_passrd.password = False
                self.icon = "eye-off-outline"
            else:
                text_passrd.password = True
                self.icon = "eye-outline"

        '''Сброс авторизации'''
        def account_reset(self):
            logger.info('Успешный сброс авторизации')
            text_field0.hint_text = "Введите логин и пароль"
            MainScreen.access = False

        '''Авторизация'''
        def on_confirm(self):
            try:
                if login == text_login.text and Password == text_passrd.text:
                    text_field0.hint_text = text_login.text
                    text_passrd.text = ""
                    text_login.text = ""
                    MainScreen.access = True
                    logger.info('Авторизация прошла успешно')

                else:
                    text_field0.hint_text = "Введите логин и пароль"
                    text_passrd.text = ''
                    text_login.text = ''
                    MainScreen.access = False
                    logger.info('Неверный пароль')
            except:
                text_field0.hint_text = "Введите логин и пароль"
                text_passrd.text = ''
                text_login.text = ''
                MainScreen.access = False
                logger.debug('Ошибка авторизации')     
        
        # '''Периодическая активация функции on_error'''
        # Clock.schedule_interval(on_error, 1/5)

        '''Панель с помещениями'''
        panel = MDNavigationRail(    
                    MDNavigationRailItem(icon="account-cancel",
                                     text="Account Reset", 
                                     on_press=account_reset),          
                    MDNavigationRailItem(
                        text=f"Room 536",
                        icon="home-circle-outline",
                        on_press=self.to_second_scrn,   # Кнопка перехода к другому скрину через функцию to_second_scrn 
                        badge_icon="exclamation-thick",
                        badge_bg_color=(1, 1, 0, 1),
                        badge_icon_color=(1, 0, 0, 1)),  
                    MDNavigationRailItem(
                        text="Room 537",
                        icon="home-circle-outline"), 
                    MDNavigationRailItem(
                        text="Room 538",
                        icon="home-circle-outline"),  
                    MDNavigationRailItem(
                        text="Room 539",
                        icon="home-circle-outline"),    
                    MDNavigationRailItem(
                        text="Room 540",
                        icon="home-circle-outline"),   
                    MDNavigationRailItem(
                        text="Room 541",
                        icon="home-circle-outline"),  
                    MDNavigationRailItem(
                        text="Room 542",
                        icon="home-circle-outline"),             
                    MDNavigationRailItem(
                        text="Room 543",
                        icon="home-circle-outline"),       
                    MDNavigationRailItem(
                        text="Room 544",
                        icon="home-circle-outline"),       
                    MDNavigationRailItem(
                        text="Room 545",
                        icon="home-circle-outline"),          
                    MDNavigationRailItem(
                        text="Room 546",
                        icon="home-circle-outline"),
                    MDNavigationRailItem(
                        text="Room 548",
                        icon="home-circle-outline"),
                    MDNavigationRailItem(
                        text="Room 549a",
                        icon="home-circle-outline"),             
                    md_bg_color=(0.4, 0.4, 0.4, 1),
                    current_selected_item=1,
                    size_hint = (None, None),)

        '''Реакция смайла на pickle'''
        def checkbox_536_state(self):
            global room_536
            try:
                with open('my_exe_client/data_states.pickle', 'rb') as f:
                    logger.info(f'Считывание pickle!')
                    first = f.read()
                    flag = pickle.loads(first)
                    tap_flag = flag["room_536"]
            except FileNotFoundError:
                pass
            logger.info(f'Проверка свежих данных на помещении')
            if not tap_flag or datetime.fromisoformat(tap_flag).date() != datetime.now().date():
                # badge_icon="exclamation-thick"  
                pass
            else:
            #     badge_icon="" 
                pass

        panel.height = 17 * 56 + 20
    
        '''Лейбл логин'''
        text_login = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.5, "center_y": 0.8},
                                 mode="rectangle",
                                 hint_text="Никнейм",
                                 hint_text_color_normal = blue,
                                 icon_left_color_normal = blue,
                                 max_text_length=16,
                                 error_color = blue,
                                 text_color_normal = blue,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="account",
                                 foreground_color=green,
                                 on_text_validate=next_field,
                                 fill_color_normal=green)
        
        '''Лейбл пароль'''
        text_passrd = MDTextField(size_hint=(0.4, None),
                                  pos_hint={"center_x": 0.5, "center_y": 0.68},
                                  mode="rectangle",
                                  hint_text="Пароль",
                                  icon_left="lock-outline",
                                  hint_text_color_normal = blue,
                                  icon_left_color_normal = blue,
                                  helper_text="Минимальная длинна 8 символов.",
                                  helper_text_mode="on_error",
                                  password=True,
                                  password_mask="X")

        '''Текст состояния авторизации'''
        text_field0 = MDTextField(size_hint=(0.4, None),
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
                                    pos_hint={"center_x": 0.5, "center_y": 0.2},
                                    on_press=on_confirm)

        '''Лейбл связи с сервером'''
        text_server = MDTextField(size_hint=(0.4, None),
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

        '''Кнопка выхода из приложения'''
        exit_button = MDFloatingActionButton(icon="exit-run",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      pos_hint={"center_x": 0.15, "center_y": 0.08},
                                      on_press=stop_program)
        
        '''Кнопка подключения к серверу'''
        server_button = MDFloatingActionButton(icon="connection",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      pos_hint={"center_x": 0.15, "center_y": 0.18},
                                      on_press=on_server)

        '''Создание пустого макета, не привязанного к экрану'''
        main_layout = MDBoxLayout(orientation="vertical")   

        '''Значок глаза на лейбл пароль'''
        eye_outline = MDIconButton(icon="eye-outline",
                                    pos_hint={"center_x": 0.67, "center_y": 0.67},
                                    on_press=show_password)

        '''Ролик на боковую панель'''
        ml = ScrollView(do_scroll_x = False,
                        bar_pos_y = 'left')

        ml.add_widget(panel)
        self.add_widget(ml)
        
        self.add_widget(text_field0)
        self.add_widget(text_passrd)
        self.add_widget(text_login)
        self.add_widget(text_server)        
        
        self.add_widget(confirm)
        self.add_widget(server_button)
        self.add_widget(exit_button)
        self.add_widget(eye_outline)
        self.add_widget(main_layout)

    def to_second_scrn(self, *args):
        if MainScreen.access == True:
            self.manager.current = 'Screen_536'  # Выбор экрана по имени (в данном случае по имени "Second")
            return 0  # Не обязательно
    
if __name__ == '__main__':
    MainScreen().run()