import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt

class GraphWindow:
    def __init__(self, master, YForce, ZForce, YTorque, ZTorque, distance):
        self.master = master
        self.YForce = YForce
        self.ZForce = ZForce
        self.YTorque = YTorque
        self.ZTorque = ZTorque
        self.distance = distance
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.window_with_graf()

    def display_graph(self, selected_theory, selected_graph):
        plt.figure()
        plt.title(f"Graph for {selected_theory} - {selected_graph}")
        plt.xlabel("lengh [m]")

        # distance list
        distance_list = []
        for i in range(len(self.distance)):
            distance_list.append(sum(self.distance[:i+1]))

        if selected_graph == "XY force graph":
            plt.ylabel("Force [N]")
            plt.plot(distance_list, self.YForce)

        if selected_graph == "XZ force graph":
            plt.ylabel("Force [N]")
            plt.plot(distance_list, self.ZForce)

        if selected_graph == "Force graph":
            plt.ylabel("Torque [N]")
            plt.plot(distance_list, self.__sum_force())

        if selected_graph == "XY torque graph":
            plt.ylabel("Torque [Nm]")
            plt.plot(distance_list, self.YTorque)

        if selected_graph == "XZ torque graph":
            plt.ylabel("Torque [Nm]")
            plt.plot(distance_list, self.ZTorque)

        if selected_graph == "torque reduced on both axes" and selected_theory == "Huber–Misesa–Hencky H-M-H":
            plt.ylabel("Torque [Nm]")
            plt.plot(distance_list, self.__HMH)

        elif selected_graph == "torque reduced on both axes" and selected_theory == "Coulomb–Tresci–Guest C-T-G":
            plt.ylabel("Torque [Nm]")
            plt.plot(distance_list, self.__CTG)

        else:
            plt.ylabel("Torque [Nm]")
            plt.plot(0, 0)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    def update_graph(self, *args):
        selected_theory = self.theory_var.get()
        selected_graph = self.graph_var.get()
        self.display_graph(selected_theory, selected_graph)

    def window_with_graf(self):
        # Option menu to choose stress theory
        self.theory_var = tk.StringVar(self.frame)
        self.theory_var.set("set stress theory")
        theory_menu = tk.OptionMenu(self.frame, self.theory_var, "Coulomb–Tresci–Guest C-T-G", "Huber–Misesa–Hencky H-M-H")
        theory_menu.grid(row=0, column=0, pady=10)
        self.theory_var.trace_add("write", self.update_graph)

        # Option menu to choose which graph should be displayed
        self.graph_var = tk.StringVar(self.frame)
        self.graph_var.set("set graph")
        graph_menu = tk.OptionMenu(self.frame, self.graph_var, "XY force graph", "XZ force graph", "Force graph"
                                   "XY torque graph", "XZ torque graph",
                                   "torque reduced on both axes")
        graph_menu.grid(row=0, column=1, pady=10)
        self.graph_var.trace_add("write", self.update_graph)

        # Initial graph display
        self.display_graph(self.theory_var.get(), self.graph_var.get())
         

    def __sum_force(self):
        reduce_forces = []
        for i in range(len(self.YForce)):
            reduce_force = sqrt(self.YForce[i]**2 + self.ZForce[i]**2)
            reduce_forces.append(reduce_force)

        return reduce_forces
    

    # Ztorque is torque and Ytorque is bending moment
    def __HMH(self):
        HMH_torques = []
        for i in range(len(self.YTorque)):
            HMH_torque = sqrt(self.YTorque**2 + 0.75*self.ZTorque**2)
            HMH_torques.append(HMH_torque)

        return HMH_torques

    def __CTG(self):
        CTG_torques = []
        for i in range(len(self.YTorque)):
            CTG_torque = sqrt(self.YForce**2 + self.ZTorque**2)
            CTG_torques.append(CTG_torque)

        return CTG_torques
