import tkinter as tk
from threading import Thread


class ControlPanelUI:

    def __init__(self, drone, drone_sweep):
        self.drone = drone
        self.drone_sweep = drone_sweep

        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)

        self.informationFrame = tk.Frame(self.root, padx=5, pady=20)
        self.informationFrame.pack()
        self.currentX = tk.Label(self.informationFrame, text="Current X : " + str(self.drone.x))
        self.currentX.pack()
        self.currentY = tk.Label(self.informationFrame, text="Current Y : " + str(self.drone.y))
        self.currentY.pack()
        self.currentDirection = tk.Label(self.informationFrame, text="Current direction : " + str(self.drone.angle))
        self.currentDirection.pack()
        self.moveDistance = tk.Label(self.informationFrame, text="Distance to move : " + str(self.drone.distance))
        self.moveDistance.pack()
        self.rotateDegree = tk.Label(self.informationFrame, text="Degree to turn : " + str(self.drone.rotateAngle))
        self.rotateDegree.pack()
        self.manualMode = tk.Label(self.informationFrame, text="Manual mode : " + str(self.drone.manual))
        self.manualMode.pack()
        self.currentRoute = tk.Label(self.informationFrame, text="Current Route : " + str(self.drone_sweep.route_name))
        self.currentRoute.pack()

        self.setFrame = tk.Frame(self.root)
        self.setFrame.pack()
        self.setDistance = tk.Label(self.setFrame, text="Set Distance : ").grid(row=0, column=0, sticky=tk.E)
        self.distance20 = tk.Button(self.setFrame, text=" 20 ", command=lambda: self.drone.set_distance(20)).grid(row=0, column=1, sticky=tk.S, padx=5)
        self.distance50 = tk.Button(self.setFrame, text=" 50 ", command=lambda: self.drone.set_distance(50)).grid(row=0, column=2, sticky=tk.S, padx=5)
        self.distance70 = tk.Button(self.setFrame, text=" 70 ", command=lambda: self.drone.set_distance(70)).grid(row=0, column=3, sticky=tk.S, padx=5)
        self.distance100 = tk.Button(self.setFrame, text=" 100 ", command=lambda: self.drone.set_distance(100)).grid(row=0, column=4, sticky=tk.S, padx=5)

        self.setDegree = tk.Label(self.setFrame, text="Set Degree : ").grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        self.degree15 = tk.Button(self.setFrame, text=" 15 ", command=lambda: self.drone.set_degree(15)).grid(row=1, column=1, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree30 = tk.Button(self.setFrame, text=" 30 ", command=lambda: self.drone.set_degree(30)).grid(row=1, column=2, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree60 = tk.Button(self.setFrame, text=" 60 ", command=lambda: self.drone.set_degree(60)).grid(row=1, column=3, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree90 = tk.Button(self.setFrame, text=" 90 ", command=lambda: self.drone.set_degree(90)).grid(row=1, column=4, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree180 = tk.Button(self.setFrame, text=" 180 ", command=lambda: self.drone.set_degree(180)).grid(row=1, column=5, sticky=tk.S, padx=5, pady=(5, 0))

        self.setRoute = tk.Label(self.setFrame, text="Set Route : ").grid(row=2, column=0, sticky=tk.E, pady=(5, 0))
        self.route1 = tk.Button(self.setFrame, text="Polygon Route", command=lambda: self.drone_sweep.set_route(1)).grid(row=2, column=1, columnspan=2, sticky=tk.S, padx=5, pady=(5, 0))
        self.route2 = tk.Button(self.setFrame, text="Triangle Route", command=lambda: self.drone_sweep.set_route(2)).grid(row=2, column=3, columnspan=2, sticky=tk.S, padx=5, pady=(5, 0))

        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.pack()
        self.moveForward = tk.Button(self.buttonFrame, text='Move Forward', fg="red", command=self.drone.move_forward).grid(row=0, column=0, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveBackward = tk.Button(self.buttonFrame, text='Move Backward', fg="red", command=self.drone.move_backward).grid(row=0, column=1, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveLeft = tk.Button(self.buttonFrame, text='Move Left', fg="red", command=self.drone.move_left).grid(row=0, column=2, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveRight = tk.Button(self.buttonFrame, text='Move Right', fg="red", command=self.drone.move_right).grid(row=0, column=3, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveUp = tk.Button(self.buttonFrame, text='Move Up', fg="red", command=self.drone.move_up).grid(row=0, column=4, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveDown = tk.Button(self.buttonFrame, text='Move Down', fg="red", command=self.drone.move_down).grid(row=0, column=5, sticky=tk.W, padx=5, pady=(20, 5))
        self.rotateClockwise = tk.Button(self.buttonFrame, text='Rotate Clockwise', fg="red", command=self.drone.rotate_cw).grid(row=1, column=0, pady=5, padx=5)
        self.rotateCounterclockwise = tk.Button(self.buttonFrame, text='Rotate Counter-clockwise', fg="red", command=self.drone.rotate_ccw).grid(row=1, column=1, columnspan=2, pady=5)
        self.perimeterSweep = tk.Button(self.buttonFrame, text='Pre-plan Route Sweep', fg="red", command=lambda: Thread(target=self.drone_sweep.perform_sweep).start()).grid(row=1, column=3, columnspan=2, pady=5, padx=5)
        self.takeOff = tk.Button(self.buttonFrame, text='Take off', fg='red', command=self.drone.takeoff).grid(row=2, column=0, padx=5, pady=5)
        self.land = tk.Button(self.buttonFrame, text='Land', fg='red', command=self.drone.land).grid(row=2, column=1, padx=5, pady=5)
        self.stop = tk.Button(self.buttonFrame, text='Stop', fg='red', command=self.drone.stop).grid(row=2, column=2, padx=5, pady=5)
        self.backToBase = tk.Button(self.buttonFrame, text='Back To Base', fg='red', command=self.drone.back_base).grid(row=2, column=3, padx=5, pady=5)
        # frame for video// to do
        # videoFrame = tk.Frame(root)
        # bottomFrame.pack(side=tk.BOTTOM)

        # reload ui
        self.reload()

    def reload(self):
        self.currentX.configure(text="Current X : " + str(self.drone.x))
        self.currentY.configure(text="Current Y : " + str(self.drone.y))
        self.currentDirection.configure(text="Current direction : " + str(self.drone.angle))
        self.moveDistance.configure(text="Distance to move : " + str(self.drone.distance))
        self.rotateDegree.configure(text="Degree to turn : " + str(self.drone.rotateAngle))
        self.manualMode.configure(text="Manual mode : " + str(self.drone.manual))
        self.currentRoute.configure(text="Current route : " + str(self.drone_sweep.route_name))
        self.informationFrame.after(500, self.reload)

    def start_ui(self):
        self.root.mainloop()
