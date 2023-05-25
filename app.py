from cv2 import imwrite, imread, cvtColor, COLOR_BGR2RGB, medianBlur, filter2D, resize, IMREAD_UNCHANGED

from os import getcwd

from tkinter import Button, Label, Radiobutton, StringVar, IntVar, Frame, Scale, DoubleVar, Checkbutton, font, Menu, \
    LabelFrame

from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename, asksaveasfilename

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from seaborn import set, heatmap

from pandas import DataFrame

from kernel import *

from noise import *

PADX_FRAME = 8
PADY_FRAME = 4
PADX_WIDGET = 4
PADY_WIDGET = 2
FOREGROUND_COLOR = "#2196F3"
BACKGORUND_COLOR = "#1976D2"
FONT_FAMILY = "Arial"
FONT_SIZE = 12
FONT_SIZE_KERNEL = 8
PLOT_SIZE = (4, 3)
IMG_SIZE = 300


class Application(Frame):
    # constructor
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('ans.ico')))
        self.master.minsize(800, 400)
        self.master.option_add("*Font", font.Font(family="Arial", size=13))

        self.panelA = None
        self.panelB = None
        self.panelC = None
        self.panelD = None
        self.img = None
        self.img_new = None

        self.mask_box = None
        self.start_button = None
        self.noise_scale = None
        self.add_swap_button = None
        self.add_noise_button = None

        self.noise = Noise()
        self.kernel = Kernel()
        self.noise_type = IntVar()
        self.path = StringVar()
        self.h1 = StringVar()
        self.h2 = StringVar()
        self.h3 = StringVar()
        self.n1 = StringVar()
        self.n2 = StringVar()
        self.n3 = StringVar()
        self.b0 = StringVar()
        self.b1 = StringVar()
        self.b2 = StringVar()
        self.b3 = StringVar()
        self.b4 = StringVar()
        self.b5 = StringVar()
        self.b6 = StringVar()
        self.lang = IntVar()
        self.l1 = StringVar()
        self.l2 = StringVar()
        self.l3 = StringVar()
        self.l4 = StringVar()
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
        self.w3 = IntVar()

        self.mainmenu = Menu(self.master)
        self.master.config(menu=self.mainmenu)
        # Menu 1
        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(command=self.select_image)
        self.filemenu.add_command(command=self.image_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.master.destroy)
        self.mainmenu.add_cascade(menu=self.filemenu)
        # Menu 2
        self.noise_menu = Menu(self.mainmenu, tearoff=0)
        self.noise_menu.add_radiobutton(variable=self.noise_type, value=301, activeforeground=FOREGROUND_COLOR,
                                        command=self.set_noise_type)
        self.noise_menu.add_radiobutton(variable=self.noise_type, value=302, activeforeground=FOREGROUND_COLOR,
                                        command=self.set_noise_type)
        self.noise_menu.add_separator()
        self.noise_menu.add_checkbutton(variable=self.w2, command=self.plot_noise)
        self.noise_menu.add_checkbutton(variable=self.w3, command=self.plot_kernel)
        self.mainmenu.add_cascade(menu=self.noise_menu)

        # Menu 3
        self.menu_3 = Menu(self.mainmenu, tearoff=0)
        self.menu_3.add_radiobutton(label="English", value=201, variable=self.lang, activeforeground=FOREGROUND_COLOR,
                                    command=self.change_language)
        self.menu_3.add_radiobutton(label="Polski", value=202, variable=self.lang, activeforeground=FOREGROUND_COLOR,
                                    command=self.change_language)
        self.menu_3.add_radiobutton(label="Deutsch", value=203, variable=self.lang, activeforeground=FOREGROUND_COLOR,
                                    command=self.change_language)
        self.menu_3.add_radiobutton(label="Español", value=204, variable=self.lang, activeforeground=FOREGROUND_COLOR,
                                    command=self.change_language)
        self.menu_3.add_radiobutton(label="Українська", value=205, variable=self.lang,
                                    activeforeground=FOREGROUND_COLOR, command=self.change_language)
        self.mainmenu.add_cascade(menu=self.menu_3)

        self.frame0 = Frame(self.master)
        self.frame1 = Frame(master=self.frame0, width=300)

        self.frame1_label1 = LabelFrame(self.frame1)
        self.frame1_label2 = LabelFrame(self.frame1)
        self.frame1_label3 = LabelFrame(self.frame1)
        # self.frame1_label4 = LabelFrame(self.frame1)
        self.frame1a = Frame(self.frame1)

        self.frame2 = Frame(self.frame0)
        self.frame2a = Frame(self.frame2)
        self.frame2b = Frame(self.frame2)

        self.frame2a1 = Frame(self.frame2a)
        self.frame2a2 = Frame(self.frame2a)
        self.frame2b1 = Frame(self.frame2b)
        self.frame2b2 = Frame(self.frame2b)

        self.frame0.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1.pack(side="left", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2.pack(side="left", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2a.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2b.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)

        self.frame2a1.pack(side="left", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2a2.pack(side="right", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2b1.pack(side="left", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame2b2.pack(side="right", pady=PADY_FRAME, padx=PADX_FRAME)

        self.create_widgets()
        self.change_language()
        self.select_image(1)
        self.start()
        self.plot_noise()
        self.plot_kernel()

    # function for creating widgets
    def create_widgets(self):
        masks = [(102, self.m1),
                 (103, self.m2),
                 (105, self.m3),
                 (106, self.m4),
                 (107, self.m5),
                 (101, self.m6), ]

        sizes = [("3x3", 3),
                 ("5x5", 5),
                 ("7x7", 7),
                 ("9x9", 9),
                 ("11x11", 11)]

        self.mask_size.set(3)
        self.mask_size.set(5)
        self.mask_type.set(102)
        self.noise_type.set(301)
        self.lang.set(201)
        self.w1.set(0.25)
        self.w2.set(1)
        self.w3.set(1)

        self.frame1_label1.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1_label2.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1_label3.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        # self.frame1_label4.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1a.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)

        for val, m in masks:
            Radiobutton(self.frame1_label1,
                        textvariable=m,
                        padx=PADX_WIDGET,
                        pady=PADY_WIDGET,
                        variable=self.mask_type,
                        command=self.set_kernel_type,
                        activeforeground=FOREGROUND_COLOR,
                        value=val).pack(anchor="w")

        for size, val in sizes:
            Radiobutton(self.frame1_label2,
                        text=size,
                        padx=PADX_WIDGET,
                        pady=PADY_WIDGET,
                        variable=self.mask_size,
                        command=self.set_kernel_size,
                        activeforeground=FOREGROUND_COLOR,
                        value=val).pack(anchor="w")

        self.noise_scale = Scale(self.frame1_label3, from_=0.01, resolution=0.01, to=1,
                                 orient="horizontal", background=BACKGORUND_COLOR, highlightcolor=FOREGROUND_COLOR,
                                 variable=self.w1, command=self.noise.set_mul)
        self.noise_scale.pack(side="top", fill="both", expand=1, padx=PADX_WIDGET, pady=PADY_WIDGET)

        self.add_noise_button = Button(self.frame1, textvariable=self.b5, bg=BACKGORUND_COLOR,
                                       activeforeground=FOREGROUND_COLOR, command=self.image_noise)
        self.add_noise_button.pack(side="right", fill="both", expand=1, padx=PADX_WIDGET, pady=PADY_WIDGET)

        self.add_swap_button = Button(self.frame1a, textvariable=self.b2, bg=BACKGORUND_COLOR,
                                      activeforeground=FOREGROUND_COLOR, command=self.image_swap)
        self.add_swap_button.pack(side="left", fill="both", expand=1, padx=PADX_WIDGET, pady=PADY_WIDGET)

        self.start_button = Button(self.frame1a, textvariable=self.b3, bg=BACKGORUND_COLOR,
                                   activeforeground=FOREGROUND_COLOR, command=self.start)
        self.start_button.pack(side="top", fill="both", expand=1, padx=PADX_WIDGET, pady=PADY_WIDGET)

    def set_kernel_type(self):
        self.kernel.set_type(self.mask_type.get())
        self.plot_kernel()

    def set_kernel_size(self):
        self.kernel.set_size(self.mask_size.get())
        self.plot_kernel()

    def set_noise_multiplier(self):
        self.noise.set_mul(self.w2.get())
        self.plot_noise()

    def set_noise_type(self):
        self.noise.set_type(self.noise_type.get())
        self.plot_noise()

    def change_language(self):
        ukr = {
            "l1": "Тип маски:",
            "l2": "Розмір маски:",
            "l3": "Мова",
            "l4": "Шум",
            "l5": "Файл",

            "k1": "Маска:",
            "k2": "Вхід:",
            "k3": "Вихід:",
            "k4": "Інструмент налаштування зображення",

            "m1": "Середнє",
            "m2": "Гауссівське",
            "m3": "Креслення",
            "m4": "Еліпс",
            "m5": "Трапеція",
            "m6": "Медіана",
            "m7": "Білатеральне",

            "b0": "Вибрати зображення",
            "b1": "Зберегти зображення як",
            "b2": "Замінити зображення",
            "b10": "Вихід",

            "b3": "Фільтрувати",
            "b5": "Додати шум",
            "b6": "Показати гістограму шуму",
            "b7": "Показати маску",

            "b4": "Рівень шуму",

            "n1": "Гауссівський",
            "n2": "Сіль і перець",

            "h1": "Значення пікселя",
            "h2": "Щільність",
            "h3": "Розподіл шуму",
        }

        esp = {
            "l1": "Tipo de máscara:",
            "l2": "Tamaño de la máscara:",
            "l3": "Idioma",
            "l4": "Ruido",
            "l5": "Archivo",

            "k1": "Máscara:",
            "k2": "Entrada:",
            "k3": "Salida:",
            "k4": "Herramienta de ajuste de",

            "m1": "Promedio",
            "m2": "Gaussiana",
            "m3": "Cruz",
            "m4": "Elipse",
            "m5": "Trapecio",
            "m6": "Mediana",
            "m7": "Bilateral",

            "b0": "Seleccionar imagen",
            "b1": "Guardar imagen como",
            "b2": "Intercambiar imagen",
            "b10": "Salir",

            "b3": "Filtrar",
            "b5": "Agregar ruido",
            "b6": "Mostrar histograma de ruido",
            "b7": "Mostrar máscara",

            "b4": "Nivel de ruido",

            "n1": "Gaussiano",
            "n2": "Sal y pimienta",

            "h1": "Valor del píxel",
            "h2": "Densidad",
            "h3": "Distribución del ruido",
        }

        ger = {
            "l1": "Maskentyp:",
            "l2": "Maskengröße:",
            "l3": "Sprache",
            "l4": "Rauschen",
            "l5": "Datei",

            "k1": "Maske:",
            "k2": "Eingabe:",
            "k3": "Ausgabe:",
            "k4": "Bildanpassungswerkzeug",

            "m1": "Durchschnitt",
            "m2": "Gaussisch",
            "m3": "Kreuz",
            "m4": "Ellipse",
            "m5": "Trapez",
            "m6": "Median",
            "m7": "Bilateral",

            "b0": "Bild auswählen",
            "b1": "Bild speichern als",
            "b2": "Bild austauschen",
            "b10": "Beenden",

            "b3": "Filtern",
            "b5": "Rauschen hinzufügen",
            "b6": "Rauschhistogramm anzeigen",
            "b7": "Maske anzeigen",

            "b4": "Rauschpegel",

            "n1": "Gaussisch",
            "n2": "Salz und Pfeffer",

            "h1": "Pixelwert",
            "h2": "Dichte",
            "h3": "Verteilung des Rauschens",
        }

        pol = {
            "l1": "Rodzaj maski:",
            "l2": "Rozmiar maski:",
            "l3": "Język",
            "l4": "Szum",
            "l5": "Plik",

            "k1": "Maska:",
            "k2": "Wejście:",
            "k3": "Wyjście:",
            "k4": "Narzędzie do dostosowania obrazu",

            "m1": "Średnia",
            "m2": "Gaussowska",
            "m3": "Krzyżowa",
            "m4": "Elipsa",
            "m5": "Trapez",
            "m6": "Mediana",
            "m7": "Bilateralna",

            "b0": "Wybierz obraz",
            "b1": "Zapisz obraz jako",
            "b2": "Zamień obraz",
            "b10": "Wyjście",

            "b3": "Filtruj",
            "b5": "Dodaj szum",
            "b6": "Pokaż histogram szumu",
            "b7": "Pokaż maskę",

            "b4": "Poziom szumu",

            "n1": "Gaussowski",
            "n2": "Sól i pieprz",

            "h1": "Wartość piksela",
            "h2": "Gęstość",
            "h3": "Rozkład szumu",
        }

        eng = {
            "l1": "Kernel type:",
            "l2": "Kernel size:",
            "l3": "Language",
            "l4": "Noise",
            "l5": "File",

            "k1": "Kernel:",
            "k2": "Input:",
            "k3": "Output:",
            "k4": "Image adjustment tool",

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
            "b10": "Exit",

            "b3": "Filter",
            "b5": "Add noise",
            "b6": "Show noise histogram",
            "b7": "Show kernel",

            "b4": "Noise Level",

            "n1": "Gaussian",
            "n2": "Salt and pepper",

            "h1": "Pixel value",
            "h2": "Density",
            "h3": "Distribution of noise",
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

        self.h1.set(dict1["h1"])
        self.h2.set(dict1["h2"])
        self.h3.set(dict1["h3"])

        self.b2.set(dict1["b2"])
        self.b3.set(dict1["b3"])
        self.b5.set(dict1["b5"])

        self.mainmenu.entryconfigure(1, label=dict1["l5"])
        self.mainmenu.entryconfigure(2, label=dict1["l4"])
        self.mainmenu.entryconfigure(3, label=dict1["l3"])

        self.filemenu.entryconfigure(0, label=dict1["b0"])
        self.filemenu.entryconfigure(1, label=dict1["b1"])
        self.filemenu.entryconfigure(4, label=dict1["b10"])

        self.noise_menu.entryconfigure(0, label=dict1["n1"])
        self.noise_menu.entryconfigure(1, label=dict1["n2"])
        self.noise_menu.entryconfigure(3, label=dict1["b6"])
        self.noise_menu.entryconfigure(4, label=dict1["b7"])

        # self.noise_scale.configure(label=dict1["b4"])

        self.frame1_label1.configure(text=dict1["l1"])
        self.frame1_label2.configure(text=dict1["l2"])
        self.frame1_label3.configure(text=dict1["b4"])
        # self.frame1_label4.configure(text=dict1["l4"])

    def image_swap(self):
        self.img = self.img_new
        self.show_image()

    def image_noise(self):
        self.img_new = self.noise.image_noise(self.img)
        self.show_image()

    def plot_noise(self):
        if self.panelC is not None:
            self.panelC.get_tk_widget().destroy()
        if self.w2.get() == 1:
            fig, ax = plt.subplots(figsize=PLOT_SIZE)
            if self.noise.channels == 1:
                hist_colors = ['darkblue']
            else:
                hist_colors = ['blue', 'red', 'green']
            ax.hist(self.noise.noise[0], bins='auto', density=True, color=hist_colors)
            # ax.set_xlabel(self.h1.get())
            # ax.set_ylabel(self.h2.get())
            ax.set_title(self.h3.get())
            self.panelC = FigureCanvasTkAgg(fig, self.frame2b1)
            self.panelC.draw()
            self.panelC.get_tk_widget().pack(padx=PADX_WIDGET, pady=PADY_WIDGET, expand=1)
            plt.close()

    def plot_kernel(self):
        if self.panelD is not None:
            self.panelD.get_tk_widget().destroy()
        if self.w3.get() == 1:
            df_cm = DataFrame(self.kernel.get_teo_kernel())
            plt.figure(figsize=PLOT_SIZE)
            set(font_scale=1.2)  # for label size
            heatmap(df_cm, annot=True, annot_kws={"size": FONT_SIZE_KERNEL})  # font size
            if self.panelD is not None:
                self.panelD.get_tk_widget().destroy()
            self.panelD = FigureCanvasTkAgg(plt.gcf(), self.frame2a1)
            self.panelD.draw()
            self.panelD.get_tk_widget().pack(padx=PADX_WIDGET, pady=PADY_WIDGET, fill="both", expand=1)
            plt.close()

    def start(self):
        if self.kernel.type == 101:
            self.img_new = medianBlur(self.img, self.kernel.size).astype(uint8)
        else:
            self.img_new = filter2D(self.img, -1, self.kernel.get_real_kernel()).astype(uint8)
        self.show_image()

    def image_save(self):
        file_path = asksaveasfilename(initialdir=getcwd() + "/images/", initialfile='new_image.png',
                                      defaultextension="*.png", title=self.b1.get(),
                                      filetypes=[("All Files", "*.*"), ("PNG", "*.png"), ("JPG", "*.jpg"),
                                                 ("BMP", "*.bmp")])
        if file_path:
            with open(file_path, 'wb'):
                imwrite(file_path, self.img_new)
        assert file_path is not None, "file could not be write, check with os.path.exists()"

    def select_image(self, flag=0):
        if flag == 0:
            file_path = askopenfilename(initialdir=getcwd() + "/images/", initialfile='lena.bmp', title=self.b0.get(),
                                        filetypes=[("All Files", "*.*"), ("PNG", "*.png"), ("JPG", "*.jpg"),
                                                   ("BMP", "*.bmp")])
        else:
            file_path = "images/lena.bmp"
        if file_path:
            with open(file_path, "rb"):
                self.img = imread(file_path, IMREAD_UNCHANGED)
            self.img = resize(self.img, (int(IMG_SIZE * (self.img.shape[1] / self.img.shape[0])), IMG_SIZE))
            self.img_new = self.img
        assert self.img is not None, "file could not be read, check with os.path.exists()"
        self.show_image()
        self.noise.set_size(self.img.shape)
        self.plot_noise()

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
            self.panelA = Label(self.frame2a2, image=img_show)
            self.panelA.image = img_show
            self.panelA.pack(padx=PADX_WIDGET, pady=PADY_WIDGET)
            # while the second panel will store the edge map
            self.panelB = Label(self.frame2b2, image=img_new_show)
            self.panelB.image = img_new_show
            self.panelB.pack(padx=PADX_WIDGET, pady=PADY_WIDGET)
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panelA.configure(image=img_show)
            self.panelB.configure(image=img_new_show)
            self.panelA.image = img_show
            self.panelB.image = img_new_show
