import cv2
import numpy
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename


def select_image():
    path.set(askopenfilename())


def show_image(imgA, imgB):
    # grab a reference to the image panels
    global panelA, panelB
    # OpenCV represents images in BGR order; however PIL represents
    # images in RGB order, so we need to swap the channels
    img = cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)
    # convert the images to PIL format...
    img = Image.fromarray(img)
    img_new = Image.fromarray(imgB)
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


def start():
    # open a file chooser dialog and allow the user to select an input
    # image
    size = mask_size.get()
    m_type = mask_type.get()
    # ensure a file path was selected
    if len(path.get()) > 0:
        # load the image from disk
        img = cv2.imread(path.get())
        img_new = img
        assert img is not None, "file could not be read, check with os.path.exists()"

        # The operation works like this: keep this kernel above a pixel, add all the 25 pixels below this kernel,
        # take the average, and replace the central pixel with the new average value.
        # This operation is continued for all the pixels in the image.

        if m_type == 102:
            mask = numpy.ones((size, size), dtype=float) / size ** 2
            img_new = cv2.filter2D(img, -1, mask)
        elif m_type == 101:
            img_new = cv2.medianBlur(img, size)
        elif m_type == 103:
            img_new = cv2.GaussianBlur(img, (size, size), 0)
        elif m_type == 104:
            img_new = cv2.bilateralFilter(img, 9, 75, 75)

        img_new = img_new.astype(numpy.uint8)
        show_image(img, img_new)


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Low pass filter")
panelA = None
panelB = None
# file path
path = StringVar()

# Mask type
mask_type = IntVar()
mask_type.set(1)

masks = [("Median", 101),
         ("Average", 102),
         ("Gaussian", 103),
         ("Bilateral", 104)]

Label(root,
      text="Choose mask type:",
      justify=LEFT,
      padx=20).pack()

for mask, val in masks:
    Radiobutton(root,
                text=mask,
                padx=20,
                variable=mask_type,
                value=val).pack(anchor=W)

# Mask size
Label(root,
      text="Choose mask size:",
      justify=LEFT,
      padx=20).pack()

mask_size = Scale(root, from_=1, to=10, orient=HORIZONTAL)
mask_size.set(3)
mask_size.pack()

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
btn1 = Button(root, text="Start", command=start)
btn1.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
# kick off the GUI
root.mainloop()
