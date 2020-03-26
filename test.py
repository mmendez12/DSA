import unittest
from DSA import Player
from DSA import Chip


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("p1")
        self.p1.stock = [Chip(4, 10), Chip(3, 2)]
        self.p2 = Player("p2")
        self.p2.stock = [Chip(4, 10), Chip(3, 2)]
        self.p3 = Player("p3")
        self.p3.stock = [Chip(4, 10), Chip(3, 1), Chip(3, 1)]
        self.p4 = Player("p4")
        self.p4.stock = [Chip(4, 6),  Chip(3, 1)]

    def test_equal_players(self):
        self.assertEqual(self.p1, self.p2)

    def test_non_equal_players(self):
        self.assertNotEqual(self.p1, self.p4)

    def test_players_with_same_total_score(self):
        self.assertLess(self.p2, self.p3)

    def test_sort_players(self):
        players = [self.p1, self.p3, self.p4]
        sorted_player_names = [p.name for p in sorted(players)]
        expected = ["p4", "p1", "p3"]
        self.assertEqual(sorted_player_names, expected)


if __name__ == '__main__':
    unittest.main()
