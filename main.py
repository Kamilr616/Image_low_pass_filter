import cv2
import numpy
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename


#TODO image_save
def select_image(flag):
    global img, img_new
    if flag == 1:
        path.set(askopenfilename())
    else:
        path.set("images/lena.bmp")
    if len(path.get()) > 0:
        img = cv2.imread(path.get())
        img_new = img
    assert img is not None, "file could not be read, check with os.path.exists()"
    #show_image()
    start()

#TODO show_mask
def show_image():
    # grab a reference to the image panels
    global panelA, panelB, img, img_new
    # OpenCV represents images in BGR order; however PIL represents
    # images in RGB order, so we need to swap the channels
    img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_new_show = cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB)

    # convert the images to PIL format...
    img_show = Image.fromarray(img_show)
    img_new_show = Image.fromarray(img_new_show)
    # ...and then to ImageTk format
    img_show = ImageTk.PhotoImage(img_show)
    img_new_show = ImageTk.PhotoImage(img_new_show)
    # if the panels are None, initialize them
    if panelA is None or panelB is None:
        # the first panel will store our original image
        panelA = Label(image=img_show)
        panelA.image = img_show
        panelA.pack(side="left", padx=10, pady=10)
        # while the second panel will store the edge map
        panelB = Label(image=img_new_show)
        panelB.image = img_new_show
        panelB.pack(side="right", padx=10, pady=10)
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image=img_show)
        panelB.configure(image=img_new_show)
        panelA.image = img_show
        panelB.image = img_new_show


def start():
    # open a file chooser dialog and allow the user to select an input
    # image
    global img, img_new
    m_size = int(mask_size.get())
    m_type = mask_type.get()

    if m_type == 102:
        img_new = cv2.blur(img, (m_size, m_size))
    elif m_type == 101:
        img_new = cv2.medianBlur(img, m_size)
    elif m_type == 103:
        img_new = cv2.GaussianBlur(img, (m_size, m_size), 0)
    elif m_type == 104:
        img_new = cv2.bilateralFilter(img, m_size, 75, 75)

    img_new = img_new.astype(numpy.uint8)
    show_image()


def image_swap():
    global img, img_new
    img, img_new = img_new, img
    show_image()

#TODO image noise func
def image_noise():
    global img
    gauss_noise = numpy.zeros(img.shape, dtype=numpy.uint8)
    cv2.randn(gauss_noise, 128, 20)
    gauss_noise = (gauss_noise * 0.5).astype(numpy.uint8)
    img = cv2.add(img, gauss_noise)
    show_image()


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Low pass filter")
panelA = None
panelB = None
img = None
img_new = None
# file path
path = StringVar()

# Mask type
mask_type = IntVar()
mask_type.set(102)

masks = [("Median", 101),
         ("Average", 102),
         ("Gaussian", 103),
         ("Bilateral", 104)]

Label(root,
      text="Choose mask type:",
      justify=LEFT,
      padx=20).pack(anchor=W)

for mask, val in masks:
    Radiobutton(root,
                text=mask,
                padx=20,
                variable=mask_type,
                value=val).pack(anchor=W)

# Mask size
mask_size = IntVar()
mask_size.set(3)

sizes = [("3x3", 3),
         ("5x5", 5),
         ("7x7", 7),
         ("9x9", 9),
         ("11x11", 11)]

Label(root,
      text="Choose mask size:",
      justify=LEFT,
      padx=20).pack(anchor=W)

for size, val in sizes:
    Radiobutton(root,
                text=size,
                padx=20,
                variable=mask_size,
                value=val).pack(anchor=W)
select_image(0)

# create a button,then add the button the GUI
btn = Button(root, text="Select an image", command=lambda: select_image(1))
btn.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
btn1 = Button(root, text="Filter", command=start)
btn1.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
btn2 = Button(root, text="Swap images", command=image_swap)
btn2.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")
btn3 = Button(root, text="Add noise", command=image_noise)
btn3.pack(side="bottom", fill="both", expand=1, padx="10", pady="10")

# kick off the GUI
root.mainloop()
