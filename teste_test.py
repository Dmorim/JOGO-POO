import unittest
from Battle import Battle
from Player import Player
from Army import Army
from Province import Province
from Terrain import Terrain


import unittest
from Battle import Battle
from Player import Player
from Army import Army
from Province import Province
from Terrain import Terrain


class TestBattleSimulation(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.atacante = Player("Atacante")
        self.defensor = Player("Defensor")
        self.terrain = Terrain("Plains", 1.0, 1.0, 1.0)

    def test_battle_simulation(self):
        offensive_wins = 0
        defensive_wins = 0
        num_simulations = 100

        for _ in range(num_simulations):
            # Criar uma nova instância da província para cada simulação
            prov_atacante = Province("Província", self.atacante, self.terrain)
            prov_defensor = Province("Província", self.defensor, self.terrain)
            prov_atacante.level = 1
            prov_defensor.level = 1

            self.atacante.add_province(prov_atacante)
            self.defensor.add_province(prov_defensor)

            army_off = [Army(prov_atacante, self.atacante) for _ in range(10)]
            army_def = [Army(prov_defensor, self.defensor) for _ in range(10)]

            battle = Battle(self.atacante, self.defensor, prov_defensor)
            for army in army_off:
                battle.add_off_army(army)
            for army in army_def:
                battle.add_def_army(army)

            while not battle.battle_going():
                pass

            battle.finish_battle()

            if battle.get_winner() == self.atacante:
                offensive_wins += 1
            elif battle.get_winner() == self.defensor:
                defensive_wins += 1

            # Remover as províncias dos jogadores para a próxima simulação
            self.atacante.debugg_clear_provinces()
            self.defensor.debugg_clear_provinces()

        print(f"Ofensivo venceu {offensive_wins} vezes.")
        print(f"Defensivo venceu {defensive_wins} vezes.")

        # Verificar se o número total de vitórias é igual ao número de simulações
        self.assertEqual(offensive_wins + defensive_wins, num_simulations)


if __name__ == '__main__':
    unittest.main()
