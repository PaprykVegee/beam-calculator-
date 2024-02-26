import math
import string
import numpy as np
import tkinter as tk
from tkinter import Canvas, messagebox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import groupby


class BearingsDesigner:
    def __init__(self, master, forceX, forceZ, diameter_list, X_list):
        # Initialize the class with necessary parameters
        self.master = master
        self.force = max([math.sqrt(forceX[0]**2 + forceZ[0]**2), math.sqrt(forceX[-1]**2 + forceZ[-1]**2)]) 
        diameter = max([diameter_list[0], diameter_list[-1]])

        # Convert diameter_list to a list
        self.diameter_list = list(diameter_list)

        # Assign values to the first and last elements of diameter_list
        self.diameter_list[0] = diameter
        self.diameter_list[-1] = diameter

        self.X_list = X_list

        self.master.title("Bearings Designer")

        # Create a new window (Toplevel) for the application
        self.frame = tk.Toplevel(self.master)
        self.frame.geometry(("800x500"))

        # Add labels and entry fields for user input
        service_life_label = tk.Label(self.frame, text="Service Life (h):")
        service_life_label.place(x=30, y=30)
        self.service_life_entry = tk.Entry(self.frame)
        self.service_life_entry.place(x=180, y=30)

        temperature_label = tk.Label(self.frame, text="Temperature of Work (°C):")
        temperature_label.place(x=30, y=60)
        self.temperature_entry = tk.Entry(self.frame)
        self.temperature_entry.place(x=180, y=60)

        rotation_speed_label = tk.Label(self.frame, text="Rotation Speed (rot/min):")
        rotation_speed_label.place(x=30, y=90)
        self.rotation_speed_entry = tk.Entry(self.frame)
        self.rotation_speed_entry.place(x=180, y=90)

        # Dropdown menu for selecting type of bearing
        self.type_of_bearing = ["Ball Bearings", "Roller Bearings", "Needle Bearings"]
        self.Bearing_var = tk.StringVar()
        self.Bearing_var.set("set type of bearing")
        self.Bearing_var.trace("w", self.update_canvas)
        self.Bearing_dropdown = tk.OptionMenu(self.frame, self.Bearing_var, *self.type_of_bearing)
        self.Bearing_dropdown.place(x=180, y=120)

        # Buttons for calculation and exiting the application
        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calulate)
        self.calculate_button.place(x=180, y=150)

        self.Exit_button = tk.Button(self.frame, text="Exit", command=self.frame.destroy)
        self.Exit_button.place(x=30, y=150)

        self.Display_Graph_button = tk.Button(self.frame, text="Disaply Graph with bearings", command=self.Draw)
        self.Display_Graph_button.place(x=350, y=30)

        # Canvas for displaying the 3D plot
        #self.canvas = tk.Canvas(self.frame, width=800, height=400)
        #self.canvas.configure(bg=self.frame.cget('bg'))
        #self.canvas.place(x=600, y=400)


    # Method to update canvas based on dropdown selection
    def update_canvas(self, *args):
        self.draw_looks_of_bearings()


    def open_file(self, file_path):
        rdy_file = []
        with open(file_path, 'r') as file:
            value = None  # Inicjalizacja wartości
            for idx, row in enumerate(file):
                column = row.strip().split(',')
                if idx == 0:
                    column_lower = [item.strip() for item in column]
                    column = column_lower
                if idx != 0:
                    if column[0].strip() != "":
                        value = column[0]  # Aktualizacja wartości tylko jeśli pierwsza kolumna nie jest pusta
                    else:
                        column[0] = value  # Ustawienie wartości na poprzednią, jeśli pierwsza kolumna jest pusta
                rdy_file.append(column)

        # Grupowanie danych na podstawie wartości 'd'
        grouped_data = [list(group) for key, group in groupby(rdy_file, key=lambda x: x[0])]

        return grouped_data


    def selector(self, lists, val,  val_idx):
        closest_row = None
        closest_difference = float('inf')

        for idx, row in enumerate(lists):
            difference = float(row[val_idx]) - val
            if difference > 0 and abs(difference) < closest_difference:
                closest_difference = abs(difference)
                closest_row = row

        if closest_row:
            return closest_row
        else:
            return None

    # Method to calculate and draw bearing
    def calulate(self):
        if not self.temperature_entry.get() or not self.service_life_entry.get() or not self.rotation_speed_entry.get():
            if not self.temperature_entry.get().isdigit() or self.service_life_entry.get().isdigit() or self.rotation_speed_entry.get().isdigit():
                messagebox.showerror("Error", "Please enter values for all fields.")
                return

        # Get user inputs
        service_life = float(self.service_life_entry.get())
        temperature = float(self.temperature_entry.get())
        rotation_speed = float(self.rotation_speed_entry.get())

        # Calculate some parameters based on user inputs
        fn = pow(33.333/temperature, (1/3))
        fh = pow(temperature, (1/3))
        if temperature < 150:
            ft = 1

        C = self.force*(fh/(fn*ft)) * 0.001
        C_idx = 3

        D = self.diameter_list[0]
        D_idx = 0

        if self.Bearing_var.get() == "Ball Bearings":
            file_path = r"C:\Users\patry\source\repos\wal\wal\LozyskaKulkowe.txt"

        elif self.Bearing_var.get() == "Roller Bearings":
            file_path = r"C:\Users\patry\source\repos\wal\wal\LozyskaKulkowe.txt"

        elif self.Bearing_var.get() == "Needle Bearings":
            file_path = r"C:\Users\patry\source\repos\wal\wal\LozyskaKulkowe.txt"

        else:
            messagebox.showerror("Error", "Please choose type of bearing")
            return

        grouped_data = self.open_file(file_path)[1:]

        self.d = self.selector([val for sub in grouped_data if (val := self.selector(sub, C, C_idx)) is not None], D, D_idx)
        print(f"D: {D}")
        print(f"C: {C}")
        print(self.d)



    def Draw(self):

        # Create new figure and subplot for the second plot
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')

        # Plot second plot
        for idx, d in enumerate(self.diameter_list):
            theta = np.linspace(0, 2*np.pi, 20)
            r = d / 2
            x = self.X_list[idx]
            x_extended = np.linspace(x[0], x[-1], len(x))
            theta_2d, x_2d = np.meshgrid(theta, x_extended)
            y = r * np.cos(theta_2d)
            z = r * np.sin(theta_2d)
            ax2.plot_surface(x_2d, y, z, color='Red')
            


        # Clear the previous plot on canvas
        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.frame)
        self.canvas2_widget = self.canvas2.get_tk_widget()

        # Powiększenie okna Canvas dwukrotnie
        self.canvas2_widget.config(width=2*self.canvas2_widget.winfo_reqwidth(), 
                                    height=2*self.canvas2_widget.winfo_reqheight())

        # Display the second 3D plot in the tkinter window
        canvas_widget2 = self.canvas2.get_tk_widget()
        canvas_widget2.place(x=600, y=230)

        try:
            if self.d is None:
                messagebox.showerror("Error", "Imposible to find bearings !")
                return
            d = float(self.d[0])
            D = float(self.d[1])
            B = float(self.d[2])
            d0 = float(self.d[4])
            D0 = float(self.d[5])     
            R = 2/3*B
        except AttributeError:
            messagebox.showerror("Error", "Please firstly add valu to calulate")
            return

        number = math.ceil(np.pi * (d+R)/(2*R))
        for b in [B, self.X_list[-1][-1] - B]:
            for point in self.circle_trajectory(d=(D + d)/2, num_points=number):

                if self.Bearing_var.get() == "Ball Bearings":
                    self.draw_sphere(ax2, point[0] , point[1], point[2] + b, R, point, 10, color='blue')

                if self.Bearing_var.get() == "Roller Bearings":
                    self.draw_roller(ax2, point[0], point[1], point[2] + b, R, 1, point, 10, color='blue')

                if self.Bearing_var.get() == "Needle Bearings":
                    self.draw_roller(ax2, point[0], point[1], point[2] + b, R, 1, point, 10, color='blue')
                
                for dim in [d, d0, D0, D]:
                    x, y, z = self.create_ring_mesh(D=dim, H=B, z0=b,  num_segments=15, num_rings=3)
                    ax2.plot_surface(x, y, z, color='gray')

            ax2.set_box_aspect([(self.X_list[-1][-1])/(4*R), 1, 1])
            self.canvas2.draw()


    # Function to create mesh for a ring
    def create_ring_mesh(self, D, H=1, x0=0, y0=0, z0=0, num_segments=20, num_rings=20):
        theta = np.linspace(0, 2*np.pi, num_segments)
        z = z0 + np.linspace(-H/2, H/2, num_rings)
        theta, z = np.meshgrid(theta, z)
        x = x0 + (D / 2) * np.cos(theta)
        y = y0 + (D / 2) * np.sin(theta)
        return z, y, x

    # Function to create trajectory for a circle
    def circle_trajectory(self, d, num_points):
        radius = d / 2
        theta = np.linspace(0, 2 * np.pi, num_points + 1)[:-1]
        x_traj = radius * np.cos(theta)
        y_traj = radius * np.sin(theta)
        z_traj = np.zeros_like(x_traj)
        points = np.column_stack([x_traj, y_traj, z_traj])
        return points

    # Function to draw a sphere
    def draw_sphere(self, ax, x, y, z, d, point, mes_point=10, color='red'):
        u = np.linspace(0, 2 * np.pi, mes_point)
        v = np.linspace(0, np.pi, mes_point)
        x_sphere = x + (d / 2) * np.outer(np.cos(u), np.sin(v))
        y_sphere = y + (d / 2) * np.outer(np.sin(u), np.sin(v))
        z_sphere = z + (d / 2) * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(z_sphere, y_sphere, x_sphere, color=color)


    # Function to draw a roller
    def draw_roller(self, ax, x, y, z, d, h, point, mes_point=10, color='red'):
        u = np.linspace(0, 2 * np.pi, mes_point)
        v = np.linspace(-1, h, mes_point)
        x_roller = x + (d / 2) * np.outer(np.cos(u), np.ones(np.size(v)))
        y_roller = y + (d / 2) * np.outer(np.sin(u), np.ones(np.size(v)))
        z_roller = z + np.outer(np.ones(np.size(u)), v)
        ax.plot_surface(z_roller, y_roller, x_roller, color=color)

    def draw_looks_of_bearings(self, mes_point=10, ball_diameter=2, roller_diameter=2, needle_diameter=1, cage_diameter=2):
        # Define parameters for drawing
        mes_point = int(mes_point)
        D1 = 10 
        D2 = D1 + 2 * cage_diameter
        number = math.floor(np.pi * D2 / cage_diameter)

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Turn off axis and grid
        ax.set_axis_off()
        ax.grid(False)

        # Draw rings
        for D in [D1 - 1.5, D1, D2, D2 + 1.5]:
            x, y, z = self.create_ring_mesh(D = D)
            ax.plot_surface(x, y, z, color='gray')
    
        # Draw bearing elements
        for point in self.circle_trajectory(D2 - cage_diameter, number):
            if self.Bearing_var.get() == "Ball Bearings":
                self.draw_sphere(ax, point[0], point[1], point[2], ball_diameter, point, mes_point)

            if self.Bearing_var.get() == "Roller Bearings":
                self.draw_roller(ax, point[0], point[1], point[2], roller_diameter, 1, point, mes_point)

            if self.Bearing_var.get() == "Needle Bearings":
                self.draw_roller(ax, point[0], point[1], point[2], needle_diameter, 1, point, mes_point)

        # Display the 3D plot in the tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.place(x=30, y=230)
        ax.set_box_aspect([1/8, 1, 1])

        self.canvas.draw()



