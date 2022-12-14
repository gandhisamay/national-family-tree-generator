from chromedriver_autoinstaller.utils import download_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# TODO
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import requests

from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from mimetypes import guess_extension
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from ..mainCaptcha import main
from time import sleep
# from captcha import main


# driver_path = "/home/samaygandhi/Documents/chromedriver"
    
options = webdriver.ChromeOptions()
# options.binary_location = "/usr/bin/brave-browser"
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
# driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)
# driver.get("https://ceotserms2.telangana.gov.in/ts_erolls/rolls.aspx")
driver.maximize_window()
# https://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber=8&roll=EnglishMotherRoll&districtName=DIST_08&acname=AC_024&acnameeng=A24&acno=24&acnameurdu=024
# https://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber=6&roll=EnglishMotherRoll&districtName=DIST_17&acname=AC_067&acnameeng=A67&acno=67&acnameurdu=067
#https://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber=1&roll=EnglishMotherRoll&districtName=DIST_03&acname=AC_007&acnameeng=A7&acno=7&acnameurdu=007
partNumber = 6
districtNumber = 17
assemblyConstituencyNumber = 67

if len(str(districtNumber)) == 1:
    districtNumber = f"0{districtNumber}"


# if len(str(pollingStationNumber)) == 1:
#     pollingStationNumberString = f"0{pollingStationNumber}"
# else:
#     pollingStationNumberString = str(pollingStationNumber)
#

url = f"https://ceotserms2.telangana.gov.in/ts_erolls/Popuppage.aspx?partNumber={partNumber}&roll=EnglishMotherRoll&districtName=DIST_{districtNumber}&acname=AC_0{assemblyConstituencyNumber}&acnameeng=A{assemblyConstituencyNumber}&acno={assemblyConstituencyNumber}&acnameurdu=0{assemblyConstituencyNumber}"

driver.get(url)



# district = "3-Adilabad"
# assemblyConstituency = "8-Boath(ST)"
#
# selectDistrict = Select(driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_ddlDist"))
# selectDistrict.select_by_visible_text(district)
#
# selectAssemblyConstituency = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlAC"))
# selectAssemblyConstituency.select_by_visible_text(assemblyConstituency)
#
# driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnlogin").click()
#
#
# pollingStationNumber = 9
# pollingStationName = "Zilla Parishad Secondary School, Arlit"
#
# # driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_GridView3")
#
# # soup = BeautifulSoup(driver.page_source, 'lxml')
# # print(soup.prettify)
#
# # print(soup.find("table").tbody)
# pollingStationNumberString = ""
#
# if len(str(pollingStationNumber)) == 1:
#     pollingStationNumberString = f"0{pollingStationNumber}"
# else:
#     pollingStationNumberString = str(pollingStationNumber)
#
# englishId = f"ctl00_ContentPlaceHolder1_GridView3_ctl{pollingStationNumberString}_lnkEnglish"
#
# driver.find_element(By.ID, englishId).click()
#
# print(driver.window_handles)
#
# ?partNumber=17&roll=EnglishMotherRoll&districtName=DIST_03&acname=AC_008&acnameeng=A8&acno=8&acnameurdu=008


# print(soup.find("a", {"id": englishId})['href'])



# for row in soup.find("table", {"id" : "ctl00_ContentPlaceHolder1_GridView3"}).tbody:
#         for entry in row:
#             try:
#                 if pollingStationName in entry:
#                     found = True
#                     if found:
#                         if 
#             except:
#                 pass
#

# print(table)

# print(table)
#
# for station in table:
#     print(station)
#     print(station.find_element(By.ID, "ctl00_ContentPlaceHolder1_GridView3_ctl06_lnkEnglish"))
#
#
# print(table)


# selectPart = Select(driver.find_element(By.ID, "ctl00_Content_PartList"))
# selectPart.select_by_value(str(part))
#
s = requests.session()
for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)


r = s.get(url)
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    r = s.get("https://ceotserms2.telangana.gov.in/ts_erolls/Captcha.aspx")
    if r.status_code == 200:
        guess = guess_extension(r.headers['content-type'])
        if not guess: guess = ".png"
        if guess:
            with open("scripts/telangana/captcha" + guess, "wb") as f:
                f.write(r.content)
            # Image.open(BytesIO(r.content)).show()

CAPTCHA_TEXT = main(state="telangana")
print(f"Captcha Text obtained: {CAPTCHA_TEXT}")

driver.find_element(By.ID, "txtVerificationCode").send_keys(CAPTCHA_TEXT)

soup = BeautifulSoup(driver.page_source, 'lxml')
print(soup.find('input', {'id': 'btnSubmit'}))

driver.find_element(By.ID, "btnSubmit").submit()
sleep(0.1)

for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)

print("Parsing PDF...")
payload = {
    'txtVerificationCode': CAPTCHA_TEXT,
    'btnSubmit': 'Submit'
}

r = s.post(url, data=payload)
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    if r.status_code == 200:
        guess = guess_extension(r.headers['content-type'])
        if not guess: guess = ".pdf"
        if guess:
            print("Storing pdf...")
            with open("scripts/telangana/electoral_rolls" + guess, "wb") as f:
                f.write(r.content)


