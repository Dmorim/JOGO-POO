from Game.Battle_Control.Battle_Control import BattleControl


class GameMap:
    def __init__(self, game):
        self.game = game
        self.battle_control = BattleControl()
        pass

    def print_map(self):
        # Print the map with province ownership and armies
        print(f"\nTurno: {self.game.get_turn_count()}")
        print("\nMapa:")
        for player in self.game.players:
            print(f"{'-'*110}\nJogador: {player.get_player_name()}\n{'-'*110}")
            for province in player.get_player_province():
                print(
                    f"Província: {province.get_name()}, Terreno: {province.get_terrain().get_terrain_name()}. (Nível: {
                        province.get_level()}) Vizinhos: {', '.join(neighbor.get_name() for neighbor in province.get_neighbors())}"
                )
                if player.get_armys():
                    armies = [
                        army
                        for army in player.get_armys()
                        if army.get_province() == province
                    ]
                    for army in armies:
                        print(army.army_situation())
            print()
        if self.battle_control.ongoing_battles:
            print(f"{'='*25}\nBatalhas em andamento:\n{'='*25}")
            for i, battle in enumerate(self.battle_control.ongoing_battles):
                print(
                    f"Batalha {i} em {battle.get_province().get_name()} entre {battle.get_off_army_owner().get_player_name()} e {battle.get_def_army_owner().get_player_name()}.\nExército atacante: Quantidade: {battle.total_off_army()}, Ataque: {battle.get_off_total_attack()}, Defesa: {battle.get_off_total_defense()}, Vida: {round(
                        battle.get_off_actual_health(), 2)}, {battle.get_off_army_owner().get_player_name()}\nExército defensor: Quantidade: {battle.total_def_army()}, Ataque: {battle.get_def_total_attack()}, Defesa: {battle.get_def_total_defense()}, Vida: {round(battle.get_def_actual_health(), 2)}, {battle.get_def_army_owner().get_player_name()}"
                )
                print(f"{'='*78}")
                print(battle.get_last_off_damage())
                print(f"{battle.get_last_def_damage()}\n")
                if self.battle_control.ongoing_battles.index(battle) != len(self.battle_control.ongoing_battles) - 1:
                    print(f"{'='*78}\n")
