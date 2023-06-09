import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
from tkinter.ttk import Style
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import ctypes as ct


class GUI:
    def __init__(self, window):
        self.blank_image = Image.open("img/blank.png")
        self.var_area = IntVar()
        self.var_tilt = IntVar()
        self.var_pan = IntVar()
        self.index_var = StringVar()
        self.port_var = StringVar()
        self.color_var = StringVar()
        self.hue_bawah = IntVar()
        self.hue_atas = IntVar()
        self.saturation_bawah = IntVar()
        self.saturation_atas = IntVar()
        self.value_bawah = IntVar()
        self.value_atas = IntVar()
        self.servo_cond = BooleanVar()
        self.frame_font = Font(
            family="JetBrains Mono ExtraBold", size=12, weight="bold"
        )
        self.button_font = Font(
            family="JetBrains Mono ExtraBold", size=11, weight="bold"
        )
        self.label_font = Font(
            family="JetBrains Mono ExtraBold", size=10, weight="bold"
        )
        self.window = window
        self.style_window()
        self.style_ttk()
        self.notebook = ttk.Notebook(window)
        self.tab1 = Frame(self.notebook)
        self.tab2 = Frame(self.notebook)
        self.tab3 = Frame(self.notebook)
        self.notebook.add(self.tab1, text="Home")
        self.notebook.add(self.tab2, text="Bantuan")
        self.notebook.add(self.tab3, text="Tentang")
        self.notebook.place(x=-1, y=0, width=1081, height=735)
        window.title("Color Detection and Tracking")
        window.geometry("1080x735")
        window.resizable(False, False)

        self.video_frame = Frame(self.tab1, bg="#2d325c", relief="flat")
        self.video_frame.place(x=10, y=10, width=820, height=435)
        self.video_label = Label(
            self.tab1,
            text="Video Display",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.video_label.place(x=10, y=10, width=820, height=20)
        self.label1 = Label(self.tab1, bg="#141835")
        self.label1.place(x=20, y=35, width=530, height=400)
        self.label2 = Label(self.tab1, bg="#141835")
        self.label2.place(x=560, y=35, width=260, height=196)
        self.label3 = Label(self.tab1, bg="#141835")
        self.label3.place(x=560, y=239, width=260, height=196)
        self.setup_frame = Frame(self.tab1, bg="#2d325c", relief="flat")
        self.setup_frame.place(x=838, y=10, width=232, height=223)
        self.label_setup = Label(
            self.tab1,
            text="Setup",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.label_setup.place(x=838, y=10, width=232, height=20)

        self.wc_label = Label(
            self.tab1, text="Camera Index", font=self.label_font, fg="#43dfca"
        )
        self.wc_label.place(x=856, y=37, width=100, height=21)

        self.index_combobox = ttk.Combobox(
            self.tab1, textvariable=self.index_var, font=self.label_font
        )
        self.index_combobox.place(x=856, y=64, width=105, height=27)
        # isi combobox dengan daftar port yang tersedia
        self.index_list = ["0", "1", "2", "3"]
        self.index_combobox["values"] = self.index_list
        # buat tombol untuk menampilkan port yang dipilih
        self.slc_button = Button(
            self.tab1,
            text="Select",
            command=select_index,
            bg="#42dfc9",
            fg="#141835",
            relief="flat",
        )
        self.slc_button.place(x=966, y=64, width=95, height=27)

        # detection color
        self.dc_label = Label(
            self.tab1, text="Detection Color", font=self.label_font, fg="#43dfca"
        )
        self.dc_label.place(x=856, y=97, width=130, height=21)

        self.color_combobox = ttk.Combobox(
            self.tab1, textvariable=self.color_var, font=self.label_font
        )
        self.color_combobox.place(x=856, y=124, width=105, height=27)

        # isi combobox dengan daftar port yang tersedia
        self.color_list = ["Merah", "Hijau", "Biru"]
        self.color_combobox["values"] = self.color_list

        # buat tombol untuk menampilkan port yang dipilih
        self.color_button = Button(
            self.tab1,
            text="SET",
            command=select_color,
            bg="#42dfc9",
            fg="#141835",
            relief="flat",
        )
        self.color_button.place(x=966, y=124, width=95, height=27)

        # arduino port
        self.port_label = Label(
            self.tab1, text="Arduino Port", font=self.label_font, fg="#43dfca"
        )
        self.port_label.place(x=856, y=161, width=100, height=21)

        self.port_combobox = ttk.Combobox(
            self.tab1,
            textvariable=self.port_var,
            font=self.label_font,
        )
        self.port_combobox.place(x=856, y=188, width=105, height=27)

        # isi combobox dengan daftar port yang tersedia
        self.port_list = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox["values"] = self.port_list

        # buat tombol untuk menampilkan port yang dipilih
        self.conn_button = Button(
            self.tab1,
            text="Connect",
            command=lambda: select_port(),
            bg="#42dfc9",
            fg="#141835",
            relief="flat",
        )
        self.conn_button.place(x=966, y=188, width=95, height=27)

        # frame video control
        self.vcont_frame = Frame(
            self.tab1,
            bg="#2d325c",
            relief="flat",
        )
        self.vcont_frame.place(x=838, y=241, width=232, height=204)
        self.vcont_label = Label(
            self.tab1,
            text="Video Control",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.vcont_label.place(x=838, y=241, width=232, height=20)
        # Create A Button
        self.wcv_button = Button(
            self.tab1,
            text="Off",
            bg="#7883c1",
            fg="#141835",
            relief="flat",
            width=10,
            command=lambda: change_switch(1),
        )
        self.wcv_button.place(x=866, y=289, width=52, height=24)
        self.wcv_label = Label(
            self.tab1, text="Webcam Video", font=self.label_font, fg="#43dfca"
        )
        self.wcv_label.place(x=936, y=290, width=110, height=21)

        self.msv_button = Button(
            self.tab1,
            text="Off",
            bg="#7883c1",
            fg="#141835",
            relief="flat",
            width=10,
            command=lambda: change_switch(2),
        )
        self.msv_button.place(x=866, y=332, width=52, height=24)
        self.msv_label = Label(
            self.tab1, text="Masking Video", font=self.label_font, fg="#43dfca"
        )
        self.msv_label.place(x=936, y=333, width=110, height=21)

        self.cv_button = Button(
            self.tab1,
            text="Off",
            bg="#7883c1",
            fg="#141835",
            relief="flat",
            width=10,
            command=lambda: change_switch(3),
        )
        self.cv_button.place(x=866, y=372, width=52, height=24)
        self.cv_label = Label(
            self.tab1, text="Result Video", font=self.label_font, fg="#43dfca"
        )
        self.cv_label.place(x=936, y=373, width=110, height=21)

        # frame servo control
        self.servcont_frame = Frame(self.tab1, bg="#2d325c", relief="flat")
        self.servcont_frame.place(x=10, y=453, width=265, height=245)
        self.servcont_label = Label(
            self.tab1,
            text="Servo Manual Control",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.servcont_label.place(x=10, y=453, width=265, height=20)
        # checkbox
        self.cb_servo = ttk.Checkbutton(
            self.tab1,
            text="Manual",
            variable=self.servo_cond,
            onvalue=1,
            offvalue=0,
            command=toggle_servo,
        )
        self.cb_servo.place(x=180, y=505, width=90, height=20)
        self.pan_label = Label(
            self.tab1, text="Pan Servo", font=self.label_font, fg="#43dfca"
        )
        self.pan_label.place(x=38, y=505, width=75, height=21)
        self.pan_scale = Scale(
            self.tab1,
            variable=self.var_pan,
            from_=0,
            to=180,
            orient=HORIZONTAL,
            state="disabled",
            troughcolor="#43dfca",
            font=self.label_font,
        )
        self.pan_scale.place(x=38, y=530, width=210, height=40)

        self.tilt_label = Label(
            self.tab1, text="Tilt Servo", font=self.label_font, fg="#43dfca"
        )
        self.tilt_label.place(x=38, y=580, width=85, height=21)
        self.tilt_scale = Scale(
            self.tab1,
            variable=self.var_tilt,
            from_=0,
            to=180,
            orient=HORIZONTAL,
            state="disabled",
            troughcolor="#43dfca",
        )
        self.tilt_scale.place(x=38, y=605, width=210, height=40)

        # frame area control
        self.areacont_frame = Frame(self.tab1, background="#2d325c", relief="flat")
        self.areacont_frame.place(x=283, y=453, width=265, height=120)
        self.areacont_label = Label(
            self.tab1,
            text="Minimum Contour Area",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.areacont_label.place(x=283, y=453, width=265, height=20)
        self.area_scale = Scale(
            self.tab1,
            variable=self.var_area,
            from_=200,
            to=5000,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.area_scale.place(x=321, y=505, width=190, height=40)

        self.coordinate_frame = Frame(self.tab1, background="#2d325c", relief="flat")
        self.coordinate_frame.place(x=283, y=582, width=265, height=116)
        self.coordinate_label = Label(
            self.tab1,
            text="Coordinate",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.coordinate_label.place(x=283, y=582, width=265, height=20)
        self.coordX_label = Label(
            self.tab1, text="X", font=self.label_font, fg="#43dfca"
        )
        self.coordX_label.place(x=300, y=632, width=30, height=30)
        self.coordX_val = Label(
            self.tab1, text="0", font=self.label_font, fg="#141835", bg="white"
        )
        self.coordX_val.place(x=340, y=632, width=70, height=30)
        self.coordX_label = Label(
            self.tab1, text="Y", font=self.label_font, fg="#43dfca"
        )
        self.coordX_label.place(x=420, y=632, width=30, height=30)
        self.coordY_val = Label(
            self.tab1, text="0", font=self.label_font, fg="#141835", bg="white"
        )
        self.coordY_val.place(x=460, y=632, width=70, height=30)

        # frame hsv control
        self.hsvcont_frame = Frame(self.tab1, background="#2d325c", relief="flat")
        self.hsvcont_frame.place(x=556, y=453, width=513, height=245)
        self.hsvcont_label = Label(
            self.tab1,
            text="HSV Control",
            bg="#42dfc9",
            fg="#141835",
            font=self.frame_font,
        )
        self.hsvcont_label.place(x=556, y=453, width=513, height=20)
        self.h_bawah = Scale(
            self.tab1,
            variable=self.hue_bawah,
            from_=0,
            to=179,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.h_bawah.place(x=590, y=505, width=210, heigh=40)
        self.hue_label = Label(
            self.tab1, text="Hue", font=self.label_font, fg="#43dfca"
        )
        self.hue_label.place(x=590, y=481, width=60, height=21)
        self.lowerLimit_label = Label(
            self.tab1, text="Batas Bawah", font=self.label_font, fg="#43dfca"
        )
        self.lowerLimit_label.place(x=710, y=481, width=90, height=21)
        self.h_atas = Scale(
            self.tab1,
            variable=self.hue_atas,
            from_=0,
            to=179,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.h_atas.place(x=825, y=505, width=210, height=40)
        self.hsv_label = Label(
            self.tab1, text="Hue", font=self.label_font, fg="#43dfca"
        )
        self.hsv_label.place(x=825, y=481, width=60, height=21)
        self.upperLimit_label = Label(
            self.tab1, text="Batas Atas", font=self.label_font, fg="#43dfca"
        )
        self.upperLimit_label.place(x=946, y=481, width=90, height=21)

        self.s_bawah = Scale(
            self.tab1,
            variable=self.saturation_bawah,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.s_bawah.place(x=590, y=575, width=210, height=40)
        self.hsv_label = Label(
            self.tab1, text="Saturation", font=self.label_font, fg="#43dfca"
        )
        self.hsv_label.place(x=590, y=551, width=80, height=21)
        self.lowerLimit_label = Label(
            self.tab1, text="Batas Bawah", font=self.label_font, fg="#43dfca"
        )
        self.lowerLimit_label.place(x=710, y=551, width=90, height=21)
        self.s_atas = Scale(
            self.tab1,
            variable=self.saturation_atas,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.s_atas.place(x=825, y=575, width=210, height=40)
        self.hsv_label = Label(
            self.tab1, text="Saturation", font=self.label_font, fg="#43dfca"
        )
        self.hsv_label.place(x=825, y=551, width=80, height=21)
        self.upperLimit_label = Label(
            self.tab1, text="Batas Atas", font=self.label_font, fg="#43dfca"
        )
        self.upperLimit_label.place(x=946, y=551, width=90, height=21)

        self.v_bawah = Scale(
            self.tab1,
            variable=self.value_bawah,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.v_bawah.place(x=590, y=645, width=210, height=40)
        self.hsv_label = Label(
            self.tab1, text="Value", font=self.label_font, fg="#43dfca"
        )
        self.hsv_label.place(x=590, y=621, width=60, height=21)
        self.lowerLimit_label = Label(
            self.tab1, text="Batas Bawah", font=self.label_font, fg="#43dfca"
        )
        self.lowerLimit_label.place(x=710, y=621, width=90, height=21)
        self.v_atas = Scale(
            self.tab1,
            variable=self.value_atas,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            troughcolor="#43dfca",
        )
        self.v_atas.place(x=825, y=645, width=210, height=40)
        self.hsv_label = Label(
            self.tab1, text="Value", font=self.label_font, fg="#43dfca"
        )
        self.hsv_label.place(x=825, y=621, width=60, height=21)
        self.upperLimit_label = Label(
            self.tab1, text="Batas Atas", font=self.label_font, fg="#43dfca"
        )
        self.upperLimit_label.place(x=946, y=621, width=90, height=21)

        self.image1 = Image.open("img/help.png")
        self.image1_resize = self.image1.resize((720, 480))
        self.help_image = ImageTk.PhotoImage(self.image1_resize)
        self.help_label = Label(self.tab2, image=self.help_image)
        self.help_label.place(x=180, y=70, width=720, height=480)
        self.image2 = Image.open("img/about_dev.png")
        self.about_image = ImageTk.PhotoImage(self.image2)
        self.about_label = Label(self.tab3, image=self.about_image)
        self.about_label.place(x=13, y=40)

    def style_window(self):
        self.window.option_add("*background", "#141835")
        self.window.option_add("*foreground", "white")
        self.window.option_add("*TCombobox*Listbox.font", self.label_font)
        self.window.option_add("*TCombobox.state", "readonly")
        self.window.option_add("*Scale.font", self.label_font)
        self.window.option_add("*Button.font", self.button_font)

    def style_ttk(self):
        self.style = Style()
        self.style.theme_create(
            "rifki_skripsi",
            parent="alt",
            settings={
                "TNotebook": {"configure": {"tabmargins": [0, 0, 0, -1]}},
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 1],
                        "background": "#7883c1",
                        "foreground": "#141835",
                        "font": self.frame_font,
                    },
                    "map": {
                        "background": [("selected", "#43dfca")],
                        "foreground": [("selected", "#141835")],
                        "expand": [("selected", [1, 1, 1, 0])],
                    },
                },
                "TCheckbutton": {
                    "configure": {
                        "background": "#2d325c",
                        "foreground": "#43dfca",
                        "font": self.label_font,
                    }
                },
                "TCombobox": {
                    "configure": {
                        "background": "white",
                        "fieldbackground": "white",
                    }
                },
            },
        )
        self.style.theme_use("rifki_skripsi")

    def dark_title_bar(self, window):
        """
        MORE INFO:
        https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


def servo_manual():
    if serial_condition == True and my_gui.servo_cond.get() == True:
        pan_angle = my_gui.var_pan.get()
        tilt_angle = my_gui.var_tilt.get()
        serial_data1(pan_angle, tilt_angle)
        my_gui.window.after(20, servo_manual)


def toggle_servo():
    if my_gui.servo_cond.get() == True and serial_condition == True:
        my_gui.pan_scale.config(state="normal")
        my_gui.tilt_scale.config(state="normal")
        messagebox.showinfo("Servo Manual", "Servo bergerak manual")
        servo_manual()
    else:
        my_gui.pan_scale.config(state="disabled")
        my_gui.tilt_scale.config(state="disabled")
        my_gui.servo_cond.set(False)
        messagebox.showinfo("Satus Port", "Silhkan Pilih Port Terlebih Dauhulu")


# fungsi memilih port arduino
def select_port():
    global serial_begin, serial_condition
    port = my_gui.port_var.get()
    try:
        if my_gui.conn_button.config("text")[-1] == "Connect":
            serial_begin = serial.Serial(port, "9600", timeout=5)
            # serial_begin = serial.Serial(port, "115200", timeout=5)
            my_gui.conn_button.config(text="Disconnect", bg="#7883c1", width="100")
            serial_condition = True
            messagebox.showinfo("Status Port", "Terhubung dengan Port " + port)
        else:
            serial_begin.close()
            my_gui.conn_button.config(text="Connect", bg="#42dfc9")
            serial_condition = False
            my_gui.servo_cond.set(False)
            my_gui.pan_scale.config(state="disabled")
            my_gui.tilt_scale.config(state="disabled")
            messagebox.showinfo("Status Port", "Port " + port + " diputus")
    except serial.SerialException:
        messagebox.showinfo(
            "Status Port", "Port Salah, Pastikan Memilih Port yang Sesuai"
        )


def serial_data1(panAngle, tiltAngle):
    serial_begin.write(
        (str(int(panAngle)) + "a" + str(int(tiltAngle)) + "b").encode("utf-8")
    )
    # print(panAngle, tiltAngle)


def serial_data2(img, x, y):
    global panAngle, tiltAngle
    rows, cols, _ = img.shape

    centerX = int(cols / 2)
    centerY = int(rows / 2)
    print("Center x: ", centerX, "   Center y:", centerY)
    # print("row :", rows)

    objectX = int(x + 5)
    objectY = int(y + 5)

    movement = 0.7
    # angleSet = 45
    angleSet = 90

    if objectX > centerX + angleSet:
        panAngle += movement
        if panAngle >= 180:
            panAngle = 180

    elif objectX < centerX - angleSet:
        panAngle -= movement
        if panAngle < 0:
            panAngle = 0

    if objectY > centerY + angleSet:
        tiltAngle -= movement
        if tiltAngle < 0:
            tiltAngle = 0

    elif objectY < centerX - angleSet:
        tiltAngle += movement
        if tiltAngle >= 180:
            tiltAngle = 180

    # serial_begin.write(
    #     ("a" + str(int(panAngle)) + "b" + str(int(tiltAngle))).encode("utf-8")
    # )
    serial_begin.write(
        (str(int(panAngle)) + "a" + str(int(tiltAngle)) + "b").encode("utf-8")
    )


# fungi untuk menampilkan dan menyembunyikan frame video
def change_switch(channel):
    if channel == 1:
        if my_gui.wcv_button.config("text")[-1] == "On":
            my_gui.wcv_button.config(text="Off", bg="#7883c1")
            my_gui.label1.image = my_gui.blank_image
        else:
            my_gui.wcv_button.config(text="On", bg="#42dfc9")
    elif channel == 2:
        if my_gui.msv_button.config("text")[-1] == "On":
            my_gui.msv_button.config(text="Off", bg="#7883c1")
            my_gui.label2.image = my_gui.blank_image
        else:
            my_gui.msv_button.config(text="On", bg="#42dfc9")
    else:
        if my_gui.cv_button.config("text")[-1] == "On":
            my_gui.cv_button.config(text="Off", bg="#7883c1")
            my_gui.label3.image = my_gui.blank_image
        else:
            my_gui.cv_button.config(text="On", bg="#42dfc9")


# fungsi untuk memilih index camera
def select_index():
    global cam_index
    if my_gui.slc_button.config("text")[-1] == "Select":
        cam_index = int(my_gui.index_var.get())
        my_gui.slc_button.config(text="Deselect", bg="#7883c1")
    elif my_gui.slc_button.config("text")[-1] == "Deselect":
        cam_index = None
        my_gui.slc_button.config(text="Select", bg="#42dfc9")


# fungsi untuk memilih warna yang akan dideteksi
def select_color():
    global cam_index
    if my_gui.color_button.config("text")[-1] == "SET":
        global cap
        cap = cv2.VideoCapture(cam_index)
        color = my_gui.color_var.get()
        # if color == "Merah":
        #     set_hsv(136, 87, 111, 180, 255, 255)
        # elif color == "Hijau":
        #     set_hsv(25, 52, 72, 102, 255, 255)
        # else:
        #     set_hsv(94, 90, 2, 120, 255, 255)
        if color == "Merah":
            set_hsv(0, 50, 50, 10, 255, 255)
        elif color == "Hijau":
            set_hsv(40, 50, 50, 80, 255, 255)
        else:
            set_hsv(90, 50, 50, 130, 255, 255)
        # threading.Thread(target=detect_color(color)).start
        detect_color()
        my_gui.color_button.config(text="RESET", bg="#7883c1")

    else:
        cap.release()
        my_gui.color_button.config(text="SET", bg="#42dfc9")


# fungsi untuk mendeteksi warna yang telah dipilih
def detect_color():
    try:
        _, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (530, 400))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        l_b = np.array(
            [
                my_gui.hue_bawah.get(),
                my_gui.saturation_bawah.get(),
                my_gui.value_bawah.get(),
            ]
        )
        u_b = np.array(
            [
                my_gui.hue_atas.get(),
                my_gui.saturation_atas.get(),
                my_gui.value_atas.get(),
            ]
        )

        mask = cv2.inRange(hsv, l_b, u_b)
        kernal = np.ones((5, 5), "uint8")
        color = cv2.dilate(mask, kernal)
        res = cv2.bitwise_and(img, img, mask=mask)
        rgb2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        contours, _ = cv2.findContours(color, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > my_gui.var_area.get():
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                circle = cv2.circle(rgb, center, 10, (66, 223, 201), 3)
                if serial_condition == True and my_gui.servo_cond.get() == False:
                    serial_data2(img, x, y)
                update_coordinate(int(x), int(y))

        webcam_frame(rgb, my_gui.label1, 20, 35)
        frame(
            mask,
            my_gui.label2,
            560,
            35,
            260,
            196,
            my_gui.msv_button.config("text")[-1],
        )
        frame(
            rgb2, my_gui.label3, 560, 239, 260, 196, my_gui.cv_button.config("text")[-1]
        )
        my_gui.window.after(20, detect_color)

    except PermissionError as e:
        messagebox.showinfo("Port Sibuk", "Pastikan Memilih Port yang Sesuai")
        detect_color(select_color)

    except cv2.error as e:
        messagebox.showinfo("Warna di RESET", "silahkan SET warna terlebih dahulu")


# fungsi menampilkan frame video masking
def frame(img, label, x, y, w, h, kondisi_saklar):
    img = cv2.resize(img, (w, h))
    image = Image.fromarray(img)
    imageTk = ImageTk.PhotoImage(image)
    label.configure(image=imageTk)
    if kondisi_saklar == "On":
        label.image = imageTk
    else:
        label.image = my_gui.blank_image
    label.place(x=x, y=y)


# fungsi menampilkan frame video webcam
def webcam_frame(img, label, x, y):
    image = Image.fromarray(img)
    imageTk = ImageTk.PhotoImage(image)
    label.configure(image=imageTk)
    if my_gui.wcv_button.config("text")[-1] == "On":
        label.image = imageTk
    else:
        label.image = my_gui.blank_image
        my_gui.label1.config(bg="#141835")
    label.place(x=x, y=y)


def set_hsv(h_lower, s_lower, v_lower, h_upper, s_upper, v_upper):
    my_gui.h_bawah.set(h_lower)
    my_gui.h_atas.set(h_upper)
    my_gui.s_atas.set(s_upper)
    my_gui.s_bawah.set(s_lower)
    my_gui.v_atas.set(v_upper)
    my_gui.v_bawah.set(v_lower)


def update_coordinate(x, y):
    my_gui.coordX_val.config(text=str(x))
    my_gui.coordY_val.config(text=str(y))


if __name__ == "__main__":
    serial_condition = False
    panAngle = 90
    tiltAngle = 15
    port = None
    cam_index = None

    root = Tk()
    my_gui = GUI(root)
    my_gui.dark_title_bar(root)
    root.mainloop()
