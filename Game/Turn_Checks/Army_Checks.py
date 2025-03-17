from Player import Player
from Game.Turn_Checks.Checks_Execution.Army_Move_Checks import ArmyMoveChecks
from Game.Turn_Checks.Checks_Execution.Army_Group_Checks import ArmyGroupCheck
from Game.Turn_Checks.Checks_Execution.Province_Checks import ProvinceChecks


class ArmyChecks:
    def __init__(self, move_checks: ArmyMoveChecks, group_checks: ArmyGroupCheck, province_checks: ProvinceChecks):
        self.group_checks = group_checks
        self.move_checks = move_checks
        self.province_checks = province_checks

    def army_checks(self, player: Player):
        self.group_checks.group_checks(player)
        self.move_checks.move_checks(player)
        self.province_checks.province_checks(player)
