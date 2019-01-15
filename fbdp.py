from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import re
from time import sleep
import json
import requests

# Error code:
# 10701 - не попали на страницу фейсбука.
# 10702 - аккаунт зарегестрировали но не смогли подтвердить по почте, не смогли попасть на gmail => проверить gmail
# 10703 - не пришло письмо от фейсбука. Необходимо зайти в фб и отправить письмо повторно


def transport(browser, todo):
    # Выбираем действие
    rest = 9
    if(todo['sub_todo'] == 'fbwallpost'):
        print('fbwallpost called')
        rest = fbwallpost(browser, todo)
    elif(todo['sub_todo'] == 'fbwall'):
        print('fbwall called')
        rest = fbwall(browser, todo)
    elif (todo['sub_todo'] == 'fbfreesurf'):
        print('fbfreesurf called')
        rest = fbfreesurf(browser, todo)
    return rest


def entering(browser, data):
    subdata = list(data)
    for i in range(subdata.__len__()):
        paction = ActionChains(browser)
        if(subdata[i].isupper()):
            paction.key_down(Keys.SHIFT).perform()
            sleep(random.uniform(0.0, 1.0))
            paction.reset_actions()
            paction.key_down(subdata[i]).perform()
            paction.reset_actions()
            paction.key_up(Keys.SHIFT).perform()
        else:
            paction.key_down(subdata[i]).perform()
        sleep(random.uniform(0.0, 1.0))


def fb_reg(browser, user_data):
    bday = user_data['bday'].split('-')
    mon_l = dict()
    mon_l = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    # Переходим на facebook
    browser.get('https://www.facebook.com/')
    sleep(random.randint(5, 15))
    # Проверяем попали ли мы на странцицу facebook
    try:
        ActionChains(browser).move_to_element(
            browser.find_element_by_name("firstname")).perform()
        entering(browser, user_data['firstname'])
    except (TimeoutException, NoSuchElementException):
        browser.refresh()
        sleep(random.randint(5, 15))
        try:
            ActionChains(browser).move_to_element(
                browser.find_element_by_name("firstname")).perform()
            entering(browser, user_data['firstname'])
        except (TimeoutException, NoSuchElementException):
            return 10701

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("lastname")).perform()
    entering(browser, user_data['lastname'])

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("reg_email__")).perform()
    entering(browser, user_data['login'] + '@gmail.com')

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("reg_email_confirmation__")).perform()
    entering(browser, user_data['login'] + '@gmail.com')

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("reg_passwd__")).perform()
    entering(browser, user_data['pass'])

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("birthday_day")).send_keys(random.randint(1, 26)).perform()

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("birthday_month")).send_keys(bday[1]).perform()

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_name("birthday_year")).send_keys(bday[0]).perform()

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_xpath("//input[@type='radio'][@name='sex'][@value='2']")).click().perform()

    sleep(random.randint(2, 6))
    ActionChains(browser).move_to_element(
        browser.find_element_by_xpath("//button[@type='submit'][@name='websubmit']")).click().perform()
    sleep(random.randint(5, 15))

    # Проверяем сказано ли нам идти на гугл или что то еще
    # Возможно прийдется вбивать капчу, мало ли.


    try:
        browser.find_element_by_css_selector('div.clearfix > div.rfloat._ohf > button')
    except (TimeoutException, NoSuchElementException):
        print("We need to check gmail")
    browser.get('https://gmail.com')
    sleep(random.randint(5, 10))
    try:
        browser.find_element_by_class_name('UI')
    except (TimeoutException, NoSuchElementException):
        browser.refresh()
        sleep(random.randint(5, 10))
        try:
            browser.find_element_by_class_name('UI')
        except (TimeoutException, NoSuchElementException):
            return 10702

    mlist = browser.find_elements_by_css_selector('tr.zA.yO')
    for i in range(mlist.__len__()):
        minhtml = mlist[i].get_attribute('innerHTML')
        print(minhtml)
        print('---------------------------------')
        sleep(2)
        if 'facebook' in minhtml:
            print('Found facebook mail')
            browser.find_element_by_class_name('yW').click()
            sleep(10)
            browser.find_element_by_css_selector('tr > td > a').click()
            browser.switch_to.window(browser.window_handles[1])
            print('We should be on facebook now')
            break
    else:
        print('No mail yet from Facebook')
        return 10703

    sleep(random.randint(2, 6))
    try:
        browser.find_element_by_css_selector('div > a > span > span')
        print(" We're on facebook! ")
        browser.find_element_by_css_selector('div > a > span > span').click()
    except (TimeoutException, NoSuchElementException):
        print("No sure we're on facebook")


def fbwallpost(browser, subtodo_data):
    if(subtodo_data['keyword'] == None):
        result_data = dict()
        result_data['potokid'] = subtodo_data['potokid']
        result_data['sub_todo'] = 'fbfreesurf'
        result_data['th_state'] = '1'
        result_data['th_type'] = 'elite'
        result_data['todo_res'] = 'ok'
        result_data['select'] = subtodo_data['select']
        get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
        print(get_data.url)
        print(get_data.content)
        return get_data
    browser.get('https://facebook.com')
    time.sleep(random.randint(7, 16))
    ActionChains(browser).move_to_element(browser.find_element_by_name('xhpc_message')).click().perform()
    time.sleep(random.randint(2, 5))
    # ActionChains(browser).send_keys('I want to find many friend here').perform()
    wpost = subtodo_data['keyword'] + ' ' + subtodo_data['site_url']
    entering(browser, wpost)
    time.sleep(random.randint(2, 5))
    container = browser.find_element_by_id("feedx_sprouts_container")
    container_inhtml = container.get_attribute('innerHTML')
    regexp = re.compile('(?<=<button\ class=")[\w\W]*?(?=")')
    btn_class = regexp.findall(container_inhtml)
    time.sleep(random.randint(2, 5))
    browser.find_element_by_css_selector('button[class="%s"]' % btn_class[0]).click()
    time.sleep(random.randint(2, 5))
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fbwallpost'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'elite'
    result_data['todo_res'] = 'ok'
    result_data['select'] = subtodo_data['select']
    result_data['siteid'] = subtodo_data['siteid']
    result_data['keywordid'] = subtodo_data['keywordid']
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    print(get_data.content)
    return get_data


def fbwall(browser, subtodo_data):
    print('fbwall')
    browser.get('https://facebook.com')
    time.sleep(random.randint(10,20))
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fbwall'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'elite'
    result_data['todo_res'] = 'ok'
    result_data['select'] = subtodo_data['select']
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    print(get_data.content)
    return get_data


def fbfreesurf(browser, subtodo_data):
    print('surfing')
    browser.get('https://facebook.com')
    time.sleep(random.randint(10,20))
    emenu = browser.find_elements_by_class_name('imgWrap')
    emenu[random.randint(2,9)].click()
    time.sleep(random.randint(10,20))
    result_data = dict()
    result_data['potokid'] = subtodo_data['potokid']
    result_data['sub_todo'] = 'fbfreesurf'
    result_data['th_state'] = '1'
    result_data['th_type'] = 'elite'
    result_data['todo_res'] = 'ok'
    result_data['select'] = subtodo_data['select']
    get_data = requests.get('https://seo-god.com/socail-api/?id=subtodoresults', params=result_data)
    print(get_data.url)
    print(get_data.content)
    return get_data


