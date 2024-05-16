import psycopg2

# Параметры подключения к базе данных
DB_NAME = 'engcard'
DB_USER = 'postgres'
DB_PASSWORD = 'ВАШ_ПАРОЛЬ'
DB_HOST = 'localhost'


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )


# Создание таблиц
def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id SERIAL PRIMARY KEY,
            word VARCHAR(255) UNIQUE,
            translation VARCHAR(255)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_words (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            word VARCHAR(255),
            translation VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()


# Добавление слова в базу данных
def add_word(word, translation):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO words (word, translation) VALUES (%s, %s) ON CONFLICT (word) DO NOTHING",
                (word, translation))
    conn.commit()
    conn.close()


# Добавление слова пользователя в базу данных
def add_user_word(user_id, word, translation):
    if not user_exists(user_id):
        add_user(user_id)
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_words (user_id, word, translation) VALUES (%s, %s, %s)", (user_id, word, translation))
    conn.commit()
    conn.close()


# Проверка существования пользователя
def user_exists(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


# Добавление пользователя
def add_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
    conn.commit()
    conn.close()


# Получение всех слов из базы данных
def get_all_words():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT word, translation FROM words")
    rows = cur.fetchall()
    conn.close()
    return rows


# Получение всех слов пользователя из его базы данных
def get_user_words(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT word, translation FROM user_words WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


# Удаление слова пользователя из его базы данных
def delete_user_word(user_id, word):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_words WHERE user_id = %s AND (word = %s OR translation = %s)", (user_id, word, word))
    affected_rows = cur.rowcount
    conn.commit()
    conn.close()
    return affected_rows > 0


# Создание тестовых слов в общей базе (можно закомментировать после первого старта или отключить в bot.py)
def add_test_data():
    test_words = [
        ('cat', 'кот'),
        ('dog', 'собака'),
        ('apple', 'яблоко'),
        ('orange', 'апельсин'),
        ('book', 'книга'),
        ('car', 'машина'),
        ('house', 'дом'),
        ('tree', 'дерево'),
        ('river', 'река'),
        ('computer', 'компьютер')
    ]
    for word, translation in test_words:
        add_word(word, translation)
