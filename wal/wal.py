"""
import tkinter as tk
import numpy as np


def add_value():
    number = 0
    dic = {}
    distances = []

    while True:
        dic[f"nod {number}"] = {
            "force": None,
            "momentum": None,
            "distance": None
        }

        while True:
            try:
                force = float(input(f"sila wezla {number}: "))
                dic[f"nod {number}"]["force"] = force
                break
            except ValueError:
                print("sila musi byc liczba")
                continue

        while True:
            try:
                momentum = float(input(f"moment wezla {number}: "))
                dic[f"nod {number}"]["momentum"] = momentum
                break
            except ValueError:
                print("moment musi byc liczba")
                continue

        while True:
            if number == 0:
                dic[f"nod {number}"]["distance"] = 0
                break
            else:
                try:
                    distance = float(input(f"distance nod {number}: "))
                    if distance <= 0:
                        print ("distance can not be 0" )
                        continue
                    else:
                        distances.append(distance)
                        dic[f"nod {number}"]["distance"] = sum(distances[:number])
                        break
                except ValueError:
                    print("distance musi byc liczba")
                    continue

        decision = input("Czy zakonczyc? T/N")
        if decision == "T":
            break

        number += 1

    print(dic)

    decision = input("czy jest obciazenie ciagle? T/N")
    if decision == "T":
        while True:
            list_cumulate = []
            first_nod = input("wybierz pkt poczatkowy: (nod {numer})")

            if first_nod not in dic:
                print ("nie ma takiego pkt")
                continue

            last_nod = input("wybierz pkt koncowy: (nod {numer})")

            if last_nod not in dic:
                print ("nie ma takiego pkt")
                continue

            list_cumulate.append(first_nod)
            list_cumulate.append(last_nod)
            list_cumulate = sorted(list_cumulate)

            while True:
                try:
                    value_of_statick_force = float(input("wartosc obciazenia ciaglego: "))
                    break
                except ValueError:
                    print ("musi byc liczba")
                    continue

            lenght = abs(dic[list_cumulate[1]]["distance"] - dic[list_cumulate[0]]["distance"])
            cumulate_force = value_of_statick_force * lenght
            cumulate_distance = dic[list_cumulate[0]]["distance"] + lenght/2

            new_index = (int(first_nod.split()[1]) + int(last_nod.split()[1])) / 2

            dic[f"nod {new_index}"] = {
                "force": cumulate_force,
                "momentum": 0,
                "distance": cumulate_distance
            }
            break
    print (dic)
    return dic



# nie dziala cos w obliczniu reakcji
def force_of_reaction():
    dic = add_value()
    momenty = []
    sily = []
    odleglosc = []
    moment_z_sily = []

    for nod, values in dic.items():
        sily.append(values["force"])
        momenty.append(values["momentum"])
        odleglosc.append(values["distance"])
        moment_z_sily.append(values["force"] * values["distance"])
    R_2 = -((sum(moment_z_sily) + sum(momenty))/odleglosc[-1])
    R_1 = -(sum(sily) + R_2)
    print (f"moment z sily {sum(moment_z_sily)}")
    print (f"sum moment  {sum(momenty)}")
    print (f"sum sily  {sum(sily)}")
    print (odleglosc[-1])
    print (R_1, R_2)

force_of_reaction()
"""

from math import exp
import tkinter as tk

class BeamCalulator():
    def __init__(self):
        self.nodes =[]
        self.supports = []

    def add_node(self, position):
        self.nodes.append({"position": position, "force": 0, "moment": 0})

    def set_force(self, node_index, force):
        self.nodes[node_index]["force"] = force

    def set_moment(self, node_index, moment):
        self.nodes[node_index]["moment"] = moment

    def add_support(self, position, support_type):
        self.supports.append({"position": position, "type": support_type})



class BeamApp:
    def __init__(self, master):
        # ustawienia okna głuwnego 
        self.master = master
        self.master.title("Beam Calculator")
        self.master.geometry("800x500")

        # obszar na ktorymbedzie tworzona wizualizacja belki
        self.canvas = tk.Canvas(self.master, width=800, height=200)
        self.canvas.place(x=0, y=0)

        self.beam_calculator = BeamCalulator()

        self.add_node_button = tk.Button(self.master, text="add nod", command=self.add_node)
        self.add_node_button.place(x=0, y=300)

        #self.calulate_button = tk.Button(self.master, test="calulate",command=pass)


    def add_node(self):
        node_position = len(self.beam_calculator.nodes) + 1
        self.beam_calculator.add_node(node_position)

        node_x = 50 + node_position * 100
        node_y = 200

        if node_position == 1:
            self.canvas.create_text(node_x, node_y - 30, text=f"solid", tags="text")
            self.draw_triangle(node_x, 120, color="black")
        else:
            self.canvas.create_text(node_x, node_y - 30, text=f"nod {node_position-1}", tags="text")
            self.draw_circle(node_x, 120, 5, color="black")
            
            # Połącz poprzedni węzeł z aktualnym
            self.connect_nodes(node_x, 120, self.previous_node_position)

        self.previous_node_position = {"x": node_x, "y": 100}

        # dodawanie sil
        force_entry = tk.Entry(self.master, width=10)
        force_entry.place(x=node_x, y=node_y + 20)
        force_entry.insert(0, "0")
        force_label = tk.Label(self.master, text="Force")
        force_label.place(x=node_x, y=node_y)

        # dodawnaie momentów
        torque_entry = tk.Entry(self.master, width=10)
        torque_entry.place(x=node_x, y=node_y + 60)
        torque_entry.insert(0, "0")
        torque_label = tk.Label(self.master, text="Torque")
        torque_label.place(x=node_x, y=node_y + 40)

        # dodawanie miedzy wezlami
        distance_entry = tk.Entry(self.master, width=10)
        distance_entry.place(x=node_x, y=node_y + 100)
        distance_entry.insert(0, "0")
        distance_label = tk.Label(self.master, text="distance")
        distance_label.place(x=node_x, y=node_y + 80)

        def set_force():
            self.beam_calculator.set_force(node_position - 1, float(force_entry.get()))
            try:
                if float(force_entry.get()) > 0:
                    self.draw_arrow(node_x, node_y, node_x, node_y - 30, color="blue")
                elif float(force_entry.get()) < 0:
                    self.draw_arrow(node_x, node_y, node_x, node_y + 30, color="blue")
                else:
                    pass
            except:
                error_window = tk.Toplevel(self.master)
                error_text = "ERROR warosci muszą byc liczbami"
                label = tk.Label(error_window, text=error_text)
                label.pack(padx=20, pady=20)

        def set_torque():
            self.beam_calculator.set_moment(node_position - 1, float(torque_entry.get()))
            try:
                if float(torque_entry.get()) > 0:
                    self.draw_circle_arrow(node_x, node_y, orientation=True, color="red")
                elif float(torque_entry.get()) < 0:
                    self.draw_circle_arrow(node_x, node_y, orientation=True, color="red")
            except ValueError:
                error_window = tk.Toplevel(self.master)
                error_text = "ERROR warosci muszą byc liczbami"
                label = tk.Label(error_window, text=error_text)
                label.pack(padx=20, pady=20)

    def draw_triangle(self, apex_x, apex_y, color="black"):
        height = 20
        base = 30
        x1 = apex_x - base / 2
        x2 = apex_x + base / 2
        y = apex_y + height
        self.canvas.create_polygon(apex_x, apex_y, x1, y, x2, y, fill=color, outline=color)

    def draw_circle(self, center_x, center_y, radius, color="black"):
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def connect_nodes(self, current_x, current_y, previous_position):
        # Współrzędne poprzedniego węzła
        previous_x = previous_position["x"]
        previous_y = previous_position["y"]

        # Rysuj linie łączące trójkąt z poprzednim węzłem
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

if __name__ == "__main__":
    root = tk.Tk()
    app = BeamApp(root)
    root.mainloop()
