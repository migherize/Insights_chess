#1 import libraries
from selenium import webdriver
from scrapy import Selector
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

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
    variant()

def variant():
    #extrae los primeros datos del isight
    html = driver.page_source
    respObj = Selector(text=html)
    '''
    table_xpath = './/table[contains(@class,"slist")]/thead'
    item_list2 = respObj.xpath(table_xpath)
    print("item_list2:", item_list2)

    item_list = respObj.xpath('.//table[contains(@class,"slist")]').get()
    for elem in item_list2:
        print("elem",elem)
    '''

    item_list = respObj.xpath('.//th/text()').getall()

    column1 = respObj.xpath('.//td[contains(@class,"data")]/text()').getall()
    column2 = respObj.xpath('.//td[contains(@class,"size")]/text()').getall()
    print(item_list[0]," | ",item_list[1]," | ",item_list[2])
    print(item_list[3]," | ",column1[0]," | ",column2[0])
    print(item_list[4]," | ",column1[1]," | ",column2[1])
    print(item_list[5]," | ",column1[2]," | ",column2[2])
    print(item_list[6]," | ",column1[3]," | ",column2[3])
    
    #print("item_list:", item_list)
    #print("column1:", column1)
    #print("column2:", column2)






dr = ChromeDriverManager().install()
driver = initChromeDriver(dr)
time.sleep(1)

#Open lichess
start_lichess()



