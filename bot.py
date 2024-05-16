import telebot
import random
from telebot import types
import db

# Указываем параметры подключения и токен вашего бота
TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Временная структура для хранения состояния пользователей (удаление слов, викторина и статистика)
user_stats = {}
user_quiz_data = {}
user_state = {}

# Состояния
STATE_NONE = 0
STATE_ADD_WORD = 1
STATE_DELETE_WORD = 2


# Инициализация данных пользователя
def init_user_data(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {'correct': 0, 'incorrect': 0, 'in_quiz': False}
    if user_id not in user_quiz_data:
        user_quiz_data[user_id] = {}
    if user_id not in user_state:
        user_state[user_id] = STATE_NONE


# Создаем клавиатуру для викторины
def create_quiz_keyboard(correct_translation, all_translations):
    options = set([correct_translation])
    while len(options) < 4:
        options.add(random.choice(all_translations))
    options = list(options)
    random.shuffle(options)

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    for i in range(0, len(options), 2):
        buttons = [types.KeyboardButton(text) for text in options[i:i + 2]]
        keyboard.row(*buttons)

    keyboard.add(types.KeyboardButton(text="Завершить викторину 🚫"))

    return keyboard


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    init_user_data(user_id)
    bot.send_message(user_id, "Привет 👋 Давай попрактикуемся в английском языке.", reply_markup=main_menu())


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    init_user_data(user_id)  # Инициализация данных пользователя
    if message.text == '📗 Добавить слово':
        user_state[user_id] = STATE_ADD_WORD
        add_word_handler(message)
    elif message.text == '❌ Удалить слово':
        user_state[user_id] = STATE_DELETE_WORD
        delete_word_handler(message)
    elif message.text == '🎲 Начать викторину':
        user_state[user_id] = STATE_NONE
        start_quiz_handler(message)
    elif message.text == '📈 Статистика':
        user_state[user_id] = STATE_NONE
        show_stats(message)
    else:
        if user_stats.get(user_id, {}).get('in_quiz', False):
            quiz_answer_handler(message)
        elif user_state.get(user_id) == STATE_DELETE_WORD:
            handle_delete_word(message)
        elif user_state.get(user_id) == STATE_ADD_WORD:
            add_word(message)
        else:
            handle_unrecognized_text(message)


def add_word_handler(message):
    bot.send_message(message.chat.id, "Введите слово и его перевод через двоеточие (например, слово : перевод):")


def add_word(message):
    user_id = message.chat.id
    text = message.text.strip()
    if ':' not in text:
        bot.send_message(user_id,
                         "Некорректный формат. Пожалуйста, введите слово и его перевод "
                         "через двоеточие (например, слово : перевод).")
        return

    word, translation = text.split(':', 1)
    word = word.strip()
    translation = translation.strip()

    if not word or not translation:
        bot.send_message(user_id, "Некорректный формат. Слово или перевод не могут быть пустыми.")
        return

    db.add_user_word(user_id, word, translation)
    bot.send_message(user_id, "Слово успешно добавлено!")
    user_state[user_id] = STATE_NONE


def delete_word_handler(message):
    bot.send_message(message.chat.id, "Введите слово или его перевод для удаления:")


def handle_delete_word(message):
    user_id = message.chat.id
    word_to_delete = message.text.strip()
    if db.delete_user_word(user_id, word_to_delete):
        bot.send_message(user_id, f"Слово '{word_to_delete}' успешно удалено!")
    else:
        bot.send_message(user_id, "Такого слова нет, вы можете удалять только свои слова.")
    user_state[user_id] = STATE_NONE


def start_quiz_handler(message):
    user_id = message.chat.id
    init_user_data(user_id)  # Инициализация данных пользователя
    user_stats[user_id]['in_quiz'] = True
    next_quiz_question(message)


def next_quiz_question(message):
    user_id = message.chat.id
    all_words = db.get_all_words() + db.get_user_words(user_id)
    random.shuffle(all_words)

    if not all_words:
        bot.send_message(user_id, "В базе данных нет новых слов для викторины.", reply_markup=main_menu())
        user_stats[user_id]['in_quiz'] = False
        return

    word, correct_translation = random.choice(all_words)
    all_translations = [item[1] for item in all_words]
    keyboard = create_quiz_keyboard(correct_translation, all_translations)

    user_quiz_data[user_id] = {'word': word, 'correct_translation': correct_translation}
    bot.send_message(user_id, f"Что означает слово '{word}'?", reply_markup=keyboard)


def quiz_answer_handler(message):
    user_id = message.chat.id
    if message.text == "Завершить викторину 🚫":
        user_stats[user_id]['in_quiz'] = False
        bot.send_message(user_id, "Вы завершили викторину!", reply_markup=main_menu())
        return

    data = user_quiz_data.get(user_id)
    if not data or 'correct_translation' not in data:
        bot.send_message(user_id, "Ошибка в данных викторины. Попробуйте снова.", reply_markup=main_menu())
        return

    correct_translation = data['correct_translation']
    if message.text == correct_translation:
        bot.send_message(user_id, "✅ Правильно!")
        user_stats[user_id]['correct'] += 1
        next_quiz_question(message)
    else:
        bot.send_message(user_id, "🔴 Неправильно! Попробуйте еще раз.")
        user_stats[user_id]['incorrect'] += 1


def show_stats(message):
    user_id = message.chat.id
    stats = user_stats.get(user_id, {'correct': 0, 'incorrect': 0})
    bot.send_message(message.chat.id, f"Угадано слов: {stats['correct']}\nОшибки: {stats['incorrect']}")


def handle_unrecognized_text(message):
    bot.send_message(message.chat.id, "Я не понимаю, что вы хотите. Пожалуйста, воспользуйтесь меню.",
                     reply_markup=main_menu())


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["📗 Добавить слово", "❌ Удалить слово", "🎲 Начать викторину", "📈 Статистика"]
    keyboard.add(*buttons)
    return keyboard


if __name__ == '__main__':
    db.create_tables()  # Создание таблиц в базе данных если их нет. База должна уже быть.
    db.add_test_data()  # Добавление тестовых данных (закомментируйте после страта, чтобы не плодить дубликаты в БД)
    bot.polling(none_stop=True)
