import random
import time


class Ship(object):
  direction_dict = {"UP": [1, 0], "DOWN": [-1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
  def __init__(self, board_size, ship_size, position, direction):
    self.board_size = board_size
    self.positions = self.make_position_arr(ship_size, position[:], self.direction_dict[direction])
  def make_position_arr(self, ship_size, start, direction):
    arr = []
    for i in range(0, ship_size):
      if start[0] < 0 or start[1] < 0 or start[0] > self.board_size - 1 or start[1] > self.board_size - 1:
        return False
      arr.append(tuple(start))
      start[0] += direction[0]
      start[1] += direction[1]
    return arr
  def get_delete_position(self, position):
    for i in range(0, len(self.positions)):
      if self.positions[i][0] == position[0] and self.positions[i][1] == position[1]:
        del self.positions[i]
        return True
    return False
  def __str__(self):
    return str(self.positions)
    return "SHIP:  | " + "".join(self.positions)
    
class Board(object):
  direction_dict = {"UP": [1, 0], "DOWN": [-1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
  def __init__(self, size, ships_a, ships_b):
    self.size = size
    self.positions = {"a": set(), "b": set()}
    self.no_hits = {"a": [], "b": []}
    self.hits = {"a": [], "b": []}
    self.ships = {"a": [], "b": []}
    self.add_ships(ships_a, "a")
    self.add_ships(ships_b, "b")
  def add_ships(self, ships_arr, letter):
    for i in ships_arr:
      new_ship = Ship(self.size, i[0], i[1], i[2])
      new_positions = new_ship.positions
      if new_positions == False:
        self.ships[letter] = False
        return False
      else:
        break_out = False
        for j in range(0, len(new_positions)):
          if new_positions[j] in self.positions[letter]:
            break_out = True
            break
        if break_out != True:
          self.ships[letter].append(new_ship)
          self.positions[letter].update(new_positions)
    return True
  def get_possible_positions(self, letter, ship_size, direction):
    ship_positions = []
    curr_direction_dict = self.direction_dict[direction]
    for i in range(0, self.size):
      for j in range(0, self.size):
        n_pos = (i, j)
        for c in range(0, ship_size):
          if n_pos in self.positions[letter] or n_pos[0] < 0 or n_pos[0] >= self.size or n_pos[1] < 0 or n_pos[1] >= self.size:
            break
          elif c == ship_size - 1:
            ship_positions.append((i, j))
          n_pos = (n_pos[0] + curr_direction_dict[0], n_pos[1] + curr_direction_dict[1])
    return ship_positions
  def auto_fill_ships(self, letter, sizes="CLASSIC"):
    if sizes == "CLASSIC":
      sizes = [5, 4, 3, 3, 2]
    for i in sizes:
      possible_positions = []
      for j in self.direction_dict.keys():
        possible_positions += [[x, j] for x in self.get_possible_positions(letter, i, j)]
      r_position = random.choice(possible_positions)
      self.add_ships([[i, list(r_position[0]), r_position[1]]], letter)
  def get_hit(self, position, letter):
    if self.ships[letter] == False or position[0] < 0 or position[0] >= self.size or position[1] < 0 or position[1] >= self.size:
      return "NOT HIT"
    for i in range(0, len(self.ships[letter])):
      if self.ships[letter][i].get_delete_position(position):
        self.hits[letter].append(position)
        if len(self.ships[letter][i].positions) < 1:
          del self.ships[letter][i]
          return "SUNK"
        return "HIT"
    self.no_hits[letter].append(position)
    return "NOT HIT"
  def print_board(self, letter, no_hits=True, hits=True, ships=False):
    margin_left = " " * 2
    padding_between = " " * 1
    dis_arr = [["." for y in range(0, self.size)] for x in range(0, self.size)]
    if hits:
      for i in self.hits[letter]:
        dis_arr[i[0]][i[1]] = "o"
    if ships:
      ships_arr = []
      for x in self.ships[letter]:
        ships_arr += x.positions
      for i in ships_arr:
        dis_arr[i[0]][i[1]] = "l"
    if no_hits:
      for i in self.no_hits[letter]:
        dis_arr[i[0]][i[1]] = "x"
    print(margin_left + "  " + "".join([padding_between +  x for x in "ABCDEFGHIJ"]))
    for i in range(1, 11):
      print(margin_left + ("{:>2}".format(i) + " " + " ".join(dis_arr[i - 1])))
      
class Game(object):
  ship_dict = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}
  direction_dict = {"UP": [1, 0], "DOWN": [-1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
  alpha_dict = {"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[x]: x for x in range(0, 26)}
  reverse_direction = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
  table = {0: "PLAYER_1", 1: "PLAYER_2"}
  def __init__(self, name):
    self.player = name
    self.turn = "player"
    self.board = Board(10, [], [])
    self.ai_vars = {"found_ship": False, "position": False, "current_position": [], "direction": False, "tried": []}
  def get_position(self, phrase="Type in position of the ship you want to place: "):
    while 1:
      a = input(phrase).strip(" ").split(" ")
      a = [x.replace(" ", "") for x in a]
      if len(a) == 2:
        a[0] = a[0].upper()
        if a[0] in self.alpha_dict.keys() and a[1].isdigit():
          return [int(a[1]) - 1, self.alpha_dict[a[0]]]
      print("Invalid Input")
      print("Try Again")
  def get_direction(self):
    a = input("Type in the direction of the ship you want to place: ").strip(" ").lower()
    if "l" in a:
      return "LEFT"
    elif "r" in a:
      return "RIGHT"
    elif "u" in a:
      return "UP"
    else:
      return "DOWN"
  def get_ships(self, letter, sizes="CLASSIC"):
    if sizes == "CLASSIC":
      sizes = self.ship_dict.values()
    for i in sizes:
      output = False
      while output == False:
        self.board.print_board(letter, hits=False, ships=True)
        print(f"The size of this ship is {i}.")
        position = self.get_position()
        direction = self.get_direction()
        output = self.board.add_ships([[i, position, direction]], letter)
        if output == False:
          print("Position of ship out of range.")
        else:
          output = True
  def get_game_over(self):
    if len(self.board.ships["a"]) < 1:
      return "a"
    elif len(self.board.ships["b"]) < 1:
      return "b"
    else:
      return False
  def get_around(self, position):
    arr = []
    new_position = [0, 0]
    for i in range(-1, 2):
      new_position[0] = position[0] + i
      if new_position[0] >= 0 and new_position[0] < self.board.size:
        for j in range(-1, 2):
          if i == 0 and j == 0 or (abs(i) + abs(j)) > 1:
            continue
          new_position[1] = position[1] + j
          if new_position[1] >= 0 and new_position[1] < self.board.size:
            arr.append(new_position[:])
    return arr
  def direction_from_positions(self, first_pos, second_pos):
    n_pos = [first_pos[0] - second_pos[0], first_pos[1] - second_pos[1]]
    if n_pos[0] == 1:
      return "DOWN"
    elif n_pos[0] == -1:
      return "UP"
    elif n_pos[1] == 1:
      return "RIGHT"
    else:
      return "LEFT"
  def ai_calculate(self):
    n_arr = [[y, x] for x in range(0, 10) for y in range(0, 10) if [y, x] not in self.board.no_hits["a"] + self.board.hits["a"]]
    if self.ai_vars["found_ship"] == False:
      random_position = random.choice(n_arr)
      get_hit = self.board.get_hit(random_position, "a")
      if get_hit == "HIT":
        self.ai_vars["found_ship"] = True
        self.ai_vars["position"] = random_position
        self.ai_vars["current_position"] = self.ai_vars["position"][:]
        return "HIT"
      else:
        return "NOT HIT"
    else:
      if self.ai_vars["direction"] != False:
        d_arr = self.direction_dict[self.ai_vars["direction"]]
        self.ai_vars["current_position"][0] += d_arr[0]
        self.ai_vars["current_position"][1] += d_arr[1]
        get_hit = self.board.get_hit(self.ai_vars["current_position"], "a")
        if get_hit == "NOT HIT":
          self.ai_vars["direction"] = self.reverse_direction[self.ai_vars["direction"]]
          self.ai_vars["current_position"] = self.ai_vars["position"][:]
          return "NOT HIT"
        elif get_hit == "HIT":
          return "HIT"
      else:
        if len(self.ai_vars["tried"]) < 1:
          self.ai_vars["tried"] = [x for x in self.get_around(self.ai_vars["position"]) if x not in self.board.hits["a"] + self.board.no_hits["a"]]
        new_pos = self.ai_vars["tried"].pop()
        get_hit = self.board.get_hit(new_pos, "a")
        if get_hit == "HIT":
          self.ai_vars["direction"] = self.direction_from_positions(self.ai_vars["position"], new_pos)
          self.ai_vars["current_position"] = new_pos[:]
          return "HIT"
      if get_hit == "SUNK":
        self.ai_vars["tried"] = []
        self.ai_vars["found_ship"] = False
        return "SUNK"
    
  def game(self):
    self.get_ships("a")
    self.board.auto_fill_ships("b")
    while not self.get_game_over():
      print("ENEMY BOARD")
      self.board.print_board("b")
      hit_position = self.get_position(phrase="Type in position of place you want to hit: ")
      self.board.get_hit(hit_position, "b")
      print("\n\n\n\nENEMY BOARD")
      self.board.print_board("b")
      if self.get_game_over() != False:
        break
      input("Press enter to continue: ")
      print("\n\n\nthinking", end="", flush=True)
      time.sleep(0.4)
      print(".", end="", flush=True)
      time.sleep(0.4)
      print(".", end="", flush=True)
      time.sleep(0.4)
      print(".")
      time.sleep(1)
      self.ai_calculate()
      print("\n\n\nYOUR BOARD")
      self.board.print_board("a", ships=True)
      if self.get_game_over() != False:
        break
      input("Press enter to continue: ")
      print("\n\n\n")
    if self.get_game_over() == "a":
      sleep(1)
      print("\n\n\nCongragulations! You Win!")
    else:
      sleep(1)
      print("\n\n\nOh No! You Lost!")
    
