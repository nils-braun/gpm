class BaseSnapshot:
    def __init__(self):
        pass

    @property
    def name_param(self):
        raise NotImplementedError

    @property
    def name(self):
        return "{class_name}: {name_param}".format(class_name=self.__class__.__name__,
                                                   name_param=self.name_param)
