from cv2 import *
import time
from tkinter import *
import numpy as np
from pynput.mouse import Controller, Button as bt

glower = np.array([40, 100, 60])
gupper = np.array([80, 255, 255])
openker = np.ones((5, 5))
closeker = np.ones((20, 20))
drag = 0
mouse = Controller()
resx, resy = 0, 0
camx, camy = (320, 240) 


def endUI():
    root = Tk()
    root.title("Closing Page")
    root.geometry("400x100")
    Label(
        root, text="Thank you! \nThis was made by Soumya Mukhija.", font="Times 20"
    ).grid(row=0, column=0)
    Button(root, text="Done", bg="yellow", command=root.destroy).grid(row=1, column=0)
    root.mainloop()


def triggerUI():
    global resx, resy
    root = Tk()
    root.title("Welcome page")
    root.geometry("400x150")
    resx = root.winfo_screenwidth() 
    resy = root.winfo_screenheight()
    Label(
        root,
        text="Gesture Recognition System\nOn the basis of the colour Green.",
        font="Times 20",
    ).grid(row=0, column=0)
    Button(
        root, text="Proceed", fg="Green", font="Times 20", command=root.destroy
    ).grid(row=1, column=0)
    root.mainloop()


def detectObject():
    global drag
    cap = VideoCapture(0)
    time.sleep(2)
    while True:
        try:
            retval, frame = cap.read()  # retreive() + grab() = read()
            frame = resize(frame, (500, 500))
            font = FONT_HERSHEY_SIMPLEX
            putText(
                frame,
                "Gesture Recognition System by Soumya",
                (0, 40),
                font,
                1,
                (0, 0, 0),
                1,
                LINE_AA,
            )
            HSVframe = cvtColor(frame, COLOR_BGR2HSV)
            mask = inRange(HSVframe, glower, gupper)
            openmask = morphologyEx(mask, MORPH_OPEN, openker)
            closemask = morphologyEx(openmask, MORPH_CLOSE, closeker)
            x, contours, y = findContours(closemask, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
            drawContours(frame, contours, -1, (0, 255, 0), 3)
            for i in range(len(contours)):
                x, y, w, h = boundingRect(contours[i])
                rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if len(contours) == 2:
                if drag == 1:
                    drag = 0
                aw, ax, ay, az = boundingRect(contours[0])
                bw, bx, by, bz = boundingRect(contours[1])
                mpx1 = (aw + ay) / 2
                mpy1 = (ax + az) / 2
                mpx2 = (bw + by) / 2
                mpy2 = (bx + bz) / 2
                mpx = (mpx1 + mpx2) / 2
                mpy = (mpy1 + mpy2) / 2
                mouse.release(bt.left)
                current_locn = (resx - (resx * mpx / camx), mpy * resy / camy)  ##
                mouse.position = current_locn
                while mouse.position != current_locn:
                    pass
            elif len(contours) == 1:
                if drag == 0:
                    drag = 1
                    aw, ax, ay, az = boundingRect(contours[0])
                    mpx = (aw + ay) / 2
                    mpy = (ax + az) / 2
                    mouse.press(bt.left)
                    current_locn = (resx - (resx * mpx) / camx, mpy * resy / camy)
                    mouse.position = current_locn
                    while mouse.position != current_locn:
                        pass
            imshow("Green: ", mask)
            #waitKey(1)
            imshow("Original image: ", frame)
            #waitKey(1)
            #imshow("Open Mask", openmask)
            #imshow("Final Mask", closemask)
            key = waitKey(0) & 0xFF #waitkey should have a non0 param to avoid freezing
            if key == ord("q"):
                break
        except:
            raise
            root = Tk()
            root.title("Error")
            Label(
                root,
                text="Whoops! There seems to be some problem. Please try again.",
                font="Times 20",
            ).grid(row=0, column=0)
            root.mainloop()


triggerUI()
detectObject()
destroyAllWindows()
endUI()
