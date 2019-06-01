import time
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import video_capture as vid
import hand as h

start = False
base = []


class HandyBrowser(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # logo = PhotoImage(file='favicon.ico')
        # Tk.iconbitmap(self, logo)
        img = Image("photo", file="favicon.gif")
        self.tk.call('wm', 'iconphoto', Tk._w, img)
        # Tk.iconbitmap(self, img)
        Tk.wm_title(self, "Handy browser")

        self.view = StringVar(value="BasePage")
        self.menu_bar_init()

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky=(N, S, E, W))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (BasePage, CameraPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=(N, S, E, W))
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(BasePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.view.set(cont.__name__)
        frame.tkraise()

    def menu_bar_init(self):
        self.option_add('*tearOff', FALSE)
        menu_bar = Menu(self)
        self['menu'] = menu_bar
        menu_view = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_view, label='View')
        menu_bar.add_cascade(menu=menu_help, label='Help')

        menu_theme = Menu(menu_view)
        menu_view.add_cascade(menu=menu_theme, label='Change theme')

        # Why it works? Why self.style not needed to have pre selected?
        style = StringVar(value=ttk.Style().theme_use())
        for theme in ttk.Style().theme_names():
            menu_theme.add_radiobutton(label=theme, value=theme,
                                       variable=style,
                                       command=lambda: ttk.Style().theme_use(
                                           style.get()))

        menu_view.add_separator()

        # Why it works? Why self.style needed to have pre selected?
        menu_view.add_radiobutton(label='Basic view', value="BasePage",
                                  variable=self.view,
                                  command=lambda: self.show_frame(BasePage))

        # menu_view.add_radiobutton(label='Camera view', value="CameraPage",
        #                           variable=self.view,
        #                           command=lambda: self.show_frame(CameraPage))

        menu_help.add_command(label='Manual',
                              command=lambda: webbrowser.open_new_tab(
                                  "https://github.com/mikiisz/Handy-Browser"))

        menu_help.add_separator()

        menu_help.add_command(label='About', command=lambda: self.show_about())

    @staticmethod
    def show_about():
        messagebox.showinfo("About", "Handy Browser 2019, version 1.0.0\n"
                                     "Dominik Mondzik and Michał Szkarłat")


class Browser:
    def __init__(self):
        self.state = "Not found"

    def set(self, set_to):
        self.state = set_to


class Pages:
    def __init__(self):
        self.state = []

    def set(self, set1, set2, cam):
        global start
        if not start:
            if browser.state != "Not found":
                self.state.append(set1)
                self.state.append(set2)
                start = True
                global base
                base = vid.start(self.state, browser.state)
                # time.sleep(1)
                cam.__del__()
                global app
                app.destroy()
                h.init(base)
            else:
                messagebox.showinfo("Error",
                                    "Before staring choose browser")


browser = Browser()
pages = Pages()


class BasePage(Frame):
    # vid = vid.MyVideoCapture(0)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        padding_container = ttk.Frame(self, padding=(40, 20, 40, 20))
        padding_container.grid(row=0, column=0)

        left_frame = ttk.Frame(padding_container, padding=(0, 20, 20, 20))
        left_frame.grid(row=0, column=0, sticky=(N, S, E, W))

        def press(event):
            browser.set(camera_choice.get())
            print(browser.state)
            # camera_status = StringVar(value="")

        camera_choice = StringVar(value="Select browser")
        camera_combobox = ttk.Combobox(left_frame, textvariable=camera_choice,
                                       width=30,
                                       values=["Firefox", "Chrome", "Opera"])
        camera_combobox.grid(row=0, column=0, columnspan=2, pady=10)
        camera_combobox.bind('<<ComboboxSelected>>', press)

        camera_status = StringVar(
            value="Choose browser you would \n"
                  "like to operate.")
        camera_label = ttk.Label(left_frame, text=camera_status.get())
        camera_label.grid(row=1, column=0, columnspan=2, pady=10, sticky=W)

        # separator
        left_separator = ttk.Separator(left_frame, orient=HORIZONTAL)
        left_separator.grid(row=2, column=0, columnspan=2, sticky=(E, W),
                            pady=20)

        webpage = StringVar(value="Identify fingers with webpages")
        webpage_label = ttk.Label(left_frame, text=webpage.get())
        webpage_label.grid(row=3, column=0, columnspan=2, pady=10, sticky=N)

        ttk.Label(left_frame, text="Two Fingers, right:").grid(row=4, sticky=W)
        ttk.Label(left_frame, text="Two Fingers, left:").grid(row=5, sticky=W)

        e1 = ttk.Entry(left_frame)
        e2 = ttk.Entry(left_frame)
        e1.insert(10, "youtube.com")
        e2.insert(10, "gmail.com")

        e1.grid(row=4, column=1)
        e2.grid(row=5, column=1)

        left_separator = ttk.Separator(left_frame, orient=HORIZONTAL)
        left_separator.grid(row=6, column=0, columnspan=2, sticky=(E, W),
                            pady=20)

        # browser_choice = StringVar(value="Select browser")
        # browser_combox = ttk.Combobox(left_frame, textvariable=browser_choice,
        #                               width=30)
        # browser_combox.grid(row=3, column=0, columnspan=2, pady=10)

        # browser_status = StringVar(value=browser.state)
        # browser_label = ttk.Label(left_frame, text=browser_status.get())
        # browser_label.grid(row=4, column=0, columnspan=2, pady=10, sticky=E)
        self.vid = vid.MyVideoCapture(0)

        label = ttk.Label(left_frame, text="For more information \n"
                                           "check manual: \n"
                                           "Help -> Manual", padding=(20, 10))
        button = ttk.Button(left_frame, text="Start",
                            command=lambda: pages.set(e1.get(), e2.get(),
                                                      self.vid))
        label.grid(row=7, column=0, sticky=W)
        button.grid(row=7, column=1, sticky=E)

        # separator
        central_separator = ttk.Separator(padding_container, orient=VERTICAL)
        central_separator.grid(row=0, column=1, sticky=(N, S), padx=20)

        # right part:
        right_frame = ttk.Frame(padding_container)
        right_frame.grid(row=0, column=2)

        # open video source (by default this will try to open the computer webcam)
        # self.vid = MyVideoCapture("big_buck_bunny_480p_stereo.avi")

        self.cam1 = Canvas(right_frame, width=320, height=240)
        self.cam1.grid(row=0, column=0, pady=20)

        self.cam2 = Canvas(right_frame, width=320, height=240)
        self.cam2.grid(row=0, column=1, pady=20)

        # names sX to change
        scale_frame = ttk.Frame(right_frame)
        self.s1_variable = DoubleVar(value=100000)
        self.s2_variable = DoubleVar(value=5000)
        self.s3_variable = DoubleVar(value=150)
        self.s4_variable = DoubleVar(value=150)

        ttk.Label(scale_frame, text="Size of pixel detection",
                  padding=(20, 10)).grid(
            row=0, column=0, sticky=W)
        ttk.Label(scale_frame, text="Number of motion pixels",
                  padding=(20, 10)).grid(
            row=1, column=0, sticky=W)
        ttk.Label(scale_frame, text="x offset",
                  padding=(20, 10)).grid(
            row=2, column=0, sticky=W)
        ttk.Label(scale_frame, text="y offset",
                  padding=(20, 10)).grid(
            row=3, column=0, sticky=W)

        s1 = ttk.Scale(scale_frame, orient=HORIZONTAL,
                       variable=self.s1_variable,
                       length=200, from_=0, to=500000)
        s2 = ttk.Scale(scale_frame, orient=HORIZONTAL,
                       variable=self.s2_variable,
                       length=200, from_=0, to=10000)
        s3 = ttk.Scale(scale_frame, orient=HORIZONTAL,
                       variable=self.s3_variable,
                       length=200, from_=0, to=500)
        s4 = ttk.Scale(scale_frame, orient=HORIZONTAL,
                       variable=self.s4_variable,
                       length=200, from_=0, to=500)
        scale_frame.grid(row=1, column=0, pady=20)
        s1.grid(row=0, column=1, pady=2)
        s2.grid(row=1, column=1, pady=2)
        s3.grid(row=2, column=1, pady=2)
        s4.grid(row=3, column=1, pady=2)

        self.delay = 15

        self.update()

    def update(self):
        # Get a frame from the video source
        ret, fg_mask, mask = self.vid.get_frame(int(self.s1_variable.get()),
                                                int(self.s2_variable.get()),
                                                int(self.s3_variable.get()),
                                                int(self.s4_variable.get()))

        if ret:
            self.photo1 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(fg_mask).resize((320, 240)))
            self.cam1.create_image(0, 0, image=self.photo1, anchor=NW)

            self.photo2 = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(mask))
            self.cam2.create_image(0, 0, image=self.photo2, anchor=NW)

        self.cam1.after(self.delay, self.update)


class CameraPage(Frame):
    # vid = BasePage.vid
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # self.vid = vid.MyVideoCapture("big_buck_bunny_480p_stereo.avi")
        # self.vid = MyVideoCapture(0)
        self.camera_canvas = Canvas(self, width=640, height=480)
        self.camera_canvas.grid(row=0, column=0)
        self.camera_canvas.bind("<Button-1>",
                                lambda e: controller.show_frame(BasePage))


#
#         self.delay = 15
#         self.update()
#
#     def update(self):
#         # Get a frame from the video source
#         ret, frame, s = self.vid.get_frame()
#
#         if ret:
#             self.photo = PIL.ImageTk.PhotoImage(
#                 image=PIL.Image.fromarray(frame).resize((640, 480)))
#             self.camera_canvas.create_image(0, 0, image=self.photo, anchor=NW)
#
#         self.camera_canvas.after(self.delay, self.update)


app = HandyBrowser()
app.mainloop()

