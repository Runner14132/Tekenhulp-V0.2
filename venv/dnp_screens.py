#               dnp staat voor Draw and Paint

# Opmerking 1:  Deze constructie gedaan omdat het blijkbaar niet mogelijk is boolean variabelen
#               als kwarg mee te geven. Daarom een string "True" of "False" meegeven en deze bij
#               het afvangen omzetten naar boolean


from tkinter import (Menu, Frame, ttk, Canvas, Checkbutton, Spinbox, IntVar, StringVar, filedialog, Button, Label,
                     Entry, RIDGE, SUNKEN, DISABLED, ACTIVE, messagebox)
from PIL     import Image, ImageTk, ImageEnhance, ImageDraw
from pathlib import Path
from screens import MainScreen


class DnPDataScreen:
    def __init__(self, on_top_of, x, y, width, height, imagescreenobject):
        self.window = on_top_of                     # Waar komt het DnP datascreen op te staan. Meestal Root
        self.image_screen = imagescreenobject       # Om variabelen op het image_screen te kunnen adresseren
        self.main_screen = MainScreen(on_top_of)
        self.pos_x = x                              # De x-positie van het datascreen
        self.pos_y = y                              # De y-positie van het datascreen
        self.width = width                          # De breedte van het datascreen
        self.height = height                        # De hoogte van het datascreen
        self.background="#FFFFFF"                   # De achtergrondkleur van het datascreen
        self.b_w_var = IntVar()                     # Variabele die gebruikt wordt om aan te geven of de afbeelding
                                                    # zwart/wit (=1) of kleur (=0) is
        self.luminance_value = StringVar()          # Variabele voor de helderheid van de afbeelding (-10 t/m 10)
        self.old_image = ""                         # Wordt gebruikt bij het laden van een afbeelding of er een nieuwe
                                                    # afbeelding geladen is
        self.actual_image = ""                      # De afbeelding waarmee geweerkt wordt
        self.papierbreedte = StringVar()            # Opgegeven waarde voor de breedte van het papier in mm
        self.papierhoogte = StringVar()             # Opgegeven waarde voor de hoogte van het papier in mm
        self.verhouding = -1                        # verhouding is papierbreedte / papierhoogte
        self.crop_x1 = StringVar()                  # Tijdelijke variabelen die de cropwaarden op het scherm tonen
        self.crop_y1 = StringVar()                  # Wordt dus gebruikt voor testdoeleinden
        self.crop_x2 = StringVar()
        self.crop_y2 = StringVar()

    def show(self):
        # Wat variabelen maken om later makkelijker de layout aan te kunnen passen
        linespace = 50
        height = 50
        column1 = 40
        column2 = 210

        # Het frame plaatsen ======================================================================
        dataframe = Frame(self.window,
                          background=self.background,
                          width=self.width,
                          height=self.height,
                          highlightbackground="#DDDDDD",
                          highlightthickness=2)
        dataframe.place(x=self.pos_x, y=self.pos_y)

        # Projectnaam ============================================================================
        projectnaam_label = Label(dataframe,
                                  text="Projectnaam",
                                  font=("Arial", 12),
                                  background=self.background)
        projectnaam_label.place(x=column1, y=height)

        projectnaam_entry = Entry(dataframe, width=40, font=("Arial", 12), relief=SUNKEN, borderwidth=2)
        projectnaam_entry.place(x=column2, y=height)
        height += linespace

        # Projectbestand =========================================================================
        self.projectbestand = StringVar()
        projectbestand_label = Label(dataframe,
                                     text="Bestand",
                                     font=("Arial", 12),
                                     background=self.background)
        projectbestand_label.place(x=column1, y=height)

        projectbestand_inhoud_label = Label(dataframe,
                                            text="",
                                            font=("Arial", 12),
                                            background=self.background,
                                            height=3,
                                            width=40,
                                            borderwidth=2,
                                            relief=SUNKEN,
                                            anchor="nw",
                                            justify="left",
                                            textvariable=self.projectbestand)
        projectbestand_inhoud_label.place(x=column2, y=height)
        height += linespace + 10

        get_file_button = Button(dataframe, text="Open bestand", width=51, command=self.load_image)
        get_file_button.place(x=column2, y=height)
        height += linespace

        # Zwart/wit ===============================================================================
        zwartwit_label = Label(dataframe,
                               text="Zwart/wit",
                               font=("Arial", 12),
                                background=self.background)
        zwartwit_label.place(x=column1, y=height)

        self.checkbox = Checkbutton(dataframe,
                               text="",
                               variable=self.b_w_var,
                               onvalue=1,
                               offvalue=0,
                               command=self.b_w_pressed,
                               background=self.background,
                               activebackground=self.background,
                               state=DISABLED)
        self.checkbox.place(x=column2, y=height)
        height += linespace

        # Helderheid =============================================================================
        helderheid_label = Label(dataframe,
                               text="Helderheid",
                               font=("Arial", 12),
                               background=self.background)
        helderheid_label.place(x=column1, y=height)

        self.luminance_value.set("0")
        self.luminance_box = Spinbox(dataframe,
                                from_=-10, to=10,
                                textvariable=self.luminance_value,
                                width=5,
                                command=self.luminance_changed,
                                disabledbackground=self.background,
                                readonlybackground=self.background,
                                state=DISABLED)
        self.luminance_box.place(x=column2, y=height)
        height += linespace

        # Formaat tekenpapier ==============================================================================
        formaat_tekenpapier_label = Label(dataframe,
                                          text="Formaat tekenpapier",
                                          font=("Arial", 12),
                                          background=self.background)
        formaat_tekenpapier_label.place(x=column1, y=height)

        formaat_tekenpapier_b1_label = Label(dataframe,
                                            text="-",
                                            font=("Arial", 12),
                                            background=self.background)
        formaat_tekenpapier_b1_label.place(x=column2-15, y=height)

        formaat_tekenpapier_b_entry = Entry(dataframe,
                                            width=5,
                                            font=("Arial", 12),
                                            relief=SUNKEN,
                                            borderwidth=2,
                                            textvariable=self.papierbreedte)
        formaat_tekenpapier_b_entry.bind("<FocusOut>", self.papersize_changed)
        formaat_tekenpapier_b_entry.place(x=column2, y=height)

        formaat_tekenpapier_b2_label = Label(dataframe,
                                             text="breedte (mm)",
                                             font=("Arial", 12),
                                             background=self.background)
        formaat_tekenpapier_b2_label.place(x=column2 + 60, y=height)

        formaat_tekenpapier_h1_label = Label(dataframe,
                                            text="-",
                                            font=("Arial", 12),
                                            background=self.background)
        formaat_tekenpapier_h1_label.place(x=column2-15, y=height+25)

        formaat_tekenpapier_h_entry = Entry(dataframe,
                                            width=5,
                                            font=("Arial", 12),
                                            relief=SUNKEN,
                                            borderwidth=2,
                                            textvariable=self.papierhoogte)
        formaat_tekenpapier_h_entry.bind("<FocusOut>", self.papersize_changed)
        formaat_tekenpapier_h_entry.place(x=column2, y=height+25)

        formaat_tekenpapier_h2_label = Label(dataframe,
                                             text="hoogte (mm)",
                                             font=("Arial", 12),
                                             background=self.background)
        formaat_tekenpapier_h2_label.place(x=column2 + 60, y=height+25)
        height += linespace


        # Cropwindow - Heeft in de definitieve versie geen waarde =========================================
        cropwindow_label = Label(dataframe,
                                 text="Cropwindow",
                                 font=("Arial", 9),
                                 background=self.background)
        cropwindow_label.place(x=column1 + 90, y=height)

        cropwindow_x1_label = Label(dataframe,
                                 text="x1:",
                                 font=("Arial", 9),
                                 background=self.background)
        cropwindow_x1_label.place(x=column2, y=height)

        cropwindow_x1_waarde_label = Label(dataframe,
                                           font=("Arial", 9),
                                           background=self.background,
                                           textvariable=self.crop_x1)
        cropwindow_x1_waarde_label.place(x=column2 + 18, y=height)

        cropwindow_y1_label = Label(dataframe,
                                 text="y1:",
                                 font=("Arial", 9),
                                 background=self.background)
        cropwindow_y1_label.place(x=column2 + 60, y=height)

        cropwindow_y1_waarde_label = Label(dataframe,
                                           font=("Arial", 9),
                                           background=self.background,
                                           textvariable=self.crop_y1)
        cropwindow_y1_waarde_label.place(x=column2 + 78, y=height)

        cropwindow_x2_label = Label(dataframe,
                                    text="x2:",
                                    font=("Arial", 9),
                                    background=self.background)
        cropwindow_x2_label.place(x=column2 + 120, y=height)

        cropwindow_x2_waarde_label = Label(dataframe,
                                           font=("Arial", 9),
                                           background=self.background,
                                           textvariable=self.crop_x2)
        cropwindow_x2_waarde_label.place(x=column2 + 138, y=height)


        cropwindow_y2_label = Label(dataframe,
                                    text="y2:",
                                    font=("Arial", 9),
                                    background=self.background)
        cropwindow_y2_label.place(x=column2 + 180, y=height)

        cropwindow_y2_waarde_label = Label(dataframe,
                                           font=("Arial", 9),
                                           background=self.background,
                                           textvariable=self.crop_y2)
        cropwindow_y2_waarde_label.place(x=column2 + 198, y=height)

        height += linespace


        # Offset tekenboard ============================================================================
        offset_tekenboard_label = Label(dataframe,
                                        text="Offset tekenboard",
                                        font=("Arial", 12),
                                        background=self.background)
        offset_tekenboard_label.place(x=column1, y=height)

        offset_tekenboard_x1_label = Label(dataframe,
                                          text="-",
                                          font=("Arial", 12),
                                          background=self.background)
        offset_tekenboard_x1_label.place(x=column2 - 15, y=height)

        offset_tekenboard_x_entry = Entry(dataframe,
                                          width=5,
                                          font=("Arial", 12),
                                          relief=SUNKEN,
                                          borderwidth=2)
        offset_tekenboard_x_entry.place(x=column2, y=height)

        offset_tekenboard_x2_label = Label(dataframe,
                                           text="x (mm)",
                                           font=("Arial", 12),
                                           background=self.background)
        offset_tekenboard_x2_label.place(x=column2 + 60, y=height)
        height += 25

        offset_tekenboard_y1_label = Label(dataframe,
                                          text="-",
                                          font=("Arial", 12),
                                          background=self.background)
        offset_tekenboard_y1_label.place(x=column2 - 15, y=height)

        offset_tekenboard_y_entry = Entry(dataframe,
                                          width=5,
                                          font=("Arial", 12),
                                          relief=SUNKEN,
                                          borderwidth=2)
        offset_tekenboard_y_entry.place(x=column2, y=height)

        offset_tekenboard_y2_label = Label(dataframe,
                                           text="y (mm)",
                                           font=("Arial", 12),
                                           background=self.background)
        offset_tekenboard_y2_label.place(x=column2 + 60, y=height)

        # Buttons annuleren en opslaan =====================================================================
        height = self.height - 30
        annuleren_button = Button(dataframe, text="Annuleren", width=40, command=self.annuleren)
        annuleren_button.place(x=0, y=height)
        opslaan_button = Button(dataframe, text="Opslaan", width=40, command=self.load_image)
        opslaan_button.place(x=int(self.width/2) + 10, y=height)

    def b_w_pressed(self):
        if self.b_w_var.get() == 1:
            self.image_screen.set_black_white()
        else:
            self.image_screen.set_color()

    def luminance_changed(self):
        self.image_screen.set_brightness(self.luminance_value.get())

    def papersize_changed(self, event):
        papierbreedte = self.papierbreedte.get()                    # Ophalen waarden voor het papierformaat
        papierhoogte = self.papierhoogte.get()
        if papierbreedte != "" and papierhoogte != "":              # Alleen uitvoeren als er iets ingevuld staat
            try:                                                    # Als de waarde van papierbreedte of papierhoogte
                int_papierbreedte = int(papierbreedte)              # niet om te zetten is naar een integer, wordt
            except ValueError:                                      # deze op -1 gezet. De -1 wordt later gebruikt om
                int_papierbreedte = -1                              # een foutmelding te genereren.

            try:
                int_papierhoogte = int(papierhoogte)
            except ValueError:
                int_papierhoogte = -1

            if int_papierbreedte == -1 or int_papierhoogte == -1:   # De foutmelding zoals hierboven beschreven
                melding_breedte = "De breedte bevat een niet toegestane waarde {}\n".format(
                    papierbreedte) if int_papierbreedte == -1 else ""
                melding_hoogte = "De hoogte bevat een niet toegestane waarde {}\n".format(
                    papierhoogte) if int_papierhoogte == -1 else ""

                messagebox.showerror(title="Geen toegestane waarde", message=melding_breedte + melding_hoogte)

                if int_papierhoogte == -1:                          # Entry die geen integer bevat leegmaken
                    self.papierhoogte.set("")
                if int_papierbreedte == -1:
                    self.papierbreedte.set("")

            else:
                self.verhouding = int_papierbreedte / int_papierhoogte  # Verhouding breedte/hoogte berekenen
                self.image_screen.verhouding = self.verhouding

    def load_image(self):
        self.old_image = self.actual_image                  # Huidige image opslaan om een wijziging te kunnen
                                                            # detecteren
        self.actual_image = self.image_screen.load_image()  # Afbeelding ophalen
        self.checkbox.config(state=ACTIVE)                  # Zwart/wit en helderheid weer instelbaar maken
        self.luminance_box.config(state="readonly")
        self.image_screen.img = self.actual_image
        self.image_screen.show_image()                      # Afbeelding plaatsen
        if len(self.actual_image) > 40:
            afbeelding = self.actual_image[:40] + "\n" + self.actual_image[40:]
            self.projectbestand.set(afbeelding)
        if self.old_image != self.actual_image:             # Als er een nieuwe afbeelding geladen is B/W en helderheid
            self.b_w_var.set(0)                             # op 0 zetten
            self.luminance_value.set(0)
        self.b_w_pressed()
        self.luminance_changed()

    def annuleren(self):
        self.main_screen.clear_screen()

    def set_crop_vars(self,crop):
        self.crop_x1.set(crop[0])
        self.crop_y1.set(crop[1])
        self.crop_x2.set(crop[2])
        self.crop_y2.set(crop[3])

class DnPImageScreen():
    def __init__(self, on_top_of, x, y, width, height, datascreenobject, **kwargs):
        self.datascreen = datascreenobject
        self.canvas = Canvas
        self.window = on_top_of
        self.pos_x = x
        self.pos_y = y
        self.width = width
        self.height = height

        # Met config in te stellen variablen
        self.canvas_background = "#EEEEEE"          # achtergrondkleur van het canvas
        self.image_cursors = ["arrow",              # cursorvormen voor de afbeelding
                              "top_left_corner",
                              "top_right_corner",
                              "bottom_left_corner",
                              "bottom_right_corner",
                              "hand2"]
        self.img = None                             # Het pad en naam van de afbeelding
        self.randkleur = "#EEEEEE"                  # De kleur van de rand om het frame
        self.randdikte = 2                          # De dikte van de rand om het frame
        self.image_center = True                    # Centreren van de afbeelding in het frame; ja (True) of nee (false

        # Globale variabelen
        self.actual_image = None                    # Werkafbeelding
        self.brightness_image = None                # Image die getoond wordt als de brightness aangepast is
        self.initial_color_image = None             # Initiele afbeelding zodat makkelijk teruggegaan kan worden
        self.initial_bw_image = None                # Initiele zw/w afbeelding
        self.bw = False                             # Is de afbeelding zwart/wit (bw = True) of kleur (bw = False)
        self.image_frame = None                     # Het frame waarop de afbeelding wordt geplaatst
        self.brightness_value = 0                   # Waarde van de helderheid
        self.cropwindow = -1
        self.afbeelding_x = 0
        self.afbeelding_y = 0
        self.cropcoords = [0, 0, 0, 0]
        self.button_1_pressed = False
        self.file_path = ""
        self.dnp_data_screen = DnPDataScreen
        self.afbeelding_size_b = 0
        self.afbeelding_size_h = 0
        self.last_cursor_pos_x = 0
        self.last_cursor_pos_y = 0
        self.verhouding = -1

        self.config(**kwargs)

    def config(self, **kwargs):
        if kwargs.get("datascreenobject"):
            self.datascreen = kwargs.get("datascreenobject", self.datascreen)
        if kwargs.get("image"):
            self.img = kwargs.get("image", self.img)
        if kwargs.get("bg"):
            self.canvas_background = kwargs.get("bg", self.canvas_background)
        if kwargs.get("cursor"):
            self.image_cursor = kwargs.get("cursor", self.image_cursor)
        if kwargs.get("linethickness"):
            self.randdikte = kwargs.get("linethickness", self.randdikte)
        if kwargs.get("linecolor"):
            self.randkleur = kwargs.get("linecolor", self.randkleur)
        if kwargs.get("image_center"):
            self.image_center = kwargs.get("image_center", self.image_center)
            if self.image_center in ["True", "False"]:
                self.image_center = eval(self.image_center)
            else:
                self.image_center = True
            # print(temp)

    def show_canvas(self):
        self.image_frame = Frame(self.window,
                                 width=self.width,
                                 height=self.height,
                                 highlightbackground=self.randkleur,
                                 highlightthickness=self.randdikte,
                                 background=self.canvas_background)
        self.image_frame.place(x=self.pos_x, y=self.pos_y)






    def show_image(self):
        if self.get_image():                                    # Volgende alleen uitvoeren als er een image geladen is
            self.img = ImageTk.PhotoImage(self.actual_image)

            # Zorgen dat de foto geresized wordt om op het canvas te passen
            cropfactor_h = 1.0
            cropfactor_b = 1.0
            randdikte = int(self.randdikte) * 2
            if self.actual_image.size[0] > (self.width - randdikte):            # De foto is breder dan het canvas
                cropfactor_b = (self.width - randdikte)/self.actual_image.size[0]
            if self.actual_image.size[1] > self.height - randdikte:             # De foto is hoger dan het canvas
                cropfactor_h = (self.height - randdikte)/self.actual_image.size[1]
            cropfactor = min(cropfactor_h, cropfactor_b)
            self.afbeelding_size_b = int(self.actual_image.size[0] * cropfactor)
            self.afbeelding_size_h = int(self.actual_image.size[1] * cropfactor)
            self.actual_image = self.actual_image.resize((self.afbeelding_size_b, self.afbeelding_size_h))

            self.img = ImageTk.PhotoImage(self.actual_image)
            self.initial_color_image = self.actual_image                        # Initiele image veilig stellen zodat er
                                                                                # na bewerkingen makkelijk teruggegaan
                                                                                # kan worden
            # Maak een canvas op het frame en plaats daar de afbeelding op
            self.canvas = Canvas(self.image_frame, width=self.width, height=self.height)
            self.canvas.config(background=self.canvas_background, cursor=self.image_cursors[0], relief='ridge',
                               highlightthickness=0)
            self.canvas.bind("<Motion>",self.motion_canvas)
            self.canvas.bind("<Button-1>", self.button_pressed_canvas)
            self.canvas.bind("<ButtonRelease-1>", self.button_released_canvas)

            # Bepaal x- en y-coördinaat van het canvas aan de hand van wel of niet centreren
            x = 0
            y = 0
            if self.image_center:
                if self.afbeelding_size_b >= self.afbeelding_size_h: # afbeelding is landscape of vierkant
                    self.afbeelding_y = int((self.height- (2 * int(self.randdikte)))/2) - int(self.afbeelding_size_h/2)
                else: # Afbeelding is portrait
                    self.afbeelding_x = int((self.width - (2 * int(self.randdikte))) / 2) - int(self.afbeelding_size_b / 2)

            # Plaats het canvas
            self.canvas.place(x=0, y=0)
            if (self.verhouding == -1) or (self.verhouding == 1.0):
                self.cropcoords = [self.afbeelding_x,
                                   self.afbeelding_y,
                                   self.afbeelding_x + self.afbeelding_size_b,
                                   self.afbeelding_y + self.afbeelding_size_h]
            else:
                if self.verhouding < 1:         # Portrait
                    self.cropcoords = [self.afbeelding_x,
                                       self.afbeelding_y,
                                       self.afbeelding_x + self.afbeelding_size_b * self.verhouding,
                                       self.afbeelding_y + self.afbeelding_size_h]
                else:
                    self.cropcoords = [self.afbeelding_x,
                                       self.afbeelding_y,
                                       self.afbeelding_x + self.afbeelding_size_b,
                                       self.afbeelding_y + self.afbeelding_size_h / self.verhouding]

            print(self.verhouding)
            self.show_cropwindow()
            self.canvas.create_image(self.afbeelding_x, self.afbeelding_y, anchor="nw", image=self.img,
                                     tags=("afbeelding"))
            # self.canvas.update_idletasks

    def get_cursor_location(self, event):
        # cursorvorm 1: De cursor bevindt zich links boven
        marge = 20
        if (event.x > self.cropcoords[0] - marge) and \
                (event.x < self.cropcoords[0] + marge) and \
                (event.y > self.cropcoords[1] - marge) and \
                (event.y < self.cropcoords[1] + marge):
            return 1
        else:
            # locatie 1: De cursor bevindt zich rechts boven
            if (event.x > self.cropcoords[2] - marge) and \
                (event.x < self.cropcoords[2] + marge) and \
                (event.y > self.cropcoords[1] - marge) and \
                (event.y < self.cropcoords[1] + marge):
                return 2
            else:
                # locatie 2: De cursor bevindt zich links onder
                if (event.x > self.cropcoords[0] - marge) and \
                        (event.x < self.cropcoords[0] + marge) and \
                        (event.y > self.cropcoords[3] - marge) and \
                        (event.y < self.cropcoords[3] + marge):
                    return 3
                else:
                    # locatie 3: De cursor bevindt zich links onder
                    if (event.x > self.cropcoords[2] - marge) and \
                            (event.x < self.cropcoords[2] + marge) and \
                            (event.y > self.cropcoords[3] - marge) and \
                            (event.y < self.cropcoords[3] + marge):
                        return 4
                    else:
                        # locatie 4: De cusor bevindt zich binnen het cropwindow, maar niet in de hoeken
                        if (event.x > self.cropcoords[0]) and \
                                (event.x < self.cropcoords[2]) and \
                                (event.y > self.cropcoords[1]) and \
                                (event.y < self.cropcoords[3]):
                            return 5
                        else:
                            return 0

    def motion_canvas(self, event):
        cursor_locatie = self.get_cursor_location(event)
        self.canvas.config(cursor=self.image_cursors[cursor_locatie])
        if self.button_1_pressed:
            if cursor_locatie == 1:
                if event.x >= self.afbeelding_x:
                    self.cropcoords[0] = event.x
                if event.y >= self.afbeelding_y:
                    self.cropcoords[1] = event.y
            else:
                if cursor_locatie == 2:
                    if event.x <= self.afbeelding_x + self.afbeelding_size_b:
                        self.cropcoords[2] = event.x
                    if event.y >= self.afbeelding_y:
                        self.cropcoords[1] = event.y
                else:
                    if cursor_locatie == 3:
                        if event.x >= self.afbeelding_x:
                            self.cropcoords[0] = event.x
                        if event.y <= self.afbeelding_y + self.afbeelding_size_h:
                            self.cropcoords[3] = event.y
                    else:
                        if cursor_locatie == 4:
                            if event.x <= self.afbeelding_x + self.afbeelding_size_b:
                                self.cropcoords[2] = event.x
                            if event.y <= self.afbeelding_y + self.afbeelding_size_h:
                                self.cropcoords[3] = event.y
                        else:
                            if cursor_locatie == 5:
                                delta_x = (self.last_cursor_pos_x - event.x) * -1
                                delta_y = (self.last_cursor_pos_y - event.y) * -1
                                if (self.cropcoords[0] + delta_x > self.afbeelding_x) and \
                                    (self.cropcoords[1] + delta_y > self.afbeelding_y) and \
                                    (self.cropcoords[2] + delta_x < self.afbeelding_x + self.afbeelding_size_b) and \
                                    (self.cropcoords[3] + delta_y < self.afbeelding_y + self.afbeelding_size_h):
                                    self.cropcoords[0] += delta_x
                                    self.cropcoords[1] += delta_y
                                    self.cropcoords[2] += delta_x
                                    self.cropcoords[3] += delta_y

            self.show_cropwindow()
        self.last_cursor_pos_x = event.x
        self.last_cursor_pos_y = event.y

    def button_pressed_canvas(self, event):
        self.button_1_pressed = True

    def button_released_canvas(self, event):
        self.button_1_pressed = False

    def show_cropwindow(self):

        if self.cropwindow >= 0:
            self.canvas.delete(self.cropwindow)
        self.cropwindow = self.canvas.create_rectangle(self.cropcoords[0],
                                                       self.cropcoords[1],
                                                       self.cropcoords[2],
                                                       self.cropcoords[3],
                                                       width= 3, outline="red",
                                                       tags=("cropvierkant"))

        self.canvas.tag_raise("cropvierkant")
        self.datascreen.set_crop_vars(self.cropcoords)
        self.canvas.update_idletasks

    def get_image(self):
        try:
            self.actual_image = Image.open(self.img)
            return True
        except:
            return False

    def set_black_white(self):
        self.bw = True
        self.initial_bw_image = self.initial_color_image.convert('L')
        self.actual_image = self.initial_bw_image
        self.img = ImageTk.PhotoImage(self.actual_image)
        print ("x = ", self.afbeelding_x, "y = ", self.afbeelding_y)
        self.canvas.create_image(self.afbeelding_x, self.afbeelding_y, anchor="center", image=self.img)
        self.canvas.update_idletasks()
        self.set_brightness(self.brightness_value)

    def set_color(self):
        if self.actual_image != None:
            self.bw = False
            self.actual_image = self.initial_color_image
            self.img = ImageTk.PhotoImage(self.actual_image)
            self.canvas.create_image(self.afbeelding_x, self.afbeelding_y, anchor="nw", image=self.img, tags="afbeelding")
            self.canvas.tag_lower("afbeelding")
            self.canvas.update_idletasks()
            self.set_brightness(self.brightness_value)

    def set_brightness(self, value):
        if self.actual_image != None:
            self.brightness_value = value
            if self.bw:
                self.brightness_image = ImageEnhance.Brightness(self.initial_bw_image)
            else:
                self.brightness_image = ImageEnhance.Brightness(self.initial_color_image)
            self.actual_image = self.brightness_image.enhance(1 + (int(value)/10))
            self.img = ImageTk.PhotoImage(self.actual_image)
            self.canvas.create_image(self.afbeelding_x, self.afbeelding_y, anchor="nw", image=self.img, tags="afbeelding")
            self.canvas.tag_lower("afbeelding")
            self.canvas.update_idletasks()

    def load_image(self):
        image_files = [".jpg", ".jpeg", ".png", ".ico"]
        image_file_type = ""
        for image_file in image_files:
            image_file_type += image_file + " "
        self.file_path = filedialog.askopenfilename(initialdir="C:\\Users\\vario\\PycharmProjects\\Tekenhulp V0.2\\images",
                                               title="Kies een afbeelding",
                                               filetypes=(("image files", image_file_type),
                                                          ("all files", "*.*")))
        if ((Path(self.file_path).suffix) not in image_files) and self.file_path != "":
            messagebox.showerror(title="Geen toegestane afbeelding",
                                 message="Geen toegestane afbeelding!\n\n"
                                         "Afbeeldingen die toegestaan zijn:\n"
                                         + image_file_type)
            # file_path = ""

        return self.file_path