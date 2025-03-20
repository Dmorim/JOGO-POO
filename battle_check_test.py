import unittest
from unittest.mock import MagicMock
from Player import Player
from Game.Turn_Checks.Game_Turn_Check import GameTurnChecks
from Game.Turn_Checks.Checks_Execution.Army_Move_Checks import ArmyMoveChecks
from Game.Turn_Checks.Checks_Execution.Army_Group_Checks import ArmyGroupCheck
from Game.Turn_Checks.Checks_Execution.Province_Checks import ProvinceChecks
from Game.Turn_Checks.Checks_Execution.Army_Health_Check import ArmyHealthChecker
from Game.Turn_Checks.Checks_Execution.Army_Battle_Updater import BattleUpdater
from Game.Turn_Checks.Checks_Execution.Army_Battle_Finisher import BattleFinisher
from Game.Battle_Control import Battle_Control
from Game.Turn_Checks.Army_Checks import ArmyChecks
from Game.Turn_Checks.Battle_Checks import BattleChecks

class TestGameTurnChecks(unittest.TestCase):

    def setUp(self):
        self.battle_control = MagicMock(Battle_Control)
        self.army_move_checks = MagicMock(ArmyMoveChecks)
        self.army_group_checks = MagicMock(ArmyGroupCheck)
        self.province_checks = MagicMock(ProvinceChecks)
        self.army_health_checker = MagicMock(ArmyHealthChecker)
        self.battle_finisher = MagicMock(BattleFinisher)
        self.battle_updater = MagicMock(BattleUpdater)
        self.army_checks = MagicMock(ArmyChecks)
        self.battle_checks = MagicMock(BattleChecks)

        self.game_turn_checks = GameTurnChecks()
        self.game_turn_checks.battle_control = self.battle_control
        self.game_turn_checks.army_move_checks = self.army_move_checks
        self.game_turn_checks.army_group_checks = self.army_group_checks
        self.game_turn_checks.province_checks = self.province_checks
        self.game_turn_checks.army_health_checker = self.army_health_checker
        self.game_turn_checks.battle_finisher = self.battle_finisher
        self.game_turn_checks.battle_updater = self.battle_updater
        self.game_turn_checks.army_checks = self.army_checks
        self.game_turn_checks.battle_checks = self.battle_checks

    def test_end_of_turns_checks(self):
        player = MagicMock(Player)
        self.game_turn_checks.end_of_turns_checks(player)
        self.army_checks.army_checks.assert_called_once_with(player)

    def test_begin_of_turns_checks(self):
        player = MagicMock(Player)
        self.game_turn_checks.begin_of_turns_checks(player)
        self.battle_checks.battle_checks.assert_called_once_with(player)

if __name__ == '__main__':
    unittest.main()