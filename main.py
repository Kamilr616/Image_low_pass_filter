from tkinter import Tk

from app import *


def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
