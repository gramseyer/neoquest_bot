from selenium import webdriver
import time

class NeoquestRunner:
  def __init__(self):
    self.driver = webdriver.Chrome('/mnt/d/Downloads/chromedriver_win32/chromedriver.exe')

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

  
