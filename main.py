import cv2
import numpy
from tkinter import Button, Label, Radiobutton, Tk, StringVar, IntVar, Frame, Scale
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfile


def image_save():
    global img_new
    file = asksaveasfile(initialfile='image.png', defaultextension="*.png",
                         filetypes=[("All Files", "*.*"), ("PNG", "*.png")])
    if file:
        cv2.imwrite(file.name, img_new)


def select_image(flag=0):
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


def create_kernel_labels():
    global kernel
    m_size = mask_size.get()
    for i in range(m_size):
        for j in range(m_size):
            g = Label(kernel_frame, text=f"{kernel[i][j]:.2f}", borderwidth=1, relief="solid",
                      width=(52 // m_size),
                      height=(26 // m_size))
            g.grid(row=i, column=j)


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
    for g in kernel_frame.grid_slaves():
        g.destroy()
    create_kernel_labels()
    root.update()


def start():
    # open a file chooser dialog and allow the user to select an input
    # image
    global img, img_new, kernel
    m_size = mask_size.get()
    m_type = mask_type.get()

    if m_type == 102:
        kernel = numpy.ones((m_size, m_size), numpy.uint8) / m_size ** 2
        kernel = kernel / numpy.sum(kernel)
    if m_type == 105:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (m_size, m_size))
        kernel = kernel / numpy.sum(kernel)
    elif m_type == 106:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (m_size, m_size))
        kernel = kernel / numpy.sum(kernel)
    elif m_type == 107:
        kernel = numpy.ones((m_size, m_size), dtype=numpy.uint8)
        kernel = kernel / numpy.sum(kernel)
        kernel[0, 0] = 0
        kernel[0, -1] = 0
        kernel[-1, 0] = 0
        kernel[-1, -1] = 0
    elif m_type == 101:
        kernel = numpy.ones((m_size, m_size), numpy.uint8)
        img_new = cv2.medianBlur(img, m_size)
    elif m_type == 103:
        kernel = cv2.getGaussianKernel(m_size, 0)
        kernel = numpy.outer(kernel, kernel.transpose())
    elif m_type == 104:
        kernel = numpy.ones((m_size, m_size), numpy.uint8)
        img_new = cv2.bilateralFilter(img, m_size, 75, 75)

    if m_type != 104 and m_type != 101:
        img_new = cv2.filter2D(img, -1, kernel)

    img_new = img_new.astype(numpy.uint8)
    show_image()


def image_swap():
    global img, img_new
    img, img_new = img_new, img
    show_image()


def image_noise():
    global img
    mul = w1.get()
    gauss_noise = numpy.zeros(img.shape, dtype=numpy.uint8)
    mean = numpy.ones(3, dtype=numpy.uint8) * 128
    dst = numpy.ones(3, dtype=numpy.uint8) * 20
    cv2.randn(gauss_noise, mean, dst)
    gauss_noise = (gauss_noise * mul).astype(numpy.uint8)
    img = cv2.add(img, gauss_noise)
    show_image()


def change_language():
    ger = {
        "l1": "Wählen Sie den Kernel-Typ:",
        "l2": "Wählen Sie die Kernel-Größe:",
        "l3": "Wählen Sie die Sprache:",

        "k1": "Kernel:",
        "k2": "Input:",
        "k3": "Output:",

        "m1": "Durchschnitt",
        "m2": "Gaussian",
        "m3": "Rechteck",
        "m4": "Ellipse",
        "m5": "Trapezoid",
        "m6": "Median",
        "m7": "Bilateral",

        "b0": "Wählen Sie ein Bild",
        "b1": "Bild speichern als",
        "b2": "Bilder tauschen",
        "b5": "Rauschen hinzufügen",
    }
    pol = {
        "l1": "Wybierz typ maski:",
        "l2": "Wybierz rozmiar maski:",
        "l3": "Wybierz język:",

        "k1": "Maska:",
        "k2": "Wejście:",
        "k3": "Wyjście:",

        "m1": "Średnia",
        "m2": "Gaussowska",
        "m3": "Prostokątna",
        "m4": "Elipsa",
        "m5": "Trapezoidalna",
        "m6": "Medianowa",
        "m7": "Bilateralna",

        "b0": "Wybierz obraz",
        "b1": "Zapisz obraz jako",
        "b2": "Zamień obrazy",
        "b5": "Dodaj szum",
    }
    eng = {
        "l1": "Choose kernel type:",
        "l2": "Choose kernel size:",
        "l3": "Choose language:",

        "k1": "Kernel:",
        "k2": "Input:",
        "k3": "Output:",

        "m1": "Average",
        "m2": "Gaussian",
        "m3": "Rectangle",
        "m4": "Eclipse",
        "m5": "Trapezoid",
        "m6": "Median",
        "m7": "Bilateral",

        "b0": "Select image",
        "b1": "Save image as",
        "b2": "Swap images",
        "b5": "Add noise",
    }
    typed = lang.get()
    if typed == 201:
        dict1 = eng
    elif typed == 202:
        dict1 = pol
    elif typed == 203:
        dict1 = ger
    else:
        dict1 = eng

    m1.set(dict1["m1"])
    m2.set(dict1["m2"])
    m3.set(dict1["m3"])
    m4.set(dict1["m4"])
    m5.set(dict1["m5"])
    m6.set(dict1["m6"])
    m7.set(dict1["m7"])

    l1.set(dict1["l1"])
    l2.set(dict1["l2"])
    l3.set(dict1["l3"])

    k1.set(dict1["k1"])
    k2.set(dict1["k2"])
    k3.set(dict1["k3"])

    b0.set(dict1["b0"])
    b1.set(dict1["b1"])
    b2.set(dict1["b2"])
    b5.set(dict1["b5"])


root = Tk()
root.title("Low pass filter")

ico = Image.open('images/ans.jpeg')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)


panelA = None
panelB = None
img = None
img_new = None
kernel = None

path = StringVar()
b0 = StringVar()
b1 = StringVar()
b2 = StringVar()
b3 = StringVar()
b4 = StringVar()
b5 = StringVar()
lang = IntVar()
l1 = StringVar()
l2 = StringVar()
l3 = StringVar()
k1 = StringVar()
k2 = StringVar()
k3 = StringVar()
mask_type = IntVar()
m1 = StringVar()
m2 = StringVar()
m3 = StringVar()
m4 = StringVar()
m5 = StringVar()
m6 = StringVar()
m7 = StringVar()
mask_size = IntVar()

labels = [l1, l2, l3]

labels2 = [k1, k2, k3]

masks = [(102, m1),
         (103, m2),
         (105, m3),
         (106, m4),
         (107, m5),
         (101, m6),
         (104, m7)]

sizes = [("3x3", 3),
         ("5x5", 5),
         ("7x7", 7),
         ("9x9", 9),
         ("11x11", 11)]

buttons = [(lambda: select_image(1), b0),
           (image_save, b1),
           (image_swap, b2),
           (image_noise, b5)]

langs = [("English", 201, lambda: change_language()),
         ("Polski", 202, lambda: change_language()),
         ("Deutsch", 203, lambda: change_language())]

mask_size.set(3)
mask_size.set(5)
mask_type.set(102)
lang.set(201)

frame = Frame(root)
frame1 = Frame(root)
frame1.pack(side="top", pady=20)
frame2 = Frame(root)
frame2.pack(side="top")
frame3 = Frame(root)
frame3.pack(side="top")
frame3a = Frame(frame3)
frame3a.pack(side="left", padx=20)
frame3b = Frame(frame3)
frame3b.pack(side="left", padx=20)
frame3c = Frame(frame3)
frame3c.pack(side="left", padx=20)
frame4 = Frame(root)
frame4.pack(side="top", pady=15)
image_frame = Frame(root)
image_frame.pack(side="top", pady=20)
kernel_frame = Frame(image_frame)
kernel_frame.pack(side="left", pady=20)

for comm, b in buttons:
    Button(frame1,
           textvariable=b,
           bg="#1976D2",
           activeforeground="#2196F3",
           command=comm).pack(side="left", fill="both", expand=1, padx="10", pady="10")

w1 = Scale(frame1, from_=0, resolution=0.1, to=10, orient="horizontal", foreground="#2196F3")
w1.pack(side="left", fill="both", expand=1, ipadx="40", pady="10")
w1.set(0.5)

for label in labels:
    Label(frame2,
          textvariable=label,
          padx=20,
          justify="left").pack(anchor="w", side="left")

for val, m in masks:
    Radiobutton(frame3a,
                textvariable=m,
                padx=20,
                variable=mask_type,
                command=start,
                activeforeground="#2196F3",
                value=val).pack(anchor="w")

for size, val in sizes:
    Radiobutton(frame3b,
                text=size,
                padx=20,
                variable=mask_size,
                command=start,
                activeforeground="#2196F3",
                value=val).pack(anchor="w")

for t, val, comm in langs:
    Radiobutton(frame3c,
                text=t,
                padx=20,
                variable=lang,
                command=comm,
                activeforeground="#2196F3",
                value=val).pack(anchor="w")

for k in labels2:
    Label(frame4,
          textvariable=k,
          padx=40,
          justify="left").pack(anchor="w", padx="200", side="left")

change_language()
select_image()

# kick off the GUI
root.mainloop()
