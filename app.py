from cv2 import imwrite, imread, cvtColor, COLOR_BGR2RGB, medianBlur, filter2D, resize, IMREAD_UNCHANGED

from os import getcwd

from tkinter import Button, Label, Radiobutton, StringVar, IntVar, Frame, Scale, DoubleVar, font, Menu, \
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
PADY_FRAME = 5
PADX_WIDGET = 4
PADY_WIDGET = 2
FOREGROUND_COLOR = "#32CD32"
BACKGROUND_COLOR = "#228B22"
FONT_FAMILY = "Thaoma"
FONT_SIZE = 15  # 21
FONT_SIZE_KERNEL = 12
FONT_SIZE_TITLE = 35
PLOT_SIZE = (5.75, 4.9)
IMG_SIZE = 575


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack()
        self.master.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('ans.ico')))
        self.master.minsize(800, 400)
        self.master.option_add("*Font", font.Font(family=FONT_FAMILY, size=FONT_SIZE))

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
        self.frame0_title_label = None
        self.noise_type_label_1 = None
        self.noise_type_label_2 = None

        self.noise = Noise()
        self.kernel = Kernel()
        self.noise_type = IntVar()
        self.path = StringVar()

        self.h1 = StringVar()
        self.h2 = StringVar()
        self.h3 = StringVar()
        self.n1 = StringVar()
        self.n2 = StringVar()
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
        self.k4 = StringVar()
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

        self.mainmenu = Menu(self.master, activeforeground=FOREGROUND_COLOR)
        self.master.config(menu=self.mainmenu)
        # Menu 1
        self.filemenu = Menu(self.mainmenu, tearoff=0, activeforeground=FOREGROUND_COLOR)
        self.filemenu.add_command(command=self.select_image)
        self.filemenu.add_command(command=self.image_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.master.destroy)
        self.mainmenu.add_cascade(menu=self.filemenu)
        # Menu 2
        self.optionsmenu = Menu(self.mainmenu, tearoff=0, activeforeground=FOREGROUND_COLOR)
        self.optionsmenu.add_checkbutton(variable=self.w2, command=self.plot_noise)
        self.optionsmenu.add_separator()
        self.optionsmenu.add_checkbutton(variable=self.w3, command=self.plot_kernel)
        self.mainmenu.add_cascade(menu=self.optionsmenu)

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
        self.menu_3.add_radiobutton(label="Italiano", value=206, variable=self.lang,
                                    activeforeground=FOREGROUND_COLOR, command=self.change_language)
        self.menu_3.add_radiobutton(label="中文", value=207, variable=self.lang,
                                    activeforeground=FOREGROUND_COLOR, command=self.change_language)
        self.mainmenu.add_cascade(menu=self.menu_3)

        self.frame0 = Frame(self.master)
        self.frame0_title = Frame(self.frame0)
        self.frame1 = Frame(master=self.frame0, width=280)

        self.frame1_label1 = LabelFrame(self.frame1)
        self.frame1_label2 = LabelFrame(self.frame1)
        self.frame1_label3 = LabelFrame(self.frame1)
        self.frame1_label4 = LabelFrame(self.frame1)

        self.frame1a = Frame(self.frame1)

        self.frame2 = Frame(self.frame0)
        self.frame2a = Frame(self.frame2)
        self.frame2b = Frame(self.frame2)

        self.frame2a1 = Frame(self.frame2a)
        self.frame2a2 = Frame(self.frame2a)
        self.frame2b1 = Frame(self.frame2b)
        self.frame2b2 = Frame(self.frame2b)

        self.frame0.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame0_title.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)

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
        self.w1.set(0.5)
        self.w2.set(1)
        self.w3.set(1)

        self.frame0_title_label = Label(self.frame0_title, textvariable=self.k4, padx=PADX_WIDGET,
                                        pady=PADY_WIDGET, font=(FONT_FAMILY, FONT_SIZE_TITLE))
        self.frame0_title_label.pack(side="top", pady=PADY_FRAME, padx=PADX_FRAME)

        self.frame1_label1.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1_label2.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1_label3.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)
        self.frame1_label4.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)

        self.frame1a.pack(side="top", fill="both", pady=PADY_FRAME, padx=PADX_FRAME)

        for val, m in masks:
            Radiobutton(self.frame1_label1,
                        textvariable=m,
                        padx=PADX_WIDGET,
                        pady=PADY_WIDGET,
                        font=(FONT_FAMILY, FONT_SIZE),
                        variable=self.mask_type,
                        command=self.set_kernel_type,
                        activeforeground=FOREGROUND_COLOR,
                        value=val).pack(anchor="w")

        for size, val in sizes:
            Radiobutton(self.frame1_label2,
                        text=size,
                        padx=PADX_WIDGET,
                        pady=PADY_WIDGET,
                        font=(FONT_FAMILY, FONT_SIZE),
                        variable=self.mask_size,
                        command=self.set_kernel_size,
                        activeforeground=FOREGROUND_COLOR,
                        value=val).pack(anchor="w")

        self.noise_type_label_1 = Radiobutton(self.frame1_label3,
                                              textvariable=self.n1,
                                              padx=PADX_WIDGET,
                                              pady=PADY_WIDGET,
                                              font=(FONT_FAMILY, FONT_SIZE),
                                              variable=self.noise_type,
                                              command=self.set_noise_type,
                                              activeforeground=FOREGROUND_COLOR,
                                              value=301)
        self.noise_type_label_1.pack(anchor="w")

        self.noise_type_label_2 = Radiobutton(self.frame1_label3,
                                              textvariable=self.n2,
                                              padx=PADX_WIDGET,
                                              pady=PADY_WIDGET,
                                              font=(FONT_FAMILY, FONT_SIZE),
                                              variable=self.noise_type,
                                              command=self.set_noise_type,
                                              activeforeground=FOREGROUND_COLOR,
                                              value=302)
        self.noise_type_label_2.pack(anchor="w")

        self.noise_scale = Scale(self.frame1_label4, from_=0.01, resolution=0.01, to=1,
                                 orient="horizontal", font=(FONT_FAMILY, FONT_SIZE),
                                 background=BACKGROUND_COLOR, highlightcolor=FOREGROUND_COLOR,
                                 variable=self.w1, command=self.set_noise_multiplier)
        self.noise_scale.pack(side="top", fill="both", padx=PADX_WIDGET, pady=PADY_WIDGET)

        self.add_noise_button = Button(self.frame1, textvariable=self.b5, bg=BACKGROUND_COLOR,
                                       activeforeground=FOREGROUND_COLOR, command=self.image_noise,
                                       font=(FONT_FAMILY, FONT_SIZE))
        self.add_noise_button.pack(side="top", fill="y", expand=0, padx=PADX_WIDGET, pady=PADY_WIDGET)

        self.start_button = Button(self.frame1, textvariable=self.b3, bg=BACKGROUND_COLOR,
                                   font=(FONT_FAMILY, (FONT_SIZE + 5)),
                                   activeforeground=FOREGROUND_COLOR, command=self.start)
        self.start_button.pack(side="top", fill="both", expand=1, padx=0, pady=0)

        self.add_swap_button = Button(self.frame1, textvariable=self.b2, bg=BACKGROUND_COLOR,
                                      activeforeground=FOREGROUND_COLOR, command=self.image_swap,
                                      font=(FONT_FAMILY, FONT_SIZE))
        self.add_swap_button.pack(side="top", fill="y", expand=0, padx=PADX_WIDGET, pady=PADY_WIDGET)

    def set_kernel_type(self):
        self.kernel.set_type(self.mask_type.get())
        self.plot_kernel()

    def set_kernel_size(self):
        self.kernel.set_size(self.mask_size.get())
        self.plot_kernel()

    def set_noise_multiplier(self, mul1):
        self.noise.set_mul(mul1)

    def set_noise_type(self):
        self.noise.set_type(self.noise_type.get())
        self.plot_noise()

    def change_language(self):
        ukr = {
            "l1": "Тип маски:",
            "l2": "Розмір маски:",
            "l3": "Мова",
            "l4": "Тип шуму",
            "l5": "Файл",
            "l6": "Параметри",

            "k1": "Маска:",
            "k2": "Вхід:",
            "k3": "Вихід:",
            "k4": "Покращення зображення",

            "m1": "Середнє",
            "m2": "Гауссівське",
            "m3": "Креслення",
            "m4": "Еліпс",
            "m5": "Трапеція",
            "m6": "Медіана",

            "b0": "Вибрати зображення",
            "b1": "Зберегти зображення як",
            "b2": "Замінити зображення",
            "b10": "Вийти",

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
            "l4": "Tipo de ruido",
            "l5": "Archivo",
            "l6": "Opciones",

            "k1": "Máscara:",
            "k2": "Entrada:",
            "k3": "Salida:",
            "k4": "Mejora de imagen",

            "m1": "Promedio",
            "m2": "Gaussiana",
            "m3": "Cruz",
            "m4": "Elipse",
            "m5": "Trapecio",
            "m6": "Mediana",

            "b0": "Seleccionar imagen",
            "b1": "Guardar imagen como",
            "b2": "Cambiar imagen",
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

        ita = {
            "l1": "Tipo di kernel:",
            "l2": "Dimensione del kernel:",
            "l3": "Lingua",
            "l4": "Tipo di rumore",
            "l5": "File",
            "l6": "Opzioni",

            "k1": "Kernel:",
            "k2": "Input:",
            "k3": "Output:",
            "k4": "Miglioramento immagine",

            "m1": "Media",
            "m2": "Gaussiano",
            "m3": "Croce",
            "m4": "Ellisse",
            "m5": "Trapezio",
            "m6": "Mediana",

            "b0": "Seleziona immagine",
            "b1": "Salva immagine come",
            "b2": "Scambia immagine",
            "b10": "Esci",

            "b3": "Filtra",
            "b5": "Aggiungi rumore",
            "b6": "Mostra istogramma del rumore",
            "b7": "Mostra kernel",

            "b4": "Livello di rumore",

            "n1": "Gaussiano",
            "n2": "Sale e pepe",

            "h1": "Valore del pixel",
            "h2": "Densità",
            "h3": "Distribuzione del rumore",
        }

        ger = {
            "l1": "Maskentyp:",
            "l2": "Maskengröße:",
            "l3": "Sprache",
            "l4": "Rauschtyp",
            "l5": "Datei",
            "l6": "Optionen",

            "k1": "Maske:",
            "k2": "Eingabe:",
            "k3": "Ausgabe:",
            "k4": "Bildverbesserung",

            "m1": "Durchschnitt",
            "m2": "Gauß",
            "m3": "Kreuz",
            "m4": "Ellipse",
            "m5": "Trapez",
            "m6": "Median",

            "b0": "Bild auswählen",
            "b1": "Bild speichern als",
            "b2": "Bild austauschen",
            "b10": "Beenden",

            "b3": "Filtern",
            "b5": "Rauschen hinzufügen",
            "b6": "Rauschhistogramm anzeigen",
            "b7": "Maske anzeigen",

            "b4": "Rauschpegel",

            "n1": "Gauß",
            "n2": "Salz und Pfeffer",

            "h1": "Pixelwert",
            "h2": "Dichte",
            "h3": "Verteilung des Rauschens",
        }

        chi = {
            "l1": "内核类型：",
            "l2": "内核大小：",
            "l3": "语言",
            "l4": "噪声类型",
            "l5": "文件",
            "l6": "选项",

            "k1": "内核：",
            "k2": "输入：",
            "k3": "输出：",
            "k4": "图像增强",

            "m1": "平均",
            "m2": "高斯",
            "m3": "交叉",
            "m4": "椭圆",
            "m5": "梯形",
            "m6": "中值",

            "b0": "选择图像",
            "b1": "另存为图像",
            "b2": "交换图像",
            "b10": "退出",

            "b3": "滤波",
            "b5": "添加噪声",
            "b6": "显示噪声直方图",
            "b7": "显示内核",

            "b4": "噪声级别",

            "n1": "高斯",
            "n2": "椒盐",

            "h1": "像素值",
            "h2": "密度",
            "h3": "噪声分布",
        }

        pol = {
            "l1": "Rodzaj maski:",
            "l2": "Rozmiar maski:",
            "l3": "Język",
            "l4": "Szum",
            "l5": "Plik",
            "l6": "Opcje",

            "k1": "Maska:",
            "k2": "Wejście:",
            "k3": "Wyjście:",
            "k4": "Filtracja obrazu",

            "m1": "Średnia",
            "m2": "Gaussowska",
            "m3": "Krzyżowa",
            "m4": "Elipsa",
            "m5": "Trapez",
            "m6": "Mediana",

            "b0": "Wybierz obraz",
            "b1": "Zapisz obraz jako",
            "b2": "Zamień obraz",
            "b10": "Zakończ",

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
            "l4": "Noise type",
            "l5": "File",
            "l6": "Options",

            "k1": "Kernel:",
            "k2": "Input:",
            "k3": "Output:",
            "k4": "Image enhancement",

            "m1": "Average",
            "m2": "Gaussian",
            "m3": "Cross",
            "m4": "Eclipse",
            "m5": "Trapezoid",
            "m6": "Median",

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
        elif typed == 206:
            dict1 = ita
        elif typed == 207:
            dict1 = chi
        else:
            dict1 = eng

        self.master.title(dict1["k4"])
        self.k4.set(dict1["k4"])
        self.m1.set(dict1["m1"])
        self.m2.set(dict1["m2"])
        self.m3.set(dict1["m3"])
        self.m4.set(dict1["m4"])
        self.m5.set(dict1["m5"])
        self.m6.set(dict1["m6"])

        self.h1.set(dict1["h1"])
        self.h2.set(dict1["h2"])
        self.h3.set(dict1["h3"])

        self.n1.set(dict1["n1"])
        self.n2.set(dict1["n2"])

        self.b2.set(dict1["b2"])
        self.b3.set(dict1["b3"])
        self.b5.set(dict1["b5"])

        self.mainmenu.entryconfigure(1, label=dict1["l5"])
        self.mainmenu.entryconfigure(2, label=dict1["l6"])
        self.mainmenu.entryconfigure(3, label=dict1["l3"])

        self.filemenu.entryconfigure(0, label=dict1["b0"])
        self.filemenu.entryconfigure(1, label=dict1["b1"])
        self.filemenu.entryconfigure(4, label=dict1["b10"])

        self.optionsmenu.entryconfigure(0, label=dict1["b6"])
        self.optionsmenu.entryconfigure(2, label=dict1["b7"])

        self.frame1_label1.configure(text=dict1["l1"], font=(FONT_FAMILY, FONT_SIZE))
        self.frame1_label2.configure(text=dict1["l2"], font=(FONT_FAMILY, FONT_SIZE))
        self.frame1_label4.configure(text=dict1["b4"], font=(FONT_FAMILY, FONT_SIZE))
        self.frame1_label3.configure(text=dict1["l4"], font=(FONT_FAMILY, FONT_SIZE))

        self.plot_noise()

    def image_swap(self):
        self.img = self.img_new
        self.show_image()

    def image_noise(self):
        self.img_new = self.noise.image_noise(self.img)
        self.img_new = clip(self.img_new - (96 * self.w1.get()), 0, 255).astype(uint8)
        self.show_image()
        self.plot_noise()

    def plot_noise(self):
        if self.panelC is not None:
            self.panelC.get_tk_widget().destroy()
        if self.w2.get() == 1:
            fig, ax = plt.subplots(figsize=PLOT_SIZE)
            if self.noise.channels == 1:
                hist_colors = [BACKGROUND_COLOR]
            else:
                hist_colors = ['blue', 'red', 'green']
            ax.hist(self.noise.noise[0], bins='auto', density=True, color=hist_colors)
            ax.axis([0, 255, None, None])  # Oś x od 0 do 255
            ax.yaxis.set_visible(False)
            # ax.set_xlabel(self.h1.get())
            # ax.set_ylabel(self.h2.get())
            ax.set_title(self.h3.get(), fontsize=FONT_SIZE)
            self.panelC = FigureCanvasTkAgg(fig, self.frame2b2)
            self.panelC.draw()
            self.panelC.get_tk_widget().pack(padx=PADX_WIDGET, pady=PADY_WIDGET, expand=1)
            plt.close()

    def plot_kernel(self):
        if self.panelD is not None:
            self.panelD.get_tk_widget().destroy()
        if self.w3.get() == 1:
            df_cm = DataFrame(self.kernel.get_teo_kernel())
            plt.figure(figsize=PLOT_SIZE)
            set(font_scale=1.35)  # for label size
            heatmap(df_cm, annot=True, annot_kws={"size": FONT_SIZE_KERNEL}, fmt=".1g", square=True)  # font size
            if self.panelD is not None:
                self.panelD.get_tk_widget().destroy()
            self.panelD = FigureCanvasTkAgg(plt.gcf(), self.frame2b1)
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
                                      filetypes=[("All Files", "*.*"), ("PNG", "*.png"), ("JPEG", "*.jpeg;*.jpg"),
                                                 ("BMP", "*.bmp")])
        if file_path:
            with open(file_path, 'wb'):
                imwrite(file_path, self.img_new)
        assert file_path is not None, "file could not be write, check with os.path.exists()"

    def select_image(self, flag=0):
        if flag == 0:
            file_path = askopenfilename(initialdir=getcwd() + "/images/", initialfile='lena.bmp', title=self.b0.get(),
                                        filetypes=[("All Files", "*.*"), ("PNG", "*.png"), ("JPEG", "*.jpeg;*.jpg"),
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
        img_show = cvtColor(self.img, COLOR_BGR2RGB)
        img_new_show = cvtColor(self.img_new, COLOR_BGR2RGB)
        img_show = Image.fromarray(img_show)
        img_new_show = Image.fromarray(img_new_show)
        img_show = ImageTk.PhotoImage(img_show)
        img_new_show = ImageTk.PhotoImage(img_new_show)
        if self.panelA is None or self.panelB is None:
            self.panelA = Label(self.frame2a1, image=img_show)
            self.panelA.image = img_show
            self.panelA.pack(padx=PADX_WIDGET, pady=PADY_WIDGET)
            self.panelB = Label(self.frame2a2, image=img_new_show)
            self.panelB.image = img_new_show
            self.panelB.pack(padx=PADX_WIDGET, pady=PADY_WIDGET)
        else:
            self.panelA.configure(image=img_show)
            self.panelB.configure(image=img_new_show)
            self.panelA.image = img_show
            self.panelB.image = img_new_show
