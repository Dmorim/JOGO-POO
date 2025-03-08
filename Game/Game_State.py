

class Game_State():
    _isInstance = None

    def __new__(cls):
        if cls._isInstance is None:
            cls._isInstance = super().__new__(cls)
        return cls._isInstance

    def __init__(self):
        self.__mapmode = True
        self.__player_skip = False

    @property
    def mapmode(self) -> bool:
        return self.__mapmode

    @mapmode.setter
    def mapmode(self, value: bool):
        self.__mapmode = value

    @property
    def player_skip(self) -> bool:
        return self.__player_skip

    @player_skip.setter
    def player_skip(self, value: bool):
        self.__player_skip = value
