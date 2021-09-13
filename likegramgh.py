from time import sleep
from selenium import webdriver
from myigbot import MyIGBot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import requests, os
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options = options)

uerr = 0
ierr = 0

#Discord Webhook
webhook = ''

#Instagram account credentials
bot = MyIGBot('username', 'password')

#Likegram credentials
useremail = 'email'
userpassw = 'passwd'

#Logo:
def logo():
    print('''
    dMP    .aMMMMP dMMMMb  .aMMMb dMMMMMMP 
   dMP    dMP"    dMP"dMP dMP"dMP   dMP    
  dMP    dMP MMP"dMMMMK" dMP dMP   dMP     
 dMP    dMP.dMP dMP.aMF dMP.aMP   dMP      
dMMMMMP VMMMP" dMMMMP"  VMMMP"   dMP      
- likegram.cz bot, created by github.com/exzedik
''')

### LOGIN into likegram
def login():
    try:
        driver.get("https://likegram.cz/login")
        email = driver.find_element_by_id("email")
        email.send_keys(useremail)
        passw = driver.find_element_by_id("password")
        passw.send_keys(userpassw)
        passw.send_keys(Keys.RETURN)
        sleep(1)
        if driver.current_url == 'https://likegram.cz/dashboard':
            os.system(f'title LGBot  -  {useremail}');os.system('cls');logo()
            print(f'Logged in as {useremail}')
        else:
            print('[!] Error while logging into likegram.cz! Retrying in 5 minutes')
            sleep(300)
            login()
    except:
        print('[!] Error while logging into likegram.cz! Retrying in 5 minutes')
        sleep(300)
        login()

#Skip account (used if account is private)
def skip():
    driver.find_elements_by_tag_name('button')[3].click()

#Send a message to a discord webhook
def whookSend(content):
    requests.post(webhook, json = {"content" : content})
### Start Job
login()
while True:
    try:
        driver.get("https://likegram.cz/earn")
        sleep(0.5)
        username = driver.find_elements_by_tag_name('h3')[0].text.strip()
        print(f'Checking private status of @{username}')
        private = bot.private_user(username)
        following = bot.followed_by_me(username)
        print(f'Private status: {private}')
        print(f'Already following? {following}')
        driver.execute_script('function LoadIG(username){}')
        if private == True:
            print("Private account, skipping, waiting 2s\n____________________")
            skip()
            sleep(2)
            private = None
        elif following == True:
            print('Already following, unfollowing, waiting 2s')
            print(bot.unfollow(username.lstrip()))
            sleep(2)
            print(f'Following @{username}')
            driver.find_elements_by_tag_name('button')[2].click()
            response = bot.follow(username.lstrip())
            print(f'Following @{username} returned the response {response}, waiting 5s')
            sleep(5)
            driver.execute_script('$(".followBtnAfter").click()')
            print('Done, waiting 35s\n____________________')
            sleep(35)
            print(f"Balance = {driver.find_element_by_id('zustatekOP').text}, Followed today: {driver.find_element_by_id('sledovanOP').text}, Followed total: {driver.find_element_by_id('sledovanCelkem').text}")
        else:
            print(f'Following @{username}')
            driver.find_elements_by_tag_name('button')[2].click()
            response = bot.follow(username.lstrip())
            print(f'Following @{username} returned the response {response}, waiting 5s')
            sleep(5)
            driver.execute_script('$(".followBtnAfter").click()')
            print('Done, waiting 35s\n____________________')
            sleep(35)
            print(f"Balance = {driver.find_element_by_id('zustatekOP').text}, Followed today: {driver.find_element_by_id('sledovanOP').text}, Followed total: {driver.find_element_by_id('sledovanCelkem').text}")
    except IndexError:
        if ierr > 0:
            ierr += 1
            print(f'[!] No more people to follow! Retrying in 3 minutes [{ierr}]')
            sleep(180)
        else:
            print('[!] No more people to follow! Retrying in 3 minutes')
            sleep(180)
    except KeyboardInterrupt:
        print('Interrupting, closing all drivers. Bye!')
        driver.quit()
    except:
        if uerr > 5:
            whookSend(f"Too many unknown errors! ({uerr})")
            print('[!] Unknown error! Retrying in 15 minutes')
            uerr += 1
            sleep(900)
        else:
            print('[!] Unknown error! Retrying in 15 minutes')
            uerr += 1
            sleep(900)