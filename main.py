from cv2 import add, imwrite, imread, cvtColor, getStructuringElement, COLOR_BGR2RGB, MORPH_CROSS, MORPH_RECT, \
    MORPH_ELLIPSE, getGaussianKernel, medianBlur, bilateralFilter, filter2D, randn, resize

from numpy import ones, sum, uint8, outer

from tkinter import Button, Label, Radiobutton, Tk, StringVar, IntVar, Frame, Scale, DoubleVar, Checkbutton

from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename, asksaveasfilename


# class for creating a graphical user interface for image manipulation
class Application(Frame):
    # constructor
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('ans.ico')))
        self.master.minsize(900, 600)
        self.panelA = None
        self.panelB = None
        self.img = None
        self.img_new = None
        self.kernel = None
        self.path = StringVar()
        self.b0 = StringVar()
        self.b1 = StringVar()
        self.b2 = StringVar()
        self.b3 = StringVar()
        self.b4 = StringVar()
        self.b5 = StringVar()
        self.lang = IntVar()
        self.l1 = StringVar()
        self.l2 = StringVar()
        self.l3 = StringVar()
        self.k1 = StringVar()
        self.k2 = StringVar()
        self.k3 = StringVar()
        self.mask_type = IntVar()
        self.m1 = StringVar()
        self.m2 = StringVar()
        self.m3 = StringVar()
        self.m4 = StringVar()
        self.m5 = StringVar()
        self.m6 = StringVar()
        self.m7 = StringVar()
        self.mask_size = IntVar()
        self.w1 = DoubleVar()
        self.w2 = IntVar()
        self.frame1 = Frame(self.master)
        self.frame1.pack(side="top", pady=20)
        self.frame2 = Frame(self.master)
        self.frame2.pack(side="top")
        self.frame3 = Frame(self.master)
        self.frame3.pack(side="top")
        self.frame3a = Frame(self.frame3)
        self.frame3a.pack(side="left", padx=20)
        self.frame3b = Frame(self.frame3)
        self.frame3b.pack(side="left", padx=20)
        self.frame3c = Frame(self.frame3)
        self.frame3c.pack(side="left", padx=20)
        self.frame4 = Frame(self.master)
        self.frame4.pack(side="top", pady=15)
        self.image_frame = Frame(self.master)
        self.image_frame.pack(side="top", pady=20)
        self.kernel_frame = Frame(self.image_frame)
        self.kernel_frame.pack(side="right", pady=20)
        self.create_widgets()
        self.change_language()
        self.select_image()

    # function for creating widgets
    def create_widgets(self):
        labels = [self.l1, self.l2, self.l3]

        masks = [(102, self.m1),
                 (103, self.m2),
                 (105, self.m3),
                 (106, self.m4),
                 (107, self.m5),
                 (101, self.m6),
                 (104, self.m7)]

        sizes = [("3x3", 3),
                 ("5x5", 5),
                 ("7x7", 7),
                 ("9x9", 9),
                 ("11x11", 11)]

        buttons = [(lambda: self.select_image(1), self.b0),
                   (self.image_save, self.b1),
                   (self.image_swap, self.b2),
                   (self.image_noise, self.b5)]

        langs = [("English", 201, lambda: self.change_language()),
                 ("Polski", 202, lambda: self.change_language()),
                 ("Deutsch", 203, lambda: self.change_language()),
                 ("Español", 204, lambda: self.change_language()),
                 ("Українська", 205, lambda: self.change_language())]

        self.mask_size.set(3)
        self.mask_size.set(5)
        self.mask_type.set(102)
        self.lang.set(201)
        self.w1.set(0.5)
        self.w2.set(0)

        for comm, b in buttons:
            Button(self.frame1,
                   textvariable=b,
                   bg="#1976D2",
                   activeforeground="#2196F3",
                   command=comm).pack(side="left", fill="both", expand=1, padx="10", pady="10")

        Scale(self.frame1, from_=0.05, resolution=0.05, to=5, orient="horizontal", background="#1976D2", length="120",
              highlightcolor="#2196F3", variable=self.w1).pack(side="left", fill="both", expand=1, ipadx="10",
                                                               pady="10")

        Checkbutton(self.frame1,
                    textvariable=self.b3,
                    bg="#1976D2",
                    activeforeground="#2196F3",
                    variable=self.w2).pack(side="left", fill="both", expand=1, padx="10", pady="10")
        for label in labels:
            Label(self.frame2,
                  textvariable=label,
                  padx=20,
                  justify="left").pack(anchor="w", side="left")
        for val, m in masks:
            Radiobutton(self.frame3a,
                        textvariable=m,
                        padx=20,
                        variable=self.mask_type,
                        command=self.start,
                        activeforeground="#2196F3",
                        value=val).pack(anchor="w")

        for size, val in sizes:
            Radiobutton(self.frame3b,
                        text=size,
                        padx=20,
                        variable=self.mask_size,
                        command=self.start,
                        activeforeground="#2196F3",
                        value=val).pack(anchor="w")

        for t, val, comm in langs:
            Radiobutton(self.frame3c,
                        text=t,
                        padx=20,
                        variable=self.lang,
                        command=comm,
                        activeforeground="#2196F3",
                        value=val).pack(anchor="w")

    def show_kernel(self):
        if self.kernel_frame.slaves is not None:
            for g in self.kernel_frame.grid_slaves():
                g.grid_remove()
        if self.w2.get() and self.kernel is not None:
            m_size = self.mask_size.get()
            for i in range(m_size):
                for j in range(m_size):
                    g = Label(self.kernel_frame, text=f"{self.kernel[i][j]:.2f}", borderwidth=1, relief="solid",
                              width=(52 // m_size),
                              height=(26 // m_size))
                    g.grid(row=i, column=j)

    def change_language(self):
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
        typed = self.lang.get()
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

        self.master.title(dict1["k4"])
        self.m1.set(dict1["m1"])
        self.m2.set(dict1["m2"])
        self.m3.set(dict1["m3"])
        self.m4.set(dict1["m4"])
        self.m5.set(dict1["m5"])
        self.m6.set(dict1["m6"])
        self.m7.set(dict1["m7"])

        self.l1.set(dict1["l1"])
        self.l2.set(dict1["l2"])
        self.l3.set(dict1["l3"])

        self.b0.set(dict1["b0"])
        self.b1.set(dict1["b1"])
        self.b2.set(dict1["b2"])
        self.b3.set(dict1["b3"])
        self.b5.set(dict1["b5"])

    def image_swap(self):
        self.img = self.img_new
        self.show_image()

    def image_noise(self):
        mul = self.w1.get()
        gauss_noise = ones(self.img.shape, dtype=uint8)
        mean = ones(3, dtype=uint8) * 128
        dst = ones(3, dtype=uint8) * 20
        randn(gauss_noise, mean, dst)
        gauss_noise = (gauss_noise * mul).astype(uint8)
        self.img = add(self.img, gauss_noise)
        self.show_image()

    def start(self):
        # open a file chooser dialog and allow the user to select an input
        # image
        m_size = self.mask_size.get()
        m_type = self.mask_type.get()

        if m_type == 102:
            self.kernel = getStructuringElement(MORPH_RECT, (m_size, m_size))
            self.kernel = self.kernel / sum(self.kernel)
        if m_type == 105:
            self.kernel = getStructuringElement(MORPH_CROSS, (m_size, m_size))
            self.kernel = self.kernel / sum(self.kernel)
        elif m_type == 106:
            self.kernel = getStructuringElement(MORPH_ELLIPSE, (m_size, m_size))
            self.kernel = self.kernel / sum(self.kernel)
        elif m_type == 107:
            self.kernel = ones((m_size, m_size), dtype=uint8)
            self.kernel = self.kernel / sum(self.kernel)
            self.kernel[0, 0] = 0
            self.kernel[0, -1] = 0
            self.kernel[-1, 0] = 0
            self.kernel[-1, -1] = 0
        elif m_type == 101:
            self.img_new = medianBlur(self.img, m_size)
        elif m_type == 103:
            self.kernel = getGaussianKernel(m_size, 0)
            self.kernel = outer(self.kernel, self.kernel.transpose())
        elif m_type == 104:
            self.img_new = bilateralFilter(self.img, m_size, 75, 75)

        if m_type != 104 and m_type != 101:
            self.img_new = filter2D(self.img, -1, self.kernel)
        else:
            self.kernel = ones((m_size, m_size), uint8)

        img_new = self.img_new.astype(uint8)
        self.show_image()

    def image_save(self):
        file_path = asksaveasfilename(initialfile='image.png', defaultextension="*.png",
                                      filetypes=[("All Files", "*.*"), ("PNG", "*.png")])
        if file_path:
            with open(file_path, 'wb') as file:
                imwrite(file_path, self.img_new)
        assert file_path is not None, "file could not be write, check with os.path.exists()"

    def select_image(self, flag=0):
        if flag == 1:
            file_path = askopenfilename()
        else:
            file_path = "images/lena.bmp"
        if file_path:
            with open(file_path, "rb") as file:
                self.img = imread(file_path)
            height = 400
            self.img = resize(self.img, (int(height * (self.img.shape[1] / self.img.shape[0])), height))
            self.img_new = self.img
        assert self.img is not None, "file could not be read, check with os.path.exists()"
        self.start()

    def show_image(self):
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        img_show = cvtColor(self.img, COLOR_BGR2RGB)
        img_new_show = cvtColor(self.img_new, COLOR_BGR2RGB)

        # convert the images to PIL format...
        img_show = Image.fromarray(img_show)
        img_new_show = Image.fromarray(img_new_show)
        # ...and then to ImageTk format
        img_show = ImageTk.PhotoImage(img_show)
        img_new_show = ImageTk.PhotoImage(img_new_show)
        # if the panels are None, initialize them
        if self.panelA is None or self.panelB is None:
            # the first panel will store our original image
            self.panelA = Label(self.image_frame, image=img_show)
            self.panelA.image = img_show
            self.panelA.pack(side="left", padx=10, pady=10)
            # while the second panel will store the edge map
            self.panelB = Label(self.image_frame, image=img_new_show)
            self.panelB.image = img_new_show
            self.panelB.pack(side="right", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panelA.configure(image=img_show)
            self.panelB.configure(image=img_new_show)
            self.panelA.image = img_show
            self.panelB.image = img_new_show
        self.show_kernel()
        self.update()


def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
