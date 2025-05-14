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
env.read_env('my_exe_client\inter.env') # Методом read_env() читаем файл .env и загружаем из него переменные в окружение
                          
url_server = env('url')  # Получаем и сохраняем значение переменной окружения в переменную

logger = logging.getLogger(__name__)

class MainScreen(MDScreen):
    '''здесь я создаю первый экран с именем MainScreen'''
    access = True # Поставить на False
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)  
 
        """Проверка сервера в сети"""
        def on_server(self, url=f'http://{url_server}/hello/'):
            
            def success(req, result):
                logger.info(f'Сервер прислал ответ: {req._result}')
                text_server.hint_text = 'Cервер на связи'

            def failur(req, result):
                logger.info(f'Сервер прислал ответ: {req._result}')
                text_server.hint_text = 'Cервер на связи'

            def error(req, result):
                logger.error(result)
                text_server.hint_text = 'Нет связи с сервером'

            logger.info(f'Проверка наличия сервера в сети')
            response = UrlRequest(url, 
                                  on_success=success, 
                                  on_failure=failur, 
                                  on_error=error)
            Clock.schedule_once(lambda dt: on_server(self, url), 5) # Повторная попытка через 5 секунд

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

            """В случае успеха"""
            @mainthread
            def success(req, result):
                text_field0.hint_text = text_login.text if req._result else "Введите логин и пароль"
                text_passrd.text = ""
                text_login.text = ""
                MainScreen.access = req._result
                logger.info(f'Авторизация прошла успешно')

            """В случае неудачи"""
            @mainthread
            def on_error(req, error):
                text_field0.hint_text = "Сервер не отвечает"
                text_passrd.text = ''
                text_login.text = ''
                MainScreen.access = req._result
                logger.debug(f'Ошибка авторизации') 

            """Данные на сервер на сервер переданы, но есть проблема"""
            @mainthread
            def failure(req, result):
                text_field0.hint_text = "Введите логин и пароль"
                text_passrd.text = ''
                text_login.text = ''
                MainScreen.access = req._result
                logger.debug(f'Какие-то проблемы') 

            """Проверка наличия интернета"""
            def is_network_available():
                logger.info(f'Проверка наличия интернета')
                try:
                    response = requests.head("http://www.google.com")
                    logger.info(f'Интернет есть')
                    return response.status_code == 200
                except:
                    return False

            def load():          
                logger.info(f'Попытка отправить запрос на сервер')    
                if is_network_available():
                    logger.error(f'Загрузка на сервер')
                    req = UrlRequest(url=f'http://{url_server}/avt/?login={text_login.text}&password={text_passrd.text}', 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_error=on_error)
                else:
                    logger.error(f'Интернета нет')
                    text_field0.hint_text = "Нет подключения к сети. Попробуем позже..."
                    Clock.schedule_once(lambda dt: load(), 5) # Повторная попытка через 5 секунд

            load()
       
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
        panel.height = 17 * 56 + 20
    
        '''Лейбл логин'''
        text_login = MDTextField(size_hint=(0.4, None),
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
                                  helper_text="Минимальная длина 8 символов.",
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

        '''Лейбл ввода IP'''
        text_ip = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.9, "center_y": 0.4},
                                 size_hint_x=0.15,
                                 mode="line",
                                 hint_text="Введите IP: 192.168.1.33",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="")
        
        '''Лейбл для порта'''
        text_port = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.9, "center_y": 0.3},
                                 size_hint_x=0.15,
                                 mode="line",
                                 hint_text="Введите порт: 8066",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 icon_left="")

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
                                      pos_hint={"center_x": 0.94, "center_y": 0.08},
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
        self.add_widget(text_ip)        
        self.add_widget(text_port) 
        
        self.add_widget(confirm)
        self.add_widget(server_button)
        self.add_widget(exit_button)
        self.add_widget(eye_outline)
        self.add_widget(main_layout)

    def to_second_scrn(self, *args):
        if MainScreen.access == True:
            self.manager.current = 'Screen'  # Выбор экрана по имени (в данном случае по имени "Second")
            return 0  # Не обязательно
    
if __name__ == '__main__':
    MainScreen().run()