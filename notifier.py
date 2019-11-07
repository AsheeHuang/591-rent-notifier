from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
from selenium.common import exceptions  

def check_for_new_house(seen) :
    def get_region_id(url):
        region_id = ""
        idx = url.find("region=") + 7
        while url[idx].isdigit() :
            region_id += url[idx]
            idx += 1
        return region_id
    config = json.load(open("config.json"))
    house_url = config["591_url"]

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    driver = webdriver.Chrome(executable_path=config["default_driver_dir"], options=options)
    driver.get(house_url)
    # driver.set_window_size(1920,1080)

    region_id = get_region_id(house_url)
    newtaipei = driver.find_element_by_css_selector("dd[data-id='%s']" % region_id) 
    newtaipei.click()

    # wait for loading
    sleep(2) 
    houses = driver.find_elements_by_css_selector("img[class='boxImg lazy']")

    new_houses = {}
    for house in houses :
        try : 
            house_code = house.get_attribute("data-bind")
            house_txt = house.get_attribute("alt")
        except exceptions.StaleElementReferenceException:
            break
        if house_code not in seen :
            new_houses[house_code] = house_txt
            seen[house_code] = house_txt
    driver.close()
    return new_houses

def run_notifier() :
    seen = {}
    while True :
        new_houses = check_for_new_house(seen)
        if(not new_houses) :
            print(datetime.datetime.now(), ": No new object")
        else :
            print(datetime.datetime.now(), ": New object")
            print(new_houses)
            send_email_to_me(new_houses)
        sleep(600)

def send_email_to_me(new_houses) :
    config = json.load(open("config.json"))
    sender = config["email_acc"]
    receivers = [config["email_acc"]]
    mail_text = ''
    for house_code, house_txt in new_houses.items() :
        template = "<a href='https://rent.591.com.tw/rent-detail-%s.html'> %s</a>" %(house_code, house_txt) + "<br><br>"
        mail_text += template
    message = MIMEText(mail_text, 'html', 'utf-8')
    message['From'] = Header("Myself", 'utf-8')
    message['To'] = Header("Myself", 'utf-8')
    message['Subject'] = Header("New house ! Check it !", 'utf-8')

    try : 
        smtp = smtplib.SMTP(config["smtp_server"])
        smtp.ehlo()
        smtp.starttls()
        smtp.login(config["email_acc"], config["email_pass"])
        smtp.sendmail(sender, receivers, message.as_string())
        print("Sent ! ")
    except :
        print("Error ! Check your email account and password")
        exit(1)

if __name__ == "__main__" : 
    run_notifier()