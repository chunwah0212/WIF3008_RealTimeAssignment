import pynput
import math
import tello
import Sweep
import tkinter as tk

if __name__ == '__main__':
    drone = tello.Tello()
    drone_sweep = Sweep.Sweep(drone)

    root = tk.Tk()
    root.resizable(width=False, height=False)

    informationFrame = tk.Frame(root, padx=5, pady=20)
    informationFrame.pack()
    currentX = tk.Label(informationFrame, text="Current X : " + str(drone.x))
    currentX.pack()
    currentY = tk.Label(informationFrame, text="Current Y : " + str(drone.y))
    currentY.pack()
    currentDirection = tk.Label(informationFrame, text="Current direction : " + str(drone.angle))
    currentDirection.pack()
    moveDistance = tk.Label(informationFrame, text="Distance to move : " + str(drone.distance))
    moveDistance.pack()
    rotateDegree = tk.Label(informationFrame, text="Degree to turn : " + str(drone.rotateAngle))
    rotateDegree.pack()
    manualMode = tk.Label(informationFrame, text="Manual mode : " + str(drone.manual))
    manualMode.pack()
    currentRoute = tk.Label(informationFrame, text="Current Route : ")
    currentRoute.pack()

    setFrame = tk.Frame(root)
    setFrame.pack()
    setDistance = tk.Label(setFrame, text="Set Distance : ").grid(row=0, column=0, sticky=tk.E)
    distance20 = tk.Button(setFrame, text=" 20 ", command=lambda: drone.set_distance(20)).grid(row=0, column=1, sticky=tk.S, padx=5)
    distance50 = tk.Button(setFrame, text=" 50 ", command=lambda: drone.set_distance(50)).grid(row=0, column=2, sticky=tk.S, padx=5)
    distance70 = tk.Button(setFrame, text=" 70 ", command=lambda: drone.set_distance(70)).grid(row=0, column=3, sticky=tk.S, padx=5)
    distance100 = tk.Button(setFrame, text=" 100 ", command=lambda: drone.set_distance(100)).grid(row=0, column=4, sticky=tk.S, padx=5)

    setDegree = tk.Label(setFrame, text="Set Degree : ").grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
    degree15 = tk.Button(setFrame, text=" 15 ", command=lambda: drone.set_degree(15)).grid(row=1, column=1, sticky=tk.S, padx=5, pady=(5, 0))
    degree30 = tk.Button(setFrame, text=" 30 ", command=lambda: drone.set_degree(30)).grid(row=1, column=2, sticky=tk.S, padx=5, pady=(5, 0))
    degree60 = tk.Button(setFrame, text=" 60 ", command=lambda: drone.set_degree(60)).grid(row=1, column=3, sticky=tk.S, padx=5, pady=(5, 0))
    degree90 = tk.Button(setFrame, text=" 90 ", command=lambda: drone.set_degree(90)).grid(row=1, column=4, sticky=tk.S, padx=5, pady=(5, 0))
    degree180 = tk.Button(setFrame, text=" 180 ", command=lambda: drone.set_degree(180)).grid(row=1, column=5, sticky=tk.S, padx=5, pady=(5, 0))

    setRoute = tk.Label(setFrame, text="Set Route : ").grid(row=2, column=0, sticky=tk.E, pady=(5, 0))
    route1 = tk.Button(setFrame, text="Polygon Route", command=lambda: drone_sweep.set_route(1)).grid(row=2, column=1, columnspan=2, sticky=tk.S, padx=5, pady=(5, 0))
    route2 = tk.Button(setFrame, text="Triangle Route", command=lambda: drone_sweep.set_route(2)).grid(row=2, column=3, columnspan=2, sticky=tk.S, padx=5, pady=(5, 0))

    buttonFrame = tk.Frame(root)
    buttonFrame.pack()
    moveForward = tk.Button(buttonFrame, text='Move Forward', fg="red", command=drone.move_forward).grid(row=0, column=0, sticky=tk.W, padx=5, pady=(20, 5))
    moveBackward = tk.Button(buttonFrame, text='Move Backward', fg="red", command=drone.move_backward).grid(row=0, column=1, sticky=tk.W, padx=5, pady=(20, 5))
    moveLeft = tk.Button(buttonFrame, text='Move Left', fg="red", command=drone.move_left).grid(row=0, column=2, sticky=tk.W, padx=5, pady=(20, 5))
    moveRight = tk.Button(buttonFrame, text='Move Right', fg="red", command=drone.move_right).grid(row=0, column=3, sticky=tk.W, padx=5, pady=(20, 5))
    moveUp = tk.Button(buttonFrame, text='Move Up', fg="red", command=drone.move_up).grid(row=0, column=4, sticky=tk.W, padx=5, pady=(20, 5))
    moveDown = tk.Button(buttonFrame, text='Move Down', fg="red", command=drone.move_down).grid(row=0, column=5, sticky=tk.W, padx=5, pady=(20, 5))
    rotateClockwise = tk.Button(buttonFrame, text='Rotate Clockwise', fg="red", command=drone.rotate_cw).grid(row=1, column=0, pady=5, padx=5)
    rotateCounterclockwise = tk.Button(buttonFrame, text='Rotate Counter-clockwise', fg="red", command=drone.rotate_ccw).grid(row=1, column=1, columnspan=2, pady=5)
    perimeterSweep = tk.Button(buttonFrame, text='Pre-plan Route Sweep', fg="red", command=drone_sweep.perform_sweep).grid(row=1, column=3, columnspan=2, pady=5, padx=5)
    takeOff = tk.Button(buttonFrame, text='Take off', fg='red', command=drone.takeoff).grid(row=2, column=0, padx=5, pady=5)
    land = tk.Button(buttonFrame, text='Land', fg='red', command=drone.land).grid(row=2, column=1, padx=5, pady=5)
    stop = tk.Button(buttonFrame, text='Stop', fg='red', command=drone.stop).grid(row=2, column=2, padx=5, pady=5)
    backToBase = tk.Button(buttonFrame, text='Back To Base', fg='red', command=drone.back_base).grid(row=2, column=3, padx=5, pady=5)

    #frome for video?// to do
    # bottomFrame = tk.Frame(root)
    # bottomFrame.pack(side=tk.BOTTOM)
    # root.update_idletasks()

    # reload ui
    def reload():
        currentX.configure(text="Current X : " + str(drone.x))
        currentY.configure(text="Current Y : " + str(drone.y))
        currentDirection.configure(text="Current direction : " + str(drone.angle))
        moveDistance.configure(text="Distance to move : " + str(drone.distance))
        rotateDegree.configure(text="Degree to turn : " + str(drone.rotateAngle))
        manualMode.configure(text="Manual mode : " + str(drone.manual))
        informationFrame.after(500, reload)

    reload()
    root.mainloop()

