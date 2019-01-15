# Модулья godp.py отвечает за реализацию и обработку заданий напрямую или косвенно связанных с google
# Данный модуль включает в себя: реализацию механизма ПФ, сбор саджестов по поисковому запросу,
# Парсинг результатов выдачи, проверку наличия имени в поисковой выдаче соц. сетей, а так же
# полную реализацию регистрации gmail средствами селеинума - ввод данных в поля, нажатия кнопок
# и наведение мышки на элементы. Обработки ошибок основаны на таймауте страницы, и в случае
# возникновения основных ошибок возвращаются коды ошибок

# Описание кодов ошибок:
# ========================================================================
# Коды ошибок:
# 10601 - проблема с прокси
# 10616 - какая то чепушню - вызывайте экзорциста.
# 10618 - проблема с загрузкой страницы.
# 10619 - не уникальный логин, нужен новый.
# 10620 - проблема с телефоном, гугл говорит не порядок.
# 10621 - не получил код из смс вообще.
# 10622 - аккаунт был заблокирован сразу после регистрации. АХТУНГ!!!
# 10623 - аккаунт вроде был зарегестрирован, но во время перехода на почту что то не получилось,
#		  сохранить данные и проверить.
# 10624 - аккаунт прошел регистрацию с телефоном, но во время перехода на почту что то не получилось,
#		  сохранить данные и проверить, возможно его сразу заблокировало.
# 10626 - не смогли кликнуть по кнопке submitbutton, на главное странице регистрации.
# 10627 - не смогли кликнуть по кнопке iagreebutton, в окне приёма соглашения при регистрации.
# 10628 - не смогли спарсить ответ с смс кодом, проверить формат ответа и собсно сам парсер.
# 10629 - не смогли спарсить телефон из subtodo data.
# 10630 - ошибка использования телефона. Лимит регистрации временно исчерпан.
# 10631 - неопределённая ошибка с телефоном и кодом
#
# --------------------
# Код статусов регистрации:
# 1 - Успех
# 2 - Дырка
# 3 - Аккаунт словил банан
# 4 - Лимит регистрации с телефонов исчерпан, нужно подождать
# 5 - Лимит регистрации аккаунтов исчерпан, нужно подождат
# 6 - Какая то чепушня, вызывайте экзорциста
#
# ========================================================================


# Описание функций модуля:
# transport(browser, todo)              -  функция распределения заданий, в параметрах принимает обьект
#                                         браузера и словарь с данными subtodo
#                                           Возвращает следующее задание от сервера

# googlesuggest(browser, subtodo_data)  -  функция поискового запроса, в параметрах принимает обьект
#                                         браузера и словарь с данными subtodo
#                                           Возвращает следующее задание от сервера

# googlepassportcheck(browser, subtodo_data) -  функция поискового запроса по людям, в параметрах принимает обьект
#                                         браузера и словарь с данными subtodo
#                                           Возвращает следующее задание от сервера

# googleregistration(browser, user_data) -  функция регистрации gmail, в параметрах принимает обьект браузера
#                                         и словарь данных subtodo
#                                           Возвращает следующее задание от сервера

# googlepf(browser, subtodo_data, th_type) - функция google ПФ, выполняет поисковый запрос, ищет нужную ссылку на
#                                          первых 6 страницах, если находит нужную позицию - переходит
#                                          в параметрах принимает обьект браузера, пакет данных subtodo_data,
#                                          и тип потока th_type
#                                           Возвращает следующее задание от сервера

# googlepf_advanced(browser, subtodo_data) - функция дополнительного запроса google ПФ, выполняет уточняющий запрос ПФ
#                                           с указанием ссылки ресура. В параметрах принимает обьект браузера и
#                                           пакет данных subtodo_data.
#                                           Возвращает следующее задание от сервера

#
#
#
# Вспомогательные функции модуля:
# find_elem_for_mouse(browser, element) - вспомогательная функция поиска позиции элемента на странице
#                                         принимает обьект браузера и обьект элемента позицию которого,
#                                         нужно вычислить. В результате возвращает x, y ко-ты эл-та
# reg_result_to_server(user_data, state) - вспомогательная функция общения с сервером при регистрации,
#                                         принимает обьект браузера и статус сообщений, который нужно передать серверу



# ================================


import requests
import json
import random
import time
import re
import pickle
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pyautogui import typewrite, hotkey


# Определяем какое sub_todo делаем и вызываем его функцию
def transport(browser, todo):
    # Выбираем действие
    rest = 9
    if(todo['sub_todo'] == 'googlepassportcheck'):
        print('googlepassportcheck called')
        rest = passportcheck(browser, todo)
    elif(todo['sub_todo'] == 'googlesuggest'):
        print('googlesuggest called')
        rest = googlesuggest(browser, todo)
    elif(todo['sub_todo'] == 'fgooglepf'):
        print('fgooglepf called')
        rest = googlepf(browser, todo, 'fgooglepf')
    elif (todo['sub_todo'] == 'agooglepf'):
        print('agooglepf called')
        rest = googlepf(browser, todo, 'agooglepf')
    elif(todo['sub_todo'] == 'googleregistration'):
        print('googleregistration called')
        rest = gmail_reg(browser, todo)
    elif (todo['sub_todo'] == 'fgoogleytwatch'):
        print('fgoogleytwatch called')
        rest = fgoogleytwatch(browser, todo)
    elif (todo['sub_todo'] == 'fgoogleqytwatch'):
        print('fgoogleqytwatch called')
        rest = fgoogleqytwatch(browser, todo)
    return rest


# ======================================================


def googlepf(browser, subtodo_data, th_type):
    # Формируем результирующий пакет данных
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = subtodo_data['sub_todo']
    result_data['th_state'] = '1'
    result_data['th_type'] = th_type
    # result_data['proxyid'] = subtodo_data['proxyid']
    result_data['todo_res'] = 'fail'
    result_data['select'] = subtodo_data['select']
    result_data['siteid'] = subtodo_data['siteid']
    result_data['keywordid'] = subtodo_data['keywordid']

    browser.get("https://google.com")
    time.sleep(random.randint(5, 15))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['keyword'])
        time.sleep(random.randint(2, 5))
        ActionChains(browser).send_keys(Keys.ENTER).perform()
    except (NoSuchElementException, TimeoutException):
        print("We did not end up on google page...")
        return 0

    time.sleep(random.randint(3, 6))
    link = subtodo_data['site_url']
    for j in range(6):
        psource = browser.page_source
        if link in psource:
            try:
                elements = browser.find_elements_by_class_name('r')
            except:
                print('It seems proxy is not working')
                return 0
            for i in range(0, elements.__len__()):
                inhtml = elements[i].get_attribute('innerHTML')
                if link in inhtml:
                    browser.get(link)
                    time.sleep(random.randint(120, 240))
                    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(random.randint(120, 240))
                    result_data['todo_res'] = 'ok'
                    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
                    return get_data
        else:
            print('No link on this page')
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                browser.find_element_by_css_selector('#pnnext').click()
                time.sleep(random.randint(15, 30))
            except:
                browser.get(link)
                time.sleep(random.randint(120, 240))
                break
    else:
        print('Link was not found on first 6 pages...')
        try:
            googlepf_advanced(browser, subtodo_data)
            # browser.get(link)
            time.sleep(random.randint(120, 240))
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(random.randint(120, 240))
        except:
            print('Error calling fgooglepf_advanced')
    time.sleep(10)
    result_data['todo_res'] = 'ok'
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    return get_data


# Конкретный ПФ
def fgooglepf(browser, subtodo_data):
    browser.get("https://google.com")
    time.sleep(random.randint(5, 15))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['keyword'])
        time.sleep(random.randint(2, 5))
        ActionChains(browser).send_keys(Keys.ENTER).perform()
    except (NoSuchElementException, TimeoutException):
        print("We did not end up on google page...")
        return 0
    time.sleep(random.randint(3, 6))
    link = subtodo_data['site_url']
    # Формируем результирующий пакет данных
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fgooglepf'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'free'
    # result_data['proxyid'] = subtodo_data['proxyid']
    result_data['todo_res'] = 'ok'
    result_data['select'] = subtodo_data['select']
    result_data['siteid'] = subtodo_data['siteid']
    result_data['keywordid'] = subtodo_data['keywordid']

    for j in range(6):
        psource = browser.page_source
        if link in psource:
            try:
                elements = browser.find_elements_by_class_name('r')
            except:
                print('It seems proxy is not working')
                return 10501
            for i in range(0, elements.__len__()):
                inhtml = elements[i].get_attribute('innerHTML')
                if link in inhtml:
                    # elements[i].click()
                    browser.get(link)
                    time.sleep(random.randint(120, 240))
                    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(random.randint(120, 240))
                    result_data['todo_res'] = 'ok'
                    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)

                    return get_data
        else:
            print('No link on this page')
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                browser.find_element_by_css_selector('#pnnext').click()
                time.sleep(random.randint(15, 30))
            except:
                browser.get(link)
                time.sleep(random.randint(120, 240))
                break
    else:
        print('Link was not found on first 6 pages...')
        try:
            # googlepf_advanced(browser, subtodo_data)
            browser.get(link)
            time.sleep(random.randint(120, 240))
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(random.randint(120, 240))
        except:
            print('Error calling fgooglepf_advanced')
    time.sleep(10)
    result_data['todo_res'] = 'ok'
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    return get_data


# Конкретный ПФ
def agooglepf(browser, subtodo_data):
    browser.get("https://google.com")
    time.sleep(random.randint(5, 15))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['keyword'])
        time.sleep(random.randint(2, 5))
        ActionChains(browser).send_keys(Keys.ENTER).perform()
    except (NoSuchElementException, TimeoutException):
        print("We did not end up on google page...")
        return 0
    time.sleep(random.randint(3, 6))
    link = subtodo_data['site_url']
    # Формируем результирующий пакет данных
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'agooglepf'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'elite'
    # result_data['proxyid'] = subtodo_data['proxyid']
    result_data['todo_res'] = 'ok'
    result_data['select'] = subtodo_data['select']
    result_data['siteid'] = subtodo_data['siteid']
    result_data['keywordid'] = subtodo_data['keywordid']

    for j in range(6):
        psource = browser.page_source
        if link in psource:
            try:
                elements = browser.find_elements_by_class_name('r')
            except:
                print('It seems proxy is not working')
                return 10501
            for i in range(0, elements.__len__()):
                inhtml = elements[i].get_attribute('innerHTML')
                if link in inhtml:
                    # elements[i].click()
                    browser.get(link)
                    time.sleep(random.randint(120, 240))
                    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(random.randint(120, 240))
                    result_data['todo_res'] = 'ok'
                    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
                    return get_data
        else:
            print('No link on this page')
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                browser.find_element_by_css_selector('#pnnext').click()
                time.sleep(random.randint(5, 15))
            except:
                browser.get(link)
                time.sleep(random.randint(10,30))
                break
    else:
        print('Link was not found on first 6 pages...')
        try:
            # googlepf_advanced(browser, subtodo_data)
            browser.get(link)
            time.sleep(random.randint(120, 240))
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(random.randint(120, 240))
        except:
            print('Error calling fgooglepf_advanced')
    time.sleep(10)
    result_data['todo_res'] = 'ok'
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    return get_data


# Дополнительный запрос ПФ с указанием адреса ресурса
def googlepf_advanced(browser, subtodo_data):
    browser.get("https://google.com")
    time.sleep(random.randint(5, 15))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['keyword']
                                                             + ' '
                                                             + subtodo_data['site_url'])
        time.sleep(random.randint(2, 5))
        ActionChains(browser).send_keys(Keys.ENTER).perform()
    except (NoSuchElementException, TimeoutException):
        print("We did not end up on google page...")
        return 0
    time.sleep(random.randint(3, 6))
    link = subtodo_data['site_url']

    for j in range(5):
        psource = browser.page_source
        if link in psource:
            try:
                elements = browser.find_elements_by_class_name('r')
            except:
                print('It seems proxy is not working')
                return 10501
            for i in range(0, elements.__len__()):
                inhtml = elements[i].get_attribute('innerHTML')
                if link in inhtml:
                    elements[i].click()
                    time.sleep(random.randint(120, 240))
                    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(random.randint(120, 240))
                    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
        else:
            print('No link on this page')
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                browser.find_element_by_css_selector('#pnnext').click()
                time.sleep(random.randint(15, 30))
            except:
                break
    else:
        print('Link was not found on first 6 pages, moving to the link directly')
        try:
            browser.get(link)
            time.sleep(random.randint(120, 240))
        except:
            print('Check if link is correct with http(s)://')
            time.sleep(50)


# Выборка саджестов
# Выбор из выдачи ТОП 3
# Ожидание на сайта 2-5 минут
def googlesuggest(browser, subtodo_data):
    # Проверяем находимся ли мы на странице гугла
    browser.get('https://google.com')
    time.sleep(random.randint(3, 6))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['text'])
    except (NoSuchElementException, TimeoutException):
        return 10618

    # Формируем параметры для ответного запроса
    dict1 = dict()
    dict1['topid'] = subtodo_data['sugid']
    dict1['potokid'] = subtodo_data['potokid']
    dict1['sub_todo'] = 'googlesuggest'
    time.sleep(random.randint(2, 6))
    suggests = browser.find_elements_by_class_name('sbqs_c')
    for i in range(suggests.__len__()):
        dict1['text'] = suggests[i].text
        ech1 = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=dict1)
    # Нажимаем энтер
    paction = ActionChains(browser)
    paction.send_keys(Keys.ENTER).perform()
    time.sleep(random.randint(5, 15))
    element = browser.find_elements_by_class_name('r')
    try:
        element[random.randint(3, 6)].click()
        time.sleep(random.randint(119, 239))
    except:
        time.sleep(random.randint(5, 20))
        paction.send_keys(Keys.DOWN).perform()
        time.sleep(random.randint(5, 20))
    return 1


# Проверка наличия человека из фейсбука в выдаче гугла
# Проверка данных паспорта
def passportcheck(browser, subtodo_data):
    # Проверяем находимся ли мы на странице гугла
    browser.get('https://google.com')
    time.sleep(random.randint(3, 6))
    try:
        browser.find_element_by_class_name('gsfi')
    except (NoSuchElementException, TimeoutException):
        browser.get('https://google.com')
        time.sleep(random.randint(5, 15))

    sdata = dict()
    namestr = subtodo_data['text']
    sdata['potokid'] = subtodo_data['potokid']
    sdata['sub_todo'] = subtodo_data['todo']
    sdata['passportid'] = subtodo_data['passportid']
    sdata['rating'] = 0

    # Вводим поисковый запрос
    try:
        browser.find_element_by_class_name('gsfi').send_keys(subtodo_data['text'] + ' facebook')
    except (NoSuchElementException, TimeoutException):
        return 10618

    paction = ActionChains(browser)
    paction.send_keys(Keys.ENTER).perform()
    time.sleep(random.randint(3, 7))
    elements = browser.find_elements_by_class_name('r')
    num1 = 0
    for i in range(0, elements.__len__()):
        inhtml = elements[i].get_attribute('innerHTML')
        # print(inhtml)
        if namestr in inhtml:
            num1 += 1
    print(num1)
    if (num1 == 0):
        sdata['rating'] = 1
    requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=sdata)
    sdata.clear()
    return 1


# Регистрация gmail
def gmail_reg(browser, user_data):
    bday = user_data['bday'].split('-')
    bmonth = dict()
    bmonth = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
              '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

    browser.get('https://gmail.com')
    time.sleep(random.randint(3, 9))

    # Проверяем на каком типе страницы мы оказались (Красивый или обычный)
    # пытаемся нажать по красивой кнопке, если её нет - нажимаем обычную
    try:
        browser.find_element_by_class_name('hero_home__link__desktop').click()
        time.sleep(random.randint(2, 5))
        # Переключаем фокус селениума на вторую вкладку в котороый открылась регистрация
        browser.switch_to.window(browser.window_handles[1])
    except (TimeoutException, NoSuchElementException):
        try:
            browser.find_element_by_xpath('//*[@id="view_container"]/form/div[2]/div/div[2]/div[2]/div').click()
            time.sleep(5)
            browser.find_element_by_id('SIGNUP').click()
        except:
            browser.refresh()
            try:
                browser.find_element_by_class_name('hero_home__link__desktop').click()
                time.sleep(random.randint(2, 5))
                # Переключаем фокус селениума на вторую вкладку в котороый открылась регистрация
                browser.switch_to.window(browser.window_handles[1])
            except (TimeoutException, NoSuchElementException):
                browser.find_element_by_xpath('//*[@id="view_container"]/form/div[2]/div/div[2]/div[2]/div').click()
                time.sleep(5)
                browser.find_element_by_id('SIGNUP').click()
            else:
                print('Proxy trouble')

    # Проверяем попали ли мы на страницу регистрации - пробуем заполнить поле имени
    try:
        # NAME
        time.sleep(random.randint(2, 6))
        ActionChains(browser).move_to_element(browser.find_element_by_id("FirstName")).click().perform()
        time.sleep(random.randint(1, 3))
        browser.find_element_by_id("FirstName").send_keys(user_data['firstname'])
    except (TimeoutException, NoSuchElementException):
        print('Cant target Firstname field. Refreshing page')
        browser.refresh()
        try:
            # NAME
            time.sleep(random.randint(2, 6))
            ActionChains(browser).move_to_element(browser.find_element_by_id("FirstName")).perform()
            time.sleep(random.randint(1, 3))
            browser.find_element_by_id("FirstName").send_keys(user_data['firstname'])
        except (TimeoutException, NoSuchElementException):
            return 10618

    # LASTNAME
    time.sleep(random.randint(2, 6))
    browser.find_element_by_id("LastName").send_keys(user_data['lastname'])
    # MAIL_ADDRESS/LOGIN
    time.sleep(random.randint(2, 6))
    browser.find_element_by_id("GmailAddress").send_keys(user_data['login'])
    # PASSWORD
    time.sleep(random.randint(2, 6))
    browser.find_element_by_id("Passwd").send_keys(user_data['password'])
    # PASSWORD2
    time.sleep(random.randint(2, 6))
    browser.find_element_by_id("PasswdAgain").send_keys(user_data['password'])
    # Проверяем уникален ли логин
    check_elem = browser.find_element_by_id('username-suggestions')
    if (check_elem.is_displayed()):
        print('Need new login')
        browser.find_element_by_id('GmailAddress').clear()
        time.sleep(random.randint(2, 5))
        user_data['login'] = user_data['login'] + bday[0]
        browser.find_element_by_id("GmailAddress").send_keys(user_data['login'])
    else:
        print('Login is uniq')
    # BIRTHDAY
    time.sleep(random.randint(1, 4))
    browser.find_element_by_id("BirthDay").send_keys(random.randint(1, 27))
    # BIRTHMONTH
    time.sleep(random.randint(1, 4))
    element = browser.find_element_by_xpath("//*[@id=\"BirthMonth\"]/div[1]")
    element.send_keys(Keys.DOWN)
    time.sleep(random.randint(1, 3))
    element.send_keys(bmonth[bday[1]])
    element.send_keys(Keys.ENTER)
    time.sleep(random.randint(2, 6))
    # BIRTHYEAR
    time.sleep(random.randint(1, 3))
    browser.find_element_by_id("BirthYear").send_keys(bday[0])
    # GENDER
    element = browser.find_element_by_xpath("//*[@id=\"Gender\"]/div[1]")
    time.sleep(random.randint(2, 6))
    element.send_keys(Keys.DOWN)
    element.send_keys(Keys.DOWN)
    element.send_keys(Keys.DOWN)
    element.send_keys(Keys.ENTER)
    time.sleep(random.randint(2, 6))
    # PHONE
    sms_code = 0
    try:
        if (user_data['phonenum'] != ""):
            sms_phone = user_data['phonenum']

        else:
            print('Empty number field in subtodo')
            reg_result_to_server(user_data, 4)
            return 10629
    except:
        print('Cant parse phonenum from user_data')
        reg_result_to_server(user_data, 4)
        return 10629

    print(sms_phone)

    # Получаем текущую ссылку страницы, для дальнейшей проверки перешли ли мы на след.
    reg_page_url = browser.current_url

    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
# ---------------------------------------------------------------
    time.sleep(random.randint(2, 5))

    try:
        browser.execute_script('document.getElementById("submitbutton").click()')
    except:
        print("Cant click submitbutton. Check if its available")
        return 10616

    time.sleep(random.randint(2, 6))
    print('Pagedown')
    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(random.randint(2, 6))
    print('Pagedown')
    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(random.randint(2, 6))

    try:
        browser.execute_script('document.getElementById("iagreebutton").click()')
    except:
        print("Cant click iagreebutton. Check if its available")
        return 10616

    time.sleep(random.randint(5, 15))
    if(browser.current_url == reg_page_url):
        print("It seems we're still on the same page. Solving this problem")
        ActionChains(browser).move_to_element(
            browser.find_element_by_css_selector('#iagreebutton')).double_click().perform()
        time.sleep(random.randint(5, 16))
    else:
        print('Passed registration page')
    time.sleep(random.randint(5, 15))


    # ----------------------------------------------------------

    # Проверка, может нас сразу зарегало
    try:

        print('Checking if we were registrated')
        browser.execute_script('document.getElementById("submitbutton").click()')
        time.sleep(random.randint(5, 15))

        # Проверка попадания в почтовик
        try:
            print('Checking if we appeared at gmail main page')
            browser.find_element_by_class_name('UI')
            print('We should be on the mail now')
            # Сообщаем о регистрации
            reg_result_to_server(user_data, 1)
            # Пытаемся жмякнуть на кнопощьку на почте

            try:
                print('Trying to press X button on the mail')
                ActionChains(browser).move_to_element(
                    browser.find_element_by_xpath('//*[@id="close-button"]')).click().perform()
                return 1
            except (TimeoutException, NoSuchElementException):
                print('Could not press X button on the mail')
                return 1

        except (TimeoutException, NoSuchElementException):
            # Если уж мы нажали на submitbutton - значит мы пропустили форму с телефоном,
            # и нам нужно проверять, либо мы зарегались, либо аккаунт словил банан
            try:
                browser.get('https://gmail.com')
                time.sleep(random.randint(5, 15))
                # При переходе на страницу gmail гугл предлагает залогинится - признак что акк забанили сразу после регистрации
                pswd = browser.find_element_by_id('password')
                pswd_inhtml = pswd.get_attribute('innerHTML')
                # В случае если нам таки предложили ввести пароль - сообщем что аккаунт упал.
                if 'Enter your password' in pswd_inhtml:
                    print('Daim, seems account got banned')
                    reg_result_to_server(user_data, 3)
                    return 10622

            except (TimeoutException, NoSuchElementException):
                print('Something unnatural !')
                reg_result_to_server(user_data, 6)
                requests.get('https://seo-god.com/smsapi/?id=updatephone&nomer=%s&passport=0' % str(sms_phone))
                return 10616

    except:
        try:
            print('Checking if we can use phone to register')
            # Проверка, если нас сразу не зарегало, можем ли мы использовать телефон для регистрации
            ActionChains(browser).move_to_element(
                browser.find_element_by_id('signupidvinput')).click().perform()
        except (TimeoutException, NoSuchElementException):
            print('Something unnatural !')
            reg_result_to_server(user_data, 6)
            requests.get('https://seo-god.com/smsapi/?id=updatephone&nomer=%s&passport=0' % str(sms_phone))
            return 10616

    print('Entering phone')
    print(sms_phone)
    # Вводим телефон
    ActionChains(browser).send_keys('+7' + sms_phone).perform()
    time.sleep(random.randint(2, 5))

    try:
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//input[@id='next-button'][@name='SendCode']")).click().perform()
    except (TimeoutException, NoSuchElementException):
        print('Could not press send button. Trying to press enter')
        ActionChains(browser).send_keys(Keys.ENTER).perform()

    time.sleep(random.randint(5, 15))

    try:
        err_check = browser.find_element_by_class_name('errormsg')
        err_inhtml = err_check.get_attribute('innerHTML')
        if 'phone' in err_inhtml:
            print('We have an error here!!!')
            time.sleep(random.randint(10, 30))
            reg_result_to_server(user_data, 4)
            return 10630
    except (TimeoutException, NoSuchElementException):
        print('Seems we can continue registration')

    time.sleep(random.randint(5, 15))

    print('Checking code enter page')
    # Проверяем перешли ли мы на страницу для ввода кода смс
    try:
        ActionChains(browser).move_to_element(
            browser.find_element_by_name('smsUserPin')).click().perform()
    except (TimeoutException, NoSuchElementException):
        browser.refresh()
        time.sleep(random.randint(3, 8))
        try:
            ActionChains(browser).move_to_element(
                browser.find_element_by_name('smsUserPin')).click().perform()
            # Мы на странице для ввода кода из смс
        except (TimeoutException, NoSuchElementException):
            print("Not sure we're ready to accept sms code")
            # Проверка вдруг мы остались на странице с телефоном
            try:
                ActionChains(browser).move_to_element(
                    browser.find_element_by_xpath("//input[@id='next-button'][@name='SendCode']")).click().perform()
                print("We're still on a phone send page")
            except (TimeoutException, NoSuchElementException):
                print("We're NOT on a phone send page, so where are we?")
                return 10631

    # Ждём смс с кодом
    for _ in range(2):
        time.sleep(random.randint(60, 120))
        # Получаем код. Если его еще нет - ждёт еще одну итерацию
        get_sms_code = requests.get('https://seo-god.com/smsapi/?id=getsms&nomer=%s&sms=google' % sms_phone)
        try:
            check_phone = json.loads(get_sms_code.content)
            if (check_phone['id'] != 0):
                sms_code = check_phone['code']
                break
            else:
                print('no code yet')
        except:
            return 10628
    else:
        # Получаем код. Если кода нет - ждём 60-80 секунд и запрашиваем повторно.
        time.sleep(random.randint(60, 80))
        try:
            get_sms_code = requests.get('https://seo-god.com/smsapi/?id=getsms&nomer=%s&sms=last' % sms_phone)
            check_phone = json.loads(get_sms_code.content)
            if (check_phone['id'] != 0):
                sms_code = check_phone['code']
                print(sms_code)
            else:
                print('no code yet')
        except:
            return 10628

    if (sms_code == 0):
        # Если код так и не пришёл - запрашиваем смс повторно
        try:
            ActionChains(browser).move_to_element(
                browser.find_element_by_xpath('//*[@id="signupidv"]/div[2]/a')).click().perform()
            time.sleep(random.randint(4, 14))
            ActionChains(browser).move_to_element(
                browser.find_element_by_xpath("//input[@id='next-button'][@name='SendCode']")).click().perform()
            time.sleep(random.randint(5, 15))

            # Ждём смс с кодом
            for _ in range(2):
                time.sleep(random.randint(60, 120))
                # Получаем код. Если его еще нет - ждёт еще одну итерацию
                get_sms_code = requests.get('https://seo-god.com/smsapi/?id=getsms&nomer=%s&sms=google' % sms_phone)
                try:
                    check_phone = json.loads(get_sms_code.content)
                    if (check_phone['id'] != 0):
                        sms_code = check_phone['code']
                        break
                    else:
                        print('no code yet')
                except:
                    return 10628
            else:
                # Получаем код. Если кода нет - ждём 60-80 секунд и запрашиваем повторно.
                time.sleep(random.randint(60, 80))
                try:
                    get_sms_code = requests.get('https://seo-god.com/smsapi/?id=getsms&nomer=%s&sms=last' % sms_phone)
                    check_phone = json.loads(get_sms_code.content)
                    if (check_phone['id'] != 0):
                        sms_code = check_phone['code']
                        print(sms_code)
                    else:
                        print('no code yet')
                except:
                    return 10628

        except (TimeoutException, NoSuchElementException):
            print("Are you sure we're on a code receive page?")
            return 0

    if (sms_code == 0):
        return 10621
    else:
        print(sms_code)
        ActionChains(browser).send_keys(sms_code).perform()
        time.sleep(random.randint(2, 5))
        ActionChains(browser).send_keys(Keys.ENTER).perform()
        time.sleep(random.randint(5, 15))

        # Теперь мы должны оказаться на почте, проверяем успешно ли зарегестрировали акк
        try:
            browser.execute_script('document.getElementById("submitbutton").click()')
            time.sleep(random.randint(5, 15))

            # Проврка попадания в почтовик
            try:
                browser.find_element_by_class_name('UI')
                print('We should be on the mail now')
                # Сообщаем о регистрации
                reg_result_to_server(user_data, 1)
                # Пытаемся жмякнуть на кнопощьку на почте

                try:
                    ActionChains(browser).move_to_element(
                        browser.find_element_by_xpath('//*[@id="close-button"]')).click().perform()
                    return 1

                except (TimeoutException, NoSuchElementException):
                    print('Could not press X button on the mail')
                    return 1

            except (TimeoutException, NoSuchElementException):

                # Если уж мы нажали на submitbutton - значит мы пропустили форму с телефоном,
                # и нам нужно проверять, либо мы зарегались, либо аккаунт словил банан
                try:
                    browser.get('https://gmail.com')
                    time.sleep(random.randint(5, 15))
                    # При переходе на страницу gmail гугл предлагает залогинится - признак что акк забанили сразу после регистрации
                    pswd = browser.find_element_by_id('password')
                    pswd_inhtml = pswd.get_attribute('innerHTML')
                    # В случае если нам таки предложили ввести пароль - сообщем что аккаунт упал.
                    if 'Enter your password' in pswd_inhtml:
                        print('Daim, seems account got banned')
                        reg_result_to_server(user_data, 3)
                        return 10622

                except (TimeoutException, NoSuchElementException):
                    print('Something unnatural !')
                    reg_result_to_server(user_data, 6)
                    return 10624
        except:
            print('Where are we?')
            reg_result_to_server(user_data, 4)
            requests.get('https://seo-god.com/smsapi/?id=updatephone&nomer=%s&passport=0' % str(sms_phone))
            return 10621


# Просмотр Youtube
def fgoogleytwatch(browser, subtodo_data):
    if 'youtube' in subtodo_data['vid_url']:
        browser.get(subtodo_data['vid_url'])
    else:
        vid_url = 'https://www.youtube.com/watch?v=' + subtodo_data['vid_url']
        browser.get(vid_url)

    time.sleep(random.randint(30, 60))
    # Формируем результирующий запрос
    # potokid - идентификатор
    # потока
    # sub_todo - выполненное
    # задание(fgoogleytwatch)
    # todo_res - результат
    # задания(ok / fail)
    # vid_id - идентификатор
    # видео
    # vid_refid - идентификатор
    # внешней
    # ссылки
    # select - идентификатор
    # блока - задания
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fgoogleytwatch'
    result_data['todo_res'] = 'ok'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'free'
    result_data['vid_id'] = subtodo_data['vid_id']
    result_data['keywordid'] = subtodo_data['keywordid']
    result_data['select'] = subtodo_data['select']
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    print(get_data.content)
    return get_data


# Просмотр Youtube
def fgoogleqytwatch(browser, subtodo_data):
    if 'youtube' in subtodo_data['vid_url']:
        browser.get(subtodo_data['vid_url'])
    else:
        vid_url = 'https://www.youtube.com/watch?v=' + subtodo_data['vid_url']
        browser.get(vid_url)

    time.sleep(random.randint(30, 60))
    # Формируем результирующий запрос
    # potokid - идентификатор
    # потока
    # sub_todo - выполненное
    # задание(fgoogleytwatch)
    # todo_res - результат
    # задания(ok / fail)
    # vid_id - идентификатор
    # видео
    # vid_refid - идентификатор
    # внешней
    # ссылки
    # select - идентификатор
    # блока - задания
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fgoogleqytwatch'
    result_data['todo_res'] = 'ok'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'free'
    result_data['vid_id'] = subtodo_data['vid_id']
    result_data['keywordid'] = subtodo_data['keywordid']
    result_data['select'] = subtodo_data['select']
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    print(get_data.content)
    return get_data


# ==========================================================


# Ищем позицию элемента
def find_elem_for_mouse(browser, element):
    browser_navigation_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')
    y_relative_coord = element.location['y']
    elem_y = y_relative_coord + browser_navigation_panel_height + random.randint(5, 15)
    elem_x = element.location['x'] + random.randint(5, 15)
    return elem_x, elem_y


# Отправляем результат регистрации на сервер
def reg_result_to_server(user_data, state):
    reg_params = dict()
    reg_params['potokid'] = user_data['potokid']
    reg_params['sub_todo'] = user_data['sub_todo']
    reg_params['todo_res'] = 'ok'
    reg_params['th_type'] = 'elite'
    reg_params['th_state'] = '1'
    reg_params['pasportid'] = user_data['id']
    reg_params['google_login'] = user_data['login']
    reg_params['google_status'] = state
    next_todo = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=reg_params)
    print(next_todo.url)
    print(next_todo.content)
    # return state
    try:
        lfile = open('login_data.txt', 'a')
        lfile.write(
            'login: '
            + str(user_data['login']) + ' | '
            + 'passportid: '
            + str(user_data['id']) + ' | '
            + 'status: '
            + str(state)
            + '\n'
        )
        lfile.close()
    except:
        print('Login file problems')

    return next_todo


