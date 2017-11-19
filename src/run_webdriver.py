from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from enum import Enum
import configparser

class Direction(Enum):
  LEFT_UP = 1
  UP = 2
  RIGHT_UP = 3
  LEFT = 4
  RIGHT = 5
  LEFT_DOWN = 6
  DOWN = 7
  RIGHT_DOWN = 8

  @staticmethod
  def get_direction_offset(direction):
    return { Direction.LEFT_UP    : (-1, -1),
             Direction.UP         : (0, -1),
             Direction.RIGHT_UP   : (1, -1),
             Direction.LEFT       : (-1, 0),
             Direction.RIGHT      : (1, 0),
             Direction.LEFT_DOWN  : (-1, 1),
             Direction.DOWN       : (0, 1),
             Direction.RIGHT_DOWN : (1, 1),
           }[direction]

class NeoquestRunner:
  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config.read('config.ini')

    user = 'JENNY'
    
    adblockpath = self.config[user]['adblockpath']
    chromepath = self.config[user]['chromepath']

    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + adblockpath)

    if user == 'JENNY':
      self.driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
      self.driver = webdriver.Chrome(chromepath, chrome_options=chrome_options)

    self.driver.create_options()

  def login(self, login_file_name):
    username = self.config['NEOPETS']['username']
    password = self.config['NEOPETS']['password']

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
    time.sleep(.5)

  def __get_content_module(self):
    return self.driver.find_element_by_class_name("contentModule")

  # ONLY FOR MAP SCREENS
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
        output[(j, i)] = result[32:-4]
    output[(0, 0)] = output[(0, 0)][5:]
    return output

  def can_warp(self):
    content_div = self.__get_content_module()
    return ("Go!" in content_div.text)
  
  def is_battle_start_screen(self):
    content_div = self.__get_content_module()
    if "You are attacked by" in content_div.text:
      return True
    return False

  def is_battle_victory_screen(self):
    content_div = self.__get_content_module()
    return ("Click here to see what you found" in content_div.text)

  def battle_victory_resolve(self):
    content_div = self.__get_content_module()
    links = content_div.find_elements_by_tag_name("a")
    for link in links:
      if "Click here to see what you found" in link.text:
        link.click()
    content_div = self.__get_content_module()
    form = content_div.find_element_by_tag_name("form")
    form.submit()

  def battle_start(self):
    content_div = self.driver.find_element_by_class_name("contentModule")
    form = content_div.find_element_by_tag_name("form")
    form.submit()

  def __battle_get_actions(self):
    content_div = self.driver.find_element_by_class_name("contentModule")
    table = content_div.find_element_by_tag_name("table")
    trs = table.find_elements_by_tag_name("tr")
    action_block = trs[-1]
    action_links = action_block.find_elements_by_tag_name("a")
    return action_links

  def battle_action_attack(self):
    action_links = self.__battle_get_actions()
    for link in action_links:
      if "Attack" in link.text:
        link.click()
        return

  def battle_action_flee(self):
    action_links = self.__battle_get_actions()
    for link in action_links:
      if "Flee" in link.text:
        link.click()
        return

  def battle_enemy_health(self):
    content_div = self.__get_content_module()
    status_row = content_div.find_elements_by_tag_name("tr")[3]
    td = status_row.find_elements_by_tag_name("td")[1]
    health_str = td.text[td.text.find(":"): td.text.find("/")]
    return int(health_str)

  def player_health(self):
    content_div = self.__get_content_module()
    health_str = content_div.text[content_div.text.find("Health:")+7: content_div.text.find("/")]
    print health_str
    return int(health_str)

  def battle_enemy_level(self):
    content_div = self.__get_content_module()
    status_row = content_div.find_elements_by_tag_name("tr")[3]
    td = status_row.find_elements_by_tag_name("td")[1]
    level_str = td.text[td.text.find("Level:")+6:]
    return int(level_str)

  def is_battle_defeat_screen(self):
    content_div = self.__get_content_module()
    if "Click here to see the aftermath" in content_div.text:
      return True
    return False

  def battle_defeat_resolve(self):
    content_div = self.__get_content_module()
    links = content_div.find_elements_by_tag_name("a")
    for link in links:
      if "Click here to see the aftermath" in link.text:
        link.click()
    content_div = self.__get_content_module()
    form = content_div.find_element_by_tag_name("form")
    form.submit()

  def set_mode_sneaking(self):
    self.driver.get("http://www.neopets.com/games/neoquest/neoquest.phtml?movetype=3")
    time.sleep(.3)

  def set_mode_hunting(self):
    self.driver.get("http://www.neopets.com/games/neoquest/neoquest.phtml?movetype=2")
    time.sleep(.3)

  def initiate_talk(self):
    content_div = self.__get_content_module()
    links = content_div.find_elements_by_tag_name("a")
    for link in links:
      if "Talk to" in link.text:
        link.click()

  def end_talk(self):
    content_div = self.__get_content_module()
    form = content_div.find_element_by_tag_name("form")
    form.submit()
