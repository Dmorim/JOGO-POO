from Configs.Console import ConsoleClass
from Game.Battle_Control.Battle_Control import BattleControl


class Map_Battles:
    def __init__(self, battle_control: BattleControl):
        self.console = ConsoleClass.get_console()
        self.battle_control = battle_control

    def get_no_fog_battles(self):
        battles_info = {}
        for idx, (province, battle) in enumerate(self.battle_control.ongoing_battles.items(), start=1):
            battles_info[idx] = (
                province.get_name(),
                battle.get_off_army_owner().get_player_name(),
                battle.get_def_army_owner().get_player_name(),
                battle.battle_situation()
            )
        print(battles_info)
