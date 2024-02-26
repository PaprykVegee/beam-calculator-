import tkinter as tk
from tkinter import messagebox
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BearingsDesigner import BearingsDesigner

class BeamDesign:
    def __init__(self,node,  master, distance, torque, reduce_torque, bending_torque, Zforce, Xforce):
        # Initialize instance variables
        self.node = node
        self.master = master
        self.distance = [val*1000 for val in distance]
        self.torque = torque
        self.reduce_torque = reduce_torque
        self.bending_torque = bending_torque
        self.Zforce = Zforce
        self.Xforce = Xforce

        # Create a new Top Level window
        self.frame = tk.Toplevel(self.master)
        self.frame.geometry(("800x500"))

        # Available materials for dropdown
        self.materials = ["St235", "St275", "St355", "42CrMo4", "C45", "Custom Steel"]

        # Dropdown for steel material selection
        self.material_var = tk.StringVar()
        self.material_var.set(self.materials[0])
        self.material_dropdown = tk.OptionMenu(self.frame, self.material_var, *self.materials, command=self.material_changed)
        self.material_dropdown.place(x=10, y=10)

        # Label informing about Rm value
        self.rm_label = tk.Label(self.frame, text="Enter Rm value:")

        # Entry to add custom steel Rm value
        self.rm_entry = tk.Entry(self.frame)

        # Button to generate graphs
        self.generate_button = tk.Button(self.frame, text='Generate 3D Graph', command=self.generate_3d_graph)
        self.generate_button.place(x=10, y=80)

        # Exit Button
        self.Exit_button = tk.Button(self.frame, text='Exit', command=lambda: self.frame.destroy())
        self.Exit_button.place(x=150, y=80)

        # Button for BearingsDesigner
        self.BearingsDesigner_button = tk.Button(self.frame, text="Bearings Designer", command=lambda: self.Bearing_window())
        self.BearingsDesigner_button.place(x=200, y=80)

        # Dictionary for steel material and Rm value
        self.dic_of_steel = {"St235": 420, "St275": 450, "St355": 550, "42CrMo4": 570, "C45": 570}

    def Bearing_window(self):
        try:
            Bearings_Designer = BearingsDesigner(master=self.frame, forceX=self.Xforce, forceZ=self.Zforce, diameter_list=self.max_val, X_list=self.sublist_of_X)
        except AttributeError:
            messagebox.showerror("Error", "First create model.")


    def material_changed(self, *args):
        # Function to handle material selection change in dropdown
        selected_material = self.material_var.get()

        # Show or hide Entry depending on selected material
        if selected_material == "Custom Steel":
            self.rm_entry.place(x=100, y=45)
            self.rm_label.place(x=10, y=45)
        else:
            self.rm_entry.place_forget()
            self.rm_label.place_forget()

    def linear_function(self, x, y, step=300):
        # Function to perform linear interpolation
        # Collect x values with given step
        x_collected = np.arange(min(x), max(x) + step, step)
        # Interpolate y values for collected x values
        y_collected = np.interp(x_collected, x, y)

        return x_collected, y_collected

    def creating_sublist(self):
        # Function to create sublists based on torque values
        # Initialization of sublist
        sublist = [[] for _ in range(len(self.torque))]
    
        j = 0
        i = 0
        while i < len(self.torque):
            while self.torque[i] != 0:
                sublist[j].append(self.distance[i])
                i += 1
                if i == len(self.torque):
                    break
            j += 1
            i += 1
        
        # Remove empty sublists
        sublist = [val for val in sublist if val]
        # Create residual_list
        residual_list = []
        current_sublist = []
    
        for item in self.distance:
            if any(item in sub for sub in sublist):
                if current_sublist:
                    residual_list.append(current_sublist)
                    current_sublist = []
            else:
                current_sublist.append(item)
    
        if current_sublist:
            residual_list.append(current_sublist)
        
        residual_list_copy = residual_list

        index = []
        for idx, value in enumerate(residual_list_copy):
            for val in value:
                index.append(self.distance.index(val))
            min_in = min(index)
            max_in = max(index)
            try:
                residual_list[idx].append(self.distance[max_in+1])
            
                if min_in != 0:
                    residual_list[idx].insert(self.distance[min_in-1])
            except IndexError:
                residual_list = residual_list_copy
            index = []

        return sublist, residual_list


    def calcualte_diameter(self, Rm, p_zgo=0.4, p_zsj=0.5, xzg=3.5, xzs=3):
        # Function to calculate diameter based on material properties and torque
        # Calculate number of teeth for gears
        Zgo = p_zgo * Rm
        Zsj = p_zsj * Rm

        #print(f"Zgo {Zgo}")
        #print(f"Zsj {Zsj}")


        # Calculate gear ratios
        kgo = Zgo / xzg
        kjs = Zsj / xzs

        #print(f"Zsj {kgo}")
        #print(f"kjs {kjs}")

        """
        for disc in self.distance:
            if disc <= 0.05:
                step = 0.001
            else:
                step = 0.01
        """

        xy_values = []

        # Create sublist based on torque values
        SubDistance_torque, SubDistance_bending_torque = self.creating_sublist()
        for sub in SubDistance_torque:
            start_index = self.distance.index(sub[0])  # Initial index
            end_index = self.distance.index(sub[-1]) + 1  # Final index (+1 to include the last element)

            # Slice self.reduce_torque
            reduce_torque_sublist = self.reduce_torque[start_index:end_index]

            # Calculate linear function values
            x, y = self.linear_function(sub, reduce_torque_sublist, step = 30)
            # Calculate diameter values based on torque and drive transmission coefficients
            d_list = [pow((16 * y_value) / (np.pi * kjs*10**6), 1 / 3)*1000 for y_value in y]



            xy_values.extend(zip(x, d_list))

        for sub in SubDistance_bending_torque:
            start_index = self.distance.index(sub[0])  # Initial index
            end_index = self.distance.index(sub[-1]) + 1  # Final index (+1 to include the last element)

            # Slice self.bending_torque
            bending_torque_sublist = self.bending_torque[start_index:end_index]

            # Calculate linear function values
            x, y = self.linear_function(sub, bending_torque_sublist, step = 30)
            # Calculate diameter values based on torque and drive transmission coefficients
            d_list = [pow((32 * y_value) / (np.pi * kgo*10**6), 1 / 3)*1000 for y_value in y]
            xy_values.extend(zip(x, d_list))


        # Sort the xy values based on x values
        sorted_xy_values = sorted(xy_values, key=lambda tup: tup[0])
        sorted_x_values, sorted_d_values = zip(*sorted_xy_values)

        return sorted_x_values, sorted_d_values
    
    # Function because we use this more than once
    def get_Rm_val(self):
        # Function to get the Rm value based on material selection
        selected_material = self.material_var.get()

        if selected_material == "Custom Steel":
            self.Rm = self.rm_entry.get()
            if not self.Rm or not self.Rm.isnumeric():  # Check if Rm is entered and numeric
                messagebox.showerror("Error", "Please enter a valid value for Custom Steel Rm.")
                return
        else:
            self.Rm = self.dic_of_steel[selected_material]



    def generate_3d_graph(self, point = 20):
        # Function to generate 3D graph
        self.get_Rm_val()  # Get Rm value

        # Calculate diameter values
        x_values, self.d_values = self.calcualte_diameter(float(self.Rm))

        # Create a common figure for both subplots
        fig = plt.figure(figsize=(12, 5))

        # First subplot
        ax1 = fig.add_subplot(121, projection='3d')  
        for d, x in zip(self.d_values, x_values):
            # Create ring
            theta = np.linspace(0, 2*np.pi, point)
            y_circle = d / 2 * np.cos(theta)
            z_circle = d / 2 * np.sin(theta)
        
            # Define a grid
            X, Theta = np.meshgrid(x, theta)
            Y = np.tile(y_circle, (len(y_circle), 1))
            Z = np.tile(z_circle, (len(z_circle), 1))

            ax1.plot_wireframe(X, Y, Z)  # Plot on first subplot

        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Cigar chart')
        ax1.grid(False)


        # Second subplot
        ax2 = fig.add_subplot(122, projection='3d')  

        # Increase diameters for visualization
        d_values = [x * 1.1 for x in self.d_values]

        # Calculate sublist sizes
        size_sublist = len(x_values) // len(self.node) 

        self.sublist_of_X = [x_values[i:i + size_sublist + 1] for i in range(0, len(x_values), size_sublist - 1)]
        sublist_of_D = [self.d_values[i:i + size_sublist + 1] for i in range(0, len(self.d_values), size_sublist)]

        self.max_val = [max(sub) for sub in sublist_of_D]
        max_value = max(self.max_val)
        max_idx = self.max_val.index(max_value)

        # Cheak that diamiter fulfill D[i]/D[i+1] <= 1.2
        for i in range(len(self.max_val)):
            if not max_idx - i -1 < 0:
                if self.max_val[max_idx - i]/self.max_val[max_idx - i -1] <= 1.2:
                    continue
                else:
                    self.max_val[max_idx - i-1] = round(self.max_val[max_idx - i]/1.2, 2)

            if not max_idx + i + 1 >= len(self.max_val):
                if self.max_val[max_idx + i]/self.max_val[max_idx +i + 1] <= 1.2:
                    continue
                else:
                    self.max_val[max_idx + i + 1] = round(self.max_val[max_idx + i]/1.2, 2)


        for idx, d in enumerate(self.max_val):
            theta = np.linspace(0, 2*np.pi, point)
            r = d / 2
            x = self.sublist_of_X[idx]
            x_extended = np.linspace(x[0], x[-1], len(x))
            theta_2d, x_2d = np.meshgrid(theta, x_extended)
            y = r * np.cos(theta_2d)
            z = r * np.sin(theta_2d)
            ax2.plot_surface(x_2d, y, z, color='Red')


        ax2.set_xlabel('X [m]')
        ax2.set_ylabel('Y [mm]')
        ax2.set_zlabel('Z [mm]')
        ax2.set_title('Smoothed Rings')
        ax2.grid(False)

        """
        # Set the same range for both subplots
        max_range = np.array([max(x_values) - min(x_values), max(self.d_values) - min(self.d_values), max(self.d_values) - min(self.d_values)]).max() / 2.0
        mid_x = (max(x_values) + min(x_values)) * 0.5
        mid_y = (max(self.d_values) + min(self.d_values)) * 0.5
        mid_z = (max(self.d_values) + min(self.d_values)) * 0.5
        ax1.set_xlim(mid_x - max_range, mid_x + max_range)
        ax1.set_ylim(mid_y - max_range, mid_y + max_range)
        ax1.set_zlim(mid_z - max_range, mid_z + max_range)

        ax2.set_xlim(mid_x - max_range, mid_x + max_range)
        ax2.set_ylim(mid_y - max_range, mid_y + max_range)
        ax2.set_zlim(mid_z - max_range, mid_z + max_range)

        # Create sublist of bearings optimization after generating the plots
        self.sublist_of_optimization, self.sublist_of_bearing = self.creating_sublist()
        """

        # Create Tkinter canvas and display it
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        #self.frame.config(bg=('white'))
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=10, y=150)  # Adjust the column position for the second subplot
        canvas_widget.config(bg="gray")
