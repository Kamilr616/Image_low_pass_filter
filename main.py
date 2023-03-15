import cv2
import numpy
from tkinter import Tk, Label, Button
from PIL import Image
from PIL import ImageTk
from tkinter.filedialog import askopenfilename


def select_image():
    # grab a reference to the image panels
    global panelA, panelB
    # open a file chooser dialog and allow the user to select an input
    # image
    path = askopenfilename()
    # ensure a file path was selected
    if len(path) > 0:
        # load the image from disk
        img = cv2.imread(path)
        assert img is not None, "file could not be read, check with os.path.exists()"

        # The operation works like this: keep this kernel above a pixel, add all the 25 pixels below this kernel,
        # take the average, and replace the central pixel with the new average value.
        # This operation is continued for all the pixels in the image.
        mask = numpy.ones((5, 5), dtype=int) / 25
        img_new = cv2.filter2D(img, -1, mask)
        img_new = img_new.astype(numpy.uint8)

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # convert the images to PIL format...
        img = Image.fromarray(img)
        img_new = Image.fromarray(img_new)
        # ...and then to ImageTk format
        img = ImageTk.PhotoImage(img)
        img_new = ImageTk.PhotoImage(img_new)
        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=img)
            panelA.image = img
            panelA.pack(side="left", padx=10, pady=10)
            # while the second panel will store the edge map
            panelB = Label(image=img_new)
            panelB.image = img_new
            panelB.pack(side="right", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=img)
            panelB.configure(image=img_new)
            panelA.image = img
            panelB.image = img_new


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Low pass filter")
panelA = None
panelB = None
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
# kick off the GUI
root.mainloop()
