from Player import Player
from Game.Turn_Checks.Checks_Execution.Army_Move_Checks import ArmyMoveChecks
from Game.Turn_Checks.Checks_Execution.Army_Group_Checks import ArmyGroupCheck
from Game.Turn_Checks.Checks_Execution.Province_Checks import ProvinceChecks
from Game.Turn_Checks.Checks_Execution.Army_Health_Check import ArmyHealthChecker
from Game.Turn_Checks.Checks_Execution.Army_Battle_Updater import BattleUpdater
from Game.Turn_Checks.Checks_Execution.Army_Battle_Finisher import BattleFinisher
from Game.Battle_Control import Battle_Control


from Game.Turn_Checks.Army_Checks import ArmyChecks
from Game.Turn_Checks.Battle_Checks import BattleChecks


class GameTurnChecks:
    def __init__(self):
        self.battle_control = Battle_Control()

        self.army_move_checks = ArmyMoveChecks()
        self.army_group_checks = ArmyGroupCheck()
        self.province_checks = ProvinceChecks()
        self.army_health_checker = ArmyHealthChecker()
        self.battle_finisher = BattleFinisher()
        self.battle_updater = BattleUpdater(
            self.battle_control, self.battle_finisher)

        self.army_checks = ArmyChecks(
            self.army_move_checks, self.army_group_checks, self.province_checks)
        self.battle_checks = BattleChecks(
            self.battle_control, self.battle_finisher, self.army_health_checker, self.battle_updater)

    def end_of_turns_checks(self, player: Player):
        self.army_checks.army_checks(player)

    def begin_of_turns_checks(self, player: Player):
        self.battle_checks.battle_checks(player)
