import run_webdriver
import location_manager
import random
import battle_runner
import time

def run_game():
  world = location_manager.NQWorld()
  world.add_map("overworld")
  overworld_map = world.get_map("overworld")
  spawn_location = location_manager.Location((0,0), overworld_map)

  driver = run_webdriver.NeoquestRunner()
  driver.login("logindata")
  driver.load_view()
  
  start_map = driver.get_map()
  overworld_map.initialize_map(start_map, spawn_location)
  loc = spawn_location.copy()
  driver.set_mode_hunting()
  hunting = True
    
  while(True):
    direction = get_direction(hunting, loc)
    driver.send_move(direction)
    if driver.is_battle_start_screen():
      print "starting battle"
      result = battle_runner.run_battle(driver)
      print "ending battle"
      if result.defeat:
        loc = spawn_location.copy()
        print "defeated"
        continue
    map_data = driver.get_map()
    loc.process_and_move(map_data, direction, world)
    world.print_world(location = loc)
    if driver.player_health() < 10:
      hunting = False
      driver.set_mode_sneaking()
    if loc.coord == (-1, -1):
      driver.initiate_talk()
      driver.end_talk()
      driver.set_mode_hunting()
      hunting = True
    print loc.coord
    #print hunting
   # time.sleep(2) 

def get_direction(hunting, loc):
  if not hunting:
    if loc.coord[0] > -1 and loc.coord[1] > -1:
      return 1
    if loc.coord[0] == -1 and loc.coord[1] > -1:
      return 2
    if loc.coord[0] < -1 and loc.coord[1] > -1:
      return 3
    if loc.coord[0] > -1 and loc.coord[1] == -1:
      return 5
    if loc.coord[0] < -1 and loc.coord[1] == -1:
      return 4
    if loc.coord[0] > -1 and loc.coord[1] < -1:
      return 6
    if loc.coord[0] == -1 and loc.coord[1] < -1:
      return 7
    if loc.coord[0] < -1 and loc.coord[1] < -1:
      return 8   
  return random.randint(1,8)


if __name__ == "__main__":
  run_game()
