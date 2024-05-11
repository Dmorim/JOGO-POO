class Province:
    def __init__(self, name, current_owner, terrain, move_req=10):
        self.name = name
        self.current_owner = current_owner
        self.terrain_type = terrain
        self.neighbor_provinces = []
        self.army_progress = 0
        self.level = 1
        self.level_cap = 5
        self.move_req = move_req

    def upgrade(self):
        if self.level < self.level_cap:
            self.level += 1

    def produce_army(self):
        self.army_progress += self.level
        if self.army_progress >= 1:
            self.current_owner.army_creation(self)
            self.army_progress = 0
            
    def add_neighbor(self, *args):
        for neighbor in args:
            self.neighbor_provinces.append(neighbor)
            
    def get_neighbors(self):
        return self.neighbor_provinces
    
    def get_move_req(self):
        return self.move_req

    def get_name(self):
        return self.name
    
    def get_terrain(self):
        return self.terrain_type
    
    def get_level(self):
        return self.level