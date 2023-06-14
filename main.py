__author__ = "Kamil Rataj"
__credits__ = ["Marcin Golonka", "Jakub Jędrychowski"]
__version__ = "1.0.1"
__maintainer__ = "Kamil Rataj"
__email__ = "kamilr616@gmail.com"


from tkinter import Tk

from app import *


def main():
    root = Tk(className="poc")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
