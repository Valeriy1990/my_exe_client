from kivy.app import App
from kivymd.app import MDApp
from kivy.clock import Clock, mainthread
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem

import json
import logging.config
from logging_settings import logging_config
import requests
import logging
from datetime import datetime

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
    '''Здесь я создаю главный скрин'''
    rooms = tuple(i for i  in range(536, 549) if i != 547)
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        '''Панель с помещениями'''
        panel = MDNavigationRail(    
                    MDNavigationRailItem(icon="account-cancel",
                                    on_press=self.account_reset,
                                    text="Account Reset"),               
                                    md_bg_color=(0.4, 0.4, 0.4, 1),
                                    current_selected_item=-1,
                                    elevation=4,
                                    shadow_color=(0.6, 0.6, 1, 1),
                                    size_hint = (None, len(MainApp.rooms) * 0.135))
        # panel.height = 17 * 56 + 20
    
        '''Лейбл логин'''
        self.text_login = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.6, "center_y": 0.8},
                                 size_hint_x=0.6,
                                 mode="rectangle",
                                 hint_text="Login",
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
                                 on_text_validate=self.next_field,
                                 fill_color_normal=green)
        
        '''Лейбл пароль'''
        self.text_passrd = MDTextField(size_hint=(0.4, None),
                                  pos_hint={"center_x": 0.6, "center_y": 0.68},
                                  size_hint_x=0.6,
                                  mode="rectangle",
                                  hint_text="Password",
                                  icon_left="lock-outline",
                                  hint_text_color_normal = blue,
                                  icon_left_color_normal = blue,
                                  helper_text="Минимальная длина 8 символов.",
                                  helper_text_mode="on_error",
                                  password=True,
                                  password_mask="X")

        '''Текст состояния авторизации'''
        self.text_field0 = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.45, "center_y": 0.93},
                                 mode="line",
                                 hint_text=MainApp.data['info'],
                                 text = '',
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
                                 pos_hint={"center_x": 0.7, "center_y": 0.4},
                                 size_hint_x=0.3,
                                 mode="line",
                                 hint_text="Введите IP",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 text=MainApp.data['url'][:-5] if MainApp.data['url'] else '',
                                #  text='192.168.1.33',
                                 icon_left="")
        
        '''Лейбл для порта'''
        self.text_port = MDTextField(size_hint=(0.4, None),
                                 pos_hint={"center_x": 0.7, "center_y": 0.3},
                                 size_hint_x=0.3,
                                 mode="line",
                                 hint_text="Введите порт",
                                 hint_text_color_normal = my_color,
                                 icon_left_color_normal = my_color,
                                 active_line=True,
                                 allow_copy=False,
                                 base_direction="ltr",
                                 cursor_blink=True,
                                 text=MainApp.data['url'][-4:] if MainApp.data['url'] else '',
                                #  text='8066',
                                 icon_left="")

        '''Кнопка выхода из приложения'''
        exit_button = MDFloatingActionButton(icon="exit-run",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      on_press=self.on_stop,
                                    #   on_press=self.on_start,
                                      pos_hint={"center_x": 0.85, "center_y": 0.08})

        '''Создание пустого макета, не привязанного к экрану'''
        main_layout = MDBoxLayout(orientation="vertical")   

        '''Значок глаза на лейбл пароль'''
        eye_outline = MDIconButton(icon="eye-outline",
                                    on_press=self.show_password,
                                    pos_hint={"center_x": 0.82, "center_y": 0.67})

        '''Ролик на боковую панель'''
        ml = ScrollView(do_scroll_x = False,
                        bar_pos_y = 'left',
                        effect_cls = 'ScrollEffect')

        self.sm = MDScreenManager()  # Переменная manager, которая будет собирать экраны и управлять ими
        main_screen = MDScreen(name='Main')      
        self.sm.add_widget(main_screen)  # Установка значения имени экрана для менеджера экранов
              
        for room in MainApp.rooms:  # Создаём объекты Screen и MDNavigationRailItem
            self.__dict__[f'Screen_{room}'] = Screen(name=f"Screen_{room}", room=room)
            self.sm.add_widget(self.__getattribute__(f'Screen_{room}'))
            button = MDNavigationRailItem(
                        text=f"Room {room}",
                        icon="home-circle-outline",
                        on_press=self.to_scrn,   # Кнопка перехода к другому скрину через функцию to_scrn 
                        badge_icon="exclamation-thick",
                        # badge_icon="",
                        badge_bg_color=(1, 1, 0, 1),
                        badge_icon_color=(1, 0, 0, 1))
            button.screen_name = f"Screen_{room}"
            panel.add_widget(button)
            # try:
            #     if self.__getattribute__(f'Screen_{room}').checkbox_state():
            #         button.badge_icon=''
            # except:
            #     pass
        panel.add_widget(MDNavigationRailItem(icon='menu-open'))  # чтобы панели по дефолту не включались
        
        ml.add_widget(panel)
        main_screen.add_widget(ml)
       
        main_screen.add_widget(self.text_field0)
        main_screen.add_widget(self.text_passrd)
        main_screen.add_widget(self.text_login)
        main_screen.add_widget(self.text_server) 
        main_screen.add_widget(self.text_ip)        
        main_screen.add_widget(self.text_port) 
        
        main_screen.add_widget(confirm)
        main_screen.add_widget(exit_button)
        main_screen.add_widget(eye_outline)
        main_screen.add_widget(main_layout)
        
        if MainApp.data['accses']:
            self.on_server()

        return self.sm  # Тут я возвращаю менедежер, что бы работать с ним
    
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

    def on_confirm(self, instance=None):
        '''Авторизация'''

        @mainthread
        def success(req, result):
            """В случае успеха"""
            logger.info(f'Сервер подтвердил запрос')
            if req._result:
                MainApp.data['accses'] = req._result
                self.save()
                self.on_server()
                self.text_field0.hint_text = MainApp.data['info']
            else:
                self.text_field0.hint_text = "Неверный логин или пароль"
            self.text_passrd.text = ""
            self.text_login.text = ""
            logger.info(f'Процедура авторизации прошла успешно')

        @mainthread
        def on_error(req, error):
            """В случае неудачи"""
            self.text_field0.hint_text = "Ожидание ответа от сервера..."
            MainApp.data['accses'] = req._result
            load()
            logger.debug(f'Сервер не отвечает') 

        @mainthread
        def failure(req, result):
            """Данные на сервер переданы, но есть проблема"""
            self.text_field0.hint_text = "Ошибка со стороны сервера"
            MainApp.data['accses'] = req._result
            logger.debug(f'Ошибка со стороны сервера') 

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
            # self.set_url(self.text_ip.text, self.text_port.text)          
            logger.info(f'Попытка отправить запрос на сервер')    
            if is_network_available():
                logger.error(f'Загрузка на сервер')
                req = UrlRequest(url=f'http://{MainApp.data['url']}/avt/?login={MainApp.data['login']}&password={MainApp.data['password']}', 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_error=on_error)
            else:
                logger.error(f'Интернета нет')
                self.text_field0.hint_text = "Нет подключения к сети. Попробуем позже..."
                Clock.schedule_once(lambda dt: load(), 5) # Повторная попытка через 5 секунд

        MainApp.data['login'] = self.text_login.text
        MainApp.data['password'] = self.text_passrd.text
        MainApp.data['url'] = f'{self.text_ip.text}:{self.text_port.text}'   
        MainApp.data['info'] = self.text_login.text

        load()  # Вложеная функции load внутри on_confirm        

    def account_reset(self, instance):
        '''Сброс авторизации'''
        logger.info('Успешный сброс авторизации')
        self.text_field0.hint_text = "Введите логин и пароль"
        MainApp.access = False

    def on_server(self, instance=None):
        """Проверка сервера в сети"""
        # self.set_url(self.text_ip.text, self.text_port.text)   

        def success(req, result):
            logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Cервер на связи'

            # for room in MainApp.rooms:
            #     print(self.__getattribute__(f'Screen_{room}'))
            #     self.__getattribute__(f'Screen_{room}')..badge_icon=''

        def failur(req, result):
            logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Cервер на связи'

        def error(req, result):
            logger.error(result)
            self.text_server.hint_text = 'Нет связи с сервером'

        logger.info(f'Проверка наличия сервера в сети')
        response = UrlRequest(f'http://{MainApp.data['url']}/hello/', 
                                  on_success=success, 
                                  on_failure=failur, 
                                  on_error=error)
        
        Clock.schedule_once(lambda dt: self.on_server(f'http://{MainApp.data['url']}/hello/'), 5) # Повторная попытка через 5 секунд

    def to_scrn(self, instance):
        """Смена скрина"""
        if MainApp.data['accses']:
            instance.badge_icon=""
            self.__getattribute__(instance.screen_name).set_url(url=MainApp.data['url'], login=MainApp.data['login'])
            self.sm.current = instance.screen_name  # Выбор экрана по имени            

    def on_stop(self, instance):
        '''Завершить приложение'''
        logger.info('Успешный выход из программы. Ты супер!!')
        # self.profile.disable()
        # self.profile.dump_stats('my_exe_client/myapp.profile')
        # self.save()
        App.get_running_app().stop()

    # def on_start(self):
    #     logger.info('Функция on_start')
    #     self.profile = cProfile.Profile()s
    #     self.profile.enable()
        
    def on_pause(self):
       """Здесь вы можете сохранить данные, если это необходимо"""
       self.save()
       return True

    def on_resume(self):
       # Здесь вы можете проверить, нужно ли заменить какие-либо данные (обычно ничего не нужно)
       pass

    def save(self):
        """Сохранение состояния приложения"""
        logger.info(f'Состояние файла данный: {MainApp.data}') 
        with open('my_exe_client/data_client.json', 'w') as file:
            json.dump(MainApp.data, file)  

    # def exclamation_thick_state(self, room):
    #     '''Реакция смайлов'''
        
    #     @mainthread
    #     def on_success(req, result):
    #         if datetime.fromisoformat(*result).hour > 13:
    #             self.__getattribute__(f'Screen_{room}').badge_icon=""         

    #     @mainthread
    #     def failure(req, result):
    #         logger.info(f'Данные обработаны. Но есть нюанс: {result}')

    #     @mainthread
    #     def on_error(req, error):
    #         logger.info(f"Ошибка: {error}")

    #     req2 = UrlRequest(f'http://{MainApp.data['url']}/for_info/?room={room}', 
    #                       on_success=on_success, 
    #                         on_failure=failure,
    #                         on_error=on_error)

if __name__ == '__main__':
    try:
        with open('my_exe_client/data_client.json', 'r') as file:
            MainApp.data = json.load(file)
    except:
        MainApp.data = {'accses': False, # Поставить на False
                    'login': '',
                    'password': '',
                    'url' : None,
                    'info' : 'Введите логин и пароль'}
    logger.info(f'Состояние файла данный: {MainApp.data}')  
    MainApp().run()

