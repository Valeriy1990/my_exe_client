from datetime import datetime
import pandas as pd

'''Подготовка данных'''

data_549=pd.read_csv(r'C:\Users\vbekr\OneDrive\Рабочий стол\Python\CSV_EXCEL\климатика_2024_549.csv', delimiter=';')
res = pd.Series([float(i.replace(',','.')) for i in data_549.temperature_549 if type(i) == str]) # Конвертируем тип данных str в тип данных float
res2 = pd.Series([float(i.replace(',','.')) for i in data_549.humidity_549 if type(i) == str]) # Конвертируем тип данных str в тип данных float
data_549 = pd.DataFrame({'Date': [datetime.strptime(i,'%d.%m.%Y').date() for i in map(str,data_549.Date)],
                         'temperature_549': res,
                         'humidity_549': data_549.humidity_549})
data_549['Month'] = [i.month for i in data_549.Date]
data_549_mean = data_549[['humidity_549','temperature_549','Month']].groupby(['Month']).mean() # Датафрейм со средними значениями

