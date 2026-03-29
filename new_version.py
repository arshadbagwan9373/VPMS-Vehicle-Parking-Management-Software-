import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import time
from datetime import datetime
import pandas as pd

# ── Colour palette (dark industrial / neon accent) ────────────────────────────
BG_DARK    = "#0D0F14"   # deepest background
BG_CARD    = "#141720"   # card / frame background
BG_PANEL   = "#1A1E2A"   # sidebar / secondary panels
ACCENT     = "#00C2FF"   # primary cyan-blue accent
ACCENT2    = "#7B61FF"   # purple secondary accent
SUCCESS    = "#00E676"   # green
DANGER     = "#FF4D6D"   # red
WARNING    = "#FFB74D"   # amber
TEXT_PRI   = "#EAECF4"   # primary text
TEXT_SEC   = "#6B7280"   # secondary / muted text
BORDER     = "#252A38"   # subtle border
HOVER_BG   = "#1F2435"   # hover state

FONT_TITLE  = ("Segoe UI", 28, "bold")
FONT_HEAD   = ("Segoe UI", 16, "bold")
FONT_SUBHD  = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 11)
FONT_HUGE   = ("Segoe UI", 52, "bold")

# ── Helpers ───────────────────────────────────────────────────────────────────

def styled_button(parent, text, command, color=ACCENT, text_color=BG_DARK, width=18, **kw):
    btn = Button(
        parent, text=text, command=command,
        bg=color, fg=text_color, activebackground=color, activeforeground=text_color,
        font=("Segoe UI", 11, "bold"), relief=FLAT, cursor="hand2",
        width=width, padx=10, pady=8, bd=0, **kw
    )
    def on_enter(e):  btn.config(bg=_lighten(color))
    def on_leave(e):  btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def _lighten(hex_color):
    """Return a slightly lighter hex colour for hover."""
    hex_color = hex_color.lstrip("#")
    r, g, b = [min(255, int(hex_color[i:i+2], 16) + 25) for i in (0, 2, 4)]
    return f"#{r:02x}{g:02x}{b:02x}"

def styled_entry(parent, width=22, show=None):
    e = Entry(
        parent, width=width, font=FONT_BODY,
        bg=BG_PANEL, fg=TEXT_PRI, insertbackground=ACCENT,
        relief=FLAT, bd=0, highlightthickness=1,
        highlightcolor=ACCENT, highlightbackground=BORDER
    )
    if show:
        e.config(show=show)
    return e

def section_label(parent, text, color=TEXT_SEC):
    return Label(parent, text=text.upper(), font=("Segoe UI", 9, "bold"),
                 fg=color, bg=BG_CARD, letter_spacing=2)

def card_frame(parent, **kw):
    return Frame(parent, bg=BG_CARD, highlightthickness=1,
                 highlightbackground=BORDER, **kw)

def divider(parent, orientation="h", length=400):
    if orientation == "h":
        return Frame(parent, bg=BORDER, height=1, width=length)
    return Frame(parent, bg=BORDER, width=1, height=length)

def field_row(parent, label_text, entry_widget, y_label, y_entry, x=40):
    Label(parent, text=label_text, font=("Segoe UI", 10, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=x, y=y_label)
    entry_widget.place(x=x, y=y_entry)

def badge(parent, text, color=ACCENT, bg=BG_CARD):
    return Label(parent, text=f"  {text}  ", font=("Segoe UI", 9, "bold"),
                 fg=bg, bg=color, padx=6, pady=2)

def page_title(parent, text, subtitle=""):
    Label(parent, text=text, font=FONT_TITLE,
          fg=TEXT_PRI, bg=BG_CARD).place(x=40, y=24)
    if subtitle:
        Label(parent, text=subtitle, font=FONT_BODY,
              fg=TEXT_SEC, bg=BG_CARD).place(x=44, y=68)

def stat_card(parent, x, y, title, value, color=ACCENT, icon=""):
    f = card_frame(parent, width=240, height=110)
    f.place(x=x, y=y)
    f.pack_propagate(False)
    Frame(f, bg=color, width=4, height=110).place(x=0, y=0)
    Label(f, text=icon + " " + title, font=("Segoe UI", 10, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=20, y=18)
    Label(f, text=str(value), font=("Segoe UI", 40, "bold"),
          fg=color, bg=BG_CARD).place(x=20, y=44)


# ── Treeview style (shared) ───────────────────────────────────────────────────

def apply_tree_style():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Dark.Treeview",
                background=BG_PANEL, foreground=TEXT_PRI,
                rowheight=32, fieldbackground=BG_PANEL,
                borderwidth=0, font=("Segoe UI", 10))
    s.configure("Dark.Treeview.Heading",
                background=BG_DARK, foreground=ACCENT,
                font=("Segoe UI", 10, "bold"), relief=FLAT)
    s.map("Dark.Treeview",
          background=[("selected", ACCENT2)],
          foreground=[("selected", TEXT_PRI)])
    s.map("Dark.Treeview.Heading", background=[("active", BG_PANEL)])


def styled_tree(parent, columns, col_widths, height=16):
    apply_tree_style()
    tree = ttk.Treeview(parent, style="Dark.Treeview",
                        columns=columns, show="headings", height=height)
    for col, w in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor=CENTER)
    # alternating row colours
    tree.tag_configure("odd",  background=BG_CARD)
    tree.tag_configure("even", background=BG_PANEL)
    return tree


# ── DB init ───────────────────────────────────────────────────────────────────

def create_database():
    with sqlite3.connect("user_database.db") as conn:
        conn.cursor().execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE, password TEXT)''')
        conn.commit()


# ── Main window ───────────────────────────────────────────────────────────────

win = Tk()
win.geometry("1600x860")
win.title("VPMS — Vehicle Parking Management System")
win.configure(bg=BG_DARK)
win.resizable(False, False)


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════

def loginpage():
    root = Frame(win, width=1600, height=860, bg=BG_DARK)
    root.place(x=0, y=0)

    # Left decorative panel
    left = Frame(root, width=780, height=860, bg=BG_PANEL)
    left.place(x=0, y=0)

    # Accent bar
    Frame(left, width=6, height=860, bg=ACCENT).place(x=774, y=0)

    # Big brand text on left
    Label(left, text="VPMS", font=("Segoe UI", 80, "bold"),
          fg=ACCENT, bg=BG_PANEL).place(x=80, y=160)
    Label(left, text="Vehicle Parking\nManagement System",
          font=("Segoe UI", 22), fg=TEXT_PRI, bg=BG_PANEL, justify=LEFT).place(x=82, y=310)
    Label(left, text="Smart. Fast. Reliable.", font=("Segoe UI", 13),
          fg=TEXT_SEC, bg=BG_PANEL).place(x=84, y=400)

    # Decorative grid lines
    for i in range(6):
        Frame(left, width=700, height=1, bg=BORDER).place(x=50, y=500 + i*40)
    for i in range(5):
        Frame(left, width=1, height=200, bg=BORDER).place(x=190 + i*130, y=500)

    # Glowing circle accent
    canvas = Canvas(left, width=200, height=200, bg=BG_PANEL, highlightthickness=0)
    canvas.place(x=520, y=600)
    for r, alpha in [(100, "#0D1F33"), (80, "#0A2744"), (60, "#0D3A66"), (40, "#0F5299"), (20, "#00C2FF")]:
        canvas.create_oval(100-r, 100-r, 100+r, 100+r, fill=alpha, outline="")

    # ── Right login form ──────────────────────────────────────────────────────
    right = Frame(root, width=820, height=860, bg=BG_DARK)
    right.place(x=780, y=0)

    form = Frame(right, width=440, height=520, bg=BG_CARD,
                 highlightthickness=1, highlightbackground=BORDER)
    form.place(x=190, y=170)
    form.pack_propagate(False)

    Label(form, text="Welcome Back", font=("Segoe UI", 24, "bold"),
          fg=TEXT_PRI, bg=BG_CARD).place(x=40, y=36)
    Label(form, text="Sign in to your account", font=FONT_BODY,
          fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=72)
    divider(form, length=360).place(x=40, y=100)

    Label(form, text="USERNAME", font=("Segoe UI", 9, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=120)
    user_e = styled_entry(form, width=30)
    user_e.place(x=40, y=142)

    Label(form, text="PASSWORD", font=("Segoe UI", 9, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=192)
    pswd_e = styled_entry(form, width=30, show="*")
    pswd_e.place(x=40, y=214)

    user_e.focus_set()
    user_e.bind("<Return>", lambda e: pswd_e.focus_set())

    msg_lbl = Label(form, text="", font=("Segoe UI", 9),
                    fg=DANGER, bg=BG_CARD)
    msg_lbl.place(x=40, y=258)

    def login(e=None):
        username = user_e.get().strip()
        password = pswd_e.get().strip()
        if not username or not password:
            msg_lbl.config(text="⚠  Please enter username and password.")
            return
        with sqlite3.connect("user_database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (username, password))
            if cur.fetchone():
                afterlogin_gui()
            else:
                user_e.delete(0, END)
                pswd_e.delete(0, END)
                msg_lbl.config(text="⚠  Invalid credentials. Please register first.")

    def register_user():
        username = user_e.get().strip()
        password = pswd_e.get().strip()
        if not username or not password:
            msg_lbl.config(text="⚠  Username and password required.")
            return
        with sqlite3.connect("user_database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            if cur.fetchone():
                msg_lbl.config(text="⚠  Username already exists.")
            else:
                cur.execute("INSERT INTO users (username, password) VALUES (?,?)",
                            (username, password))
                conn.commit()
                msg_lbl.config(text="✔  Registered successfully! You can sign in.",
                               fg=SUCCESS)

    pswd_e.bind("<Return>", login)

    btn_login = styled_button(form, "Sign In", login, color=ACCENT,
                              text_color=BG_DARK, width=28)
    btn_login.place(x=40, y=285)

    btn_reg = styled_button(form, "Create Account", register_user,
                            color=BG_PANEL, text_color=ACCENT, width=28)
    btn_reg.place(x=40, y=336)

    # Admin link
    Label(right, text="Admin?", font=FONT_SMALL, fg=TEXT_SEC, bg=BG_DARK).place(x=580, y=716)
    admin_btn = Label(right, text="Admin Login →", font=("Segoe UI", 9, "bold"),
                      fg=ACCENT, bg=BG_DARK, cursor="hand2")
    admin_btn.place(x=628, y=716)
    admin_btn.bind("<Button-1>", lambda e: admin_login())

    # Footer
    Label(right, text="VPMS v2.0  ·  © 2024", font=FONT_SMALL,
          fg=TEXT_SEC, bg=BG_DARK).place(x=320, y=820)


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def admin_login():
    root = Frame(win, width=1600, height=860, bg=BG_DARK)
    root.place(x=0, y=0)

    left = Frame(root, width=780, height=860, bg=BG_PANEL)
    left.place(x=0, y=0)
    Frame(left, width=6, height=860, bg=ACCENT2).place(x=774, y=0)

    Label(left, text="ADMIN", font=("Segoe UI", 80, "bold"),
          fg=ACCENT2, bg=BG_PANEL).place(x=80, y=160)
    Label(left, text="Control Panel\nAccess", font=("Segoe UI", 22),
          fg=TEXT_PRI, bg=BG_PANEL, justify=LEFT).place(x=82, y=310)
    Label(left, text="Authorised personnel only.", font=("Segoe UI", 13),
          fg=TEXT_SEC, bg=BG_PANEL).place(x=84, y=390)

    right = Frame(root, width=820, height=860, bg=BG_DARK)
    right.place(x=780, y=0)

    form = Frame(right, width=440, height=420, bg=BG_CARD,
                 highlightthickness=1, highlightbackground=ACCENT2)
    form.place(x=190, y=220)

    Label(form, text="Admin Sign In", font=("Segoe UI", 24, "bold"),
          fg=TEXT_PRI, bg=BG_CARD).place(x=40, y=36)
    divider(form, length=360).place(x=40, y=80)

    Label(form, text="USERNAME", font=("Segoe UI", 9, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=100)
    adm_u = styled_entry(form, width=30)
    adm_u.place(x=40, y=122)

    Label(form, text="PASSWORD", font=("Segoe UI", 9, "bold"),
          fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=172)
    adm_p = styled_entry(form, width=30, show="*")
    adm_p.place(x=40, y=194)

    err_lbl = Label(form, text="", font=("Segoe UI", 9),
                    fg=DANGER, bg=BG_CARD)
    err_lbl.place(x=40, y=238)

    adm_u.focus_set()

    def admin_authenticate(e=None):
        if adm_u.get() == "admin" and adm_p.get() == "admin@1234":
            after_adminlogin()
        else:
            adm_u.delete(0, END); adm_p.delete(0, END)
            err_lbl.config(text="⚠  Wrong username or password.")

    adm_p.bind("<Return>", admin_authenticate)

    styled_button(form, "Access Admin Panel", admin_authenticate,
                  color=ACCENT2, text_color=TEXT_PRI, width=28).place(x=40, y=262)

    back = Label(right, text="← Back to Employee Login", font=("Segoe UI", 9, "bold"),
                 fg=ACCENT, bg=BG_DARK, cursor="hand2")
    back.place(x=280, y=680)
    back.bind("<Button-1>", lambda e: loginpage())


# ══════════════════════════════════════════════════════════════════════════════
#  AFTER ADMIN LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def after_adminlogin():
    root = Frame(win, width=1600, height=860, bg=BG_DARK)
    root.place(x=0, y=0)

    # Top bar
    topbar = Frame(root, width=1600, height=60, bg=BG_CARD)
    topbar.place(x=0, y=0)
    Frame(root, width=1600, height=2, bg=ACCENT2).place(x=0, y=60)
    Label(topbar, text="VPMS", font=("Segoe UI", 18, "bold"),
          fg=ACCENT2, bg=BG_CARD).place(x=24, y=14)
    Label(topbar, text="Admin Control Panel", font=FONT_BODY,
          fg=TEXT_SEC, bg=BG_CARD).place(x=100, y=18)
    styled_button(topbar, "Logout", loginpage, color=DANGER,
                  text_color=TEXT_PRI, width=10).place(x=1470, y=12)

    # Sidebar
    sidebar = Frame(root, width=220, height=800, bg=BG_PANEL)
    sidebar.place(x=0, y=62)

    content = Frame(root, width=1380, height=800, bg=BG_DARK)
    content.place(x=220, y=62)

    def clear_content():
        for w in content.winfo_children():
            w.destroy()

    nav_items = [
        ("👤  Employee List", "employees"),
        ("⚙   Configure Slots", "configure"),
        ("✏   Update Slots", "update"),
    ]
    current_page = {"val": None}

    def nav_button(text, page_id, y):
        def go():
            current_page["val"] = page_id
            for btn_ref in btn_refs:
                btn_ref.config(bg=BG_PANEL, fg=TEXT_PRI)
            btn_refs[nav_items.index((text, page_id))].config(bg=ACCENT2, fg=TEXT_PRI)
            pages[page_id]()
        b = Button(sidebar, text=text, font=("Segoe UI", 11),
                   fg=TEXT_PRI, bg=BG_PANEL, activebackground=ACCENT2,
                   activeforeground=TEXT_PRI, relief=FLAT, anchor=W,
                   width=22, padx=16, pady=12, cursor="hand2", command=go)
        b.place(x=0, y=y)
        return b

    btn_refs = []
    for i, (txt, pid) in enumerate(nav_items):
        btn_refs.append(nav_button(txt, pid, 20 + i * 54))

    # ── Employee list ─────────────────────────────────────────────────────────
    def show_employees():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=20)
        Label(p, text="Employee Accounts", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="All registered employee login credentials",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,14))

        with sqlite3.connect("user_database.db") as conn:
            rows = conn.cursor().execute(
                'SELECT username, password FROM users').fetchall()

        cols = ["#", "Username", "Password"]
        widths = [60, 260, 260]
        tree = styled_tree(p, cols, widths, height=18)
        tree.pack(fill=BOTH, expand=True)
        for i, row in enumerate(rows, 1):
            tag = "odd" if i % 2 else "even"
            tree.insert("", "end", values=(i,) + row, tags=(tag,))

    # ── Configure ─────────────────────────────────────────────────────────────
    def show_configure():
        clear_content()
        p = Frame(content, bg=BG_DARK, padx=30, pady=20)
        p.pack(fill=BOTH, expand=True)
        Label(p, text="Configure Parking Slots", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Initial setup — run once during first install.",
              font=FONT_BODY, fg=WARNING, bg=BG_DARK).pack(anchor=W, pady=(2,20))

        f = card_frame(p, width=500, height=280)
        f.pack(anchor=W)

        Label(f, text="VEHICLE TYPE", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=40)
        cb_style = ttk.Style()
        cb_style.configure("Dark.TCombobox",
                           fieldbackground=BG_PANEL, background=BG_PANEL,
                           foreground=TEXT_PRI, selectbackground=ACCENT2)
        v_type = ttk.Combobox(f, values=["CAR","BUS","TRUCK","BIKE"],
                              width=22, font=FONT_BODY, style="Dark.TCombobox")
        v_type.place(x=40, y=62)

        Label(f, text="TOTAL SLOTS", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=110)
        slots_e = styled_entry(f, width=10)
        slots_e.place(x=40, y=132)

        msg = Label(f, text="", font=("Segoe UI", 9), fg=SUCCESS, bg=BG_CARD)
        msg.place(x=40, y=180)

        def conf_value():
            with sqlite3.connect("vehicle_database.db") as conn:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS entryexit
                    (vehicle_No TEXT UNIQUE, Owner_Name TEXT, Mob_No TEXT,
                     Vehicle_Type TEXT, Date TEXT, Intime TEXT)''')
                c.execute('CREATE TABLE IF NOT EXISTS dashvalue (type TEXT, slots INTEGER)')
                c.execute("INSERT INTO dashvalue (type, slots) VALUES (?,?)",
                          (v_type.get(), slots_e.get()))
                conn.commit()
            msg.config(text="✔  Configured successfully!")
            v_type.delete(0, END); slots_e.delete(0, END)

        styled_button(f, "Save Configuration", conf_value,
                      color=ACCENT, text_color=BG_DARK, width=22).place(x=40, y=218)

    # ── Update ────────────────────────────────────────────────────────────────
    def show_update():
        clear_content()
        p = Frame(content, bg=BG_DARK, padx=30, pady=20)
        p.pack(fill=BOTH, expand=True)
        Label(p, text="Update Parking Slots", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Modify the total number of available slots per vehicle type.",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,20))

        f = card_frame(p, width=500, height=280)
        f.pack(anchor=W)

        Label(f, text="VEHICLE TYPE", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=40)
        v_type = ttk.Combobox(f, values=["CAR","BUS","TRUCK","BIKE"],
                              width=22, font=FONT_BODY)
        v_type.place(x=40, y=62)

        Label(f, text="NEW SLOT COUNT", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=110)
        slots_e = styled_entry(f, width=10)
        slots_e.place(x=40, y=132)

        msg = Label(f, text="", font=("Segoe UI", 9), fg=SUCCESS, bg=BG_CARD)
        msg.place(x=40, y=180)

        def upd_value():
            with sqlite3.connect("vehicle_database.db") as conn:
                conn.cursor().execute(
                    "UPDATE dashvalue SET slots=? WHERE type=?",
                    (slots_e.get(), v_type.get()))
                conn.commit()
            msg.config(text="✔  Updated successfully!")
            v_type.delete(0, END); slots_e.delete(0, END)

        styled_button(f, "Update Slots", upd_value,
                      color=ACCENT2, text_color=TEXT_PRI, width=22).place(x=40, y=218)

    pages = {"employees": show_employees,
             "configure": show_configure,
             "update":    show_update}

    show_employees()
    btn_refs[0].config(bg=ACCENT2)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP SHELL (post-login)
# ══════════════════════════════════════════════════════════════════════════════

def afterlogin_gui():
    root = Frame(win, width=1600, height=860, bg=BG_DARK)
    root.place(x=0, y=0)

    # ── Top bar ───────────────────────────────────────────────────────────────
    topbar = Frame(root, width=1600, height=64, bg=BG_CARD)
    topbar.place(x=0, y=0)
    Frame(root, width=1600, height=2, bg=ACCENT).place(x=0, y=64)

    Label(topbar, text="VPMS", font=("Segoe UI", 20, "bold"),
          fg=ACCENT, bg=BG_CARD).place(x=24, y=14)
    Label(topbar, text="Vehicle Parking Management", font=FONT_BODY,
          fg=TEXT_SEC, bg=BG_CARD).place(x=106, y=20)

    clock_lbl = Label(topbar, text="", font=("Consolas", 20, "bold"),
                      fg=ACCENT, bg=BG_CARD)
    clock_lbl.place(x=1260, y=16)

    date_lbl = Label(topbar, text="", font=("Segoe UI", 9),
                     fg=TEXT_SEC, bg=BG_CARD)
    date_lbl.place(x=1270, y=44)

    def tick():
        clock_lbl.config(text=time.strftime("%H:%M:%S"))
        date_lbl.config(text=datetime.now().strftime("%d %b %Y"))
        clock_lbl.after(1000, tick)

    tick()

    styled_button(topbar, "Log Out", loginpage,
                  color=DANGER, text_color=TEXT_PRI, width=10).place(x=1484, y=14)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    sidebar = Frame(root, width=230, height=796, bg=BG_PANEL)
    sidebar.place(x=0, y=66)
    Frame(root, width=1, height=796, bg=BORDER).place(x=230, y=66)

    # ── Content area ──────────────────────────────────────────────────────────
    content = Frame(root, width=1370, height=796, bg=BG_DARK)
    content.place(x=231, y=66)

    def clear_content():
        for w in content.winfo_children():
            w.destroy()

    # ── Sidebar nav ───────────────────────────────────────────────────────────
    nav_items = [
        ("⬛  Dashboard",       "dashboard"),
        ("＋  Add Entry",       "addentry"),
        ("✕   Delete Entry",    "deleteentry"),
        ("🅿   Parking Slots",   "parking"),
        ("🗄   Database",        "database"),
        ("📤  Export to Excel",  "export"),
    ]

    btn_refs = {}

    def make_nav(text, page_id, y):
        def go():
            for b in btn_refs.values():
                b.config(bg=BG_PANEL, fg=TEXT_PRI)
            btn_refs[page_id].config(bg=BG_CARD, fg=ACCENT)
            pages[page_id]()
        b = Button(sidebar, text=text, font=("Segoe UI", 11),
                   fg=TEXT_PRI, bg=BG_PANEL, activebackground=BG_CARD,
                   activeforeground=ACCENT, relief=FLAT, anchor=W,
                   width=22, padx=16, pady=12, cursor="hand2", command=go)
        b.place(x=0, y=y)
        btn_refs[page_id] = b

    Label(sidebar, text="NAVIGATION", font=("Segoe UI", 8, "bold"),
          fg=TEXT_SEC, bg=BG_PANEL).place(x=16, y=12)

    for i, (txt, pid) in enumerate(nav_items):
        make_nav(txt, pid, 30 + i * 54)

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Dashboard
    # ──────────────────────────────────────────────────────────────────────────
    def show_dashboard():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Dashboard", font=FONT_TITLE, fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Live overview of current parking status",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,24))

        try:
            with sqlite3.connect("vehicle_database.db") as conn:
                c = conn.cursor()
                def count(vtype):
                    c.execute("SELECT COUNT(*) FROM entryexit WHERE Vehicle_Type=?", (vtype,))
                    return c.fetchone()[0]
                counts = {v: count(v) for v in ["CAR","BIKE","BUS","TRUCK"]}
        except Exception:
            counts = {"CAR":0,"BIKE":0,"BUS":0,"TRUCK":0}

        stat_row = Frame(p, bg=BG_DARK)
        stat_row.pack(anchor=W)

        cards = [
            ("🚗  Cars",   counts["CAR"],   ACCENT),
            ("🏍  Bikes",  counts["BIKE"],  SUCCESS),
            ("🚌  Buses",  counts["BUS"],   WARNING),
            ("🚛  Trucks", counts["TRUCK"], ACCENT2),
        ]
        for i, (title, val, col) in enumerate(cards):
            stat_card(stat_row, x=i*260, y=0, title=title, value=val, color=col)

        # recent entries table
        Label(p, text="Recent Entries", font=FONT_HEAD,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W, pady=(30,8))

        try:
            with sqlite3.connect("vehicle_database.db") as conn:
                rows = conn.cursor().execute(
                    'SELECT * FROM entryexit ORDER BY rowid DESC LIMIT 10').fetchall()
        except Exception:
            rows = []

        cols = ["Vehicle No", "Owner", "Mobile", "Type", "Date", "In Time"]
        widths = [140, 220, 140, 90, 120, 110]
        tree = styled_tree(p, cols, widths, height=10)
        tree.pack(fill=X)
        for i, row in enumerate(rows):
            tag = "odd" if i % 2 else "even"
            tree.insert("", "end", values=row, tags=(tag,))

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Add Entry
    # ──────────────────────────────────────────────────────────────────────────
    def show_addentry():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Add Vehicle Entry", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Register a new vehicle entering the parking lot.",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,24))

        form = card_frame(p, width=700, height=420)
        form.pack(anchor=W)
        form.pack_propagate(False)

        fields = {}
        layout = [
            ("VEHICLE NUMBER",  "veh_no",  40,  40),
            ("OWNER NAME",      "ow_name", 40, 140),
            ("MOBILE NUMBER",   "mob_no",  380, 40),
        ]
        for lbl, key, x, y in layout:
            Label(form, text=lbl, font=("Segoe UI", 9, "bold"),
                  fg=TEXT_SEC, bg=BG_CARD).place(x=x, y=y)
            e = styled_entry(form, width=24)
            e.place(x=x, y=y+24)
            fields[key] = e

        Label(form, text="VEHICLE TYPE", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=380, y=140)
        v_type = ttk.Combobox(form, values=["CAR","BUS","TRUCK","BIKE"],
                              width=22, font=FONT_BODY)
        v_type.place(x=380, y=164)

        # auto-time display
        Label(form, text="ENTRY TIME", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=240)
        time_lbl = Label(form, font=("Consolas", 14, "bold"),
                         fg=ACCENT, bg=BG_CARD)
        time_lbl.place(x=40, y=264)

        def update_time():
            time_lbl.config(text=time.strftime("%H:%M:%S  ·  ") +
                            datetime.now().strftime("%d %b %Y"))
            form.after(1000, update_time)
        update_time()

        msg = Label(form, text="", font=("Segoe UI", 9), fg=DANGER, bg=BG_CARD)
        msg.place(x=40, y=350)

        def insert_record():
            vno  = fields["veh_no"].get().strip().upper()
            own  = fields["ow_name"].get().strip()
            mob  = fields["mob_no"].get().strip()
            vtyp = v_type.get()
            if not vno:
                msg.config(text="⚠  Vehicle number is required.", fg=DANGER); return
            intime = time.strftime("%H:%M:%S")
            date   = str(datetime.now().date())
            try:
                with sqlite3.connect("vehicle_database.db") as conn:
                    c = conn.cursor()
                    c.execute('''CREATE TABLE IF NOT EXISTS entryexit
                        (vehicle_No TEXT UNIQUE, Owner_Name TEXT, Mob_No TEXT,
                         Vehicle_Type TEXT, Date TEXT, Intime TEXT)''')
                    c.execute(
                        "INSERT INTO entryexit VALUES (?,?,?,?,?,?)",
                        (vno, own, mob, vtyp, date, intime))
                    conn.commit()
                for key in fields: fields[key].delete(0, END)
                v_type.delete(0, END)
                msg.config(text=f"✔  Entry added for {vno}", fg=SUCCESS)
            except sqlite3.IntegrityError:
                msg.config(text=f"⚠  Vehicle {vno} is already in the parking lot.", fg=DANGER)

        styled_button(form, "Add Entry", insert_record,
                      color=SUCCESS, text_color=BG_DARK, width=20).place(x=40, y=360)

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Delete Entry
    # ──────────────────────────────────────────────────────────────────────────
    def show_deleteentry():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Delete Vehicle Entry", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Record vehicle exit and move to history.",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,24))

        # Search
        search_row = Frame(p, bg=BG_DARK)
        search_row.pack(anchor=W, pady=(0,20))

        Label(search_row, text="VEHICLE NUMBER", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W)
        veh_e = styled_entry(search_row, width=28)
        veh_e.pack(side=LEFT, pady=(4,0))

        info_card = card_frame(p, width=700, height=200)
        info_card.pack(anchor=W, pady=(0,20))

        info_labels = {}
        fields_info = ["Vehicle No","Owner","Mobile","Type","Date","In Time"]
        for i, f in enumerate(fields_info):
            col = i % 3
            row = i // 3
            Label(info_card, text=f.upper(), font=("Segoe UI", 9, "bold"),
                  fg=TEXT_SEC, bg=BG_CARD).place(x=40+col*220, y=20+row*70)
            lbl = Label(info_card, text="—", font=("Segoe UI", 13, "bold"),
                        fg=TEXT_PRI, bg=BG_CARD)
            lbl.place(x=40+col*220, y=40+row*70)
            info_labels[f] = lbl

        msg = Label(p, text="", font=("Segoe UI", 9), fg=DANGER, bg=BG_DARK)
        msg.pack(anchor=W)

        def lookup(e=None):
            vno = veh_e.get().strip().upper()
            if not vno: return
            with sqlite3.connect("vehicle_database.db") as conn:
                row = conn.cursor().execute(
                    "SELECT * FROM entryexit WHERE vehicle_No=?", (vno,)).fetchone()
            if row:
                for key, val in zip(fields_info, row):
                    info_labels[key].config(text=val, fg=TEXT_PRI)
                msg.config(text="")
            else:
                for key in info_labels: info_labels[key].config(text="—")
                msg.config(text=f"⚠  Vehicle '{vno}' not found.", fg=DANGER)

        veh_e.bind("<Return>", lookup)

        btn_row = Frame(p, bg=BG_DARK)
        btn_row.pack(anchor=W, pady=8)

        styled_button(btn_row, "Lookup", lookup,
                      color=ACCENT, text_color=BG_DARK, width=12).pack(side=LEFT, padx=(0,12))

        def delete_record():
            vno = veh_e.get().strip().upper()
            if not vno:
                msg.config(text="⚠  Enter a vehicle number.", fg=DANGER); return
            out_date = str(datetime.now().date())
            out_time = time.strftime("%H:%M:%S")
            with sqlite3.connect("vehicle_database.db") as conn:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS vehicle_history
                    (vehicle_No TEXT UNIQUE, Owner_Name TEXT, Mob_No TEXT,
                     Vehicle_Type TEXT, In_Date TEXT, Intime TEXT,
                     Out_Date TEXT, Outtime TEXT)''')
                row = c.execute("SELECT * FROM entryexit WHERE vehicle_No=?",
                                (vno,)).fetchone()
                if not row:
                    msg.config(text=f"⚠  Vehicle '{vno}' not found.", fg=DANGER); return
                c.execute("INSERT INTO vehicle_history VALUES (?,?,?,?,?,?,?,?)",
                          (*row, out_date, out_time))
                c.execute("DELETE FROM entryexit WHERE vehicle_No=?", (vno,))
                conn.commit()
            veh_e.delete(0, END)
            for key in info_labels: info_labels[key].config(text="—")
            msg.config(text=f"✔  Exit recorded for {vno}  [{out_time}]", fg=SUCCESS)

        styled_button(btn_row, "Record Exit", delete_record,
                      color=DANGER, text_color=TEXT_PRI, width=14).pack(side=LEFT)

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Parking Slots
    # ──────────────────────────────────────────────────────────────────────────
    def show_parking():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Parking Slot Status", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Real-time availability per vehicle type.",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,24))

        grid = Frame(p, bg=BG_DARK)
        grid.pack(anchor=W)

        try:
            with sqlite3.connect("vehicle_database.db") as conn:
                c = conn.cursor()
                slot_data = []
                for vtype, color in [("CAR",ACCENT),("BIKE",SUCCESS),("BUS",WARNING),("TRUCK",ACCENT2)]:
                    c.execute("SELECT COUNT(*) FROM entryexit WHERE Vehicle_Type=?", (vtype,))
                    cur = c.fetchone()[0]
                    c.execute("SELECT slots FROM dashvalue WHERE type=?", (vtype,))
                    row = c.fetchone()
                    total = row[0] if row else 0
                    slot_data.append((vtype, cur, total, color))
        except Exception:
            slot_data = [("CAR",0,0,ACCENT),("BIKE",0,0,SUCCESS),
                         ("BUS",0,0,WARNING),("TRUCK",0,0,ACCENT2)]

        for i, (vtype, cur, total, col) in enumerate(slot_data):
            remaining = max(0, total - cur)
            pct = (cur / total * 100) if total > 0 else 0
            status_color = DANGER if pct >= 90 else WARNING if pct >= 60 else SUCCESS

            card = card_frame(grid, width=310, height=200)
            card.grid(row=0, column=i, padx=(0,20))

            Frame(card, bg=col, width=310, height=4).place(x=0, y=0)

            Label(card, text=vtype, font=("Segoe UI", 13, "bold"),
                  fg=col, bg=BG_CARD).place(x=20, y=20)

            Label(card, text=str(remaining), font=("Segoe UI", 52, "bold"),
                  fg=col, bg=BG_CARD).place(x=20, y=46)
            Label(card, text="slots free", font=FONT_SMALL,
                  fg=TEXT_SEC, bg=BG_CARD).place(x=26, y=108)

            # mini progress bar
            bar_bg = Frame(card, width=270, height=6, bg=BORDER)
            bar_bg.place(x=20, y=130)
            bar_fill = Frame(card, width=max(4, int(270 * pct/100)),
                             height=6, bg=status_color)
            bar_fill.place(x=20, y=130)

            Label(card, text=f"{cur}/{total} occupied",
                  font=("Segoe UI", 9), fg=TEXT_SEC, bg=BG_CARD).place(x=20, y=148)

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Database
    # ──────────────────────────────────────────────────────────────────────────
    def show_database():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Database", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)

        tab_row = Frame(p, bg=BG_DARK)
        tab_row.pack(anchor=W, pady=(8,16))

        current_tab = {"val": "current"}

        def make_tab(text, key, x):
            def go():
                current_tab["val"] = key
                for t_key, t_btn in tab_btns.items():
                    if t_key == key:
                        t_btn.config(bg=ACCENT, fg=BG_DARK)
                    else:
                        t_btn.config(bg=BG_PANEL, fg=TEXT_PRI)
                load_tab(key)
            b = Button(tab_row, text=text, font=("Segoe UI", 10, "bold"),
                       bg=BG_PANEL, fg=TEXT_PRI, relief=FLAT, padx=20, pady=8,
                       cursor="hand2", command=go)
            b.pack(side=LEFT, padx=(0,8))
            return b

        tab_btns = {}
        tab_btns["current"] = make_tab("Current Vehicles", "current", 0)
        tab_btns["history"] = make_tab("Vehicle History",  "history", 0)
        tab_btns["current"].config(bg=ACCENT, fg=BG_DARK)

        tree_frame = Frame(p, bg=BG_DARK)
        tree_frame.pack(fill=BOTH, expand=True)

        def load_tab(key):
            for w in tree_frame.winfo_children():
                w.destroy()
            try:
                with sqlite3.connect("vehicle_database.db") as conn:
                    if key == "current":
                        rows = conn.cursor().execute("SELECT * FROM entryexit").fetchall()
                        cols   = ["#","Vehicle No","Owner","Mobile","Type","Date","In Time"]
                        widths = [50,130,200,130,80,110,100]
                    else:
                        rows = conn.cursor().execute("SELECT * FROM vehicle_history").fetchall()
                        cols   = ["#","Vehicle No","Owner","Mobile","Type","In Date","In Time","Out Date","Out Time"]
                        widths = [50,120,180,120,70,100,90,100,90]
            except Exception:
                rows = []
                cols, widths = ["No data"], [200]

            tree = styled_tree(tree_frame, cols, widths, height=18)
            tree.pack(fill=BOTH, expand=True)
            for i, row in enumerate(rows, 1):
                tag = "odd" if i % 2 else "even"
                tree.insert("", "end", values=(i,)+row, tags=(tag,))

        load_tab("current")

    # ──────────────────────────────────────────────────────────────────────────
    #  PAGE: Export
    # ──────────────────────────────────────────────────────────────────────────
    def show_export():
        clear_content()
        p = Frame(content, bg=BG_DARK)
        p.pack(fill=BOTH, expand=True, padx=30, pady=24)

        Label(p, text="Export to Excel", font=FONT_TITLE,
              fg=TEXT_PRI, bg=BG_DARK).pack(anchor=W)
        Label(p, text="Download vehicle data as an Excel spreadsheet.",
              font=FONT_BODY, fg=TEXT_SEC, bg=BG_DARK).pack(anchor=W, pady=(2,24))

        form = card_frame(p, width=560, height=300)
        form.pack(anchor=W)

        Label(form, text="FILE NAME", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=40)
        fname_e = styled_entry(form, width=30)
        fname_e.place(x=40, y=64)

        Label(form, text="DATA SOURCE", font=("Segoe UI", 9, "bold"),
              fg=TEXT_SEC, bg=BG_CARD).place(x=40, y=114)
        dtype = ttk.Combobox(form, values=["CURRENT VEHICLES","VEHICLE'S HISTORY"],
                             width=26, font=FONT_BODY)
        dtype.current(0)
        dtype.place(x=40, y=138)

        msg = Label(form, text="", font=("Segoe UI", 9), fg=SUCCESS, bg=BG_CARD)
        msg.place(x=40, y=196)

        def convert():
            fname = fname_e.get().strip()
            if not fname:
                msg.config(text="⚠  Please enter a file name.", fg=DANGER); return
            table = "entryexit" if dtype.get() == "CURRENT VEHICLES" else "vehicle_history"
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            path = os.path.join(downloads, fname + ".xlsx")
            with sqlite3.connect("vehicle_database.db") as conn:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            df.to_excel(path, index=False)
            msg.config(text=f"✔  Saved to Downloads → {fname}.xlsx", fg=SUCCESS)
            fname_e.delete(0, END)

        styled_button(form, "Export Now", convert,
                      color=SUCCESS, text_color=BG_DARK, width=20).place(x=40, y=230)

    pages = {
        "dashboard":   show_dashboard,
        "addentry":    show_addentry,
        "deleteentry": show_deleteentry,
        "parking":     show_parking,
        "database":    show_database,
        "export":      show_export,
    }

    show_dashboard()
    btn_refs["dashboard"].config(bg=BG_CARD, fg=ACCENT)


# ── Entry point ───────────────────────────────────────────────────────────────

create_database()
loginpage()
win.mainloop()