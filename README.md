## Telegram-бот ENGCARD для изучения английского языка

Этот учебный проект представляет собой Telegram-бота ENGCARD, который помогает пользователям практиковаться в английском языке. Бот позволяет добавлять и удалять слова в пользовательском словаре, участвовать в викторинах и просматривать личную статистику. Данные пользователей и слов хранятся в базе данных PostgreSQL.

## Функциональность

### Взаимодействие с ботом
После запуска бота, пользователю будут доступны следующие команды и кнопки:

- **📗 Добавить слово**: Добавить новое слово и его перевод в пользовательский словарь.
- **❌ Удалить слово**: Удалить слово или его перевод из пользовательского словаря.
- **🎲 Начать викторину**: Начать викторину по английским словам.
- **📈 Статистика**: Просмотреть статистику угадывания слов.

### Викторина
В режиме викторины пользователю предлагается угадать перевод слова, случайным образом выбранного из общей базы данных или пользовательского словаря. Для каждого слова предлагается 4 варианта ответа, из которых только один верный. Пользователь может продолжать угадывать, пока не выберет правильный ответ. Викторина продолжается до тех пор, пока пользователь не решит завершить ее, нажав на кнопку "Завершить викторину 🚫".

### Статистика
Бот ведет учет правильных и неправильных ответов каждого пользователя (статистика сбрасывается при перезапуске бота) и отображает статистику по запросу:

- Количество угаданных слов.
- Количество неугаданных слов.

## Установка

### Требования

- Python 3.12
- PostgreSQL
- Библиотеки `pyTelegramBotAPI` и `psycopg2-binary`

### Клонирование репозитория

Сначала клонируйте репозиторий на ваш сервер или локальный компьютер:

```sh
git clone https://github.com/leadertv/pd101_engcard.git
cd pd101_engcard
```

### Установка зависимостей

Установите необходимые библиотеки из файла `requirements.txt`:

```sh
pip install -r requirements.txt
```

Содержимое файла `requirements.txt`:

```txt
pyTelegramBotAPI
psycopg2-binary
```

### Настройка базы данных

Создайте и настройте базу данных PostgreSQL (замените значения на свои). Используйте следующие параметры подключения:

```plaintext
DB_NAME = 'engcard'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
```

Не забудьте заменить `your_password` на ваш действительный пароль. При необходимости измените эти параметры в файле `db.py`.

### Настройка Telegram Bot

Создайте Telegram-бота с помощью [BotFather](https://t.me/BotFather) и получите токен. Затем замените значение токена в файле `bot.py`:

```python
TOKEN = 'your_telegram_bot_token_here'
```

### Создание таблиц и тестовых данных

Запустите файл `db.py`, чтобы создать необходимые таблицы и добавить тестовые данные:

```sh
python db.py
```

### Запуск бота

После успешного создания таблиц и добавления тестовых данных, запустите бота:

```sh
python3 bot.py
```

## Установка на сервер (VDS)

### Подготовка сервера

1. Подключитесь к вашему серверу через SSH.
2. Установите PostgreSQL:

```sh
sudo apt update
sudo apt install postgresql postgresql-contrib
```

3. Создайте базу данных и пользователя (замените значения на свои):

```sh
sudo -u postgres psql
CREATE DATABASE engcard;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE engcard TO postgres;
\q
```

### Установка Python и зависимостей

1. Установите Python 3.12:

```sh
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

2. Клонируйте проект:

```sh
git clone https://github.com/leadertv/pd101_engcard.git
cd pd101_engcard
```

3. Создайте и активируйте виртуальное окружение:

```sh
python3.12 -m venv venv
source venv/bin/activate
```

4. Установите зависимости:

```sh
pip install -r requirements.txt
```

### Настройка и запуск бота

Настройте параметры подключения к базе данных и токен бота в файлах `db.py` и `bot.py`.

Запустите бота:

```sh
python db.py  # Для создания таблиц и добавления тестовых данных
python bot.py  # Для запуска бота
```

## Установка на Windows

### Установка необходимых программ

1. Установите Python 3.12 с официального [сайта](https://www.python.org/) и добавьте его в PATH.
2. Установите PostgreSQL для Windows [здесь](https://www.postgresql.org/download/windows/).

### Создание базы данных

Создайте базу данных и пользователя (замените значения на свои):

```plaintext
CREATE DATABASE engcard;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE engcard TO postgres;
```

### Клонирование и настройка проекта

1. Клонируйте репозиторий и перейдите в папку проекта:

```sh
git clone https://github.com/leadertv/pd101_engcard.git
cd engcard-bot
```

2. Установите виртуальное окружение и активируйте его:

```sh
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:

```sh
pip install -r requirements.txt
```

### Настройка и запуск бота

Настройте параметры подключения к базе данных и токен бота в файлах `db.py` и `bot.py`.

Запустите бота:

```sh
python db.py  # Для создания таблиц и добавления тестовых данных
python bot.py  # Для запуска бота
```

## Лицензия

Данный проект без лицензии, это учебный проект создавался по заданию курсовой работы в онлайн школе НЕТОЛОГИЯ.

## Контакты

Для вопросов и предложений, пожалуйста, создайте issue на GitHub репозитории, обратитесь к ученику потока PD-101 Ерохин Денис Вячеславович или свяжитесь по электронной почте: youtube@leadertv.ru или leadertv@mail.ru