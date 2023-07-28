import telebot
import json
from database.dbapi import DatabaseConnector
token = "6239732739:AAGddbGuWpFloyrlPy-eXaryiD-W0pBcg7Y"
bot = telebot.TeleBot(token)


class AddBookState:
    def __init__(self):
        self.title = None
        self.author = None
        self.published = None


class FindBookState:
    def __init__(self):
        self.title = None
        self.author = None
        self.published = None
        self.book_to_find_id = None


class DeleteBookState:
    def __init__(self):
        self.title = None
        self.author = None
        self.published = None
        self.confirmation = None
        self.book_to_delete_id = None

class BorrowBookState:
    def __init__(self):
        self.title = None
        self.author = None
        self.published = None
        self.book_to_borrow_id = None

class StatsBookState:
    def __init__(self):
        self.title = None
        self.author = None
        self.published = None

db_api = DatabaseConnector()
add_book_state = AddBookState()
delete_book_state = AddBookState()
find_book_state = FindBookState()
borrow_book_state = BorrowBookState()
stats_book_state = StatsBookState()


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Добро пожаловать в чат бота-библиотеки!")


@bot.message_handler(commands=['add'])
def handle_add_book(message):
    add_book_state.title = None
    add_book_state.author = None
    add_book_state.published = None
    new_message = bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(new_message, handle_add_get_title)


def handle_add_get_title(message):
    add_book_state.title = message.text
    new_message = bot.send_message(message.chat.id, "Введите автора книги:")
    bot.register_next_step_handler(new_message, handle_add_get_author)


def handle_add_get_author(message):
    add_book_state.author = message.text
    new_message = bot.send_message(message.chat.id, "Введите год издания книги:")
    bot.register_next_step_handler(new_message, handle_add_get_year)


def handle_add_get_year(message):
    add_book_state.published = message.text
    add_book(message)


def add_book(message):
    try:
        book_ip = db_api.add(add_book_state.__dict__)
    except Exception as exp:
        bot.send_message(message.chat.id, "Ошибка при добавлении книги." + f"{str(exp)}")
    else:
        bot.send_message(message.chat.id, f"Книга добавлена ({book_ip}).")


@bot.message_handler(commands=['delete'])
def handle_delete_book(message):
    delete_book_state.title = None
    delete_book_state.author = None
    delete_book_state.published = None
    new_message = bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(new_message, handle_delete_get_title)


def handle_delete_get_title(message):
    delete_book_state.title = message.text
    new_message = bot.send_message(message.chat.id, "Введите автора книги:")
    bot.register_next_step_handler(new_message, handle_delete_get_author)


def handle_delete_get_author(message):
    delete_book_state.author = message.text
    new_message = bot.send_message(message.chat.id, "Введите год издания книги:")
    bot.register_next_step_handler(new_message, handle_delete_get_year)


def handle_delete_get_year(message):
    delete_book_state.published = message.text
    delete_book(message)

def delete_book(message):
    delete_book_state.book_to_delete_id = db_api.get_book(delete_book_state.title, delete_book_state.author, delete_book_state.published)
    if delete_book_state.book_to_delete_id is not None:
        new_message = bot.send_message(message.chat.id,
                                       f"Найдена книга: {delete_book_state.title} {delete_book_state.author} "
                                       f"{delete_book_state.published}. Удаляем? (Да/Нет)")
        bot.register_next_step_handler(new_message, handle_delete_confirmation)
    else:
        bot.send_message(message.chat.id, "Такой книги у нас нет.")


def handle_delete_confirmation(message):
    if message.text == "Да":
        try:
            db_api.delete(delete_book_state.book_to_delete_id)
        except Exception as ex:
            bot.send_message(message.chat.id, f"Невозможно удалить книгу. {str(ex)}")
        else:
            bot.send_message(message.chat.id, "Книга удалена.")
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Удаление отменено.")
    else:
        bot.send_message(message.chat.id, "Ответ не распознан. Повторите комманду.")


@bot.message_handler(commands=['list'])
def handle_list(message):
    try:
        book_list = db_api.list_books()
    except Exception as ex:
        bot.send_message(message.chat.id, f"Не удалось получить список книг. {str(ex)}")
    else:
        list_message = ""
        for book in book_list:
            list_message += f"{book['title']}, {book['author']}, {book['published']}"
            if book["date_deleted"] is not None:
                list_message += " (Удалена)"
            list_message += "\n"
        bot.send_message(message.chat.id, list_message)


@bot.message_handler(commands=['find'])
def handle_find_book(message):
    find_book_state.title = None
    find_book_state.author = None
    find_book_state.published = None
    new_message = bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(new_message, handle_find_get_title)


def handle_find_get_title(message):
    find_book_state.title = message.text
    new_message = bot.send_message(message.chat.id, "Введите автора книги:")
    bot.register_next_step_handler(new_message, handle_find_get_author)

def handle_find_get_author(message):
    find_book_state.author = message.text
    new_message = bot.send_message(message.chat.id, "Введите год издания книги:")
    bot.register_next_step_handler(new_message, handle_find_get_year)


def handle_find_get_year(message):
    find_book_state.published = message.text
    find_book(message)

def find_book(message):
    find_book_state.book_to_find_id = db_api.get_book(find_book_state.title, find_book_state.author, find_book_state.published)
    if find_book_state.book_to_find_id != None:
        bot.send_message(message.chat.id,
                         f"Найдена книга: {delete_book_state.title} {delete_book_state.author} {delete_book_state.published}.")
    else:
        bot.send_message(message.chat.id, "Такой книги у нас нет.")


@bot.message_handler(commands=['borrow'])
def handle_borrow_book(message):
    borrow_book_state.title = None
    borrow_book_state.author = None
    borrow_book_state.published = None
    new_message = bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(new_message, handle_borrow_get_title)

def handle_borrow_get_title(message):
    borrow_book_state.title = message.text
    new_message = bot.send_message(message.chat.id, "Введите автора книги:")
    bot.register_next_step_handler(new_message, handle_borrow_get_author)


def handle_borrow_get_author(message):
    borrow_book_state.author = message.text
    new_message = bot.send_message(message.chat.id, "Введите год издания книги:")
    bot.register_next_step_handler(new_message, handle_borrow_get_year)

def handle_borrow_get_year(message):
    borrow_book_state.published = message.text
    borrow_book_state.book_to_borrow_id = db_api.get_book(borrow_book_state.title, borrow_book_state.author, borrow_book_state.published)
    if borrow_book_state.book_to_borrow_id is not None:
        new_message = bot.send_message(message.chat.id, f"Найдена книга: {borrow_book_state.title} {borrow_book_state.author} {borrow_book_state.published}. Берем?(Да/Нет)")
        bot.register_next_step_handler(new_message, handle_borrow_confirmation)
    else:
        bot.send_message(message.chat.id, "Такой книги нет в библиотеке")

def handle_borrow_confirmation(message):
    if message.text == "Да":
        book = {
            "book_id": borrow_book_state.book_to_borrow_id,
            "title": borrow_book_state.title,
            "author": borrow_book_state.author,
            "published": borrow_book_state.published
        }
        borrowed_id = db_api.borrow(message.chat.id, book)
        if borrowed_id == False:
            bot.send_message(message.chat.id, f"Не удалось взять книгу")
        else:
            bot.send_message(message.chat.id, f"Вы взяли книгу({borrowed_id})")
    if message.text == "Нет":
        bot.send_message(message.chat.id, "Хорошо, не будем брать книгу")


@bot.message_handler(commands=['retrieve'])
def handle_retrieve_book(message):
    borrow_id = db_api.get_borrow(message.chat.id)
    if borrow_id:
        try:
            db_api.retrieve(borrow_id)
        except Exception as e:
            bot.send_message(message.chat.id, f"Не удалось вернуть книгу{str(e)}")
        else:
            bot.send_message(message.chat.id, "Вы вернули книгу")  # название книги?
    else:
        bot.send_message(message.chat.id, "У вас нет взятой книги")

@bot.message_handler(commands=['stats'])
def handle_stats_book(message):
    stats_book_state.title = None
    stats_book_state.author = None
    stats_book_state.published = None
    new_message = bot.send_message(message.chat.id, "Введите название книги:")
    bot.register_next_step_handler(new_message, handle_stats_get_title)

def handle_stats_get_title(message):
    stats_book_state.title = message.text
    new_message = bot.send_message(message.chat.id, "Введите автора книги:")
    bot.register_next_step_handler(new_message, handle_stats_get_author)

def handle_stats_get_author(message):
    stats_book_state.author = message.text
    new_message = bot.send_message(message.chat.id, "Введите год издания книги:")
    bot.register_next_step_handler(new_message, handle_stats_get_published)

def handle_stats_get_published(message):
    stats_book_state.published = message.text
    found_book_id = db_api.get_book(stats_book_state.title, stats_book_state.author, stats_book_state.published)
    if found_book_id is not None:
        bot.send_message(message.chat.id, f"Статистика доступна по адресу http://localhost/download/{found_book_id}")
    else:
        bot.send_message(message.chat.id, "Книга не найдена")


bot.infinity_polling()
