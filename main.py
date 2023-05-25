from tkinter import Tk

from app import *


def main():
    root = Tk(className="poc")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
