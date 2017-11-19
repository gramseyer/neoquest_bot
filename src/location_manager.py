from run_webdriver import Direction

class Location:
  def __init__(self, coordinate, cur_map):
    self.coord = coordinate
    self.cur_map = cur_map

  #Only guaranteed to mimic NQ behaviour for known tiles.  
  #For unknown tiles, must check against observed behavior.
  def move(self, direction):
    (dx, dy) = Direction.get_direction_offset(direction)
    self.coord = (self.coord[0]+dx, self.coord[1] + dy)

  def copy(self):
    return Location(self.coord, self.cur_map)

  #Maybe outside of overworld don't go down cave until you've explored everything?

  # Returns whether or not we moved successfully
  def process_observed_data(self, observed_map, direction, world):
    diff_count = 0
    unknown_count = 0
    for key in observed_map.keys():
      new_key = (key[0] + self.coord[0], key[1] + self.coord[1])
      if new_key in self.cur_map.map_data.keys():
        if observed_map[key] != self.cur_map.map_data[new_key]:
          diff_count = diff_count + 1
          if key == (0, 0):
            diff_count = diff_count + 5 # catch the case where we try to move onto an isolated impassable tile
      else:
        unknown_count = unknown_count + 1
    
    if diff_count >= 3 or unknown_count > 10:  #We're not going to have more than 1 or two changes externally
      (dx, dy) = Direction.get_direction_offset(direction)
      self.cur_map.add_data(observed_map, (self.coord[0] + dx, self.coord[1] + dy))
      world.set_passability(observed_map[(0, 0)], True)
      print "move successful"
      return True
    else:
      self.cur_map.add_data(observed_map, self.coord)
      world.set_passability(observed_map[(0, 0)], False)
      print "move failed"
      return False

  def process_and_move(self, observed_map, direction, world):
    if self.process_observed_data(observed_map, direction, world):
      self.move(direction)
      return True
    return False

class NQMap:
  def __init__(self, mapname):
    self.map_data = {}
    self.mapname = mapname
    self.warp_map = {}
    self.warp_unmapped = []

  def add_warp(self, cur_coord, new_loc):
    self.warp_map[cur_coord] = new_loc

  def mark_warp(self, coord):
   self.warp_unmapped.append(coord)

  def add_data(self, new_data, player_coord):
    (x,y) = player_coord
    for (x1, y1) in new_data.keys():
      self.map_data[(x+x1, y+y1)] = new_data[(x1, y1)]

  def print_map(self, location=None):
    (max_x, max_y) = self.map_data.keys()[0]
    (min_x, min_y) = (max_x, max_y)
    for (x, y) in self.map_data.keys():
      if (x < min_x):
        min_x = x
      if (x > max_x):
        max_x = x
      if (y < min_y):
        min_y = y
      if (y > max_y):
        max_y = y
    for y in range(min_y, max_y + 1):
      for x in range(min_x, max_x + 1):
        if location is not None and (x,y) == location.coord:
          print "P",
        elif (x,y) in self.map_data.keys():
          print self.map_data[(x,y)][0],
        else:
          print "X",
      print " "

class NQWorld:
  def __init__(self):
    self.maps = {}
    self.passability = {}
    self.warpability = {}

  def get_map(self, name):
    return self.maps[name]

  def add_map(self, name):
    self.maps[name] = NQMap(name)

  def set_passability(self, tile, passable):
    self.passability[tile] = passable

  def is_passable(self, tile):
    return self.passability[tile]

  def set_warp(self, tile, warpable):
    self.warpability[tile] = warpable

  def is_warpable(self, tile):
    return self.warpability[tile]

  def print_world(self, location = None):
    for mapname in self.maps.keys():
      print mapname
      if location is not None and location.cur_map.mapname == mapname:
        self.maps[mapname].print_map(location = location)
      else:
        self.maps[mapname].print_map()

