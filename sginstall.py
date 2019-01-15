from urllib.request import urlretrieve
from subprocess import check_output
import pip
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# API key
sg_apikey = 'SGAPIKEY'
print('Install initialized')


# downloading sg_main.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=sg_main&apikey='+sg_apikey,
                      'C:\\Python\\sg_main.py')
# downloading scdp.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=scdp&apikey='+sg_apikey,
                      'C:\\Python\\scdp.py')
# downloading godp.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=godp&apikey='+sg_apikey,
                      'C:\\Python\\godp.py')
# downloading igdp.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=igdp&apikey='+sg_apikey,
                      'C:\\Python\\igdp.py')
# downloading twdp.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=twdp&apikey='+sg_apikey,
                      'C:\\Python\\twdp.py')
# downloading fbdp.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=fbdp&apikey='+sg_apikey,
                      'C:\\Python\\fbdp.py')

print('Installing cron_file')
# downloading cron_file.py
urlretrieve('https://seo-god.com/socail-api/?id=mainersocialinst2&modulname=cron_file&apikey='+sg_apikey,
                      'C:\\Python\\cron_file.py')

print('td_main.py was installed')
# installing libs and packages
print('Installing requests package')
pip.main(['install', 'requests'])
print('Installing selenium package')
pip.main(['install', 'selenium'])
print('Installing psutill package')
pip.main(['install', 'psutil'])
print('Installing pyautogui package')
pip.main(['install', 'pyautogui'])
print('Installing chromedriver package')
pip.main(['install', 'chromedriver==2.24.1'])
print('Installing names package')
pip.main(['install', 'names'])


# adding script into windows task manager
print('Adding script into windows task manager')
try:
    command = str('schtasks /Create /SC MINUTE /MO 10 /TN Sg_main2 /TR "C:\\Python\\python.exe C:\\Python\\cron_file.py" /f')
    check_output(command, shell=True)
except:
    print('Not enough rights to add task to windows task manager')


# Finishing installs
print('Complex installed successfully. Ready to use')




