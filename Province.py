class Province:
    def __init__(self, name, current_owner, terrain):
        self.name = name
        self.current_owner = current_owner
        self.terrain_type = terrain
        self.neighbor_provinces = []
        self.army_progress = 0
        self.level = 1
        self.level_cap = 5

    def upgrade(self):
        if self.level < self.level_cap:
            self.level += 1

    def produce_army(self):
        self.army_progress += self.level
        if self.army_progress >= 1:
            self.current_owner.army_creation(self)
            self.army_progress = 0
