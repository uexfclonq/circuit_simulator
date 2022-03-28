from connectors import *

class Resistor:
    def __init__(self, name, resistance):
        self.name = name
        self.resistance = resistance


class Diode:
    def __init__(self, name):
        self.name = name
        self.IN = Input(self)
        self.OUT = Output(self)


class TransistorNpn:
    def __init__(self, name, threshold_voltage):
        self.name = name
        self.tv = threshold_voltage
        self.E = Emitter(self)
        self.B = Base(self)
        self.C = Collector(self)

    def open(self, b_voltage):
        return b_voltage >= self.tv

    def e_voltage(self, b_voltage, ce_voltage):
        return b_voltage + ce_voltage


class TransistorPnp:
    def __init__(self, name, threshold_voltage):
        self.name = name
        self.tv = threshold_voltage

    def open(self, b_voltage):
        return b_voltage >= self.tv

    def e_voltage(self, b_voltage, ce_voltage):
        return ce_voltage - b_voltage


class VoltageSource:
    def __init__(self, name, voltage, max_current, state):
        self.name = name
        self.voltage = voltage
        self.max_current = max_current
        self.on = state
        self.IN = Input(self, voltage)
        self.OUT = Output(self, voltage)
        self.resistance = 0

    def set_state(self, state):
        self.on = state