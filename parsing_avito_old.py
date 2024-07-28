import locale
import csv
import os
import time
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from loguru import logger
from seleniumbase import SB
import undetected_chromedriver as uc
from locator import LocatorAvito
from babel.dates import format_date


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

class ParsingAvito:
    def __init__(self, url: str,
                 count: int = 10,  # число страниц. парсятся по умолчанию 10
                 debug_mode: int = 0,rayon: str = ""):
        self.url = url
        self.count = count
        self.data = []
        self.iter = 0
        self.debug_mode = debug_mode  # 1 или 0 режим браузера с интерфейсом или без
        self.rayon = rayon  # добавляем переменную район




    @logger.catch() #  чтобы автоматически перехватывать и логировать любые исключения, возникающие в этом методе.
    def __create_file_csv(self): # предназначен для создания файла CSV и записи в него заголовков, если файл пустой прописывает названия столбцов
        print("Отлично, я внутри метода   __create_file_csv(self) \n , сейчас перейду в self.__is_csv_empty")
        if self.__is_csv_empty:
            print("Я был внутри self.__is_csv_empty, он проверил, файл пуст или нету. Поэтому сделаем его и заполним")
            with open (f"result/all.csv",'a', encoding='utf-8', errors='ignore') as file: # a: Открытие файла в режиме добавления. Если файл не существует, он будет создан.
                writer = csv.writer(file) # создание объекта  для записи.
                writer.writerow([
                    "Название",
                    "Цена",
                    "Ссылка",
                    "Описание",
                    "Просмотров",
                    "Дата публикации",
                    "Продавец",
                    "Адрес"

                ])

    def __get_url(self):
        print("Привет, я внутри метода self.__get_url(). Я жив!!!")
        self.driver.open(self.url)  # открываем наш путь
        print("открываем наш путь")
        print(self.driver.get_title())
        if "Доступ ограничен" in self.driver.get_title() and self.debug_mode == 0:  # проверяет, есть ли строка "Доступ ограничен" в заголовке страницы.
            print("Плохо, капча")
            self.debug_mode = 1  # установка режима браузера через интерфейс, чтобы вручную ввести капчу

            raise Exception("Перезапуск из-за блокировки IP")  # исключение будет перехвачено и обработано в методе parse()
        elif "Доступ ограничен" in self.driver.get_title() and self.debug_mode == 1:
            #print("Решите капчу и нажмите кнопку Enter")
            input("Решите капчу и нажмите кнопку Enter")


        print("В методе __get_url я уже всё сделал, перехожу в метод __paginator, ничего не знаешь!!!")
    @property
    def __is_csv_empty(self) -> bool: # проверяет, пуст ли CSV файл
        '''Проверка пустой ли файл csv или нет'''
        os.makedirs(os.path.dirname("result/"), exist_ok=True) # создает директорию result, если она еще не существует.
    # Параметр exist_ok=True предотвращает возникновение ошибки, если директория уже существует.
        try:
            with open(f"result/all.csv", 'r', encoding='utf-8', errors='ignore') as file:# открыть в режиме чтения
                # Указывает, что файл должен быть открыт с использованием кодировки UTF-8.
                # errors='ignore': Указывает, что любые ошибки, связанные с кодировкой, должны быть проигнорированы.
                # Это может быть полезно, если в файле есть некорректные или неожидаемые символы.
                reader = csv.reader(file) # Создает объект reader, который позволяет читать данные из файла CSV.
                try:
                    # попытка чтения первой строки из файла
                    next(reader) # (next - следующий элемент итератора )Читает первую строку из файла. Если файл пустой, будет вызвано исключение StopIteration.
                except StopIteration: # Обработка исключения StopIteration, которое возникает, если файл пустой.
                    # файл  пустой
                    return True # указывая, что файл пустой.
                return False #  Если исключение StopIteration не возникло, значит файл не пустой, и метод возвращает False.
        except FileNotFoundError: # исключение если файл не найден.
            return True # указывая, что файл пустой (так как его не существует)

    def __parse_relative_date(self, relative_date_str): # распознавание дат
        current_date = datetime.now()
        parts = relative_date_str.split()
        quantity = int(parts[0])
        unit = parts[1]

        if 'час' in unit:
            date = current_date - timedelta(hours=quantity)
        elif 'день' in unit or 'дня' in unit or 'дней' in unit:
            date = current_date - timedelta(days=quantity)
        elif 'недел' in unit:
            date = current_date - timedelta(weeks=quantity)
        elif 'месяц' in unit or 'месяца' in unit or 'месяцев' in unit:
            date = current_date - relativedelta(months=quantity)
        elif 'год' in unit or 'года' in unit or 'лет' in unit:
            date = current_date - relativedelta(years=quantity)
        else:
            date = current_date  # В случае, если формат не распознан

        return format_date(date, format='dd.MM.yyyy', locale='ru')

    def __paginator(self):
        logger.info('Страница успешно загружена. Просматриваю объявления')
        print("Перехожу в метод self.__create_file_csv()")
        self.__create_file_csv()
        print("Побывал в гостях у метода __create_file_csv(), он создал файл. Возвращаюсь вновь в __paginator")

        while self.count > 0:  # self.count — это количество страниц, которые нужно просмотреть.
            print("Наконец-то парсинг страницы начался. self.__parse_page() запускаю")
            print(f'Сейчас  self.count ={self.count}')
            self.__parse_page()  # парсинг этой страницы
            time.sleep(random.randint(5,7))  # Делает паузу на случайное количество секунд (от 5 до 7 секунд) перед переходом на следующую страницу.
            # чтобы имитировать поведение человека и избежать блокировок со стороны сайта.

            """Проверяем есть ли кнопка далее"""
            if self.driver.find_elements(LocatorAvito.NEXT_BTN[1], by='css selector'):
                self.driver.find_element(LocatorAvito.NEXT_BTN[1],
                                         by='css selector').click()  # Если кнопка "Далее" найдена, выполняется клик по ней, чтобы перейти на следующую страницу.
                self.count -= 1  # страница обработана, уменьшаем на 1
                print(f'Теперь self.count ={self.count}')
                if self.count>0:
                    logger.debug("Следующая страница")
                else:
                    break
            else:
                logger.info("Нет кнопки далее")
                break  # выход из цикла while, если нет кнопки "Далее"


    @logger.catch
    def __parse_page(self):  # парсинг одной страницы
        """Парсит страницу"""
        titles = self.driver.find_elements(LocatorAvito.TITLES[1], by="css selector") # -  Поиск всех объявлений на странице
        for title in titles: #  Цикл по найденным объявлениям
            print('=' * 100)  # Underscore
            name = title.find_element(*LocatorAvito.NAME).text # Извлечение имени объявления
            self.iter+=1
            print(f'{self.iter} - {name}')


            if title.find_elements(*LocatorAvito.DESCRIPTIONS): # проверяет, есть ли внутри элемента title элементы, соответствующие селектору LocatorAvito.DESCRIPTIONS
                description = title.find_element(*LocatorAvito.DESCRIPTIONS).text
                print(description)
            else:
                description = ''
            url = title.find_element(*LocatorAvito.URL).get_attribute("href") # url объявления
            print(url)
            price = title.find_element(*LocatorAvito.PRICE).get_attribute("content")
            print(f'Цена : {price} рублей')
            ads_id = title.get_attribute("data-item-id")
            print(f'Идентификатор объявления : {ads_id}')

            # Извлечение площади в квадратных метрах
            if title.find_elements(*LocatorAvito.PRICE_M2):  # проверяет, есть ли внутри элемента title элементы, соответствующие селектору для площади
                square_meters = title.find_element(*LocatorAvito.PRICE_M2).text
                print(f'Цена за квадратный метр: {square_meters}')
            else:
                square_meters = ''

            #  извлечение адреса указанного в объявлении
            if title.find_elements(*LocatorAvito.ADRESS):  # проверяет, есть ли внутри элемента title элементы, соответствующие селектору для адреса
                address = title.find_element(*LocatorAvito.ADRESS).text
                print(f'Адрес: {address}')
            else:
                address = ''
            # Извлечение даты публикации
            if title.find_elements(
                    *LocatorAvito.DATE_PUBLIC):  # проверяет, есть ли внутри элемента title элементы, соответствующие селектору для даты
                date_public_str = title.find_element(*LocatorAvito.DATE_PUBLIC).text
                date_public = self.__parse_relative_date(date_public_str)
                print(f'Дата публикации: {date_public}')
            else:
                date_public = ''
            square = "Я поле площадь, буду работать вскоре для Вас ;-)"

                # Сохранение данных объявления в self.data
            self.data.append({ # будут добавляться найденные объявления.
                'ads_id': ads_id,
                'url': url,
                'name': name,
                'price': price,
                'square_meters': square_meters,
                'square': square, # аналог главное
                'rayon': self.rayon,  # добавляем поле района
                'address': address,
                'description': description,
                'date_public': date_public,

            })
        self.__save_data() # сохраняем данные в файл


    def __save_data(self):  # сохраняем данные self.data в формате json
        # Убедитесь, что директория существует
        os.makedirs(os.path.dirname('result/kchr.csv'), exist_ok=True)

        # Сохраните данные в CSV-файл с кодировкой utf-8-sig
        with open('result/nevinnomissk.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['ads_id', 'url', 'name', 'price', 'square_meters', 'square', 'rayon', 'address', 'description','date_public']
            #fieldnames = ['Заголовок объявления', 'Описание объвления', 'Ссылка на страницу объявления', 'Цена', 'Идентификатор объявления', 'Цена за квадратный метр', 'Адрес указанный в объявлении', 'Дата публикации объявления']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames, delimiter=";")

            # Если файл только что создан, запишите заголовки
            if csvfile.tell() == 0:
                writer.writeheader()

            # Запишите данные
            for item in self.data:
                writer.writerow(item)

    def parse(self):  # парсинг доступ из вне
        while self.count>0:
            with SB(
                uc=True,  # Использовать undetected-chromedriver, чтобы избежать обнаружения ботами
                headed=True if self.debug_mode else False,  # устанавливает, будет ли браузер запущен в режиме с графическим интерфейсом (headed mode) или в режиме без графического интерфейса (headless mode), в зависимости от значения атрибута
                headless=True if not self.debug_mode else False,
                page_load_strategy="eager",  # настройка загрузки страниц. Здесь WebDriver будет ждать, пока основной HTML-документ полностью загружен и событие DOMContentLoaded сработало, но не будет ждать загрузки подресурсов, таких как изображения и стили.
                #block_images=True,  # указывает WebDriver на блокировку загрузки изображений на веб-страницах. Чтобы ускорить время загрузки страниц
                #skip_js_waits=True
            ) as self.driver:
                try:
                    self.__get_url() # переходим по нашему url
                    self.__paginator()


                except Exception as error:
                    logger.error(f"Ошибка: {error}")
            if self.count==0:
                print("Конец выборки!")
