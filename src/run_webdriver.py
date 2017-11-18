from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from enum import Enum

class Direction(Enum):
  LEFT_UP = 1
  UP = 2
  RIGHT_UP = 3
  LEFT = 4
  RIGHT = 5
  LEFT_DOWN = 6
  DOWN = 7
  RIGHT_DOWN = 8

class NeoquestRunner:
  def __init__(self):
#    adblockpath = 'D:\\adblock\\1.13.4_0\\' #'\\Users\\jorge\\AppData\\Local\\Google\\Chrome\\User\\ Data\\Default\\Extensions\\cfhdojbkjhnklbpkdaibdccddilifddb\\1.13.4_0\\'
    chrome_options = Options()
#    chrome_options.add_argument('load-extension=' + adblockpath)
    
    self.driver = webdriver.Chrome('/mnt/d/Downloads/chromedriver_win32/chromedriver.exe',
                                   chrome_options=chrome_options)
    self.driver.create_options()

  def login(self, login_file_name):
    login_file = open(login_file_name, "r")
    username = login_file.readline().strip()
    password = login_file.readline().strip()
    self.driver.get('http://www.neopets.com/login/index.phtml')
    time.sleep(.3)
    username_div = self.driver.find_element_by_class_name("welcomeLoginUsernameInput")
    username_input = username_div.find_element_by_name('username')
    username_input.send_keys(username)
    password_div = self.driver.find_element_by_class_name('welcomeLoginPasswordInput')
    password_input = password_div.find_element_by_name('password')
    password_input.send_keys(password)
    submit_button = self.driver.find_element_by_class_name('welcomeLoginButton')
    submit_button.click()

  def logout(self):
    self.driver.quit()

  def newgame(self):
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml?create=1&game_diff=0')
    time.sleep(.3)
    self.load_view()

  def load_view(self):
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml')
    time.sleep(.3)

  def choose_starting_skills(self):
    self.choose_skill("5001")
    self.choose_skill("5002")
    self.choose_skill("5003")
    self.choose_skill("3001")
    self.choose_skill("3002")
    self.choose_skill("3003")
    self.choose_skill("3004")

    self.character_create_accept()

    self.choose_starting_wand()

    self.character_create_accept()

    self.character_create_accept()

  def choose_skill(self, skillId):
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml?skill_choice=' + skillId)
    time.sleep(.3)

  def character_create_accept(self):
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml?cc_accept=1')
    time.sleep(.3)
 
  def choose_starting_wand(self):
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml?weapon_choice=5')
    time.sleep(.3)

  def send_move(self, direction):
    #Directions:
    # 1 2 3
    # 4   5
    # 6 7 8
    self.driver.get('http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir='
                     + str (direction))
    time.sleep(.3)

  def get_map(self):
    output = {}
    map_tbody = self.driver.find_element_by_class_name("contentModule") \
                           .find_elements_by_xpath('.//table//table')[0] \
                           .find_elements_by_tag_name("tr")[1:-1]
    for i in range(-3, 4):
      row = map_tbody[i+3]
      tds = row.find_elements_by_tag_name("td")[1:-1]
      for j in range(-3, 4):
        td = tds[j+3]
        result = td.find_element_by_tag_name("img").get_attribute("src")
        output[(i,j)] = result
    return output


  
