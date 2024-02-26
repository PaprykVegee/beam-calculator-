import numpy as np
import sympy as sp

class BeamCalculator():
    def __init__(self):
        self.nodes = []
        self.Force_of_reaction_on_X = None
        self.Force_of_reaction_on_Z = None


    def add_node(self, position):
        self.nodes.append({"position": position, "force": None, "moment": None, "distance": None, "torque": None})

    def set_force(self, node_index, force):
        self.nodes[node_index]["force"] = force

    def set_moment(self, node_index, moment):
        self.nodes[node_index]["moment"] = moment

    def set_distance(self, node_index, distance):
        self.nodes[node_index]["distance"] = distance

    def set_torque(self, node_index, torque):
        self.nodes[node_index]["torque"] = torque
         
    def set_ZForce(self, node_index, ZForce):
        self.nodes[node_index]["ZForce"] = ZForce

    def set_ZDistance(self, node_index, ZDistance):
        self.nodes[node_index]["ZDistance"] = ZDistance

    def calculate_force_of_reaction(self, force_list, distance_list,  moment_list = None, coordintate = 'X'):

        # force equasin
        R1, R2 = sp.symbols('R1 R2')
        # równanie sił równowagi w poziomie
        force_equation = sp.Eq(R1 + R2 + sum(force_list), 0)

        # Torque equesion
        moment_equations = []
        total_distance = 0
        distance_list = [0] + distance_list[:-1]
        if moment_list == None:
            moment_list = [0]*len(force_list)
        for i in range(len(force_list)):
            total_distance += distance_list[i]
            moment_equation = force_list[i] * total_distance + moment_list[i]
            moment_equations.append(moment_equation)
        torque_equation = sp.Eq(R2*sum(distance_list) + sum(moment_equations), 0)
        
        solution = sp.solve((force_equation, torque_equation), (R1, R2))

        if coordintate == 'X':
            self.Force_of_reaction_on_X = solution
            
        elif coordintate == 'Z':
            self.Force_of_reaction_on_Z = solution
        print(solution)

        
        R1_val = solution[R1].evalf()
        R2_val = solution[R2].evalf()

        # add reaction force and calculate point to graf on torque
        force_list[0] += float(R1_val)
        force_list[-1] += float(R2_val)

        total_distance = 0
        moment_equations = []
        for i in range(len(force_list)):
            total_distance += distance_list[i]
            moment_equation = force_list[i] * total_distance + moment_list[i]
            moment_equations.append(moment_equation)
        moment_val = []
        for i in range(len(moment_equations)):
            moment_val.append(sum(moment_equations[:i+1]))
