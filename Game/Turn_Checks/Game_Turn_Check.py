from Player import Player
from Game.Turn_Checks.Checks_Execution.Army_Move_Checks import ArmyMoveChecks
from Game.Turn_Checks.Checks_Execution.Army_Group_Checks import ArmyGroupCheck
from Game.Turn_Checks.Checks_Execution.Province_Checks import ProvinceChecks
from Game.Turn_Checks.Army_Checks import ArmyChecks


class GameTurnChecks:
    def __init__(self):
        self.army_move_checks = ArmyMoveChecks()
        self.army_group_checks = ArmyGroupCheck()
        self.province_checks = ProvinceChecks()

        self.army_checks = ArmyChecks(
            self.army_move_checks, self.army_group_checks, self.province_checks)

    def end_of_turns_checks(self, player: Player):
        self.army_checks.army_checks(player)

    def begin_of_turns_checks(self):
        pass
