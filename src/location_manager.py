from run_webdriver import Direction


class Location:
  def __init__(self, coordinate, map_name):
    self.coord = coordinate
    self.map_name = map_name

  def move(self, direction):
    (dx, dy) = Direction.get_direction_offset(direction)
    self.coord = (self.coord[0]+dx, self.coord[1] + dy)

class NQMap:
  def __init__(self, mapname):
    self.map_data = {}
    self.mapname = mapname

  def add_data(self, new_data, player_loc):
    (x,y) = player_loc
    for (x1, y1) in new_data.keys():
      if (x1 != 0 or y1 != 0):
        self.map_data[(x+x1, y+y1)] = new_data[(x1, y1)]

  def print_map(self):
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
        if (x,y) in self.map_data.keys():
          print self.map_data[(x,y)][0],
        else:
          print "X",
      print " "

class NQWorld:
  def __init__(self):
    maps = {}

  def add_map(self, name)
    maps[name] = NQMap(name)

  def print_world(self):
    for mapname in maps.keys():
      print mapname
      maps[mapname].print_map()

