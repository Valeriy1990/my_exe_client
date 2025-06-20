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

#git reset --hard mnf3m
#git push --force origin main'''

from Screen import Screen
from ccolor import *

# Загружаем настройки логирования из словаря `logging_config`
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

class MainApp(MDApp):
    '''Здесь я создаю главный скрин'''
    rooms = (i for i  in range(536, 549) if i != 547)  # Генератор содержащий все необходимые помещения
    buttons = []  # Пустой список для кнопок
    
    def build(self):
        """Метод содержит все графические компоненты"""
        self.theme_cls.theme_style = "Dark"
        
        '''Панель для помещений. Помещения будут добавленны потом'''
        panel = MDNavigationRail(    
                    MDNavigationRailItem(icon="account-cancel",
                                    on_press=self.account_reset,
                                    text="Reset"),               
                                    md_bg_color=(0.4, 0.4, 0.4, 1),
                                    current_selected_item=-1,
                                    elevation=4,
                                    shadow_color=(0.6, 0.6, 1, 1),
                                    size_hint = (None, 15 * 0.09))  # Не смог автоматизировать длинну панели с помещениями. Подобрал(
    
        '''Окно логин'''
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
        
        '''Окно пароль'''
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

        '''Окно состояния авторизации'''
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

        """Кнопка 'продолжить'"""
        confirm = MDRectangleFlatButton(text="Продолжить",
                                    on_press=self.on_confirm,
                                    pos_hint={"center_x": 0.5, "center_y": 0.2})

        '''Окно связи с сервером'''
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

        '''Окно ввода IP'''
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
                                 text=MainApp.data['url'][:-5] if MainApp.data['url'] else '',  # Если в файле JSON 'url' : None, то строка пустая. Иначе url
                                 icon_left="")
        
        '''Окно ввода порта'''
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
                                 text=MainApp.data['url'][-4:] if MainApp.data['url'] else '',  # Если в файле JSON 'url' : None, то строка пустая. Иначе port
                                 icon_left="")

        '''Кнопка выхода из приложения'''
        exit_button = MDFloatingActionButton(icon="exit-run",
                                      md_bg_color = (0, 1, 0.7, 0.7),
                                      icon_color=(1, 1, 1, 1),
                                      on_press=self.on_stop,
                                      pos_hint={"center_x": 0.85, "center_y": 0.08})

        '''Создание пустого макета, не привязанного к экрану'''
        main_layout = MDBoxLayout(orientation="vertical")   

        '''Значок глаза на окно пароля'''
        eye_outline = MDIconButton(icon="eye-outline",
                                    on_press=self.show_password,
                                    pos_hint={"center_x": 0.82, "center_y": 0.67})

        '''Ролик на боковую панель'''
        ml = ScrollView(do_scroll_x = False,
                        bar_pos_y = 'left',
                        effect_cls = 'ScrollEffect')

        self.sm = MDScreenManager()  # Переменная manager, которая будет собирать экраны и управлять ими
        main_screen = MDScreen(name='Main')  # Установка имени для главного экрана
        self.sm.add_widget(main_screen)  
              
        # room хранится в сакмом классе 
        for room in MainApp.rooms:  
            # Создаём объекты экранов для каждого помещения и называем их Screen_<номер помещения>
            self.__dict__[f'Screen_{room}'] = Screen(name=f"Screen_{room}", room=room)
            self.sm.add_widget(self.__getattribute__(f'Screen_{room}'))
            
            # Присваиваем каждому экрану кортеж. 
            # Первый False установит восклицательный знак если данные до 13:00 не загружены. 
            # Второй False установит восклицательный знак если данные после 13:00 не загружены.
            # В момента создания кортеж (False, False)
            self.sm.__dict__[f'Screen_{room}'] = (False, False)  
            
            # Создаём объекты MDNavigationRailItem
            button = MDNavigationRailItem(
                        text=f"Room {room}",
                        icon="home-circle-outline",
                        on_press=self.to_scrn,   # Кнопка перехода к другому экрану через функцию to_scrn 
                        badge_icon="exclamation-thick",
                        badge_bg_color=(1, 1, 0, 1),
                        badge_icon_color=(1, 0, 0, 1))
            
            # Добавляем объекты button в список buttons (пустой список хранится в самом классе)
            MainApp.buttons.append(button)
            # Добавляем объекту button атрибут с названием привязанного к нему экрана для функции to_scrn
            button.screen_name = f"Screen_{room}"
            
            panel.add_widget(button)
        # Последняя кнопка в боковую панель
        panel.add_widget(MDNavigationRailItem(icon='menu-open',
                                              on_press=self.val_state))  # При старте приложения будет запускаться функция val_state
        
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

        
        return self.sm  # Dозвращаю менедежер, что бы работать с ним
    
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
            if req._result:  # Если сервер вернул True
                # Открываем доступ пользователю
                MainApp.data['accses'] = req._result  
                # Сохраняем данные MainApp.data в фаил JSON
                self.save()  
                # Активируем функцию on_server. Периодически мониторим связь с сервером для контроля состояния соединения.
                # Если связь оборвётся, то будет надпись 'Нет связи с сервером'
                # В противном случае 'Cервер на связи'
                self.on_server()  
                self.text_field0.hint_text = MainApp.data['info']  # На экране появится имя пользователя

            else:
                self.text_field0.hint_text = "Неверный логин или пароль"
            self.text_passrd.text = ""
            self.text_login.text = ""
            logger.info(f'Отвер сервера обработан')

        @mainthread
        def on_error(req, error):
            """В случае неудачи"""
            self.text_field0.hint_text = "Ожидание ответа от сервера..."
            # MainApp.data['accses'] = req._result
            load()  #  Повторная попытка связаться с сервером
            logger.info(f'Сервер не отвечает') 

        @mainthread
        def failure(req, result):
            """Данные на сервер переданы, но есть проблема"""
            self.text_field0.hint_text = "Ошибка со стороны сервера"
            MainApp.data['accses'] = req._result
            logger.info(f'Ошибка со стороны сервера') 

        def is_network_available():
            """Проверка наличия интернета"""
            try:
                response = requests.head("http://www.google.com")
                logger.info(f'Проверка наличия интернета. Код: {response.status_code}')
                return response.status_code == 200
            except Exception as e:
                logger.error(f'Произошла ошибка: {e}')
                return False

        def load():
            """Get запрос с данными пользователя осуществляется здесь"""          
            if is_network_available():
                # Данные берутся из временно сохранённых в MainApp.data
                # В случае успеха данные сохраняются в JSON
                req = UrlRequest(url=f'http://{MainApp.data["url"]}/avut/?login={MainApp.data["login"]}&password={MainApp.data["password"]}', 
                                    on_success=success, 
                                    on_failure=failure,
                                    on_error=on_error)
            else:
                logger.error(f'Интернета нет')
                self.text_field0.hint_text = "Нет подключения к сети..."
                Clock.schedule_once(lambda dt: load(), 5) # Повторная попытка через 5 секунд

        # Временно сохраняем данные в MainApp.data
        MainApp.data['login'] = self.text_login.text
        MainApp.data['password'] = self.text_passrd.text
        MainApp.data['url'] = f'{self.text_ip.text}:{self.text_port.text}'   
        MainApp.data['info'] = self.text_login.text

        load()  # Вложенная функции load внутри on_confirm        

    def account_reset(self, instance):
        '''Сброс авторизации'''
        logger.info('Успешный сброс авторизации')
        self.text_field0.hint_text = "Введите логин и пароль"
        MainApp.data = {'accses': False, 
                    'login': '',
                    'password': '',
                    'url' : None,
                    'info' : 'Введите логин и пароль'}

    def on_server(self, instance=None):
        """Проверка сервера в сети и обновление восклицательных знаков"""

        def success(req, result):
            # logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Cервер на связи'
            # Обновление галочек экранов 
            self.val_state()
            # Проверка кортежей экранов для восклицательных знаков
            self.room_state()

        def failur(req, result):
            logger.info(f'Сервер прислал ответ: {req._result}')
            self.text_server.hint_text = 'Ошибка со стороны сервера'

        def error(req, result):
            # logger.error(result)
            self.text_server.hint_text = 'Нет связи с сервером'
       

        # logger.info(f'Проверка наличия сервера в сети')
        response = UrlRequest(f"http://{MainApp.data['url']}/hello/", 
                                  on_success=success, 
                                  on_failure=failur, 
                                  on_error=error)
        
        Clock.schedule_once(lambda dt: self.on_server(f"http://{MainApp.data['url']}/hello/"), 5) # Повторная попытка через 5 секунд

    def to_scrn(self, instance):
        """Смена экрана"""
        if MainApp.data['accses']:  # Если есть доступ
            # Возвращаем атрибут объекта button с названием привязанного к нему экрана
            # Возвращаемому экрану передаём данные сети и пользователя для передачи данных на сервер с самого экрана
            self.__getattribute__(instance.screen_name).set_url(url=MainApp.data['url'], login=MainApp.data['login'])
            self.sm.current = instance.screen_name  # Выбор экрана по имени            

    def on_stop(self, instance):
        '''Завершить приложение и сохранить состояние приложения'''
        logger.info('Успешный выход из программы.')
        self.save()
        App.get_running_app().stop()
     
    def on_pause(self):
       """Сохранить данные перейдя на паузу"""
       self.save()
       return True

    def on_start(self):
        # Если из приложении вышел авторизованный пользователь и не сбросил аутентификацию.
        # Приложение просто будет мониторить состояние связи с сервером
        if MainApp.data['accses']:
            self.on_server()
        return super().on_start()  # Базовая реализация метода on_start

    def save(self):
        """Сохранение состояния приложения в файл JSON"""
        logger.info(f'Состояние файла данных: {MainApp.data}') 
        with open('data_client.json', 'w') as file:
            json.dump(MainApp.data, file)  

    def val_state(self, instance=None):
        '''Обновление данных по помещениям для восклицательных знаков'''
        if MainApp.data['accses']:
            for but in MainApp.buttons:
                # Возвращаем атрибут объекта button с названием привязанного к нему экрана
                # Возвращаемому экрану передаём данные сети и пользователя для передачи данных на сервер с самого экрана
                self.__getattribute__(but.screen_name).set_url(url=MainApp.data['url'], login=MainApp.data['login'])
                # У возвращаемого экрана обновляется состояние галочек для проверки восклицательных знаков
                self.__getattribute__(but.screen_name).checkbox_state()

    def room_state(self, instance=None):
        '''Для восклицательных знаков'''
        for but in MainApp.buttons:    
            # Проверка кортежа каждого из экранов.
            # Если кортеж (False, False) то будет восклицательный знак.
            # Если кортеж (True, False), а время меньше 13:00, то восклицательный знак пропадёт.
            # Если кортеж (True, False), а время больше 13:00, то восклицательный знак появится.       
            # Если кортеж (True, True), а время меньше 13:00, то восклицательный знак пропадёт.     
            if self.sm.__dict__[but.screen_name][datetime.now().hour >= 13]:
                but.badge_icon=''
            else:
                but.badge_icon="exclamation-thick"
                
if __name__ == '__main__':
    try:
        """Проверка наличия файла в директории"""
        with open('data_client.json', 'r') as file:
            MainApp.data = json.load(file)
    except:
        """Если файла нет, то настройки по дефолту"""
        MainApp.data = {'accses': True, # Поставить на False
                    'login': '',
                    'password': '',
                    'url' : None,
                    'info' : 'Введите логин и пароль'}
    logger.info(f'Состояние файла данный: {MainApp.data}')  
    MainApp().run()
 
