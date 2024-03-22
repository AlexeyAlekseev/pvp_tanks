class GameObject:
    objects_list = []

    def __init__(self, objects_list: list):
        objects_list.append(self)
        self.objects_list = objects_list

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def damage(self, value):
        raise NotImplementedError
