import tkinter
from tkinter import Menu, Frame, Label, ttk


class MainScreen:
    """Hoofdscherm"""

    def __init__(self, screen, **kwargs):
        self.window = screen
        self.window.state("zoomed")
        self.title = "Hallo"
        self.mainscreen_color = "#DDDDDD"
        self.mainscreen_icon = "euro-icon.ico"
        self.bg_image = ""
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.header_background = "#AFD7FF"
        self.header_foreground = "#0E66BE"
        self.config(**kwargs)

    def config(self, **kwargs):
        if kwargs.get("title"):
            self.title = kwargs.get("title", self.title)
            self.window.title(self.title)
        if kwargs.get("bg"):
            self.mainscreen_color = kwargs.get("bg", self.mainscreen_color)
            self.window.config(bg=self.mainscreen_color)
        if kwargs.get("icon"):  # TODO: Deze werkt nog niet
            self.mainscreen_icon = kwargs.get("icon", self.mainscreen_icon)
            try:
                self.window.iconbitmap(self.mainscreen_icon)
            except:
                raise Exception("Het bestand '" + self.mainscreen_icon + "' bestaat niet!")
        
    def show(self):
        self.window.title(self.title)
        self.window.config(bg=self.mainscreen_color)
        try:
            self.window.iconbitmap(self.mainscreen_bitmap)
        except:
            pass
        
    def get_screensize(self):
        return self.screen_width, self.screen_height
        

    def clear_screen(self):
        for widget in self.window.winfo_children():
            if widget.winfo_class() != 'Menu':
                widget.destroy()

    def annuleren(self):
        self.clear_screen()

class Screens_Menu:
    def __init__(self, screen, menu_items, callback, **kwargs):
        self.window = screen
        self.menu_items = menu_items
        self.callback = callback
        self.menu_keuze = ""
        self.config(**kwargs)
        
    def config(self, **kwargs):
        if kwargs.get("menu_items"):
            self.menu_items = kwargs.get("menu_items", self.menu_items)

    def show(self):
        menubar = Menu(self.window)
        for menu_item in self.menu_items:
            submenu_label, submenu_items = menu_item[0], menu_item[1:]
            filemenu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label=submenu_label, menu=filemenu)
            for submenu in submenu_items:
                label, command = submenu
                filemenu.add_command(label=label, command=lambda cmd=command: self.callback(cmd))
        self.window.config(menu=menubar)

class Header:
    def __init__(self):
        self.window = None
        self.text = "No text"
        self.height = 45
        self.width = 560
        self.font_type = "Arial"
        self.font_size = 20
        self.font_weight = "bold"
        self.font_color = "#FFFFFF"
        self.x = 0,
        self.y = 0,
        self.bg_color = "#DDDDDD"

    def show(self, screen, **kwargs):
        self.window = screen
        self.config(**kwargs)
        header_frame = Frame(self.window,
                             width=self.width,
                             height=self.height,
                             background=self.bg_color)
        header_frame.place(x=0, y=0)
        header_label = Label(header_frame, text=self.text,
                             font=(self.font_type, self.font_size, self.font_weight),
                             background=self.bg_color,
                             foreground=self.font_color,
                             anchor="w")
        header_label.place(x=10, y=int((self.height-self.font_size)/5))
        
    def config(self, **kwargs):
        if kwargs.get("text"):
            self.text = kwargs.get("text", self.text)
        if kwargs.get("width"):
            self.width = kwargs.get("width", self.width)
        else:
            self.width = self.window.winfo_screenwidth()



        
if __name__ == '__main__':
    pass