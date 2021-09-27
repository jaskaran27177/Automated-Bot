from config import keys
#system libraries
import os
import random
import time
#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

def delay ():
    time.sleep(random.randint(2,3))

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print((endTime - startTime)/1000, 's')
        return result
    return wrapper
@timeme
def order(k):
    driver.get(k['product_url'])
    driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(k['name'])
 
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(k['email'])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(k['phone_number'])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(k['address'])

    driver.find_element_by_xpath('//*[@id="order_billing_country"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="order_billing_state"]/option[3]').click()
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(k['zip'])
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(k['city'])

    
    driver.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(k['credit_card_number'])
    driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(k["month"])).click()
    driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(k["year"])).click()
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(k['cvv'])
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div').click()
    driver.find_element_by_xpath('//*[@id="pay"]/input').click()
    
    # driver.get('https://www.google.com/recaptcha/api2/demo')
    # ############################################################this is to click the box, dont use on supreme site########################################
    # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span#recaptcha-anchor"))).click()
    # ################################################################################################################################################################
    
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button"))).click()

    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='recaptcha challenge']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#\\:2"))).click()
    

    #get the mp3 audio file
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print("[INFO] Audio src: %s"%src)
    #download the mp3 audio file from the source
    time.sleep(2)
    urllib.request.urlretrieve(src, "./Downloads/project/supremebot/"+"\\sample.mp3")
    sound = pydub.AudioSegment.from_mp3("./Downloads/project/supremebot/"+"\\sample.mp3")
    sound.export("./Downloads/project/supremebot/"+"\\sample.wav", format="wav")
    sample_audio = sr.AudioFile("./Downloads/project/supremebot/"+"\\sample.wav")
    r= sr.Recognizer()

    with sample_audio as source:
        audio = r.record(source)

    #translate audio to text with google voice recognition
    key=r.recognize_google(audio)
    print("[INFO] Recaptcha Passcode: %s"%key)

    #key in results and submit
    driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()

    
    

if __name__=='__main__':
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless")
    # options.add_argument("--incognito")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver=webdriver.Chrome(options=options,executable_path='./Downloads/project/supremebot/chromedriver')
 
    order(keys)