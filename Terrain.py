class Terrain:
    def __init__(
        self,
        terrain: str,
        move_modifier: float,
        upgrade_modifier: float,
        defence_modifier: float,
    ):
        self.terrain = terrain
        self.terrain_move_modifier = move_modifier
        self.terrain_upgrade_modifier = upgrade_modifier
        self.terrain_defence_modifier = defence_modifier
