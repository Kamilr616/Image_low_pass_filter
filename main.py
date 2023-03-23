import cv2
import numpy
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter import ttk


def image_save():
    global img_new
    file = asksaveasfile(initialfile='Untitled.png', defaultextension="*.png",
                         filetypes=[("All Files", "*.*"), ("PNG", "*.png")])
    if file:
        cv2.imwrite(file.name, img_new)


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
    # show_image()
    start()


def create_kernel_labels(kernel):
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            label = Label(kernel_frame, text="{:.2f}".format(kernel[i][j]), borderwidth=1, relief="solid", width=5,
                          height=2)
            label.grid(row=i, column=j)


# TODO show_mask
def show_image():
    # grab a reference to the image panels
    global panelA, panelB, img, img_new, kernel
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
    if panelA is None or panelB is None or kernel is None:
        # the first panel will store our original image
        panelA = Label(image_frame, image=img_show)
        panelA.image = img_show
        panelA.pack(side="left", padx=10, pady=10)
        # while the second panel will store the edge map
        panelB = Label(image_frame, image=img_new_show)
        panelB.image = img_new_show
        panelB.pack(side="right", padx=10, pady=10)
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image=img_show)
        panelB.configure(image=img_new_show)
        panelA.image = img_show
        panelB.image = img_new_show
    for label in kernel_frame.grid_slaves():
        label.destroy()
    create_kernel_labels(kernel)
    root.update()


def start():
    # open a file chooser dialog and allow the user to select an input
    # image
    global img, img_new, kernel
    m_size = mask_size.get()
    m_type = mask_type.get()

    if m_type == 102:
        kernel = numpy.ones((m_size, m_size), numpy.uint8) / m_size ** 2
        img_new = cv2.filter2D(img, -1, kernel)
    if m_type == 105:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (m_size, m_size))
        kernel = kernel / numpy.sum(kernel)
        img_new = cv2.filter2D(img, -1, kernel)
    elif m_type == 106:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (m_size, m_size))
        kernel = kernel / numpy.sum(kernel)
        img_new = cv2.filter2D(img, -1, kernel)
    elif m_type == 107:
        kernel = numpy.ones((m_size, m_size), dtype=numpy.uint8)
        kernel = kernel / numpy.sum(kernel)
        kernel[0, 0] = 0
        kernel[0, -1] = 0
        kernel[-1, 0] = 0
        kernel[-1, -1] = 0
        img_new = cv2.filter2D(img, -1, kernel)
    elif m_type == 101:
        kernel = numpy.ones((m_size, m_size), numpy.uint8)
        img_new = cv2.medianBlur(img, m_size)
    elif m_type == 103:
        kernel = cv2.getGaussianKernel(m_size, 0)
        kernel = numpy.outer(kernel, kernel.transpose())
        img_new = cv2.filter2D(img, -1, kernel)
    elif m_type == 104:
        img_new = cv2.bilateralFilter(img, m_size, 75, 75)

    img_new = img_new.astype(numpy.uint8)
    show_image()


def image_swap():
    global img, img_new
    img, img_new = img_new, img
    show_image()


# TODO image noise func(repair rgb)
def image_noise():
    global img
    mul = w1.get()
    gauss_noise = numpy.zeros(img.shape, dtype=numpy.uint8)
    cv2.randn(gauss_noise, 128, 20)
    gauss_noise = (gauss_noise * mul).astype(numpy.uint8)
    img = cv2.add(img, gauss_noise)
    show_image()


# initialize the window toolkit along with the two image panels
root = Tk()
root.title("Low pass filter")
frame = Frame(root)
panelA = None
panelB = None
img = None
img_new = None
kernel = None

# file path
path = StringVar()
topframe = Frame(root)
topframe.pack(side="top", pady=20)
# create a button,then add the button the GUI
btn = Button(topframe, text="Select an image", command=lambda: select_image(1))
btn.pack(side="left", fill="both", expand=1, padx="10", pady="10")
btn2 = Button(topframe, text="Swap images", command=image_swap)
btn2.pack(side="left", fill="both", expand=1, padx="10", pady="10")
btn4 = Button(topframe, text="Save as", command=image_save)
btn4.pack(side="left", fill="both", expand=1, padx="10", pady="10")
btn3 = Button(topframe, text="Add noise", command=image_noise)
btn3.pack(side="left", fill="both", expand=1, padx="10", pady="10")
w1 = Scale(topframe, from_=0, resolution=0.1, to=10, orient=HORIZONTAL)
w1.pack(side="left", fill="both", expand=1, ipadx="40", pady="10")
w1.set(0.5)
btn1 = Button(topframe, text="Filter", command=start)
btn1.pack(side="left", fill="both", expand=1, padx="10", pady="10")

frame2 = Frame(root)
frame2.pack(side="top")

l1 = Label(frame2,
           text="Choose mask type:",
           justify=LEFT,
           padx=20)
l1.pack(side=LEFT)
l2 = Label(frame2,
           text="Choose mask size:",
           justify=LEFT,
           padx=20)
l2.pack(side=LEFT)
l3 = Label(frame2,
           text="Language:",
           justify=LEFT,
           padx=20)
l3.pack(side=LEFT)

frame3 = Frame(root)
frame3.pack(side="top")
frame3a = Frame(frame3)
frame3a.pack(side="left", padx=20)
frame3b = Frame(frame3)
frame3b.pack(side="left", padx=20)
frame3c = Frame(frame3)
frame3c.pack(side="left", padx=20)


image_frame = Frame(root)
image_frame.pack(side="top", pady=20)
kernel_frame = Frame(image_frame)
kernel_frame.pack(side="left", pady=20)

mask_type = IntVar()
masks = [("Median", 101),
         ("Average", 102),
         ("Gaussian", 103),
         ("Bilateral", 104),
         ("Rectangle", 105),
         ("Eclipse", 106),
         ("Trapezoid", 107)]

for mask, val in masks:
    Radiobutton(frame3a,
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

for size, val in sizes:
    Radiobutton(frame3b,
                text=size,
                padx=20,
                variable=mask_size,
                value=val).pack(anchor=W)
lang = IntVar()
langs = [("English", 201),
         ("Polski", 202),
         ("Inny", 203)]
for t, val in langs:
    Radiobutton(frame3c,
                text=t,
                padx=20,
                variable=lang,
                value=val).pack(anchor=W)


mask_size.set(5)
mask_type.set(102)
lang.set(201)
select_image(0)

# kick off the GUI
root.mainloop()
