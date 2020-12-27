import tello
import Sweep
import Control_Panel_UI

if __name__ == '__main__':

    drone = tello.Tello()
    drone_sweep = Sweep.Sweep(drone)
    ui = Control_Panel_UI.ControlPanelUI(drone, drone_sweep)
    ui.root.mainloop()
