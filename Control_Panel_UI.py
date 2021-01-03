# from PIL import Image
import time
import os
import datetime
import platform
import Tkinter as tk
from Tkinter import Toplevel
from threading import Thread
import threading


class ControlPanelUI:

    def __init__(self, drone, drone_sweep):
        self.drone = drone
        self.drone_sweep = drone_sweep
        self.frame = None  # frame read from h264decoder

        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.panel = None

        self.btn_pause = tk.Button(self.root, text="Pause", relief="raised", command=self.pauseVideo)
        self.btn_pause.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)
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
        self.distance20 = tk.Button(self.setFrame, text=" 20 ", command=lambda: self.drone.set_distance(20)).grid(
            row=0, column=1, sticky=tk.S, padx=5)
        self.distance50 = tk.Button(self.setFrame, text=" 50 ", command=lambda: self.drone.set_distance(50)).grid(
            row=0, column=2, sticky=tk.S, padx=5)
        self.distance70 = tk.Button(self.setFrame, text=" 70 ", command=lambda: self.drone.set_distance(70)).grid(
            row=0, column=3, sticky=tk.S, padx=5)
        self.distance100 = tk.Button(self.setFrame, text=" 100 ", command=lambda: self.drone.set_distance(100)).grid(
            row=0, column=4, sticky=tk.S, padx=5)
        self.setDegree = tk.Label(self.setFrame, text="Set Degree : ").grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        self.degree15 = tk.Button(self.setFrame, text=" 15 ", command=lambda: self.drone.set_degree(15)).grid(
            row=1, column=1, sticky=tk.S, padx=5, pady=( 5, 0))
        self.degree30 = tk.Button(self.setFrame, text=" 30 ", command=lambda: self.drone.set_degree(30)).grid(
            row=1, column=2, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree60 = tk.Button(self.setFrame, text=" 60 ", command=lambda: self.drone.set_degree(60)).grid(
            row=1, column=3, sticky=tk.S, padx=5, pady=(5, 0))
        self.degree90 = tk.Button(self.setFrame, text=" 90 ", command=lambda: self.drone.set_degree(90)).grid(
            row=1, column=4, sticky=tk.S, padx=5,pady=(5, 0))
        self.degree180 = tk.Button(self.setFrame, text=" 180 ", command=lambda: self.drone.set_degree(180)).grid(
            row=1, column=5, sticky=tk.S, padx=5, pady=(5, 0))

        self.setRoute = tk.Label(self.setFrame, text="Set Route : ").grid(row=2, column=0, sticky=tk.E, pady=(5, 0))
        self.route1 = tk.Button(self.setFrame, text="Polygon Route",
                                command=lambda: self.drone_sweep.set_route(1)).grid(
            row=2, column=1, columnspan=2, sticky=tk.S, padx=5, pady=(5, 0))
        self.route2 = tk.Button(self.setFrame, text="Triangle Route",
                                command=lambda: self.drone_sweep.set_route(2)).grid(
            row=2, column=3, columnspan=2,sticky=tk.S, padx=5, pady=(5, 0))

        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.pack()
        self.moveForward = tk.Button(self.buttonFrame, text='Move Forward', fg="red",
                                     command=self.drone.move_forward).grid(row=0, column=0, sticky=tk.W, padx=5,
                                                                           pady=(20, 5))
        self.moveBackward = tk.Button(self.buttonFrame, text='Move Backward', fg="red",
                                      command=self.drone.move_backward).grid(row=0, column=1, sticky=tk.W, padx=5,
                                                                             pady=(20, 5))
        self.moveLeft = tk.Button(self.buttonFrame, text='Move Left', fg="red", command=self.drone.move_left).grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveRight = tk.Button(self.buttonFrame, text='Move Right', fg="red", command=self.drone.move_right).grid(
            row=0, column=3, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveUp = tk.Button(self.buttonFrame, text='Move Up', fg="red", command=self.drone.move_up).grid(
            row=0, column=4, sticky=tk.W, padx=5, pady=(20, 5))
        self.moveDown = tk.Button(self.buttonFrame, text='Move Down', fg="red", command=self.drone.move_down).grid(
            row=0, column=5, sticky=tk.W, padx=5, pady=(20, 5))
        self.rotateClockwise = tk.Button(self.buttonFrame, text='Rotate Clockwise', fg="red",
                                         command=self.drone.rotate_cw).grid(row=1, column=0, pady=5, padx=5)
        self.rotateCounterclockwise = tk.Button(self.buttonFrame, text='Rotate Counter-clockwise', fg="red",
                                                command=self.drone.rotate_ccw).grid(row=1, column=1, columnspan=2, pady=5)
        self.perimeterSweep = tk.Button(self.buttonFrame, text='Pre-plan Route Sweep', fg="red",
                                        command=lambda: Thread(target=self.drone_sweep.perform_sweep).start()).grid(
            row=1, column=3, columnspan=2, pady=5, padx=5)
        self.takeOff = tk.Button(self.buttonFrame, text='Take off', fg='red', command=self.drone.takeoff).grid(
            row=2, column=0, padx=5, pady=5)
        self.land = tk.Button(self.buttonFrame, text='Land', fg='red', command=self.drone.land).grid(
            row=2, column=1, padx=5, pady=5)
        self.stop = tk.Button(self.buttonFrame, text='Stop', fg='red', command=self.drone.stop).grid(
            row=2, column=2, padx=5, pady=5)
        self.backToBase = tk.Button(self.buttonFrame, text='Back To Base', fg='red', command=self.drone.back_base).grid(
            row=2, column=3, padx=5, pady=5)

        # frame for video// to do
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # the sending_command will send command to tello every 5 seconds
        self.sending_command_thread = threading.Thread(target=self._sendingCommand)

        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

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

    def videoLoop(self):
        """
        The mainloop thread of Tkinter
        Raises:
            RuntimeError: To get around a RunTime error that Tkinter throws due to threading.
        """
        try:
            # start the thread that get GUI image and draw skeleton
            time.sleep(0.5)
            self.sending_command_thread.start()
            while not self.stopEvent.is_set():
                system = platform.system()

                # read the frame for GUI show
                self.frame = self.drone.read()
                if self.frame is None or self.frame.size == 0:
                    continue

                    # transfer the format from frame to image
                image = tk.Image.fromarray(self.frame)

                # we found compatibility problem between Tkinter,PIL and Macos,and it will
                # sometimes result the very long preriod of the "ImageTk.PhotoImage" function,
                # so for Macos,we start a new thread to execute the _updateGUIImage function.
                if system == "Windows" or system == "Linux":
                    self._updateGUIImage(image)

                else:
                    thread_tmp = Thread.Thread(target=self._updateGUIImage, args=(image,))
                    thread_tmp.start()
                    time.sleep(0.03)
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def _updateGUIImage(self, image):
        """
        Main operation to initial the object of image,and update the GUI panel
        """
        image = tk.ImageTk.PhotoImage(image)
        # if the panel none ,we need to initial it
        if self.panel is None:
            self.panel = tk.Label(image=image)
            self.panel.image = image
            self.panel.pack(side="left", padx=10, pady=10)
        # otherwise, simply update the panel
        else:
            self.panel.configure(image=image)
            self.panel.image = image

    def pauseVideo(self):
        """
        Toggle the freeze/unfreze of video
        """
        if self.btn_pause.config('relief')[-1] == 'sunken':
            self.btn_pause.config(relief="raised")
            self.drone.video_freeze(False)
        else:
            self.btn_pause.config(relief="sunken")
            self.drone.video_freeze(True)

    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """

        while True:
            self.drone.send_command('command')
            time.sleep(5)

    def onClose(self):
        """
        set the stop event, cleanup the camera, and allow the rest of

        the quit process to continue
        """
        print("[INFO] closing...")
        self.stopEvent.set()
        del self.drone
        self.root.quit()