#1 import libraries
from selenium import webdriver
from scrapy import Selector
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import re, csv
import pandas as pd

lista0 = []
lista1 = []
lista2 = []
lista3 = []

def initChromeDriver(dr,proxie=None):

    options = webdriver.ChromeOptions()
    #ua = UserAgent()
    #userAgent = ua.random
    # -- Descomentar la siguiente linea, para ocultar el navegador --#
    
    #options.add_argument('--headless')
    
    #-- Descomentar las siguientes dos lineas en caso de ejecutar en MAC/LINUX  --#
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito')
    options.add_argument("--start-maximized")
    options.add_argument('ignore-certificate-errors') #ignore certificate errors for google chrome
    # -- USO DE PROXIES -- #
    if proxie != None:
        options.add_argument(f'--proxy-server={proxie}')
    #options.add_argument(f'user-agent={userAgent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=dr, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    return driver


def start_lichess():
    link = "https://lichess.org/"
    driver.get(link)
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='top']/div[2]/a").click()
    time.sleep(3)
    #Loggin in lichess
    login()

def login():
    #username = 'jab17'
    #password = '26962323'
    username = 'mherize'
    password = '25832303'

    input_user = driver.find_element(By.XPATH,'.//input[contains(@id,"username")]')
    input_pass = driver.find_element(By.XPATH,'.//input[contains(@id,"password")]')

    input_user.send_keys(username)
    input_pass.send_keys(password)

    driver.find_element_by_xpath('//*[@id="main-wrap"]/main/form/div[1]/button').click()
    time.sleep(3)
    #Pasamos al perfil y a todos los datos
    go_to_insight()

def go_to_insight():
    driver.find_element_by_xpath('//*[@id="user_tag"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="dasher_app"]/div/div[1]/a[1]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="us_profile"]/div[2]/a').click()
    time.sleep(1)
    
    #presets
    driver.find_element_by_xpath('//*[@id="insight"]/div/div[1]/div[2]/a[1]').click()
    
    for p in range(1,9):
        presets(p)

    #Data Frame with Pandas
    df = pd.DataFrame({'Busqueda': lista0,
        'Titulos' : lista0,
        'data' : lista1,
        'size' : lista2,
        })
    df.to_csv('process/scrapy.csv', index=False , encoding='utf-8')

def presets(p):
    driver.find_element_by_xpath('//*[@id="insight"]/div/div[1]/div[2]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="insight"]/div/div[1]/div[3]/a['+str(p)+']').click()
    driver.refresh() 
    time.sleep(2)
    html = driver.page_source
    respObj = Selector(text=html)
    time.sleep(2)
    item_title = respObj.xpath('.//th[contains(@class,"")]').getall()
    column1 = respObj.xpath('.//td[contains(@class,"data")]/text()').getall()
    column2 = respObj.xpath('.//td[contains(@class,"size")]/text()').getall()
    lista0.append(item_title)
    lista1.append(column1)
    lista2.append(column2)
    print("titulos:", item_title)
    print("column1:", column1)
    print("column2:", column2)

def variant():
    #extrae los primeros datos del isight
    html = driver.page_source
    respObj = Selector(text=html)
    time.sleep(2)
    item_title = respObj.xpath('.//th[contains(@class,"")]').getall()
    column1 = respObj.xpath('.//td[contains(@class,"data")]/text()').getall()
    column2 = respObj.xpath('.//td[contains(@class,"size")]/text()').getall()
    lista0.append(item_title)
    lista1.append(column1)
    lista2.append(column2)
    #for l in item_title:
    #    title = re.findall(r'\>((?:\S\s?)+)\<',l)
    #    print("title",title)

    print("titulos:", item_title)
    print("column1:", column1)
    print("column2:", column2)
    
    #presets
    driver.find_element_by_xpath('//*[@id="insight"]/div/div[1]/div[2]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="insight"]/div/div[1]/div[3]/a[1]').click()
    driver.refresh() 
    time.sleep(2)
    html = driver.page_source
    respObj2 = Selector(text=html)
    time.sleep(5)
    item_title = respObj2.xpath('.//th[contains(@class,"")]').getall()
    column1 = respObj2.xpath('.//td[contains(@class,"data")]/text()').getall()
    column2 = respObj2.xpath('.//td[contains(@class,"size")]/text()').getall()
    print("item_title:", item_title)
    print("column2:", column2)
    print("column1:", column1)
    lista0.append(item_title)
    lista1.append(column1)
    lista2.append(column2)

dr = ChromeDriverManager().install()
driver = initChromeDriver(dr)
time.sleep(1)

#Open lichess
start_lichess()



