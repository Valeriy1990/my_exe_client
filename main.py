from kivy.app import App
from kivymd.app import MDApp
import logging.config
from logging_settings import logging_config
from kivymd.uix.textfield import MDTextField


from environs import Env
import datetime
import pickle
import requests
import logging


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from MainScreen import MainScreen
from Screen import Screen

from ccolor import *

rooms_list = [f'room_{i}' for i in range(536, 549) if i != 547]


class MainApp(MDApp):
    '''Здесь я добавляю главный и второй экраны в менеджер, больше этот класс ничего не делает'''

    # Загружаем настройки логирования из словаря `logging_config`
    logging.config.dictConfig(logging_config)
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        
        main_screen = MainScreen(name='Main')      
        screen = Screen(name='Screen')
        sm = MDScreenManager()  # Необходимо создать переменную manager, которая будет собирать экраны и управлять ими

        sm.add_widget(main_screen)  # Установка значения имени экрана для менеджера экранов
        sm.add_widget(screen)
       
        print(main_screen.return_url())
        # main_screen.add_widget(text_passrd)
        # main_screen.add_widget(text_login)
 
        # main_screen.add_widget(text_ip)        
        # main_screen.add_widget(text_port) 
        
        return sm  # Тут я возвращаю менедежер, что бы работать с ним
    
if __name__ == '__main__':
    MainApp().run()

