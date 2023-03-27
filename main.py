from cv2 import add, imwrite, imread, cvtColor, getStructuringElement, COLOR_BGR2RGB, MORPH_CROSS, MORPH_RECT, \
    MORPH_ELLIPSE, getGaussianKernel, medianBlur, bilateralFilter, filter2D, randn, resize

from numpy import ones, sum, uint8, outer

from tkinter import Button, Label, Radiobutton, Tk, StringVar, IntVar, Frame, Scale, DoubleVar, Checkbutton

from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename, asksaveasfilename


def image_save():
    global img_new
    file_path = asksaveasfilename(initialfile='image.png', defaultextension="*.png",
                                  filetypes=[("All Files", "*.*"), ("PNG", "*.png")])
    if file_path:
        with open(file_path, 'wb') as file:
            imwrite(file_path, img_new)
    assert file_path is not None, "file could not be write, check with os.path.exists()"


def select_image(flag=0):
    global img, img_new
    if flag == 1:
        file_path = askopenfilename()
    else:
        file_path = "images/lena.bmp"
    if file_path:
        with open(file_path, "rb") as file:
            img = imread(file_path)
        height = 400
        img = resize(img, (int(height * (img.shape[1] / img.shape[0])), height))
        img_new = img
    assert img is not None, "file could not be read, check with os.path.exists()"
    start()


def show_image():
    # grab a reference to the image panels
    global panelA, panelB, img, img_new, kernel
    # OpenCV represents images in BGR order; however PIL represents
    # images in RGB order, so we need to swap the channels
    img_show = cvtColor(img, COLOR_BGR2RGB)
    img_new_show = cvtColor(img_new, COLOR_BGR2RGB)

    # convert the images to PIL format...
    img_show = Image.fromarray(img_show)
    img_new_show = Image.fromarray(img_new_show)
    # ...and then to ImageTk format
    img_show = ImageTk.PhotoImage(img_show)
    img_new_show = ImageTk.PhotoImage(img_new_show)
    # if the panels are None, initialize them
    if panelA is None or panelB is None:
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
    show_kernel()
    root.update()


def start():
    # open a file chooser dialog and allow the user to select an input
    # image
    global img, img_new, kernel
    m_size = mask_size.get()
    m_type = mask_type.get()

    if m_type == 102:
        kernel = getStructuringElement(MORPH_RECT, (m_size, m_size))
        kernel = kernel / sum(kernel)
    if m_type == 105:
        kernel = getStructuringElement(MORPH_CROSS, (m_size, m_size))
        kernel = kernel / sum(kernel)
    elif m_type == 106:
        kernel = getStructuringElement(MORPH_ELLIPSE, (m_size, m_size))
        kernel = kernel / sum(kernel)
    elif m_type == 107:
        kernel = ones((m_size, m_size), dtype=uint8)
        kernel = kernel / sum(kernel)
        kernel[0, 0] = 0
        kernel[0, -1] = 0
        kernel[-1, 0] = 0
        kernel[-1, -1] = 0
    elif m_type == 101:
        img_new = medianBlur(img, m_size)
    elif m_type == 103:
        kernel = getGaussianKernel(m_size, 0)
        kernel = outer(kernel, kernel.transpose())
    elif m_type == 104:
        img_new = bilateralFilter(img, m_size, 75, 75)

    if m_type != 104 and m_type != 101:
        img_new = filter2D(img, -1, kernel)
    else:
        kernel = ones((m_size, m_size), uint8)

    img_new = img_new.astype(uint8)
    show_image()


def image_swap():
    global img, img_new
    img = img_new
    show_image()


def image_noise():
    global img
    mul = w1.get()
    gauss_noise = ones(img.shape, dtype=uint8)
    mean = ones(3, dtype=uint8) * 128
    dst = ones(3, dtype=uint8) * 20
    randn(gauss_noise, mean, dst)
    gauss_noise = (gauss_noise * mul).astype(uint8)
    img = add(img, gauss_noise)
    show_image()


def change_language():
    ukr = {
        "l1": "Виберіть тип ядра:",
        "l2": "Виберіть розмір ядра:",
        "l3": "Виберіть мову:",

        "k1": "Ядро:",
        "k2": "Вхід:",
        "k3": "Вихід:",
        "k4": "Фільтрація нижчих частот",

        "m1": "Середнє",
        "m2": "Гауссівське",
        "m3": "Перехресне",
        "m4": "Еліпс",
        "m5": "Трапеція",
        "m6": "Медіанне",
        "m7": "Білатеральне",

        "b0": "Вибрати зображення",
        "b1": "Зберегти зображення як",
        "b2": "Поміняти зображення",
        "b3": "Показати ядро",
        "b5": "Додати шум",
    }
    esp = {
        "l1": "Seleccione el tipo de kernel:",
        "l2": "Seleccione el tamaño del kernel:",
        "l3": "Seleccione el idioma:",

        "k1": "Kernel:",
        "k2": "Entrada:",
        "k3": "Salida:",
        "k4": "Filtrado de paso bajo",

        "m1": "Promedio",
        "m2": "Gaussiano",
        "m3": "Cruzado",
        "m4": "Eclipse",
        "m5": "Trapecio",
        "m6": "Mediana",
        "m7": "Bilateral",

        "b0": "Seleccionar imagen",
        "b1": "Guardar imagen como",
        "b2": "Intercambiar imagen",
        "b3": "Mostrar el kernel",
        "b5": "Agregar ruido",
    }

    ger = {
        "l1": "Wähle Kerntyp:",
        "l2": "Wähle Kerngröße:",
        "l3": "Wähle Sprache:",

        "k1": "Kern:",
        "k2": "Eingabe:",
        "k3": "Ausgabe:",
        "k4": "Tiefpassfilterung",

        "m1": "Durchschnitt",
        "m2": "Gauß",
        "m3": "Kreuz",
        "m4": "Eclipse",
        "m5": "Trapezoid",
        "m6": "Median",
        "m7": "Bilateral",

        "b0": "Bild auswählen",
        "b1": "Bild speichern unter",
        "b2": "Bild austauschen",
        "b3": "Kernel anzeigen",
        "b5": "Rauschen hinzufügen"
    }

    pol = {
        "l1": "Wybierz typ maski:",
        "l2": "Wybierz rozmiar maski:",
        "l3": "Wybierz język:",

        "k1": "Maska:",
        "k2": "Wejście:",
        "k3": "Wyjście:",
        "k4": "Filtracja dolnoprzepustowa",

        "m1": "Średnia",
        "m2": "Gaussowska",
        "m3": "Krzyżowa",
        "m4": "Elipsa",
        "m5": "Trapezowa",
        "m6": "Medianowa",
        "m7": "Bilateralna",

        "b0": "Wybierz obraz",
        "b1": "Zapisz obraz jako",
        "b2": "Zamień obraz",
        "b3": "Wyświetl maskę",
        "b5": "Dodaj szum",
    }
    eng = {
        "l1": "Choose kernel type:",
        "l2": "Choose kernel size:",
        "l3": "Choose language:",

        "k1": "Kernel:",
        "k2": "Input:",
        "k3": "Output:",
        "k4": "Low-pass filtering",

        "m1": "Average",
        "m2": "Gaussian",
        "m3": "Cross",
        "m4": "Eclipse",
        "m5": "Trapezoid",
        "m6": "Median",
        "m7": "Bilateral",

        "b0": "Select image",
        "b1": "Save image as",
        "b2": "Swap image",
        "b3": "Display kernel",
        "b5": "Add noise"
    }
    typed = lang.get()
    if typed == 201:
        dict1 = eng
    elif typed == 202:
        dict1 = pol
    elif typed == 203:
        dict1 = ger
    elif typed == 204:
        dict1 = esp
    elif typed == 205:
        dict1 = ukr
    else:
        dict1 = eng

    root.title(dict1["k4"])
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

#    k1.set(dict1["k1"])
#    k2.set(dict1["k2"])
#    k3.set(dict1["k3"])

    b0.set(dict1["b0"])
    b1.set(dict1["b1"])
    b2.set(dict1["b2"])
    b3.set(dict1["b3"])
    b5.set(dict1["b5"])


def create_widgets():
    labels = [l1, l2, l3]

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
             ("Deutsch", 203, lambda: change_language()),
             ("Español", 204, lambda: change_language()),
             ("Українська", 205, lambda: change_language())]

    mask_size.set(3)
    mask_size.set(5)
    mask_type.set(102)
    lang.set(201)
    w1.set(0.5)
    w2.set(0)

    for comm, b in buttons:
        Button(frame1,
               textvariable=b,
               bg="#1976D2",
               activeforeground="#2196F3",
               command=comm).pack(side="left", fill="both", expand=1, padx="10", pady="10")

    Scale(frame1, from_=0.05, resolution=0.05, to=5, orient="horizontal", background="#1976D2", length="120",
          highlightcolor="#2196F3", variable=w1).pack(side="left", fill="both", expand=1, ipadx="10", pady="10")

    Checkbutton(frame1,
                textvariable=b3,
                bg="#1976D2",
                activeforeground="#2196F3",
                variable=w2).pack(side="left", fill="both", expand=1, padx="10", pady="10")
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


def show_kernel():
    global kernel
    if kernel_frame.slaves is not None:
        for g in kernel_frame.grid_slaves():
            g.grid_remove()
    if w2.get() and kernel is not None:
        m_size = mask_size.get()
        for i in range(m_size):
            for j in range(m_size):
                g = Label(kernel_frame, text=f"{kernel[i][j]:.2f}", borderwidth=1, relief="solid",
                          width=(52 // m_size),
                          height=(26 // m_size))
                g.grid(row=i, column=j)


root = Tk()
root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('ans.ico')))
root.minsize(800, 600)

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
w1 = DoubleVar()
w2 = IntVar()

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
kernel_frame.pack(side="right", pady=20)

create_widgets()
change_language()
select_image()

# kick off the GUI
root.mainloop()
