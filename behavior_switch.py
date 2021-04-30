from behavior import Behavior


class Switch(Behavior):
    def __init__(self, name, value, setname, setvalue):
        super(Switch, self).__init__()

        self.name = name
        self.value = value
        self.setname = setname
        self.setvalue = setvalue

    def activated(self, game_object):
        # print("switch activated")
        # print("name: " + self.name)
        # print("value: " + self.value)
        if game_object.get_property(self.name) == self.value:
            self.game_object.set_property(self.setname, self.setvalue)
