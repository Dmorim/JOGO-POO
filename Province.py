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
        self.in_battle = False
        self.dom_turns = 0
        self.create_army_requisition = 5

        self.level_defence_modifiers = {1: 1.0, 2: 1.5, 3: 1.6, 4: 1.75, 5: 1.9}

    def upgrade(self):
        if self.level < self.level_cap:
            self.level += 1

    def produce_army(self):
        self.army_progress += self.level
        if self.army_progress >= self.create_army_requisition:
            if not self.get_in_battle():
                if self.dom_turns == 0:
                    self.current_owner.army_creation(self)
                    self.army_progress = 0
                    return True
        return False

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

    def get_owner(self):
        return self.current_owner

    def get_defence_modifier(self):
        return self.level_defence_modifiers[self.level]

    def set_current_owner(self, new_owner):
        self.current_owner = new_owner

    def get_in_battle(self):
        return self.in_battle

    def set_in_battle(self, in_battle):
        self.in_battle = in_battle

    def set_dom_turns(self, turns):
        if turns > 0:
            self.dom_turns = turns

    def update_dom_turns(self):
        if self.dom_turns != 0:
            self.dom_turns -= 1

    def get_dom_turns(self):
        return self.dom_turns

    def get_level_cap(self):
        return self.level_cap
