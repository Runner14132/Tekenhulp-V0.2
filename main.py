from screens import MainScreen, Screens_Menu, Header
from dnp_screens import DnPDataScreen, DnPImageScreen
from tkinter import Tk

menu_list = [["Project",
               ("Nieuw", "Project - Nieuw"),
               ("Open", "Project - Open"),
               ("Open recent", "Project - Open recent"),
               ("Opslaan", "Project - Opslaan"),
               ("Opslaan als", "Project - Opslaan als"),
               ("Sluiten", "Project - Sluiten")],
              ["Mutaties",
               ("ING", "Mutaties - ING"),
               ("Open2", "File2 - Open2"),
               ("Save2", "File2 - Save2")],
              ["Stambestanden",
               ("Rubrieken", "Stambestanden - Rubrieken"),
               ("Verdelen", "File3 - Open3"),
               ("Save3", "File3 - Save3")],
              ["Budgetten",
               ("Definiëren periodes", "Budgetten - Definiëren budgetperiodes"),
               ("Budgetteren", "Budgetten - Budgetteren"),
               ("Save3", "File3 - Save3")]]


def nieuw_project():
    screen.clear_screen()
    header.show(root, text="Nieuw project")
    datascreen.show()
    imagescreen.config(image="", bg="#EEEEEE", linethickness="2", linecolor="#EEEEEE", image_center="True",
                       datascreenobject=datascreen)
    imagescreen.show_canvas()
    imagescreen.show_image()
    # imagescreen.load_image()


def menu_item_clicked(item):
    print("Menu item clicked:", item)
    if item == "Project - Nieuw":
        nieuw_project()
    elif item == "Project - Sluiten":
        screen.clear_screen()


def mainscreen():
    screen.show()
    menu = Screens_Menu(root, menu_items=menu_list, callback=menu_item_clicked)
    menu.show()

    nieuw_project()


if __name__ == '__main__':
    # Objecten definiëren
    root = Tk()
    screen = MainScreen(root, title="Tekenhulp Versie 2.0", bg="#FFFFFF", icon=".\\images\\colored-pencils.ico")
    header = Header()
    # Oude situatie
    # imagescreen = DnPImageScreen(root, 100, 80, 800, 800)
    # datascreen = DnPDataScreen(root, imagescreen, 1000, 80, 600, 800)

    # Nieuwe situatie
    imagescreen = DnPImageScreen(root, 100, 80, 800, 800, datascreenobject=None)
    datascreen = DnPDataScreen(root, 1000, 80, 600, 800, imagescreenobject=imagescreen)

    # Einde nieuwe situatie




    mainscreen()
    root.mainloop()

