import requests
import json

# Модули обработки
import scdp


# Идентификатор майнера
# api_key = {'apikey': 'SG-59d244a89d699'}
api_key = {'apikey': 'APIKEY'}

# Синхронизация машины с сервером
miner_server_sync = requests.get('https://seo-god.com/socail-api/?id=todo_start', params=api_key)
print(miner_server_sync.url)
print(miner_server_sync.content)
# В случае пустого ответа - вызываем состояние ожидания
if(miner_server_sync.content == b''):
    print('Nothing to do. Setting wait timout 30.0s')
    scdp.def_stay()
# Вытаскиваем json из ответа сервера, в такой форме с ним проще управляться
miner_spec = json.loads(miner_server_sync.content)
# Смотрим есть ли с чем работать
if(miner_spec['orderid'] == 0):
    print('No data to work with. Check proxy or threads')
    # Вызываем состояние ожидания
    scdp.def_stay()


# Если ответ сервера НЕ пуст и там есть данные - пробуем с ними работать
# Типы синхронизаций майнера:
# 0 - состояние ожидания
# 1 - запуск элитного потока
# 2 - запуск фри потока
# 4 - загрузка скриптов с сервера
# 7 - перезагрузка майнера как машины

if (miner_spec['mainerwtd'] == 0):
    scdp.def_stay()

elif (miner_spec['mainerwtd'] == 1):
    scdp.new_auth_thread(api_key, miner_spec)

elif (miner_spec['mainerwtd'] == 2):
    scdp.new_unauth_thread(api_key, miner_spec)

elif (miner_spec['mainerwtd'] == 4):
    scdp.download_scripts(api_key)

elif (miner_spec['mainerwtd'] == 5):
    scdp.new_auth_thread(api_key, miner_spec)

elif (miner_spec['mainerwtd'] == 6):
    scdp.new_unauth_thread(api_key, miner_spec)

elif (miner_spec['mainerwtd'] == 7):
    scdp.reboot_device()









