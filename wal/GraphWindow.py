import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
from BeamDesign import BeamDesign


class GraphWindow:
    # trzeba dodac podwoic ilosc pkt na wykresach ze wzgledu na to ze w silach sie zle one rysuja 
    def __init__(self,node, master, YForce, ZForce, YTorque, ZTorque, Torque, momentum, distance):
        self.node = node
        self.master = master
        self.YForce = YForce
        self.ZForce = ZForce
        self.YTorque = YTorque
        self.ZTorque = ZTorque
        self.Torque = Torque
        self.momentum = momentum
        self.distance = distance
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.window_with_graf()

    def display_graph(self, selected_theory, selected_graph):
        plt.figure()
        plt.title(f"Graph for {selected_theory} - {selected_graph}")
        plt.xlabel("lengh [m]")

        # distance list
        self.distance_list = []
        for i in range(len(self.distance)):
            self.distance_list.append(sum(self.distance[:i]))
        print(self.distance_list)


        if selected_graph == "XY force graph":
            plt.ylabel("Force [N]")
            if len(self.correct_distance(self.distance_list)) == len(self.correct_force(self.YForce)):
                plt.plot(self.correct_distance(self.distance_list), self.correct_force(self.YForce))
            else:
                plt.plot(self.distance_list, self.YForce)

        if selected_graph == "XZ force graph":
            plt.ylabel("Force [N]")
            if len(self.correct_distance(self.distance_list)) == len(self.correct_force(self.ZForce)):
                plt.plot(self.correct_distance(self.distance_list), self.correct_force(self.ZForce))
            else:
                plt.plot(self.distance_list, self.ZForce)

        if selected_graph == "XY torque graph":
            plt.ylabel("Torque [Nm]")
            plt.plot(self.distance_list, self.YTorque)

        if selected_graph == "XZ torque graph":
            plt.ylabel("Torque [Nm]")
            plt.plot(self.distance_list, self.ZTorque)

        if selected_graph == "Torque graph":
            plt.ylabel("Torque [Nm]")
            plt.plot(self.distance_list, self.sum_torque())

        if selected_graph == "Result torque graph":
            plt.ylabel("Torque [Nm]")

            if len(self.correct_distance(self.distance_list)) == len(self.correct_force(self.Torque)):
                plt.plot(self.correct_distance(self.distance_list), self.correct_force(self.Torque))
            else:
                plt.plot(self.distance_list, self.correct_torque(self.Torque))

        if selected_graph == "torque reduced on both axes" and selected_theory == "Huber–Misesa–Hencky H-M-H":
            plt.ylabel("Torque [Nm]")
            plt.plot(self.distance_list, self.HMH())

        elif selected_graph == "torque reduced on both axes" and selected_theory == "Coulomb–Tresci–Guest C-T-G":
            plt.ylabel("Torque [Nm]")
            plt.plot(self.distance_list, self.CTG())

        else:
            plt.ylabel("Torque [Nm]")
            plt.plot(0, 0)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    # prepering force list to disply in force graph
    def correct_force(self, force):
        new_forces = []
        for i in range(len(force)):
            new_forces.append(sum(force[:i]))

        new_forces = new_forces[1:]
        correct_Force = []
        for val in new_forces:
            if correct_Force and correct_Force[-1] == val:
                continue
            else:
                correct_Force.extend([val, val])
        return correct_Force

    # creating new list with double liste element with out firs and last element
    def correct_distance(self, distance):
        CorrectDistance = [dist for dist in distance for _ in range(2)][1:-1]

        return CorrectDistance

    def update_graph(self, *args):
        selected_theory = self.theory_var.get()
        selected_graph = self.graph_var.get()
        self.display_graph(selected_theory, selected_graph)

    def window_with_graf(self):

        close_button = tk.Button(self.frame, text='Exit', command=self.frame.destroy)
        close_button.grid(row=1, column=1, pady=10)

        # Option menu to choose stress theory
        self.theory_var = tk.StringVar(self.frame)
        self.theory_var.set("set stress theory")
        theory_menu = tk.OptionMenu(self.frame, self.theory_var, "Coulomb–Tresci–Guest C-T-G", "Huber–Misesa–Hencky H-M-H")
        theory_menu.grid(row=0, column=0, pady=10)
        self.theory_var.trace_add("write", self.update_graph)

        # Option menu to choose which graph should be displayed
        self.graph_var = tk.StringVar(self.frame)
        self.graph_var.set("set graph")
        graph_menu = tk.OptionMenu(self.frame, self.graph_var, "XY force graph", "XZ force graph",
                                   "XY torque graph", "XZ torque graph", "Torque graph",
                                   "Result torque graph", "torque reduced on both axes")
        graph_menu.grid(row=0, column=1, pady=10)
        self.graph_var.trace_add("write", self.update_graph)

        # Initial graph display
        self.display_graph(self.theory_var.get(), self.graph_var.get())

        # Create button to called BeamDesian window
        BeamDesign_button = tk.Button(self.frame, text="Beam Design Window", command=self.Beam_Desiagn)
        BeamDesign_button.grid(row=0, column=2, pady=10)
        

    def Beam_Desiagn(self):
        selected_theory = self.theory_var.get()
        reduce_torque = None

        if selected_theory == "Huber–Misesa–Hencky H-M-H":
            reduce_torque = self.HMH()
        elif selected_theory == "Coulomb–Tresci–Guest C-T-G":
            reduce_torque = self.CTG()
        else:
            tk.messagebox.showerror("Error", "Please choose theory.")

        if not selected_theory == "set stress theory":
            beam_design = BeamDesign(node = self.node, master=self.master, 
                                 distance=self.distance_list, 
                                 torque=self.correct_torque(self.Torque),
                                 reduce_torque=reduce_torque,
                                 bending_torque=self.sum_torque(),
                                 Zforce = self.ZForce, Xforce=self.YForce)


    def sum_force(self):
        reduce_forces = []
        for i in range(len(self.YForce)):
            reduce_force = sqrt(self.YForce[i]**2 + self.ZForce[i]**2)
            reduce_forces.append(reduce_force)

        return reduce_forces
    
    def sum_torque(self):
        reduce_torques = []
        for i in range(len(self.YTorque)):
            reduce_torque = sqrt(self.YTorque[i]**2 + self.ZTorque[i]**2)
            reduce_torques.append(reduce_torque)

        return reduce_torques

    def correct_torque(self, torque):
        CorrectTorques = []
        for i in range(len(torque)):
            CorrectTorques.append(sum(torque[:i]))

        return CorrectTorques

    # Ztorque is torque and Ytorque is bending moment
    def HMH(self):
        HMH_torques = []
        for i in range(len(self.YTorque)):
            HMH_torque = sqrt(16/3*(self.sum_torque()[i])**2 + 0.75*(self.correct_torque(self.Torque)[i])**2)
            HMH_torques.append(HMH_torque)
        print(f"HMH: {HMH_torques}")

        return HMH_torques 

    def CTG(self):
        CTG_torques = []
        for i in range(len(self.YTorque)):
            CTG_torque = sqrt(16/3*(self.sum_torque()[i])**2 + (self.correct_torque(self.Torque)[i])**2)
            CTG_torques.append(CTG_torque)
        print(f"CTG: {CTG_torques}")

        return CTG_torques
