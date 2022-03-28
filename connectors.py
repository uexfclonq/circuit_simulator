class Input:
    def __init__(self, parent, voltage):
        self.parent = parent
        self.voltage = voltage


class Output:
    def __init__(self, parent, voltage):
        self.parent = parent
        self.voltage = voltage


class Emitter:
    def __init__(self, parent):
        self.parent = parent


class Base:
    def __init__(self, parent):
        self.parent = parent


class Collector:
    def __init__(self, parent):
        self.parent = parent
