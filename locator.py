
from selenium.webdriver.common.by import By # класс By из библиотеки Selenium, который используется
# для указания стратегии поиска элементов на веб-странице By.CSS_SELECTOR , By.XPATH итд


class LocatorAvito:

    TITLES = (By.CSS_SELECTOR, "[data-marker='item']") # заголовки объвлений
    NAME = (By.CSS_SELECTOR, "[itemprop='name']")
    DESCRIPTIONS = (By.CSS_SELECTOR, "[class*='item-description']") # описание объявления
    URL = (By.CSS_SELECTOR, "[data-marker='item-title']")
    PRICE = (By.CSS_SELECTOR, "[itemprop='price']")
    PRICE_M2 = (By.CSS_SELECTOR,".price-root-RA1pj p.styles-module-size_s-xb_uK")
    ADRESS =(By.CSS_SELECTOR,".geo-root-zPwRk span")
    DATE_PUBLIC = (By.CSS_SELECTOR, "[data-marker='item-date']")
    NEXT_BTN = (By.CSS_SELECTOR, "[data-marker*='pagination-button/next']")