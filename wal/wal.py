import tkinter as tk
import numpy as np
import sympy as sp
from BeamCalculator import BeamCalculator
from GraphWindow import GraphWindow

class BeamApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Beam Calculator")
        self.master.geometry("800x500")

        # Canvas setup
        self.canvas = tk.Canvas(self.master, width=800, height=200)
        self.canvas.place(x=0, y=0)

        # Beam calculator instance
        self.beam_calculator = BeamCalculator()

        # Add Node button
        self.add_node_button = tk.Button(self.master, text="Add Node", command=self.add_node)
        self.add_node_button.place(x=0, y=300)

        # Draw button
        self.draw_button = tk.Button(self.master, text="Draw", command=self.calculate)
        self.draw_button.place(x=0, y=330)

        # Window graph button
        self.graph_Button = tk.Button(self.master, text="Display Graph Window", command=self.graph_window)
        self.graph_Button.place(x=0, y=390)

        # Calculate button
        self.calculate_button = tk.Button(
            self.master,
            text="Calculate",
            command=lambda: (
                self.beam_calculator.calculate_force_of_reaction(
                    force_list=self.force_list,
                    moment_list=self.torque_list,
                    distance_list=self.distence_list,
                    coordintate = 'X'
                )
                if hasattr(self, 'force_list') else self.show_error_message("No data to calculate"),

                self.beam_calculator.calculate_force_of_reaction(
                    force_list=self.ZForce_list, 
                    distance_list=self.distence_list,
                    Zdistance_list=self.ZDistance_list,
                    momentum_list=self.moemntum_list,
                    coordintate = 'Z'
                ), self.draw_force_of_react() if hasattr(self, 'ZForce_list') else self.show_error_message("No data to calculate")
            )
        )
        self.calculate_button.place(x=0, y=360)

        # Clear button
        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_all)
        self.clear_button.place(x=0, y=420)

        # Entry fields for force, torque, and distance
        self.force_entries = []
        self.torque_entries = []
        self.distance_entries = []
        self.momentum_entries = []
        self.ZForce_entries = []
        self.ZDistance_entries = []

        # Labels
        self.force_labels = []
        self.torque_labels = []
        self.distance_labels = []
        self.momentum_labels = []
        self.ZForce_labels = []
        self.ZDistance_labels = []
    
    def draw_force_of_react(self):
        #print("Force_of_reaction_on_X:", self.beam_calculator.Force_of_reaction_on_X)
        #print("Force_of_reaction_on_Z:", self.beam_calculator.Force_of_reaction_on_Z)
        R1, R2 = sp.symbols('R1 R2')
        R1x_value = self.beam_calculator.Force_of_reaction_on_X[R1]
        R2x_value = self.beam_calculator.Force_of_reaction_on_X[R2]

        R1z_value = self.beam_calculator.Force_of_reaction_on_Z[R1]
        R2z_value = self.beam_calculator.Force_of_reaction_on_Z[R2]

        self.draw_arrow(150, 120, 150, 120 - R1x_value, color="green")
        self.canvas.create_text(120, 180, text=f"R1x={int(R1x_value)}N")
        self.canvas.create_text(120, 190, text=f"R1z={int(R1z_value)}N")

        self.draw_arrow(-50 + (len(self.beam_calculator.nodes) + 1) * 100, 120, -50 + (len(self.beam_calculator.nodes) + 1)*100, 120 - R2x_value, color="green")
        self.canvas.create_text(-80 + (len(self.beam_calculator.nodes) + 1) * 100, 180, text=f"R2x={int(R2x_value)}N")
        self.canvas.create_text(-80 + (len(self.beam_calculator.nodes) + 1) * 100, 190, text=f"R2z={int(R2z_value)}N")

    def calculate(self):

        self.force_list = []
        self.torque_list = []
        self.moemntum_list = []
        self.distence_list = []
        self.ZForce_list = []
        self.ZDistance_list = []    

        try:
            # Iterate through nodes and draw relevant elements
            for i in range(len(self.beam_calculator.nodes)):
                force_entry = self.force_entries[i]
                torque_entry = self.torque_entries[i]
                distance_entry = self.distance_entries[i]
                momentum_entry = self.momentum_entries[i]
                ZForce_entry = self.ZForce_entries[i]
                ZDistance_entry = self.ZDistance_entries[i]


                force_value = float(force_entry.get())
                torque_value = float(torque_entry.get())
                distance_value = float(distance_entry.get())
                momentum_value = float(momentum_entry.get())
                ZForce_value = float(ZForce_entry.get())
                ZDistance_value = float(ZDistance_entry.get())

                self.beam_calculator.set_force(i, force_value)
                self.beam_calculator.set_moment(i, torque_value)
                self.beam_calculator.set_distance(i, distance_value)
                self.beam_calculator.set_torque(i, momentum_value)
                self.beam_calculator.set_ZForce(i, ZForce_value)
                self.beam_calculator.set_ZDistance(i, ZDistance_value)

                node_x = 50 + (i + 1) * 100
                node_y = 120

                if force_value != 0:
                    self.draw_arrow(node_x, node_y, node_x, node_y - force_value, color="blue")
                    self.canvas.create_text(node_x + 40, node_y - 50, text=f"F={force_value}N")

                if torque_value > 0:
                    self.draw_circle_arrow(node_x, node_y, orientation=True, color="red")
                elif torque_value < 0:
                    self.draw_circle_arrow(node_x, node_y, orientation=False, color="red")

                if torque_value != 0:
                    self.canvas.create_text(node_x + 40, node_y - 40, text=f"M={torque_value}Nm")
                if momentum_value != 0:
                   self.draw_arrow(node_x, node_y, node_x - momentum_value, node_y, color="green")
                   self.draw_arrow(node_x, node_y, node_x - momentum_value*(3/4), node_y, color="green")
                if momentum_value != 0:
                    self.canvas.create_text(node_x + 40, node_y - 30, text=f"T={momentum_value}Nm")

                if i != len(self.beam_calculator.nodes) - 1:
                    self.canvas.create_text(node_x + 50, node_y - 10, text=f"{distance_value}m")

                if i == len(self.beam_calculator.nodes) - 1:
                    # Draw last solid for the last node
                    self.draw_triangle(node_x, 120, color="black")

                if ZForce_value < 0:
                    self.draw_circle(node_x, 80, 5, color="black", fill_circle=False)
                    self.draw_circle(node_x, 80, 1, color="black", fill_circle=False)
                elif ZForce_value > 0:
                    self.draw_circle(node_x, 80, 5, color="black", fill_circle=False)
                    self.draw_cross(node_x, 80, 5, color="black")

                if ZForce_value != 0:
                    self.connect_nodes(node_x, 120, [node_x, 60])
                    self.canvas.create_text(node_x - 20, node_y - 35, text=f"{ZDistance_value}m")
                

                self.force_list.append(force_value)
                self.torque_list.append(torque_value)
                self.moemntum_list.append(momentum_value)
                self.distence_list.append(distance_value)
                self.ZForce_list.append(ZForce_value)
                self.ZDistance_list.append(ZDistance_value)

            # serve a error when some distance is 0
            if any(val == 0 for val in self.distence_list[:-1]):
                self.show_error_message("ERROR: Some distance is 0")
                self.clear_all()


        except ValueError:
            self.show_error_message("ERROR: Values must be numbers")

    def add_node(self):
        node_position = len(self.beam_calculator.nodes) + 1
        self.beam_calculator.add_node(node_position)

        node_x = 50 + node_position * 100
        node_y = 200

        if node_position == 1:
            self.canvas.create_text(node_x, node_y - 30, text=f"Solid", tags="text")
            self.draw_triangle(node_x, 120, color="black")
        else:
            self.canvas.create_text(node_x, node_y - 30, text=f"Node {node_position-1}", tags="text")
            self.draw_circle(node_x, 120, 5, color="black")
            self.connect_nodes(node_x, 120, self.previous_node_position)

        self.previous_node_position = {"x": node_x, "y": 100}

        # Entry fields for force, momentum, torque and distance
        # Force
        force_entry = tk.Entry(self.master, width=10)
        force_entry.place(x=node_x, y=node_y + 20)
        force_entry.insert(0, "0")
        force_label = tk.Label(self.master, text="Force")
        force_label.place(x=node_x, y=node_y)
        self.force_entries.append(force_entry)
        self.force_labels.append(force_label)

        # Momentum
        torque_entry = tk.Entry(self.master, width=10)
        torque_entry.place(x=node_x, y=node_y + 60)
        torque_entry.insert(0, "0")
        torque_label = tk.Label(self.master, text="Torque")
        torque_label.place(x=node_x, y=node_y + 40)
        self.torque_entries.append(torque_entry)
        self.torque_labels.append(torque_label)

        # Distance
        distance_entry = tk.Entry(self.master, width=10)
        distance_entry.place(x=node_x, y=node_y + 100)
        distance_entry.insert(0, "0")
        distance_label = tk.Label(self.master, text="Distance")
        distance_label.place(x=node_x, y=node_y + 80)
        self.distance_entries.append(distance_entry)
        self.distance_labels.append(distance_label)

        # Torque
        momentum_entry = tk.Entry(self.master, width=10)
        momentum_entry.place(x=node_x, y=node_y + 140)
        momentum_entry.insert(0, "0")
        momentum_label = tk.Label(self.master, text="Momentum")
        momentum_label.place(x=node_x, y=node_y + 120)
        self.momentum_entries.append(momentum_entry)
        self.momentum_labels.append(momentum_label)

        # ZForce
        ZForce_entry = tk.Entry(self.master, width=10)
        ZForce_entry.place(x=node_x, y=node_y + 200)
        ZForce_entry.insert(0, "0")
        ZForce_label = tk.Label(self.master, text="ZForce")
        ZForce_label.place(x=node_x, y=node_y + 180)
        self.ZForce_entries.append(ZForce_entry)
        self.ZForce_labels.append(ZForce_label)

        # ZDistance
        ZDistance_entry = tk.Entry(self.master, width=10)
        ZDistance_entry.place(x=node_x, y=node_y + 240)
        ZDistance_entry.insert(0, "0")
        ZDistance_label = tk.Label(self.master, text="ZDistance")
        ZDistance_label.place(x=node_x, y=node_y + 220)
        self.ZDistance_entries.append(ZDistance_entry)
        self.ZDistance_labels.append(ZDistance_label)

    # widow to create graph
    def graph_window(self):
        graph_window = GraphWindow(node=self.beam_calculator.nodes, master=self.master, YForce=self.beam_calculator.YForce, 
                                   ZForce=self.beam_calculator.ZForce, YTorque=self.beam_calculator.YTorque,
                                   Torque=self.beam_calculator.ZTorque_on_ZAxis, ZTorque=self.beam_calculator.ZTorque,
                                   distance=self.distence_list, momentum=self.moemntum_list)
        
    def clear_all(self):
        # Clear canvas and reset data
        self.canvas.delete("all")
        self.force_entries = []
        self.torque_entries = []
        self.distance_entries = []
        self.momentum_entries = []
        self.ZForce_entries = []
        self.ZDistance_entries = []
        self.beam_calculator = BeamCalculator()

        # Destroy entry widgets
        for entry in self.master.winfo_children():
            if isinstance(entry, tk.Entry):
                entry.destroy()
        # Destroy label widgets
        for label in self.force_labels + self.torque_labels + self.distance_labels + self.momentum_labels + self.ZForce_labels + self.ZDistance_labels:
            label.destroy()

    def draw_triangle(self, apex_x, apex_y, color="black", height=20):
        base = 30
        x1 = apex_x - base / 2
        x2 = apex_x + base / 2
        y = apex_y + height
        self.canvas.create_polygon(apex_x, apex_y, x1, y, x2, y, fill=color, outline=color)

    def draw_circle(self, center_x, center_y, radius, color="black", fill_circle=True):
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius

        if fill_circle:
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        else:
            self.canvas.create_oval(x1, y1, x2, y2, outline=color)


    def connect_nodes(self, current_x, current_y, previous_position):
        if isinstance (previous_position, list):
            previous_x, previous_y = previous_position[0], previous_position[1]
        else:
            previous_x = previous_position["x"]
            previous_y = previous_position["y"]

        self.canvas.create_line(previous_x, previous_y + 20, current_x, current_y, fill="black")


    def draw_arrow(self, start_x, start_y, end_x, end_y, color="black"):
        self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill=color)

    def draw_circle_arrow(self, center_x, center_y, orientation, color="black"):
        radius = 15
        start_angle = 90
        end_angle = 270
        self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                start=start_angle, extent=end_angle - start_angle, style=tk.ARC, outline=color)
        if orientation is True:
            self.draw_arrow(center_x - radius, center_y, center_x - radius, center_y - radius, color)
        else:
            self.draw_arrow(center_x - radius, center_y, center_x + radius, center_y + radius, color)

    def draw_cross(self, center_x, center_y, size, color="black"):
        x1 = center_x - size / 2
        y1 = center_y - size / 2
        x2 = center_x + size / 2
        y2 = center_y + size / 2

        # Draw horizontal line
        self.canvas.create_line(x1, center_y, x2, center_y, fill=color)

        # Draw vertical line
        self.canvas.create_line(center_x, y1, center_x, y2, fill=color)


    def show_error_message(self, message):
        error_window = tk.Toplevel(self.master)
        label = tk.Label(error_window, text=message)
        label.pack(padx=20, pady=20)
        close_button = tk.Button(error_window, text="Exit", command=error_window.destroy)
        close_button.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BeamApp(root)
    root.mainloop()