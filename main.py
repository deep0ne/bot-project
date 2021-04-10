import requests
from bs4 import BeautifulSoup
import telebot
import re
from random import randint
import config
import dbworker
from vedis import Vedis
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from flask import Flask, request
import os

bot = telebot.TeleBot(config.token)

def math_parsing(tag=0):
    url = "http://mathprofi.ru/matematika_dlya_chainikov.html"
    website = requests.get(url)
    soup = BeautifulSoup(website.content, 'lxml')
    math_dict = {}
    topics = soup.find_all('p')
    for topic in topics:
        if topic.get('class') == ['classtopic']:
            topic = topic.text.strip().replace(':', '').lower()
            math_dict[topic] = []
    themes = soup.find_all('p', {'class': 'classs'})
    n = 0
    content = {}

    for i in range(1, 16):
        for j in themes[i].find_all('a', {'class': 'classbar'}):
            content[j.get_text(separator=' ').replace('  ', ' ').replace(',', '.').title()] = 'mathprofi.ru/' + j.get(
                'href')
            math_dict[list(math_dict.keys())[n]] = content
        content = {}
        n += 1

    return math_dict


def py_parsing(n, *themes):
    driver = webdriver.Chrome('C:\Program Files (x86)\Chrome driver\chromedriver.exe')

    for theme in themes:
        themes = theme
    print(themes)
    py_info = []
    substring = 'python'
    driver.get("https://www.programiz.com/")
    for py_topic in themes:
        py_topic += ' python'
        py_field = driver.find_element_by_xpath('//*[@id="edit-keys-2"]')
        py_field.click()
        py_field.send_keys(py_topic)

        py_button = driver.find_element_by_xpath(
            '//*[@id="search-api-page-search-form-simplest-programming-tutorials-f"]/div/div/button[3]')
        py_button.click()

        links = []
        my_page = BeautifulSoup(driver.page_source, 'lxml')
        search_results = my_page.find_all('div', {'class': 'search-result__row'})
        for row in search_results:
            for j in row.find_all('a', href=True):
                if re.search(substring, j['href'].lower()):
                    links.append(j['href'])
        for link in links[:int(n)]:
            py_info.append('programiz.com' + link)

        close_button = driver.find_element_by_xpath('//*[@id="search-api-page-search-form-simplest-programming-tutorials-f"]/div/div/button[2]')
        close_button.click()
        time.sleep(0.5)
    driver.close()
    #
    return py_info

def ml_parsing(n, *themes):
    driver = webdriver.Chrome('C:\Program Files (x86)\Chrome driver\chromedriver.exe')
    for theme in themes:
        themes = theme
    print(themes)
    ml_info = []
    substring_1, substring_2 = 'post', 'blog'
    driver.get("https://habr.com/ru/top/")
    for ml_topic in themes:

        ml_field = driver.find_element_by_xpath('//*[@id="search-form-btn"]')
        ml_field.click()

        search = driver.find_element_by_xpath('//*[@id="search-form-field"]')
        search.click()
        search.send_keys(ml_topic)
        search.send_keys(Keys.ENTER)

        links = []
        my_page = BeautifulSoup(driver.page_source, 'lxml')
        search_results = my_page.find_all('article', {'class': 'post post_preview'})
        for row in search_results:
            for j in row.find_all('a', href=True):
                if re.search(substring_1, j['href'].lower()) and '#habracut' not in j['href'] and '#comments' not in j['href']\
                        or re.search(substring_2, j['href'].lower()) and '#habracut' not in j['href'] and '#comments' not in j['href']:
                    links.append(j['href'])

        for link in links[:int(n)]:
            ml_info.append(link)

        new_search = driver.find_element_by_xpath('//*[@id="TMpanel"]/div/div[1]/a')
        new_search.click()

    driver.close()
    return ml_info

def youtube_parsing(n, *themes):
    driver = webdriver.Chrome('C:\Program Files (x86)\Chrome driver\chromedriver.exe')
    for theme in themes:
        themes = theme
    print(themes)
    info = []
    driver.get("https://www.youtube.com/")
    for topic in themes:
        field = driver.find_element_by_xpath('//*[@id="search"]')
        field.click()
        field.send_keys(topic)
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        links = []
        my_page = BeautifulSoup(driver.page_source, 'lxml')

        search_results = my_page.find_all('h3', {'class': 'title-and-badge style-scope ytd-video-renderer'})
        for row in search_results:
            for j in row.find_all('a', href=True):
                links.append(j['href'])

        for link in links[:int(n)]:
            info.append('youtube.com' + link)

        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
    driver.close()
    return info

pict = [
    'https://www.computerra.ru/wp-content/uploads/2019/08/data_science_1.jpg',
    'https://media.vlpt.us/images/miscaminos/post/c82c4298-122e-4d25-ab81-19d4002b092d/datascience-pdusit-stock.jpg',
    'https://www.zdnet.com/a/hub/i/2016/04/20/b5d1ab3b-a81b-4f38-87a0-fe5999692810/big-data-path.jpg',
    'https://www.learnnow.de/wp-content/uploads/2019/02/Data-Science-Bootcamp-380x253.jpg',
    'https://s27389.pcdn.co/wp-content/uploads/2019/12/top-5-data-science-strategy-predictions-2020-1024x440.jpeg',
    'https://www.american.edu/spa/data-science/images/datascience-hero.jpg',
    'https://thumbor.forbes.com/thumbor/960x0/https%3A%2F%2Fspecials-images.forbesimg.com%2Fdam%2Fimageserve%2F955572446%2F960x0.jpg%3Ffit%3Dscale',
    'https://brandculture.london/wp-content/uploads/2019/03/Screenshot-2019-03-21-at-16.21.59-1920x1080.png',
    'https://www.druva.com/assets/blog-understanding-neural-networks-through-visualization-post.jpg',
    'https://www.tadviser.ru/images/thumb/1/15/Machine-Learning-tech.jpg/840px-Machine-Learning-tech.jpg',
]


# @bot.message_handler()
# def echo(message):
#     bot.send_photo(message.chat.id, pict[randint(0, 10)])


@bot.message_handler(commands=["info"])
def cmd_info(message):
    bot.send_message(message.chat.id, "Команда /info покажет тебе, как мною можно пользоваться.\n"
                                      "Я могу найти для тебя информацию по математике, питону или машинному обучению.\n"
                                      "Сначала тебе нужно выбрать что-то из трёх тем.\n"
                                      "Пока что я умею скидывать только статьи или видео.\n"
                                      "Поэтому нужно выбрать doc или vid.\n"
                                      "Напиши /reset чтобы начать заново.")
    bot.send_message(message.chat.id, "После этого тебе нужно прислать /content, чтобы посмотреть, о чём у меня есть информация.\n"
                                      "Все темы нужно вводить через запятую.\n"
                                      "Например вот так: Пределы, производные функций, ФНП.\n"
                                      "Ты также можешь посмотреть примерные темы в /mathcontent, /pycontent или /mlcontent\n"
                                      "В зависимости от твоего выбора тебе будет предложено выбрать количество статей/видео или подтему. \n"
                                      "Подтемы нужно также вводить через запятую (ВНИМАНИЕ: в подтеме может быть вопрос)\n"
                                      "Например: Замечательные пределы, что такое производная?, метод касательных \n"
                                      "При выборе количества статей/видео, нужно прислать число (оптимальное от 1 до 3).\n")

@bot.message_handler(commands=["content"])
def content(message):
    if dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_FIELD.value:
        bot.send_message(message.chat.id, 'Погоди, мы пока ещё не решили, что тебе нужно.\n'
                                          'Сейчас тебе нужно ввести /math, если хочешь получить что-то по математике.\n'
                                          '/python - по питону, /ml - по машинному обучению')
    elif dbworker.get_current_state(message.chat.id) == config.States.S_TYPE_OF_INFO.value:
        bot.send_message(message.chat.id, 'Не спеши, теперь тебе нужно выбрать, что ты хочешь: статья или видео.\n'
                                          'Напиши /doc для статьи или /vid для видео')
    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'math'\
            and dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        content = math_parsing()
        bot.send_message(message.chat.id, ', '.join(i.title() for i in content.keys()))

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'python'\
            and dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        bot.send_message(message.chat.id, "Пришли мне интересующую тебя тему, и я попробую найти для тебя статейку.\n"
                                          "Например, напиши 'list comprehensions'.\n"
                                          "Запрос нужно сделать на английском.\n"
                                          "У меня есть небольшой список тем, которые могут тебя заинтересовать.\n"
                                          "Но тебе не обязательно ими ограничиваться. Чтобы посмотреть их, пришли /pycontent.")

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'ml'\
            and dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        bot.send_message(message.chat.id, "Пришли мне интересующую тебя тему, и я попробую найти для тебя статейку.\n"
                                          "Например, напиши 'линейная регрессия' или 'linear regression'.\n"
                                          "У меня есть небольшой список тем, которые могут тебя заинтересовать.\n"
                                          "Но тебе не обязательно ими ограничиваться. Чтобы посмотреть их, пришли /mlcontent.")

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'math'\
        and dbworker.get_current_state(str(message.chat.id) + 'content') == 'vid':
        bot.send_message(message.chat.id, "Пришли мне интересующую тебя тему, и я попробую найти для тебя видео.\n"
                                          "Например, напиши 'линейная алгебра' или 'linear algebra'.\n"
                                          "У меня есть небольшой список тем, которые могут тебя заинтересовать.\n"
                                          "Но тебе не обязательно ими ограничиваться. Чтобы посмотреть их, пришли /mathcontent.")

    elif dbworker.get_current_state(str(message.chat.id)+ "field") == 'python'\
        and dbworker.get_current_state(str(message.chat.id) + 'content') == 'vid':
        bot.send_message(message.chat.id, "Пришли мне интересующую тебя тему, и я попробую найти для тебя видео.\n"
                                          "Например, напиши 'списковые включения' или 'list comprehensions'.\n"
                                          "У меня есть небольшой список тем, которые могут тебя заинтересовать.\n"
                                          "Но тебе не обязательно ими ограничиваться. Чтобы посмотреть их, пришли /pycontent.")

    elif dbworker.get_current_state(str(message.chat.id) + "field") == 'ml'\
        and dbworker.get_current_state(str(message.chat.id) + 'content') == 'vid':
        bot.send_message(message.chat.id, "Пришли мне интересующую тебя тему, и я попробую найти для тебя видео.\n"
                                          "Например, напиши 'линейная регрессия' или 'linear regression'.\n"
                                          "У меня есть небольшой список тем, которые могут тебя заинтересовать.\n"
                                          "Но тебе не обязательно ими ограничиваться. Чтобы посмотреть их, пришли /mlcontent.")

@bot.message_handler(commands=["pycontent"])
def pycontent(message):
    my_list = ['Functions', 'Data Types', 'File Handling', 'Object & Class',
               'Variables', 'If else', 'For loop', 'While loop', 'Break', 'Continue',
               'Pass', 'Recursion', 'Global, local and Nonlocal', 'Modules', 'List',
               'Tuple', 'Set', 'Dictionary', 'String', 'Integer', 'Float', 'Exception',
               'OOP', 'Class', 'Iterator', 'Generator', 'Decorators', 'RegEx']
    bot.send_message(message.chat.id, '- ' + '\n- '.join(i for i in my_list))

@bot.message_handler(commands=["mlcontent"])
def mlcontent(message):
    my_list = ['Линейная регрессия', 'Градиентные методы обучения', 'Классификация',
               'Логистическая регрессия', 'SVM', 'Решающие деревья', 'Бэггинг',
               'Случайные леса', 'Градиентный бустинг', 'Понижение размерности',
               'Кластеризация', 'Поиск аномалий', 'Рекомендательные системы',
               'Регуляризация', 'Переобучение']
    bot.send_message(message.chat.id, '- ' + '\n- '.join(i for i in my_list))

@bot.message_handler(commands=['mathcontent'])
def mathcontent(message):
    discrete_math = ['Множества', 'Комбинаторика', 'Неориентированные графы', 'Ориентированные графы',
                     'Алгоритмы на графах']

    calculus = ['Математический анализ', 'Функции одной переменной',
                'Пределы', 'Производная', 'Касательные', 'Критические точки функции',
                'Максимум и минимум функции', 'Интегралы', 'Функции нескольких переменных',
                'Градиент функции', 'Производная по направлению', 'Линии уровня функции',
                'Касательная плоскость', 'Оптимизационные задачи', 'Лагранжиан', 'Геометрический смысл лагранжа']
    linear_algebra = ['Линейная алгебра', 'Системы линейных уравнений', 'Матрицы', 'Обратимость и невырожденность',
                      'Определитель', 'Обратная матрица', 'Векторные пространства', 'Размерности', 'Ранги матриц',
                      'Линейные отображения', 'Билинейные и квадратичные формы', 'Скалярное произведение', 'Ортогонализация',
                      'QR разложение', 'Линейные классификаторы', 'Линейные многообразия', 'Сингулярное разложение']
    probability = ['Теория вероятностей', 'Пространство элементарных исходов', 'Случайные события', 'Вероятность и её свойства',
                   'Формула Байеса', 'Дискретные случайные величины', 'Распределение случайной величины',
                   'Независимость случайных величин', 'Математическое ожидание и дисперсия', 'Равномерное распределение',
                   'Нормальное распределение', 'Экспоненциальное распределение', 'Функции распределения',
                   'Многомерные случайные величины', 'Ковариация и корреляция', 'Неравенство маркова и чебышева',
                   'Неравенства концетрации', 'Закон больших чисел', 'Центральная предельная теорема']

    bot.send_message(message.chat.id, text='*Дискретная математика*\n\n' +
                     ', '.join([e + '\n' if i % 6 == 5 else e for i, e in enumerate(discrete_math)]).replace('\n,', ',\n'), parse_mode='Markdown')

    bot.send_message(message.chat.id, text='*Математический анализ*\n\n' +
                                           ', '.join([e + '\n' if i % 6 == 5 else e for i, e in
                                                      enumerate(calculus)]).replace('\n,', ',\n'), parse_mode='Markdown')

    bot.send_message(message.chat.id, text='*Линейная алгебра*\n\n' +
                                           ', '.join([e + '\n' if i % 6 == 5 else e for i, e in
                                                      enumerate(linear_algebra)]).replace('\n,', ',\n'), parse_mode='Markdown')

    bot.send_message(message.chat.id, text='*Теория вероятностей*\n\n' +
                                           ', '.join([e + '\n' if i % 6 == 5 else e for i, e in
                                                      enumerate(probability)]).replace('\n,', ',\n'), parse_mode='Markdown')

@bot.message_handler(commands=["commands"])
def cmd_commands(message):
    bot.send_message(message.chat.id,
                     "/reset - команда для того, чтобы всё сбросить и начать заново.\n"
                     "/start - команда для начала диалога с ботом.\n"
                     "/info - команда для того, чтобы посмотреть, что я умею.\n"
                     "/commands - ты уже знаешь, зачем это.\n"
                     "/mathcontent - примеры тем по математике.\n"
                     "/pycontent - примеры тем по питону.\n"
                     "/mlcontent - примеры тем по машинному обучению.")


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Давай начнём заново.\n"
                                      "О чём ты хочешь получить информацию: /math, /python или /ml.\n"
                                      "Отправь /info или /commands, чтобы я напомнил тебе, что я умею.")
    bot.send_photo(message.chat.id, pict[randint(0, 9)])
    dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "Привет! Я Data Science бот.\n"
                                      "Я могу помочь тебе найти интересную информацию о Data Science. Я могу найти информацию по математике, питону или машинному обучению. Напиши /math, /python или /ml.\n"
                                      "Напиши /info, чтобы посмотреть, что я умею.\n"
                                      "Напиши /commands, чтобы посмотреть, какие команды я могу выполнить.\n"
                                      "Или напиши /reset чтобы всё сбросить и начать заново.")
    bot.send_photo(message.chat.id, pict[randint(0, 9)])
    dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)


@bot.message_handler(
    func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_FIELD.value)
                         and message.text.strip().lower() not in
                         ('/reset', '/info', '/start', '/commands',
                          '/mlcontent', '/mathcontent', '/pycontent'))
def cmd_day(message):
    dbworker.del_state(str(message.chat.id) + 'field')
    if message.text.lower().strip() == '/math':
        bot.send_message(message.chat.id, "Ок, математика. Давай дальше. \n"
                                          "Что тебе прислать? Статейку или видео?\n"
                                          "Для статьи напиши /doc, для видео - /vid.\n"
                                          "Не забудь, что /info показывает, что я могу делать.\n"
                                          "Напиши /reset, чтобы начать заново.")
        dbworker.set_property(str(message.chat.id) + 'field', 'math')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_TYPE_OF_INFO.value)
    elif message.text.lower().strip() == '/python':
        bot.send_message(message.chat.id, "Хорошо, давай по питону. \n"
                                          "Что тебе прислать? Статейку или видео?\n"
                                          "Для статьи напиши /doc, для видео - /vid.\n"
                                          "Не забудь, что /info показывает, что я могу делать.\n"
                                          "Напиши /reset, чтобы начать заново.")

        dbworker.set_property(str(message.chat.id) + 'field', 'python')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_TYPE_OF_INFO.value)
    elif message.text.lower().strip() == '/ml':
        bot.send_message(message.chat.id, "Ага, машинное обучение. \n"
                                          "Что тебе прислать? Статейку или видео?\n"
                                          "Для статьи напиши /doc, для видео - /vid.\n"
                                          "Не забудь, что /info показывает, что я могу делать.\n"
                                          "Напиши /reset, чтобы начать заново.")
        dbworker.set_property(str(message.chat.id) + 'field', 'ml')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_TYPE_OF_INFO.value)
    else:
        bot.send_message(message.chat.id, "Я не очень понял твой запрос.\n"
                                          "Сейчас тебе нужно выбрать, о чём ты хочешь получить информацию.\n"
                                          "Я могу прислать тебе информацию по математике, питону или машинному обучению. \n"
                                          "Напиши /math, /python или /ml.\n"
                                          "Не забудь, что /info показывает, что я могу делать.\n"
                                          "Напиши /reset, чтобы начать заново.")


@bot.message_handler(
    func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_TYPE_OF_INFO.value)
                         and message.text.strip().lower() not in
                         ('/reset', '/info', '/start', '/commands',
                          '/mlcontent', '/mathcontent', '/pycontent'))
def cmd_country_or_region(message):
    dbworker.del_state(str(message.chat.id) + 'content')
    if message.text.lower().strip() == '/doc':
        bot.send_message(message.chat.id, "Хорошо, я могу прислать статью.\n"
                                          "Чтобы посмотреть, о чём у меня есть информация, напиши /content.\n"
                                          "После этого выбери интересующие тебя темы и пришли мне их через запятую.\n"
                                          "Можешь написать /info, если забыл, как всё это работает.\n"
                                          "Чтобы начать заново, напиши /reset")

        dbworker.set_property(str(message.chat.id) + 'content', 'doc')  # запишем день в базу
        dbworker.set_state(message.chat.id, config.States.S_ENTER_TYPE_OF_CONTENT.value)

    elif message.text.lower().strip() == '/vid':
        bot.send_message(message.chat.id, "Хорошо, я могу прислать видео.\n"
                                          "Чтобы посмотреть, о чём у меня есть информация, напиши /content.\n"
                                          "После этого выбери интересующие тебя темы и пришли мне их через запятую.\n"
                                          "Можешь написать /info, если забыл, как всё это работает.\n"
                                          "Чтобы начать заново, напиши /reset")

        dbworker.set_property(str(message.chat.id) + 'content', 'vid')
        dbworker.set_state(message.chat.id, config.States.S_ENTER_TYPE_OF_CONTENT.value)

    else:
        bot.send_message(message.chat.id, "Что-то пошло не так. Введи /doc или /vid.\n"
                                          "Напиши /info, чтобы я напомнил тебе, как я работаю.\n"
                                          "Напиши /reset, чтобы начать заново.")


@bot.message_handler(
    func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_TYPE_OF_CONTENT.value)
                         and message.text.strip().lower() not in
                         ('/reset', '/info', '/start', '/commands',
                          '/mlcontent', '/mathcontent', '/pycontent'))
def cmd_list_of_content(message):
    dbworker.del_state(str(message.chat.id) + 'list_of_content')
    if dbworker.get_current_state(str(message.chat.id) + 'field') == 'math' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        list_of_content = [x.strip().lower() for x in re.split(',', message.text)]
        bot.send_message(message.chat.id, 'Секунду, проверяю...')
        x = math_parsing()
        lst = [i for i in x.keys()]

        errors = [i for i in list_of_content if i not in lst]

        if len(errors) == 0:
            if list_of_content != list():
                bot.send_message(message.chat.id, "Хорошо. Вы выбрали темы, которые Вам интересны.\n"
                                                  "Теперь Вам нужно выбрать подтему, чтобы я мог прислать статью.\n"
                                                  "Через пару секунд снизу появятся список этих самых подтем.\n"
                                                  "Пришлите мне их через запятую.")
                time.sleep(5)
                for element in list_of_content:
                    bot.send_message(message.chat.id,
                                     "Вы выбрали следующую тему: " + element.title() + "\n\n" + "- " + "\n- ".join(
                                         x[element].keys()))

                dbworker.set_property(str(message.chat.id) + 'list_of_content', ', '.join(list_of_content))
                dbworker.set_state(message.chat.id, config.States.S_ENTER_SUBTOPICS_LIST.value)
            else:
                bot.send_message(message.chat.id, 'Введите список тем правильно!')
        else:
            bot.send_message(message.chat.id,
                             "Ты где-то ошибся.\n"
                             "Скорее всего здесь: " + ", ".join(errors) + "\n"
                                                                          "Чтобы посмотреть, как нужно вводить необходимую информацию, напиши /content")

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'python' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        bot.send_message(message.chat.id, "Хорошо. Вы выбрали темы, которые Вам интересны.\n"
                                          "Теперь пришлите количество статей от 1 до 3")

        list_of_content = [x.strip().lower() for x in re.split(',', message.text)]
        dbworker.set_property(str(message.chat.id) + 'list_of_content', ', '.join(list_of_content))
        dbworker.set_state(message.chat.id, config.States.S_ENTER_SUBTOPICS_LIST.value)

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'ml' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        bot.send_message(message.chat.id, "Хорошо. Вы выбрали темы, которые Вам интересны.\n"
                                          "Теперь пришлите количество статей от 1 до 3")

        list_of_content = [x.strip().lower() for x in re.split(',', message.text)]
        dbworker.set_property(str(message.chat.id) + 'list_of_content', ', '.join(list_of_content))
        dbworker.set_state(message.chat.id, config.States.S_ENTER_SUBTOPICS_LIST.value)

    elif dbworker.get_current_state(str(message.chat.id) + 'content') == 'vid':
        bot.send_message(message.chat.id, "Хорошо. Вы выбрали темы, которые Вам интересны.\n"
                                          "Теперь пришлите количество статей от 1 до 3")

        list_of_content = [x.strip().lower() for x in re.split(',', message.text)]
        dbworker.set_property(str(message.chat.id) + 'list_of_content', ', '.join(list_of_content))
        dbworker.set_state(message.chat.id, config.States.S_ENTER_SUBTOPICS_LIST.value)


@bot.message_handler(
    func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_SUBTOPICS_LIST.value)
                         and message.text.strip().lower() not in
                         ('/reset', '/info', '/start', '/commands',
                          '/mlcontent', '/mathcontent', '/pycontent'))
def cmd_topics(message):
    if dbworker.get_current_state(str(message.chat.id) + 'field') == 'math' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        subtopics = [x.strip().lower() for x in re.split(',', message.text)]
        bot.send_message(message.chat.id, 'Секунду, проверяю...')
        list_of_content = dbworker.get_current_state(str(message.chat.id) + 'list_of_content').split(', ')
        x = math_parsing()
        errors, links = [], []
        info = []
        for element in list_of_content:
            for j in x[element].keys():
                info.append(j.replace('  ', ' ').lower())
        for subtopic in subtopics:
            if subtopic.lower() not in info:
                errors.append(subtopic)
        print(x)
        if errors == []:
            if list_of_content != []:
                dbworker.set_state(message.chat.id, config.States.S_START.value)
                for element in list_of_content:
                    for subtopic in subtopics:
                        try:
                            links.append(x[element.lower()][subtopic.title()].replace(' ', '%20'))
                        except:
                            pass
                bot.send_message(message.chat.id, "Вот твои ссылки.\n" + '\n'.join(x for x in links))
                dbworker.del_state(str(message.chat.id) + 'field')
                dbworker.del_state(str(message.chat.id) + 'content')
                dbworker.del_state(str(message.chat.id) + 'list_of_content')
                dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)
        else:
            bot.send_message(message.chat.id,
                             "Похоже, вы где-то ошиблись.\n"
                             "Скорее всего здесь: " + ", ".join(errors) + "\n"
                                                                          "Я прислал тебе подтемы, тебе нужно выбрать из них.")

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'python' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        py_topics = dbworker.get_current_state(str(message.chat.id) + 'list_of_content').split(', ')
        number_of_topics = message.text
        if number_of_topics.isdigit():
            bot.send_message(message.chat.id, 'Секунду, проверяю...\n'
                                              'Поиск может занять некоторое время...\n')
            x = py_parsing(number_of_topics, py_topics)
            if len(x) == 0:
                bot.send_message(message.chat.id, "Я ничего не нашёл.\n"
                                                  "Возможно, ты ввёл запрос на русском.\n"
                                                  "Либо я ничего не смог найти по твоей теме.\n"
                                                  "Давай попробуем ещё раз.\n"
                                                  "Введите интересующие вас темы через запятую.\n"
                                                  "Введи /content, если запутался")
                dbworker.set_state(message.chat.id, config.States.S_ENTER_TYPE_OF_CONTENT.value)
            else:
                bot.send_message(message.chat.id, "Вот твои ссылки.\n" + '\n'.join(link for link in x))
                dbworker.del_state(str(message.chat.id) + 'field')
                dbworker.del_state(str(message.chat.id) + 'content')
                dbworker.del_state(str(message.chat.id) + 'list_of_content')
                dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)
        else:
            bot.send_message(message.chat.id, 'Нужно ввести цифру')

    elif dbworker.get_current_state(str(message.chat.id) + 'field') == 'ml' and \
            dbworker.get_current_state(str(message.chat.id) + 'content') == 'doc':
        ml_topics = dbworker.get_current_state(str(message.chat.id) + 'list_of_content').split(', ')
        number_of_topics = message.text
        if number_of_topics.isdigit():
            bot.send_message(message.chat.id, 'Секунду, проверяю...\n'
                                              'Поиск может занять некоторое время...\n')
            x = ml_parsing(number_of_topics, ml_topics)
            if len(x) == 0:
                bot.send_message(message.chat.id, "Я ничего не нашёл.\n"
                                                  "Возможно, ты ввёл запрос с ошибками.\n"
                                                  "Либо я ничего не смог найти по твоей теме.\n"
                                                  "Давай попробуем ещё раз.\n"
                                                  "Введите интересующие вас темы через запятую.\n"
                                                  "Введи /content, если запутался")
                dbworker.set_state(message.chat.id, config.States.S_ENTER_TYPE_OF_CONTENT.value)
            else:
                bot.send_message(message.chat.id, "Вот твои ссылки.\n" + '\n'.join(link for link in x))
                dbworker.del_state(str(message.chat.id) + 'field')
                dbworker.del_state(str(message.chat.id) + 'content')
                dbworker.del_state(str(message.chat.id) + 'list_of_content')
                dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)

        else:
            bot.send_message(message.chat.id, 'Нужно ввести цифру')
    elif dbworker.get_current_state(str(message.chat.id) + 'content') == 'vid':
        vid_topics = dbworker.get_current_state(str(message.chat.id) + 'list_of_content').split(', ')
        number_of_topics = message.text
        if number_of_topics.isdigit():
            bot.send_message(message.chat.id, 'Секунду, проверяю...\n'
                                              'Поиск может занять некоторое время...\n')
            x = youtube_parsing(number_of_topics, vid_topics)
            if len(x) == 0:
                bot.send_message(message.chat.id, "Я ничего не нашёл.\n"
                                                  "Возможно, ты ввёл запрос с ошибками.\n"
                                                  "Либо я ничего не смог найти по твоей теме.\n"
                                                  "Давай попробуем ещё раз.\n"
                                                  "Введите интересующие вас темы через запятую.")
                dbworker.set_state(message.chat.id, config.States.S_ENTER_TYPE_OF_CONTENT.value)
            else:
                bot.send_message(message.chat.id, "Вот твои ссылки.\n" + '\n'.join(link for link in x))
                dbworker.del_state(str(message.chat.id) + 'field')
                dbworker.del_state(str(message.chat.id) + 'content')
                dbworker.del_state(str(message.chat.id) + 'list_of_content')
                dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Давай начнём заново.\n"
                                      "О чём ты хочешь получить информацию: /math, /python или /ml.\n"
                                      "Отправь /info или /commands, чтобы я напомнил тебе, что я умею.")
    bot.send_photo(message.chat.id, pict[randint(0, 9)])
    dbworker.del_state(str(message.chat.id) + 'field')
    dbworker.del_state(str(message.chat.id) + 'content')
    dbworker.del_state(str(message.chat.id) + 'list_of_content')

    dbworker.set_state(message.chat.id, config.States.S_ENTER_FIELD.value)


@bot.message_handler(func=lambda message: message.text not in ('/reset', '/info', '/start', '/commands',
                                                               '/mlcontent',
                                                               '/mathcontent',
                                                               '/pycontent'))
def cmd_sample_message(message):
    bot.send_message(message.chat.id, "Привет, я Data Science бот!\n"
                                      "Ты здесь, чтобы погрузиться в науку о данных?\n"
                                      "Я могу помочь тебе с этим.\n"
                                      "Напиши /start и начнём. \n"
                                      "Напиши /info, чтобы посмотреть, что я умею.\n"
                                      "Напиши /commands, чтобы посмотреть, какие команды я могу выполнить")
    bot.send_photo(message.chat.id, pict[randint(0, 9)])


if __name__ == '__main__':
    bot.infinity_polling()
