from Army import Army_Group
from Game.Executions.Move_Execution import Movement
from Game.Actions.Player_Actions import Player_Action
from Game.Game_State import Game_State


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.turn_count = 0
        self.ongoing_battles = []
        self.finished_battles = []
        self.state = Game_State()

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_turn_count(self):
        return self.turn_count

    def start(self):
        # Initialize game state
        self.current_player = self.players[0]

    def end(self):
        # Check if any player has conquered all provinces
        for player in self.players:
            if len(player.get_player_province()) == 0:
                return True
        return False

    def next_turn(self):
        # Switch to the next player
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]
        self.turn_count += 1

    def turn_pass(self):
        return True if self.current_player.can_perform_action() and self.state.player_skip == False else False

    def play(self):
        # Main game loop
        while not self.end():
            # Perform player actions
            for player in self.players:
                self.current_player = player
                self.current_player.actions += 3
                self.state.mapmode = True
                self.army_move_points()
                self.actions = Player_Action()

                while self.turn_pass():
                    if self.state.mapmode:
                        self.print_map()
                    self.actions.action(
                        self.current_player.get_ia(), self.state.mapmode)

                # Update game state

                self.moviment.update_movement_turns(self.current_player)
                self.update_battles()
                for province in self.current_player.get_player_province():
                    province.increment_turns_under_control()
            self.next_turn()

    def print_map(self):
        # Print the map with province ownership and armies
        print(f"\nTurno: {self.get_turn_count()}")
        print("\nMapa:")
        for player in self.players:
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
                        if isinstance(army, Army_Group):
                            if len(army.get_armys()) > 0:
                                if army.get_in_move():
                                    print(
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense(
                                        )}, Saúde: {army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                    )
                                else:
                                    print(
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {
                                            army.get_defense()}, Saúde: {army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                    )
                        else:
                            if army.get_in_move():
                                print(
                                    f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                        army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                )
                            else:
                                print(
                                    f"Exército: Ataque: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                        army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                )
            print()
        if self.ongoing_battles:
            print(f"{'='*25}\nBatalhas em andamento:\n{'='*25}")
            for i, battle in enumerate(self.ongoing_battles):
                print(
                    f"Batalha {i} em {battle.get_province().get_name()} entre {battle.get_off_army_owner().get_player_name()} e {battle.get_def_army_owner().get_player_name()}.\nExército atacante: Quantidade: {battle.total_off_army()}, Ataque: {battle.get_off_total_attack()}, Defesa: {battle.get_off_total_defense()}, Vida: {round(
                        battle.get_off_actual_health(), 2)}, {battle.get_off_army_owner().get_player_name()}\nExército defensor: Quantidade: {battle.total_def_army()}, Ataque: {battle.get_def_total_attack()}, Defesa: {battle.get_def_total_defense()}, Vida: {round(battle.get_def_actual_health(), 2)}, {battle.get_def_army_owner().get_player_name()}"
                )
                print(f"{'='*78}")
                print(battle.get_last_off_damage())
                print(f"{battle.get_last_def_damage()}\n")
                if self.ongoing_battles.index(battle) != len(self.ongoing_battles) - 1:
                    print(f"{'='*78}\n")
