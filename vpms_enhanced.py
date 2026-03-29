import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import time
from datetime import datetime
from tkvideo import tkvideo
import pandas as pd


win = Tk()
win.geometry("1550x800")
win.title("VPMS — Vehicle Parking Management System")

# ── Colour Palette (change here to retheme everything) ────────────────────────
C = {
    # Base surfaces
    "bg_dark":      "#0D1B2A",   # deep navy  – main window / sidebar bg
    "bg_mid":       "#1B2A3B",   # medium navy – card / panel backgrounds
    "bg_light":     "#243447",   # lighter navy – elevated surfaces
    "sidebar":      "#111D2E",   # slightly darker for sidebar contrast

    # Accent & action
    "accent":       "#00C6AE",   # teal-green – primary accent
    "accent_dim":   "#00957F",   # darker teal – hover / pressed
    "accent_glow":  "#00FFD4",   # bright mint – highlights / count labels

    # Semantic colours
    "danger":       "#FF4D6D",   # vivid red-pink
    "warning":      "#FFB703",   # amber
    "success":      "#06D6A0",   # emerald
    "info":         "#118AB2",   # steel blue

    # Text
    "text_primary":   "#E8F4F8",
    "text_secondary":  "#8BA5BE",
    "text_muted":      "#506070",

    # Borders / separators
    "border":        "#1E3550",
    "separator":     "#22384F",
}

FONT_HEAD  = ("Segoe UI",  32, "bold")
FONT_TITLE = ("Segoe UI",  22, "bold")
FONT_LABEL = ("Segoe UI",  14, "bold")
FONT_BODY  = ("Segoe UI",  13)
FONT_MONO  = ("Consolas",  14, "bold")
FONT_CLOCK = ("Segoe UI",  44, "bold")
FONT_COUNT = ("Segoe UI",  60, "bold")
FONT_BTN   = ("Segoe UI",  13, "bold")

BTN_DEFAULTS = dict(
    font=FONT_BTN,
    relief="flat",
    cursor="hand2",
    activeforeground=C["text_primary"],
)


def styled_btn(parent, text, command, bg=None, fg=None, width=18):
    bg = bg or C["accent"]
    fg = fg or C["bg_dark"]
    btn = Button(
        parent, text=text, command=command,
        bg=bg, fg=fg,
        activebackground=C["accent_dim"],
        width=width,
        **BTN_DEFAULTS,
    )
    # Subtle hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=C["accent_glow"] if bg == C["accent"] else bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def separator(parent, orient="h", length=400, bg=None):
    bg = bg or C["separator"]
    if orient == "h":
        Frame(parent, width=length, height=2, bg=bg).pack(fill="x", padx=0)
    else:
        Frame(parent, width=2, height=length, bg=bg).pack(fill="y", pady=0)


# ── Database initialisation ────────────────────────────────────────────────────

def create_database():
    with sqlite3.connect("user_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )''')
        conn.commit()


# ── Reusable underline-entry widget ───────────────────────────────────────────

def underline_entry(parent, show=None, width=22):
    """Returns (container_frame, entry_widget) — bottom-border only styling."""
    container = Frame(parent, bg=C["bg_mid"])
    ent = Entry(
        container, width=width, border=0,
        font=FONT_MONO,
        bg=C["bg_mid"],
        fg=C["text_primary"],
        insertbackground=C["accent"],
        show=show or "",
    )
    ent.pack()
    Frame(container, height=2, bg=C["accent"]).pack(fill="x")
    return container, ent


# ── Login page ─────────────────────────────────────────────────────────────────

def loginpage():
    Frame_login = Frame(win, width=1550, height=800, bg=C["bg_dark"])
    Frame_login.place(x=0, y=0)

    global us, bg1
    us  = PhotoImage(file="login.png")
    bg1 = PhotoImage(file="admin_logo.png")
    Label(Frame_login, image=us,  bg=C["bg_dark"]).place(x=150, y=200)
    Label(win,         image=bg1, bg=C["bg_dark"]).place(x=1300, y=600)

    # ── Right panel card ──
    global Frame1
    Frame1 = Frame(Frame_login, width=520, height=520, bg=C["bg_mid"],
                   highlightthickness=1, highlightbackground=C["border"])
    Frame1.place(x=890, y=90)

    # Accent top bar on card
    Frame(Frame1, width=520, height=4, bg=C["accent"]).place(x=0, y=0)

    Label(Frame1, text="Employee Login",
          font=FONT_HEAD, fg=C["accent"], bg=C["bg_mid"]).place(x=60, y=40)
    Label(Frame1, text="Sign in to continue",
          font=FONT_BODY, fg=C["text_secondary"], bg=C["bg_mid"]).place(x=62, y=100)

    Label(Frame1, text="USERNAME", font=("Segoe UI", 10, "bold"),
          fg=C["text_muted"], bg=C["bg_mid"]).place(x=60, y=145)
    uf, user = underline_entry(Frame1)
    uf.place(x=60, y=168)
    user.focus_set()

    Label(Frame1, text="PASSWORD", font=("Segoe UI", 10, "bold"),
          fg=C["text_muted"], bg=C["bg_mid"]).place(x=60, y=240)
    pf, pswd = underline_entry(Frame1, show="●")
    pf.place(x=60, y=263)

    def enter_(e):
        pswd.focus_set()
    user.bind('<Return>', enter_)

    def login(e=None):
        username = user.get()
        password = pswd.get()
        if not username and not password:
            messagebox.showerror("Error", "Please Enter Username & Password")
            return
        with sqlite3.connect("user_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            authenticated_user = cursor.fetchone()
        if authenticated_user:
            messagebox.showinfo("Success", "Login successful!")
            afterlogin_gui()
        else:
            user.delete(0, END)
            pswd.delete(0, END)
            messagebox.showerror("Error", "Please Register First")

    def register_user():
        username = user.get()
        password = pswd.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        with sqlite3.connect("user_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists. Choose a different one.")
            else:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")

    pswd.bind('<Return>', login)

    styled_btn(Frame1, "SIGN IN", login, width=38).place(x=22, y=340)
    Button(
        Frame1, text="Don't have an account?  Register →",
        command=register_user,
        fg=C["accent"], bg=C["bg_mid"], font=FONT_BODY,
        border=0, cursor="hand2", activeforeground=C["accent_glow"],
        activebackground=C["bg_mid"],
    ).place(x=100, y=405)

    Button(
        win, text="Admin Login",
        command=admin_login,
        fg=C["text_secondary"], bg=C["bg_dark"],
        font=("Segoe UI", 12), border=0, cursor="hand2",
        activeforeground=C["accent"], activebackground=C["bg_dark"],
    ).place(x=1150, y=640)


# ── Admin login ────────────────────────────────────────────────────────────────

def admin_login():
    Frame_admin = Frame(win, width=1550, height=780, bg=C["bg_dark"])
    Frame_admin.place(x=0, y=0)

    global addm
    addm = PhotoImage(file="login.png")
    Label(Frame_admin, image=addm, bg=C["bg_dark"]).place(x=150, y=200)

    Frame1 = Frame(Frame_admin, width=520, height=520, bg=C["bg_mid"],
                   highlightthickness=1, highlightbackground=C["border"])
    Frame1.place(x=890, y=90)

    Frame(Frame1, width=520, height=4, bg=C["danger"]).place(x=0, y=0)

    Label(Frame1, text="Admin Login",
          font=FONT_HEAD, fg=C["danger"], bg=C["bg_mid"]).place(x=60, y=40)
    Label(Frame1, text="Authorised access only",
          font=FONT_BODY, fg=C["text_secondary"], bg=C["bg_mid"]).place(x=62, y=100)

    Label(Frame1, text="USERNAME", font=("Segoe UI", 10, "bold"),
          fg=C["text_muted"], bg=C["bg_mid"]).place(x=60, y=145)
    uf, user = underline_entry(Frame1)
    uf.place(x=60, y=168)
    user.focus_set()

    Label(Frame1, text="PASSWORD", font=("Segoe UI", 10, "bold"),
          fg=C["text_muted"], bg=C["bg_mid"]).place(x=60, y=240)
    pf, pswd = underline_entry(Frame1, show="●")
    pf.place(x=60, y=263)

    Frame(Frame1, width=400, height=2, bg=C["border"]).place(x=60, y=200)
    Frame(Frame1, width=400, height=2, bg=C["border"]).place(x=60, y=300)

    def admin_authenticate():
        if user.get() == "admin" and pswd.get() == "admin@1234":
            messagebox.showinfo("Success", "Admin login successful...")
            after_adminlogin()
        else:
            user.delete(0, END)
            pswd.delete(0, END)
            messagebox.showerror("Error", "Wrong Username or Password")

    styled_btn(Frame1, "SIGN IN", admin_authenticate,
               bg=C["danger"], fg=C["text_primary"], width=38).place(x=22, y=340)


# ── After admin login ──────────────────────────────────────────────────────────

def after_adminlogin():
    Frame_admin = Frame(win, width=1550, height=800, bg=C["bg_dark"])
    Frame_admin.place(x=0, y=0)

    global admin
    admin = PhotoImage(file="admin_logo1.png")
    Label(Frame_admin, image=admin, bg=C["bg_dark"]).place(x=110, y=100)
    Label(Frame_admin, text="Welcome, Admin",
          font=("Segoe UI", 36, "bold"), fg=C["accent"], bg=C["bg_dark"]).place(x=110, y=500)

    # ── Top button bar ──
    btn_bar = Frame(Frame_admin, bg=C["bg_mid"], height=60)
    btn_bar.place(x=600, y=120, width=900)

    def make_admin_btn(text, cmd, x):
        btn = Button(
            Frame_admin, text=text, command=cmd,
            bg=C["bg_light"], fg=C["text_primary"],
            font=FONT_BTN, relief="flat", cursor="hand2",
            activebackground=C["accent"], activeforeground=C["bg_dark"],
            width=16,
        )
        btn.place(x=x, y=130)

    def show_user():
        Frame_admin1 = Frame(Frame_admin, width=900, height=550,
                             bg=C["bg_mid"], highlightthickness=1,
                             highlightbackground=C["border"])
        Frame_admin1.place(x=600, y=200)
        Label(Frame_admin1, text="Employee Details",
              font=FONT_TITLE, fg=C["accent"], bg=C["bg_mid"]).place(x=20, y=10)

        with sqlite3.connect("user_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, password FROM users')
            rows = cursor.fetchall()

        s = ttk.Style()
        s.theme_use("clam")
        s.configure(".",                background=C["bg_mid"], foreground=C["text_primary"],
                                        font=("Segoe UI", 13))
        s.configure("Treeview",         background=C["bg_light"], foreground=C["text_primary"],
                                        fieldbackground=C["bg_light"], rowheight=28)
        s.configure("Treeview.Heading", background=C["bg_dark"], foreground=C["accent"],
                                        font=("Segoe UI", 14, "bold"))
        s.map("Treeview", background=[("selected", C["accent"])],
              foreground=[("selected", C["bg_dark"])])

        tree = ttk.Treeview(Frame_admin1, height=12, style="Treeview")
        tree.place(x=20, y=55)
        tree['show'] = 'headings'
        tree['columns'] = ('Sr.', 'Username', 'Password')
        for column in tree['columns']:
            tree.heading(column, text=column)
        tree.column("Sr.",      width=55)
        tree.column("Username", width=130)
        tree.column("Password", width=150)
        for c, row in enumerate(rows, start=1):
            tree.insert('', 'end', values=(c,) + row)

    def configure_values():
        Frame_admin2 = Frame(Frame_admin, width=900, height=550,
                             bg=C["bg_mid"], highlightthickness=1,
                             highlightbackground=C["border"])
        Frame_admin2.place(x=600, y=200)
        Label(Frame_admin2, text="Configure Parking Slots",
              font=FONT_TITLE, fg=C["accent"], bg=C["bg_mid"]).place(x=20, y=10)

        note = "Note: This step should be done only once\nduring first-time software installation."
        Label(Frame_admin2, text=note, font=FONT_BODY, bg=C["bg_mid"],
              fg=C["warning"]).place(x=150, y=440)

        Label(Frame_admin2, text="Vehicle Type :", font=FONT_LABEL,
              bg=C["bg_mid"], fg=C["text_secondary"]).place(x=150, y=200)
        entry1 = ttk.Combobox(Frame_admin2, values=["CAR", "BUS", "TRUCK", "BIKE"],
                               width=20, font=FONT_BODY)
        entry1.place(x=150, y=235)

        Label(Frame_admin2, text="Total Slots :", font=FONT_LABEL,
              bg=C["bg_mid"], fg=C["text_secondary"]).place(x=500, y=200)
        entry2 = Entry(Frame_admin2, width=6, border=0, font=FONT_MONO,
                       bg=C["bg_light"], fg=C["text_primary"],
                       insertbackground=C["accent"])
        entry2.place(x=500, y=235)

        with sqlite3.connect("vehicle_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entryexit (
                    vehicle_No   TEXT UNIQUE,
                    Owner_Name   TEXT,
                    Mob_No       TEXT,
                    Vehicle_Type TEXT,
                    Date         TEXT,
                    Intime       TEXT
                )''')
            conn.commit()

        def conf_value():
            Type     = entry1.get()
            slot_nos = entry2.get()
            with sqlite3.connect("vehicle_database.db") as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS dashvalue (type TEXT, slots INTEGER)')
                cursor.execute("INSERT INTO dashvalue (type, slots) VALUES (?, ?)", (Type, slot_nos))
                conn.commit()
            messagebox.showinfo("Success", "Configuration Successful.")
            entry1.delete(0, END)
            entry2.delete(0, END)

        styled_btn(Frame_admin2, "SUBMIT", conf_value, width=16).place(x=350, y=360)

    def update_values():
        Frame_admin3 = Frame(Frame_admin, width=900, height=550,
                             bg=C["bg_mid"], highlightthickness=1,
                             highlightbackground=C["border"])
        Frame_admin3.place(x=600, y=200)
        Label(Frame_admin3, text="Update Slot Count",
              font=FONT_TITLE, fg=C["accent"], bg=C["bg_mid"]).place(x=20, y=10)

        Label(Frame_admin3, text="Vehicle Type :", font=FONT_LABEL,
              bg=C["bg_mid"], fg=C["text_secondary"]).place(x=150, y=200)
        entry4 = ttk.Combobox(Frame_admin3, values=["CAR", "BUS", "TRUCK", "BIKE"],
                               width=20, font=FONT_BODY)
        entry4.place(x=150, y=235)

        Label(Frame_admin3, text="New Slots :", font=FONT_LABEL,
              bg=C["bg_mid"], fg=C["text_secondary"]).place(x=500, y=200)
        entry5 = Entry(Frame_admin3, width=6, border=0, font=FONT_MONO,
                       bg=C["bg_light"], fg=C["text_primary"],
                       insertbackground=C["accent"])
        entry5.place(x=500, y=235)

        def upd_value():
            Type     = entry4.get()
            slot_nos = entry5.get()
            with sqlite3.connect("vehicle_database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE dashvalue SET slots=? WHERE type=?", (slot_nos, Type))
                conn.commit()
            messagebox.showinfo("Success", "Update Successful.")
            entry4.delete(0, END)
            entry5.delete(0, END)

        styled_btn(Frame_admin3, "SUBMIT", upd_value, width=16).place(x=350, y=360)

    make_admin_btn("EMPLOYEE DETAILS", show_user,        610)
    make_admin_btn("CONFIGURE",        configure_values, 830)
    make_admin_btn("UPDATE",           update_values,    1060)
    make_admin_btn("LOGOUT",           loginpage,        1290)


# ── Dashboard ──────────────────────────────────────────────────────────────────

def dashboard():
    global car, bus, truck, bike

    Frame2 = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame2.place(x=270, y=150)

    Label(Frame2, text="DASHBOARD", font=("Segoe UI", 34, "bold"),
          fg=C["accent"], bg=C["bg_mid"]).place(x=50, y=20)
    Frame(Frame2, width=200, height=3, bg=C["accent"]).place(x=50, y=80)

    car   = PhotoImage(file="car_logo.png",   width=250, height=250)
    bike  = PhotoImage(file="bike_logo.png",  width=250, height=250)
    bus   = PhotoImage(file="bus_logo.png",   width=250, height=250)
    truck = PhotoImage(file="truck_logo.png", width=250, height=250)

    vehicles = [
        (car,   "CARS",   100,  200),
        (bike,  "BIKES",  400,  200),
        (bus,   "BUSES",  700,  200),
        (truck, "TRUCKS", 1000, 200),
    ]
    for img, label, x, y in vehicles:
        card = Frame(Frame2, width=250, height=260,
                     bg=C["bg_light"], highlightthickness=1,
                     highlightbackground=C["border"])
        card.place(x=x - 10, y=y - 10)
        Label(card, image=img, bg=C["bg_light"]).place(x=0, y=0)
        Label(card, text=label, font=("Segoe UI", 14, "bold"),
              fg=C["text_secondary"], bg=C["bg_light"]).place(x=80, y=220)

    with sqlite3.connect("vehicle_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BUS'")
        total_bus = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BIKE'")
        total_bike = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='CAR'")
        total_car = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='TRUCK'")
        total_truck = cursor.fetchone()[0]

    counts = [total_car, total_bike, total_bus, total_truck]
    xs     = [165, 465, 765, 1060]
    for val, x in zip(counts, xs):
        Label(Frame2, text=str(val), font=FONT_COUNT,
              fg=C["accent_glow"], bg=C["bg_mid"]).place(x=x, y=455)


# ── Add Entry ──────────────────────────────────────────────────────────────────

def addentry():
    Frame_addentry = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame_addentry.place(x=270, y=150)

    Label(Frame_addentry, text="ADD NEW ENTRY", font=("Segoe UI", 30, "bold"),
          fg=C["success"], bg=C["bg_mid"]).place(x=50, y=20)
    Frame(Frame_addentry, width=240, height=3, bg=C["success"]).place(x=50, y=78)

    lblvdo1 = Label(Frame_addentry, bg=C["bg_mid"])
    lblvdo1.place(x=270, y=240)
    player = tkvideo("carvdo1.mp4", lblvdo1, loop=1, size=(700, 350))
    player.play()

    fields = [
        ("Vehicle No :",   "#FFEC87", 50,  120),
        ("Owner Name :",   "#FFEC87", 50,  185),
        ("Mobile No :",    "#FFEC87", 550, 120),
    ]

    def lbl(parent, text, x, y):
        Label(parent, text=text, font=FONT_LABEL, bg=C["bg_mid"],
              fg=C["text_secondary"]).place(x=x, y=y)

    lbl(Frame_addentry, "Vehicle No :", 50, 120)
    vehno = Entry(Frame_addentry, width=20, border=0, font=FONT_MONO,
                  bg=C["bg_light"], fg=C["text_primary"], insertbackground=C["accent"])
    vehno.place(x=230, y=123)
    Frame(Frame_addentry, width=220, height=2, bg=C["accent"]).place(x=230, y=150)

    lbl(Frame_addentry, "Owner Name :", 50, 185)
    owname = Entry(Frame_addentry, width=20, border=0, font=FONT_MONO,
                   bg=C["bg_light"], fg=C["text_primary"], insertbackground=C["accent"])
    owname.place(x=230, y=188)
    Frame(Frame_addentry, width=220, height=2, bg=C["accent"]).place(x=230, y=215)

    lbl(Frame_addentry, "Mobile No :", 550, 120)
    mobno = Entry(Frame_addentry, width=20, border=0, font=FONT_MONO,
                  bg=C["bg_light"], fg=C["text_primary"], insertbackground=C["accent"])
    mobno.place(x=720, y=123)
    Frame(Frame_addentry, width=220, height=2, bg=C["accent"]).place(x=720, y=150)

    lbl(Frame_addentry, "Vehicle Type :", 550, 185)
    vtype = ttk.Combobox(Frame_addentry, values=["CAR", "BUS", "TRUCK", "BIKE"],
                         width=19, font=FONT_BODY)
    vtype.place(x=720, y=188)

    def insert_record():
        Vehicle_No   = vehno.get().strip()
        Owner_Name   = owname.get().strip()
        Mobile_No    = mobno.get().strip()
        Vehicle_Type = vtype.get()
        Intime       = time.strftime("%H:%M:%S")
        Date         = str(datetime.now().date())

        if not Vehicle_No:
            messagebox.showwarning("Error", "Please enter all details")
            return

        with sqlite3.connect("vehicle_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entryexit (
                    vehicle_No   TEXT UNIQUE,
                    Owner_Name   TEXT,
                    Mob_No       TEXT,
                    Vehicle_Type TEXT,
                    Date         TEXT,
                    Intime       TEXT
                )''')
            cursor.execute(
                "INSERT INTO entryexit (vehicle_No, Owner_Name, Mob_No, Vehicle_Type, Date, Intime)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (Vehicle_No, Owner_Name, Mobile_No, Vehicle_Type, Date, Intime)
            )
            conn.commit()

        vehno.delete(0, END)
        owname.delete(0, END)
        mobno.delete(0, END)
        vtype.delete(0, END)
        messagebox.showinfo("Success", "Entry Added Successfully")

    styled_btn(Frame_addentry, "SUBMIT DETAILS", insert_record,
               bg=C["success"], fg=C["bg_dark"], width=18).place(x=1000, y=148)


# ── Delete Entry ───────────────────────────────────────────────────────────────

def deleteentry():
    Frame_deleteentry = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame_deleteentry.place(x=270, y=150)

    Label(Frame_deleteentry, text="DELETE ENTRY", font=("Segoe UI", 30, "bold"),
          fg=C["danger"], bg=C["bg_mid"]).place(x=50, y=20)
    Frame(Frame_deleteentry, width=210, height=3, bg=C["danger"]).place(x=50, y=78)

    Label(Frame_deleteentry, text="Enter Vehicle Number :", font=FONT_LABEL,
          bg=C["bg_mid"], fg=C["text_secondary"]).place(x=50, y=150)

    veh_no = Entry(Frame_deleteentry, width=20, border=0, font=FONT_MONO,
                   bg=C["bg_light"], fg=C["text_primary"], insertbackground=C["accent"])
    veh_no.place(x=330, y=153)
    Frame(Frame_deleteentry, width=220, height=2, bg=C["danger"]).place(x=330, y=180)

    lblvdo2 = Label(Frame_deleteentry, bg=C["bg_mid"])
    lblvdo2.place(x=200, y=250)
    player = tkvideo("carvdo2.mp4", lblvdo2, loop=1, size=(800, 350))
    player.play()

    def delete_record():
        Vehicle_No1 = veh_no.get().strip()
        if not Vehicle_No1:
            messagebox.showwarning("Error", "Please enter Vehicle Number !!!")
            return

        Date     = str(datetime.now().date())
        Out_time = time.strftime("%H:%M:%S")

        with sqlite3.connect("vehicle_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehicle_history (
                    vehicle_No   TEXT UNIQUE,
                    Owner_Name   TEXT,
                    Mob_No       TEXT,
                    Vehicle_Type TEXT,
                    In_Date      TEXT,
                    Intime       TEXT,
                    Out_Date     TEXT,
                    Outtime      TEXT
                )''')

            cursor.execute("SELECT * FROM entryexit WHERE vehicle_No=?", (Vehicle_No1,))
            row_to_copy = cursor.fetchone()

            if not row_to_copy:
                messagebox.showerror("Error", "Vehicle number not found!")
                return

            final_row = (*row_to_copy, Date, Out_time)
            cursor.execute("INSERT INTO vehicle_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)", final_row)
            cursor.execute("DELETE FROM entryexit WHERE vehicle_No=?", (Vehicle_No1,))
            conn.commit()

        veh_no.delete(0, END)
        messagebox.showinfo("Success", "Entry Deleted Successfully")

    styled_btn(Frame_deleteentry, "DELETE", delete_record,
               bg=C["danger"], fg=C["text_primary"], width=20).place(x=680, y=145)


# ── Show Database ──────────────────────────────────────────────────────────────

def _apply_tree_style():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure(".",                background=C["bg_light"], foreground=C["text_primary"],
                                    font=("Segoe UI", 13))
    s.configure("Treeview",         background=C["bg_light"], foreground=C["text_primary"],
                                    fieldbackground=C["bg_light"], rowheight=28)
    s.configure("Treeview.Heading", background=C["bg_dark"], foreground=C["accent"],
                                    font=("Segoe UI", 14, "bold"))
    s.map("Treeview", background=[("selected", C["accent"])],
          foreground=[("selected", C["bg_dark"])])


def showdatabase():

    def show_current():
        Frame_showdatabase = Frame(win, width=1275, height=645, bg=C["bg_mid"])
        Frame_showdatabase.place(x=270, y=150)
        Label(Frame_showdatabase, text="DATABASE — Current Vehicles",
              font=("Segoe UI", 28, "bold"), fg=C["accent"], bg=C["bg_mid"]).place(x=50, y=20)

        styled_btn(Frame_showdatabase, "Show History", show_history,
                   bg=C["info"], fg=C["text_primary"], width=15).place(x=950, y=50)

        with sqlite3.connect("vehicle_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM entryexit')
            rows = cursor.fetchall()

        _apply_tree_style()
        tree = ttk.Treeview(Frame_showdatabase, height=20)
        tree.place(x=20, y=100)
        tree['show'] = 'headings'
        tree['columns'] = ('Sr_No', 'Vehicle_No', 'Owner_Name', 'Mobile_No', 'Type', 'In-Date', 'In-Time')

        for column in tree['columns']:
            tree.heading(column, text=column)

        tree.column("Sr_No",      width=72)
        tree.column("Type",       width=100)
        tree.column("In-Date",    width=120)
        tree.column("In-Time",    width=110)
        tree.column("Mobile_No",  width=135)
        tree.column("Owner_Name", width=235)
        tree.column("Vehicle_No", width=150)

        for c, row in enumerate(rows, start=1):
            tree.insert('', 'end', values=(c,) + row)

    def show_history():
        Frame_showdatabase = Frame(win, width=1275, height=645, bg=C["bg_mid"])
        Frame_showdatabase.place(x=270, y=150)
        Label(Frame_showdatabase, text="DATABASE — Vehicle History",
              font=("Segoe UI", 28, "bold"), fg=C["accent"], bg=C["bg_mid"]).place(x=50, y=20)

        styled_btn(Frame_showdatabase, "Show Current Data", show_current,
                   bg=C["info"], fg=C["text_primary"], width=18).place(x=950, y=50)

        with sqlite3.connect("vehicle_database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vehicle_history')
            rows = cursor.fetchall()

        _apply_tree_style()
        tree = ttk.Treeview(Frame_showdatabase, height=20)
        tree.place(x=20, y=100)
        tree['show'] = 'headings'
        tree['columns'] = ('Sr_No', 'Vehicle_No', 'Owner_Name', 'Mobile_No',
                           'Type', 'In-Date', 'In-Time', 'Out-Date', 'Out-Time')

        for column in tree['columns']:
            tree.heading(column, text=column)

        tree.column("Sr_No",      width=72)
        tree.column("Type",       width=100)
        tree.column("In-Date",    width=120)
        tree.column("Out-Date",   width=120)
        tree.column("In-Time",    width=110)
        tree.column("Out-Time",   width=110)
        tree.column("Mobile_No",  width=140)
        tree.column("Owner_Name", width=220)
        tree.column("Vehicle_No", width=160)

        for c, row in enumerate(rows, start=1):
            tree.insert('', 'end', values=(c,) + row)

    show_current()


# ── Parking Slots ──────────────────────────────────────────────────────────────

def parking_slot():
    global car, bus, truck, bike

    Frame_parking = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame_parking.place(x=270, y=150)
    Label(Frame_parking, text="REMAINING SLOTS", font=("Segoe UI", 32, "bold"),
          bg=C["bg_mid"], fg=C["accent"]).place(x=50, y=20)
    Frame(Frame_parking, width=275, height=3, bg=C["accent"]).place(x=50, y=80)

    car   = PhotoImage(file="car_clipart.png")
    bike  = PhotoImage(file="bike_clipart.png")
    bus   = PhotoImage(file="bus_clipart.png")
    truck = PhotoImage(file="truck_clipart.png")

    vehicle_data = [
        (car,   "CARS",   50,   170, 120,  370),
        (bike,  "BIKES",  380,  130, 450,  370),
        (bus,   "BUSES",  700,  130, 770,  370),
        (truck, "TRUCKS", 1000, 130, 1055, 370),
    ]
    for img, label, ix, iy, lx, ly in vehicle_data:
        Label(Frame_parking, image=img,  bg=C["bg_mid"]).place(x=ix, y=iy)
        Label(Frame_parking, text=label, font=FONT_LABEL,
              fg=C["text_secondary"], bg=C["bg_mid"]).place(x=lx, y=ly)

    with sqlite3.connect("vehicle_database.db") as conn:
        cursor = conn.cursor()
        def _count(vtype):
            cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type=?", (vtype,))
            return cursor.fetchone()[0]
        def _slots(vtype):
            cursor.execute("SELECT slots FROM dashvalue WHERE type=?", (vtype,))
            row = cursor.fetchone()
            return row[0] if row else 0

        remaining = {
            "CAR":   _slots("CAR")   - _count("CAR"),
            "BIKE":  _slots("BIKE")  - _count("BIKE"),
            "BUS":   _slots("BUS")   - _count("BUS"),
            "TRUCK": _slots("TRUCK") - _count("TRUCK"),
        }

    positions = [("CAR", 105, 410), ("BIKE", 435, 410), ("BUS", 745, 410), ("TRUCK", 1040, 410)]
    for key, x, y in positions:
        val = remaining[key]
        color = C["accent_glow"] if val > 5 else C["warning"] if val > 0 else C["danger"]
        Label(Frame_parking, text=str(val), font=FONT_COUNT,
              fg=color, bg=C["bg_mid"]).place(x=x, y=y)


# ── Export to Excel ────────────────────────────────────────────────────────────

def convertxl():
    Frame_convertxl = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame_convertxl.place(x=270, y=150)

    Label(Frame_convertxl, text="EXPORT TO EXCEL", font=("Segoe UI", 30, "bold"),
          fg=C["warning"], bg=C["bg_mid"]).place(x=50, y=20)
    Frame(Frame_convertxl, width=265, height=3, bg=C["warning"]).place(x=50, y=78)

    Label(Frame_convertxl, text="File Name :", font=FONT_LABEL,
          fg=C["text_secondary"], bg=C["bg_mid"]).place(x=50, y=150)
    file_name = Entry(Frame_convertxl, width=22, border=0, font=FONT_MONO,
                      bg=C["bg_light"], fg=C["text_primary"],
                      insertbackground=C["accent"])
    file_name.place(x=230, y=152)
    Frame(Frame_convertxl, width=240, height=2, bg=C["warning"]).place(x=230, y=179)

    Label(Frame_convertxl, text="Select Data :", font=FONT_LABEL,
          fg=C["text_secondary"], bg=C["bg_mid"]).place(x=50, y=210)
    ftype = ttk.Combobox(Frame_convertxl,
                         values=["CURRENT VEHICLES", "VEHICLE'S HISTORY"],
                         width=18, font=FONT_BODY)
    ftype.place(x=230, y=212)

    def convert_to_xl():
        fname = file_name.get().strip()
        if not fname:
            messagebox.showerror("Error", "Please Enter File Name")
            return

        table_name = "entryexit" if ftype.get() == "CURRENT VEHICLES" else "vehicle_history"
        downloads  = os.path.join(os.path.expanduser("~"), "Downloads")
        path       = os.path.join(downloads, fname + ".xlsx")

        with sqlite3.connect("vehicle_database.db") as conn:
            df = pd.read_sql_query("SELECT * FROM {}".format(table_name), conn)

        df.to_excel(path, index=False)
        messagebox.showinfo("Success", "Excel file saved at:\n" + path)
        file_name.delete(0, END)

    styled_btn(Frame_convertxl, "EXPORT", convert_to_xl,
               bg=C["warning"], fg=C["bg_dark"], width=18).place(x=560, y=148)


# ── Main GUI (post-login) ──────────────────────────────────────────────────────

def afterlogin_gui():
    # ── Top bar ──
    Frame_top  = Frame(win, width=1550, height=150, bg=C["bg_dark"])
    Frame_top.place(x=0, y=0)

    # ── Left sidebar ──
    Frame_left = Frame(win, width=270, height=650, bg=C["sidebar"])
    Frame_left.place(x=0, y=149)

    # ── Content area default ──
    Frame2 = Frame(win, width=1275, height=645, bg=C["bg_mid"])
    Frame2.place(x=260, y=150)

    # ── Video in sidebar ──
    lblvdo = Label(Frame_left, bg=C["sidebar"])
    lblvdo.place(x=0, y=405)
    player = tkvideo("carvdo.mp4", lblvdo, loop=1, size=(260, 250))
    player.play()

    dashboard()

    # ── Digital clock ──
    def digital_clock():
        label = Label(Frame_top, font=FONT_CLOCK, bg=C["bg_dark"], fg=C["accent"])
        label.place(x=1080, y=30)
        def tick():
            label.config(text=time.strftime("%H:%M:%S"))
            label.after(1000, tick)
        tick()

    digital_clock()

    # ── Top bar images ──
    global bg6, bg7, bg8
    bg6 = PhotoImage(file="car1.png",      height=150, width=450)
    bg7 = PhotoImage(file="park_logo.png", height=150, width=150)
    bg8 = PhotoImage(file="car2.png",      height=150, width=450)

    Label(Frame_top, image=bg6, bg=C["bg_dark"]).place(x=0,   y=0)
    Label(Frame_top, image=bg7, bg=C["bg_dark"]).place(x=460, y=0)
    Label(Frame_top, image=bg8, bg=C["bg_dark"]).place(x=610, y=0)

    # ── Sidebar nav buttons ──
    NAV = [
        ("⬛  DASHBOARD",     dashboard),
        ("＋  ADD ENTRY",     addentry),
        ("✕  DELETE ENTRY",  deleteentry),
        ("🅿  PARKING SLOT",  parking_slot),
        ("⊞  SHOW DATABASE", showdatabase),
        ("↗  EXPORT DATA",   convertxl),
        ("⏏  LOG OUT",       loginpage),
    ]
    for i, (label, cmd) in enumerate(NAV):
        btn = Button(
            Frame_left, text=label, command=cmd,
            bg=C["sidebar"], fg=C["text_secondary"],
            font=("Segoe UI", 12, "bold"),
            relief="flat", cursor="hand2", anchor="w",
            width=22,
            activebackground=C["accent"], activeforeground=C["bg_dark"],
        )
        btn.place(x=8, y=10 + i * 55)
        btn.bind("<Enter>", lambda e, b=btn: b.config(fg=C["accent"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(fg=C["text_secondary"]))

    # Separator between top-bar and sidebar/content
    Frame(Frame_top,  width=1550, height=2, bg=C["border"]).place(x=0,   y=147)
    Frame(Frame_left, width=2,    height=645, bg=C["border"]).place(x=267, y=0)


# ── Entry point ────────────────────────────────────────────────────────────────

win.configure(bg=C["bg_dark"])
create_database()
loginpage()
win.mainloop()
