"""Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
Код должен включать следующее:
Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода"""

import requests
from lxml import html
import time
import csv

# Определение целевого URL
url = "https://finance.yahoo.com/trending-tickers/"

# Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
try:
   response = requests.get(url, headers = {
      'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
   if response.status_code == 200:
         print("Успешный запрос по URL: ", response.url)
   else:
      print("Запрос API отклонен с кодом состояния:", response.status_code)
except Exception:
    print("Ошибка в осущественнии HTML запроса:")

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
try:
   tree = html.fromstring(response.content)
except Exception:
    print("Произошла непредвиденная ошибка:")   

# Использование выражения XPath для выбора всех строк таблицы в пределах таблицы с классом 'W(100%)'
table_rows = tree.xpath("//table[@class='W(100%)']/tbody/tr") 

# парсинг таблицы
try:
   data = []
   for row in table_rows:
      columns = row.xpath(".//td/text()")
      data.append({
         'Symbol': row.xpath(".//td[1]/a/text()")[0].strip(), 
         'name': columns[0].strip(), 
         'Last Price': row.xpath(".//td[3]/fin-streamer/text()")[0].strip(), 
         'Market Time': row.xpath(".//td[4]/fin-streamer/text()")[0].strip(), 
         'Change': row.xpath(".//td[5]/fin-streamer/span/text()")[0].strip(), 
         '% Change': row.xpath(".//td[6]/fin-streamer/span/text()")[0].strip(), 
         # с этими ячейками разобратьься не удалось :( Если подскажите, буду весьма признателен.
         #   'Volume': row.xpath(".//td[7]/fin-streamer/text()")[0].strip(), 
         # 'Market Cap': row.xpath(".//td[8]/fin-streamer/text()")[0].strip(),        
      })
      time.sleep(2)  
except Exception :
    print("Произошла непредвиденная ошибка:")
print(data)

#Сохраните извлеченные данные в CSV-файл
with open('data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0])
    writer.writeheader()
    writer.writerows(data)
