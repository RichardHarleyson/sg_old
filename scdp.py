import importlib
import time
import requests
import json
import random
import os
from time import sleep
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from pyautogui import typewrite, hotkey
import threading

# Модули обработки заданий
import godp
import fbdp
import twdp
import igdp


# Системные функции
# =============================================================

# Функция состояния ожидания
def def_stay():
    print('Default state value. Repeating request in a few minutes')
    time.sleep(30)
    exit()


# Функция загрузки скриптов
def download_scripts(api_key):
    print('Downloading scripts from server')
    print('Initializing download process')
    urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst&apikey='+api_key['apikey'], 'C:\\Python\\sginstall.py')
    exec(open('C:\\Python\\sginstall.py').read())
    print('Update finished')
    time.sleep(10)
    exit()


# Функция перезагрузки устройства
def reboot_device():
    print('Initializing device reboot')
    print('Woops, no reboot yet')
    time.sleep(10)
    exit()


# Функция обновления файловой системы
def renew():
    print('Modules renew initialized')
    try:
        importlib.reload(godp)
    except:
        print('Cant reload godp module')

    try:
        importlib.reload(fbdp)
    except:
        print('Cant reload fbdp module')

    try:
        importlib.reload(twdp)
    except:
         print('Cant reload twdp module')

    try:
        importlib.reload(igdp)
    except:
         print('Cant reload igdp module')


# =============================================================


# Функции работы с браузером
# =============================================================

# Запуск неавторизированного потока с использованием free proxy
def noauth_browser(todo_data):
    print('noauth_browser called')
    try:
        # Получаем имя пользователя для создания профиля браузера
        osuname = os.getlogin()
        br_opts = webdriver.ChromeOptions()
        # Устанавливаем папку с профилем. Генерируем при первом использовании логина,
        # profile = 'user-data-dir=C:\\Users\\' + osuname + '\\AppData\\Local\\Google\\Chrome\\User Data\\' + str(
        #     random.randint(1, 20))
        # br_opts.add_argument(profile)
        # Выставлям язык
        if (todo_data['language'] == 'en'):
            br_opts.add_argument('--lang=en-us')
        else:
            br_opts.add_argument('--lang==ru-ru')
        # Включаем ведение логов
        br_opts.add_argument("--enable-logging")
        # Устанавливаем разрешение окна
        br_opts.add_argument("--window-size=%s" % todo_data['window-size'])
        # Устанавливаем useragent
        br_opts.add_argument("user-agent=%s" % todo_data['useragent'])
        # Устанавливаем прокси, если такой указан
        if (todo_data['proxy'] != '0' or todo_data['proxy'] != ''):
            br_opts.add_argument("--proxy-server=%s" % todo_data['proxy'])
        br_opts.add_argument('--incognito')
        br_opts.add_argument('--dns-prefetch-disable')
        # Подключаем настройки
        browser = webdriver.Chrome(executable_path='C:\\Python\\chromedriver.exe', chrome_options=br_opts)
        # Устанавливаем максимальное время ожидания загрузки страницы - 120.0s
        browser.set_page_load_timeout(300)
        # Проверяем работоспособность прокси
        if (proxy_check(browser) == True):
            print('Browser session started')
            return browser
        elif (proxy_check(browser) == False):
            print('Browser session canceled')
            return 10501
    except:
        return 0


# Запуск авторизированного потока с использованием elite proxy
def auth_browser(todo_data):
    print('auth_browser called')
    # Получаем имя пользователя для создания профиля браузера
    # os.environ["LANG"] = "en_US.UTF-8"
    osuname = os.getlogin()
    try:
        if(todo_data['proxy'] == 0 or todo_data['proxy'] == None):
            return 10501
        # Парсим данные прокси - логин пасс и т.д
        proxy_data = todo_data['proxy'].split(':')
        proxy_ipdata = proxy_data[0] + ':' + proxy_data[1]
        # Задаём параметры инстанса хром
        br_opts = webdriver.ChromeOptions()
        # Устанавливаем папку с профилем. Генерируем при первом использовании логина,
        # или же используем уже созданные если логин был ранее задействован
        br_opts.add_argument(
            'user-data-dir=C:\\Users\\' + osuname + '\\AppData\\Local\\Google\\Chrome\\User Data\\' + todo_data[
                'potokid'])
        # Выставлям язык
        if (todo_data['language'] == 'en'):
            br_opts.add_argument('--lang=en-us')
        else:
            br_opts.add_argument('--lang==ru-ru')
        # Включаем ведение логов
        br_opts.add_argument("--enable-logging")
        # br_opts.add_argument('--dns-prefetch-disable')
        # Устанавливаем разрешение окна
        br_opts.add_argument("--window-size=%s" % todo_data['window-size'])
        # Устанавливаем useragent
        br_opts.add_argument("user-agent=%s" % todo_data['useragent'])
        # Устанавливаем прокси, если такой указан

        if (todo_data['proxy'] != '0' or todo_data['proxy'] != ''):
            br_opts.add_argument("--proxy-server=%s" % proxy_ipdata)

        # Подключаем настройки
        browser = webdriver.Chrome(executable_path='C:\\Python\\chromedriver.exe', chrome_options=br_opts)
        # Устанавливаем таймаут (максимальное время ожидания загрузки страницы) 60.0s
        browser.set_page_load_timeout(60)
        # time.sleep(10)
        # Авторизируем прокси
        print('Authorising proxy')
        # argument = todo_data['proxy']

        proxylog = proxy_data[2]
        proxypas = proxy_data[3]
        threading.Thread(target=proxy_auth, args=(proxylog, proxypas)).start()

        # Переходим на главную гугла. Переход иницирует механизам авторизации прокси
        browser.get("https://google.com")
        # Проверяем работоспособность прокси
        if (proxy_check(browser) == True):
            print('Browser session started')
            return browser
        elif (proxy_check(browser) == False):
            print('Browser session canceled')
            return 10501
    except:
        return 0


# Функция проверки работоспособности прокси
def proxy_check(browser):
    try:
        browser.get("https://google.com")
        time.sleep(30)
        browser.find_element_by_class_name('gsfi')
        print('Proxy check success')
        return True
    except:
        print('Proxy check failed')
        return False


# Функция авторизации прокси
def proxy_auth(proxylog, proxypas):
    # Ввводим данные для авторизация и перемещаемся по окну с помощью системного эмулятора нажатия клавишь
    # !!!! РАБОТАЕТ ТОЛЬКО ЕСЛИ ОКНО СЕЙЧАС В ФОКУСЕ СИСТЕМЫ !!!!!
    # Вводим логин. Курсор ввода сразу находится в поле логина
    # proxy_data = todo_data['proxy'].split
    
    time.sleep(20)
    # Логин
    typewrite(proxylog)
    time.sleep(3)
    hotkey('tab')
    time.sleep(3)
    # Пароль
    typewrite(proxypas)
    time.sleep(3)
    hotkey('tab')
    time.sleep(3)
    hotkey('enter')
    time.sleep(10)


# =============================================================


# Функции работы с потоком
# =============================================================

# Функция запуска авторизированного потока
def new_auth_thread(api_key, miner_spec):
    print('Starting new AUTHORISED thread')
    # Получили ли мы идентификатор
    if (miner_spec['potokid'] == 0 or miner_spec['potokid'] == None):
        print('Thread identifier has not been set')
        print('Check thread identifier mechanism')
        print('Recalling server in 120.0s')
        def_stay()
    # Выводим идентификатор и мы готовы работать
    print('Thread identifier has been set: ' + miner_spec['potokid'])
    print('Initialising browser')
    browser = auth_browser(miner_spec)
    if (browser == 0 or browser == 10501):
        print('Browser start failed. Sending data back to server')
        requests.get('https://seo-god.com/proxyapi/?id=proxy_elite_ref_status'
                     + '&proxy_id='
                     + str(miner_spec['proxyid'])
                     + '&status=1')
        time.sleep(5)
        exit()
    else:
        print('Authorised browser started')
    # Кол-во запросов не получивших задание, т.е. делать потоку нечего
    no_subtodo_count = 0
    # get_sub_todo = requests.get('https://seo-god.com/socail-api/?id=subtodo&potokid=' + miner_spec['potokid'])
    print('Calling thread state...')
    get_sub_todo = requests.get('https://seo-god.com/socail-api/?id=subtodoresults&potokid='
                                + str(miner_spec['potokid'])
                                + '&th_state='
                                + '1'
                                + '&select='
                                + str(miner_spec['select'])
                                + '&th_type=elite'
                                + '&proxyid='
                                + str(miner_spec['proxyid']))
    print(get_sub_todo.url)
    print(get_sub_todo.content)
    if(get_sub_todo.content != b''):
    # Цикл выполнений sub_todo
        while True:
            # Вытаскиваем Json форму ответа сервера
            sub_todo = json.loads(get_sub_todo.content)
            print(sub_todo)
            # Дополняем идентификатором потока
            sub_todo['potokid'] = miner_spec['potokid']
            # Проверяем возможно дана команда вырубиться
            try:
                if (get_sub_todo['result'] == 2):
                    print('Shutdown command was initiated by server...')
                    time.sleep(10)
                    browser.quit()
                    exit()
            except:
                print('No need to shutdown')
            try:
                # Отправляем на выполнение
                get_sub_todo = todo_transport(browser, sub_todo)
            except:
                print('Something gone wrong')
                print('Should send data to server')
                print('Shutting down for safe')
                time.sleep(10)
                browser.quit()
                exit()
            if (get_sub_todo == 0):
                print('Sub_todo has exited with an unexpected error')
                print('Shutdown command...')
                time.sleep(10)
                browser.quit()
                exit()
            elif(get_sub_todo.content == b''):
                print('No sub_todo this time')
                no_subtodo_count += 1
                if (no_subtodo_count == 10):
                    print("No subtodos. Shutting down thread")
                    browser.quit()
                    exit()
                time.sleep(60)
    elif(get_sub_todo.content == b''):
        print('No todo for this thread')
        print('Shutting down thread')
        browser.quit()
        exit()


# Функция запуска не авторизированного потока
def new_unauth_thread(api_key, miner_spec):
    print('Starting new UNAUTHORISED thread')
    # Получили ли мы идентификатор
    if (miner_spec['potokid'] == 0 or miner_spec['potokid'] == None):
        print('Thread identifier has not been set')
        print('Check thread identifier mechanism')
        print('Recalling server in 120.0s')
        def_stay()
    # Выводим идентификатор и мы готовы работать
    print('Thread identifier has been set: ' + miner_spec['potokid'])
    profile = 0
    # Запускаем браузер
    browser = noauth_browser(miner_spec)
    if (browser == 0 or browser == 10501):
        print('Browser start failed. Sending data back to server')
        # Сообщаем что мы НЕ готовы работать
        get_sub_todo = unauth_call_th_state(miner_spec, 0)
        sub_todo = json.loads(get_sub_todo.content)
        if(sub_todo['result'] == 2):
            print('Shutdown was initiated by server...')
            time.sleep(10)
            browser.quit()
            exit()
        else:
            print('Unknows server answer')
            print(sub_todo)
            time.sleep(10)
            browser.quit()
            exit()
    else:
        print('Browser started. Sending data back to server')
        # Сообщаем что мы готовы работать
        get_sub_todo = unauth_call_th_state(miner_spec, 1)
    # Если есть задание
    if (get_sub_todo.content != b''):
        while True:
            print(get_sub_todo.url)
            print(get_sub_todo.content)
            # Вытаскиваем Json форму задания
            sub_todo = json.loads(get_sub_todo.content)
            # Проверяем возможно дана команда вырубиться
            try:
                if (sub_todo['result'] == 2):
                    print('Shutdown command was initiated by server...')
                    time.sleep(10)
                    browser.quit()
                    exit()
            except:
                print('Checked if we need to shut down')
            # Отправляем задание на выполнение
            try:
                get_sub_todo = todo_transport(browser, sub_todo)
            except:
                print('Something unexpected happend')
                print('Should send data to server')
                print('Shutting down for safe')
                browser.quit()
                exit()
            if (get_sub_todo == 0):
                print('Sub_todo has exited with an unexpected error')
                print('Shutdown command...')
                time.sleep(10)
                browser.quit()
                exit()
            # Если нет новых заданий - глушим мотор
            elif (get_sub_todo.content == b''):
                print('No new sub_todo')
                print('Shutting browser.quit()down...')
                time.sleep(10)

                exit()
            elif(get_sub_todo.content != b''):
                print('Got new sub_todo')
    elif (get_sub_todo.content == b''):
        print('We dont have a job')
        print('Shutting down')
        time.sleep(10)
        exit()


# Функция определения куда отправить задание
def todo_transport(browser, sub_todo):
    # Результат задания
    rest = 0
    if 'google' in sub_todo['sub_todo']:
        rest = godp.transport(browser, sub_todo)
        print(rest)
        if(rest == 9):
            print('No ' + sub_todo['sub_todo'] + ' module in godp. Calling renew')
            sleep(10)
            # Вызываем обновление/переподключение локальных файлов
            # Доработка предполагает скачивание с сервера последней версии файла
            renew()
            sleep(10)
            rest = godp.transport(browser, sub_todo)
            if(rest == 9):
                print('No ' + sub_todo['sub_todo'] + ' module in godp after renew')
                rest = 0
    elif 'fb' in sub_todo['sub_todo']:
        rest = fbdp.transport(browser, sub_todo)
        print(rest)
        if(rest == 9):
            print('No ' + sub_todo['sub_todo'] + ' module in fbdp. Calling renew')
            sleep(10)
            # Вызываем обновление/переподключение локальных файлов
            # Доработка предполагает скачивание с сервера последней версии файла
            renew()
            sleep(10)
            rest = fbdp.transport(browser, sub_todo)
            if(rest == 9):
                print('No ' + sub_todo['sub_todo'] + ' module in fbdp after renew')
                rest = 0
    return rest


# Функция определения статуса потока для сервера
def unauth_call_th_state(miner_spec, th_state):
    print('Calling thread state...')
    get_sub_todo = requests.get('https://seo-god.com/socail-api/?id=subtodoresults&potokid='
                                + str(miner_spec['potokid'])
                                + '&th_state='
                                + str(th_state)
                                + '&select=2'
                                + '&th_type=free'
                                + '&proxyid='
                                + str(miner_spec['proxyid']))
    print(get_sub_todo.url)
    return get_sub_todo


# =============================================================

# ==============================


def unauth_clear_profile():
    print('Clearing unauthorised thread browser profile...')

