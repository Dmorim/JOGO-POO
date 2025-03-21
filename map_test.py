import unittest
from unittest.mock import MagicMock, patch
from Game.Game_Map import GameMap
from Game.Battle_Control.Battle_Control import BattleControl
from Player import Player
from Province import Province
from Terrain import Terrain
from Army import Army
import io
import sys

class TestGameMap(unittest.TestCase):

    def setUp(self):
        self.game = MagicMock()
        self.game.get_turn_count.return_value = 0  # Garantir que o turno seja 0
        self.battle_control = MagicMock(BattleControl)
        self.game_map = GameMap(self.game)
        self.game_map.battle_control = self.battle_control

    @patch('builtins.print')
    def test_print_map(self, mock_print):
        # Setup mock players, provinces, and armies
        player1 = MagicMock(Player)
        player1.get_player_name.return_value = "Player 1"
        player1.get_player_province.return_value = []
        player1.get_armys.return_value = []

        player2 = MagicMock(Player)
        player2.get_player_name.return_value = "Player 2"
        player2.get_player_province.return_value = []
        player2.get_armys.return_value = []

        self.game.players = [player1, player2]

        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.game_map.print_map()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Print the captured output
        print(captured_output.getvalue())

        # Verify print statements
        mock_print.assert_any_call("\nTurno: 0")
        mock_print.assert_any_call("\nMapa:")
        mock_print.assert_any_call(f"{'-'*110}\nJogador: Player 1\n{'-'*110}")
        mock_print.assert_any_call(f"{'-'*110}\nJogador: Player 2\n{'-'*110}")

    @patch('builtins.print')
    def test_print_map_with_provinces_and_armies(self, mock_print):
        # Setup mock players, provinces, and armies
        terrain = MagicMock(Terrain)
        terrain.get_terrain_name.return_value = "Plains"

        province1 = MagicMock(Province)
        province1.get_name.return_value = "Province 1"
        province1.get_terrain.return_value = terrain
        province1.get_level.return_value = 1
        province1.get_neighbors.return_value = []

        army1 = MagicMock(Army)
        army1.get_province.return_value = province1
        army1.army_situation.return_value = "Army 1 situation"

        player1 = MagicMock(Player)
        player1.get_player_name.return_value = "Player 1"
        player1.get_player_province.return_value = [province1]
        player1.get_armys.return_value = [army1]

        self.game.players = [player1]

        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.game_map.print_map()

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Print the captured output
        print(captured_output.getvalue())

        # Verify print statements
        mock_print.assert_any_call("\nTurno: 0")
        mock_print.assert_any_call("\nMapa:")
        mock_print.assert_any_call(f"{'-'*110}\nJogador: Player 1\n{'-'*110}")
        mock_print.assert_any_call("Província: Province 1, Terreno: Plains. (Nível: 1) Vizinhos: ")
        mock_print.assert_any_call("Army 1 situation")

if __name__ == '__main__':
    unittest.main()