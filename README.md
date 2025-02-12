# Проект Парсинга Данных о домах на примере Невинномысска

# Обзор

Этот проект предназначен для парсинга объявлений о недвижимости с сайта Avito и отображения полученных данных в графическом интерфейсе пользователя (GUI). Приложение создано с использованием PySide6 и включает различные библиотеки Python для обработки веб-скрапинга, парсинга данных и ведения журналов.

# Функции
- **Графический интерфейс:** Создан с помощью PySide6, GUI предоставляет интерактивный интерфейс для пользователей, чтобы начать и контролировать процесс парсинга.
- **Веб-скрапинг:** Использует undetected-chromedriver и seleniumbase для парсинга объявлений о недвижимости с Avito.
- **Хранение данных:** Полученные данные сохраняются в формате CSV для легкого анализа и доступа.
- **Логирование:** Ведется подробное логирование, логи отображаются в GUI приложении.

# Структура проекта
Основные файлы:

- **main.py:** Главный скрипт для запуска приложения.
- **parsing_avito.py:** Скрипт, отвечающий за парсинг данных с Avito.
- **main_window_ui.py:** Сгенерированный Python код для главного окна интерфейса.

# Конфигурация:

**poetry.lock** и **pyproject.toml:** Конфигурационные файлы для управления зависимостями с помощью Poetry.


# Файлы интерфейса:

**Avito.ui** и **main_window.ui**: Файлы дизайна интерфейса, созданные с помощью Qt Designer.

**Данные:**

**flats.json**: Содержит данные о квартирах.
**result/**: Каталог, в котором хранятся результаты (файлы CSV).


# Установка
Клонируйте репозиторий:

```
git clone https://github.com/yourusername/flats_data.git
cd flats_data
```

Установите зависимости с помощью Poetry:

```
poetry install
```

Запустите главный скрипт для старта приложения:

```
poetry run python main.py

```

Приложение запустится, и вы сможете начать процесс парсинга и просматривать логи непосредственно в приложении.

Вклад
