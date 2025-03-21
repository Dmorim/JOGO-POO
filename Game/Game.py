from Army import Army_Group
from Game.Actions.Player_Actions import Player_Action
from Game.Turn_Checks.Game_Turn_Check import GameTurnChecks
from Game.Game_State import Game_State


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.turn_count = 0
        self.ongoing_battles = []
        self.finished_battles = []
        self.state = Game_State()
        self.checks = GameTurnChecks()
        self.actions = Player_Action()

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
                self.checks.begin_of_turns_checks(self.current_player)

                while self.turn_pass():
                    if self.state.mapmode:
                        self.print_map()
                    self.actions.action(
                        self.current_player.get_ia(), self.state.mapmode)

                # Update game state

            self.checks.end_of_turns_checks(self.current_player)
            self.next_turn()
