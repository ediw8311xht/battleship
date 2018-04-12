import unittest
from copy import deepcopy
from battleship import Ship, Board

class TestBoard(unittest.TestCase):
  """
    Tests Board class from battleship file.
  """
  udlr = {"UP": [1, 0], "DOWN": [-1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
  ts1a = [[5, [0, 0], "DOWN"]]
  ts2a = [[5, [5, 5], "DOWN"]]
  ts1b = []
  def test_range(self):
    self.assertEqual(Board(100, [[5, [3, 0], "DOWN"]], self.ts1b).ships["a"], False)
    self.assertNotEqual(Board(100, [[5, [4, 0], "DOWN"]], self.ts1b).ships["a"], False)
    self.assertEqual(Board(100, [[10, [91, 0], "UP"]], self.ts1b).ships["a"], False)
    self.assertNotEqual(Board(100, [[10, [90, 0], "UP"]], self.ts1b).ships["a"], False)
    self.assertEqual(Board(100, [[10, [0, 91], "RIGHT"]], self.ts1b).ships["a"], False)
    self.assertNotEqual(Board(100, [[10, [0, 90], "RIGHT"]], self.ts1b).ships["a"], False)
    self.assertEqual(Board(100, [[10, [0, 8], "LEFT"]], self.ts1b).ships["a"], False)
    self.assertNotEqual(Board(100, [[10, [0, 9], "LEFT"]], self.ts1b).ships["a"], False)
  def test_hit_remove(self):
    a = Board(100, deepcopy(self.ts2a), self.ts1b)
    self.assertEqual(a.get_hit([5, 5], "a"), "HIT")
    self.assertEqual(a.get_hit([5, 5], "a"), "NOT HIT")
  def test_udlr(self):
    for i in self.udlr.keys():
      n = [[10, [30, 30], i]]
      n_pos = [30, 30]
      a = Board(100, n, self.ts1b)
      for jj in range(0, 10):
        if jj == 9:
          self.assertEqual(a.get_hit(n_pos, "a"), "SUNK")
        else:
          self.assertEqual(a.get_hit(n_pos, "a"), "HIT")
        n_pos[0] += self.udlr[i][0]
        n_pos[1] += self.udlr[i][1]
      self.assertEqual(a.get_hit(n_pos, "a"), "NOT HIT")
  def test_ship_gets_removed(self):
    a = Board(100, deepcopy(self.ts2a), self.ts1b)
    for i in range(5, 1, -1):
      self.assertEqual(a.get_hit([i, 5], "a"), "HIT")
    self.assertEqual(a.get_hit([1, 5], "a"), "SUNK")
    self.assertEqual(len(a.ships["a"]), 0)

if __name__ == "__main__":
  unittest.main()
  
  

