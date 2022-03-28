from connectors import *
from components import *


class Circuit:
    def __init__(self, schematic):
        self.schematic = schematic
        self.graph = self.get_graph()
        self.components = self.get_components()
        self.condutors = self.get_conductors()
        self.branches = []
        self.branch_resistance = {}
        self.total_resistance = 0
        self.total_voltage = self.graph[0][0].voltage
        self.resistances = {}
        self.voltages = {}
        self.currents = {}

    # Initialisierungsfunktionen

    # returns graph from schematic (connectors turned into their components)
    def get_graph(self):
        graph = []
        for i in self.schematic:
            l = []
            for j in i:
                l.append(j)
            graph.append(l)
        return graph

    # returns list of components
    def get_components(self):
        c = []
        for i in self.graph:
            for j in i:
                x = self.get_parent(j)
                if x not in c:
                    c.append(x)
        return c

    # returns a list of all conductors
    def get_conductors(self):
        conductors = []
        for i in self.graph:
            for k in [[self.get_parent(i[0]), self.get_parent(j)] for j in i[1:]]:
                conductors.append(k)
        return conductors

    # Hilfsfunktionen

    # returns component to given connector
    def get_parent(self, component):
        try:
            return component.parent
        except AttributeError:
            return component

    # returns number of all inputs to given element
    def count_input(self, component):
        return [i[1] for i in self.condutors].count(component)

    def count_output(self, component):
        return [i[0] for i in self.condutors].count(component)

    # returns graph index of element
    def get_knot(self, component):
        for i, e in enumerate(self.graph):
            if e[0] == component:
                return i

    # returns list of connections to given component
    def get_outputs(self, component):
        return [i[1] for i in self.condutors if i[0] == component]

    # returns list of connections to given component
    def get_inputs(self, component):
        return [i[0] for i in self.condutors if i[1] == component]

    def get_branch(self, component):
        for i in self.branches:
            if i[0] == component:
                return 1, i
            elif i[1] == component:
                return 2, i
        return 3, []

    # Hauptfunktionen

    def get_branches(self, component):
        if type(component) == VoltageSource or (
                self.count_input(component) > 1 and component not in [i[1] for i in self.branches]):
            return component
        while self.count_output(component) == 1:
            component = [i[1] for i in self.condutors if i[0] == component][0]
            if type(component) == VoltageSource or (
                    self.count_input(component) > 1 and component not in [i[1] for i in self.branches]):
                return component
        ends = []
        for i in self.get_outputs(component):
            ends.append(self.get_branches(i))
        if len(set(ends)) == 1:
            self.branches.append([component, ends[0]])
            return self.get_branches(ends[0])

    def get_resistance(self, component):
        connections = self.get_outputs(component)
        branch = self.get_branch(component)
        if type(component) == VoltageSource:
            return 0
        elif branch[0] == 1:
            resistors = []
            for i in connections:
                resistors.append(self.get_resistance(i))
            r = 1 / sum([1 / i for i in resistors])
            self.branch_resistance[self.branches.index(branch[1])] = r
            return component.resistance + r + self.get_resistance(branch[1][1])
        elif self.get_branch(connections[0])[0] == 2:
            return component.resistance
        else:
            return component.resistance + self.get_resistance(connections[0])

    def get_total_resistance(self):
        return 1 / sum([1 / self.get_resistance(i) for i in self.get_outputs(self.get_parent(self.graph[0][0]))])

    def get_voltage(self, component):
        r = 0
        c = component
        while type(c) != VoltageSource:
            i = self.get_inputs(c)
            if len(i) > 1:
                b = self.get_branch(c)
                r += self.branch_resistance[self.branches.index(b[1])]
                c = b[1][0]
            else:
                r += c.resistance
                c = self.get_inputs(c)[0]
        c = component
        while type(c) != VoltageSource:
            i = self.get_outputs(c)
            if len(i) > 1:
                b = self.get_branch(c)
                r += self.branch_resistance[self.branches.index(b[1])]
                c = b[1][1]
            else:
                r += c.resistance
                c = self.get_outputs(c)[0]
        return (component.resistance * self.total_voltage) / (r - component.resistance)

    # Showfunktionen

    # prints components
    def show_components(self):
        print([i.name for i in self.components])

    # prints conductors between components
    def show_conductors(self):
        print([[i[0].name, i[1].name] for i in self.condutors])

    # prints adjacency list
    def show_adj_list(self):
        for i in self.graph:
            print([self.get_parent(j).name for j in i])

    # prints adjecency matrix
    def show_adj_matrix(self):
        print("\t" + ("\t".join([str(i.name) for i in self.components])))
        for i in self.components:
            line = i.name + "\t"
            for j in self.components:
                if [i, j] in self.condutors:
                    line += "1"
                else:
                    line += "0"
                line += "\t"
            print(line)


# test environment

V1 = VoltageSource("U1", 12, 3, 1)
V2 = VoltageSource("U2", 4, 1, 1)
R1 = Resistor("R1", 2)
R2 = Resistor("R2", 4)
R3 = Resistor("R3", 5)
R4 = Resistor("R4", 1)
R5 = Resistor("R5", 1)
R6 = Resistor("R6", 1)
T1 = TransistorNpn("T1", 3)
G = [[V1.OUT, R1, R2],
     [R1, T1.E],
     [R2, V1.OUT],
     [T1.C, V1.IN],
     [V2.OUT, T1.E],
     [T1.B, V2.IN]]
G2 = [[V1.OUT, R1, R2],
      [R1, R3, R4],
      [R2, V1.IN],
      [R3, V1.IN],
      [R4, R2]]
G3 = [[V1.OUT, R1, R2],
      [R1, V1.IN],
      [R2, V1.IN]]
G4 = [[V1.OUT, R1],
      [R1, R2, R3],
      [R2, R4, R5],
      [R4, R6],
      [R5, R6],
      [R6, V1.IN],
      [R3, V1.IN]]
C = Circuit(G4)
C.show_adj_matrix()
C.get_branches(R1)
print(C.branches)
C.get_total_resistance()
C.show_adj_list()
