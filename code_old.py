from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import time
from datetime import datetime
from tkvideo import tkvideo
import pandas as pd 

win=Tk()
win.geometry("1550x800")
win.title("VPMS")


def loginpage():
    Frame_login=Frame(win,width=1550,height=800,bg="#C6FFFF")
    Frame_login.place(x=0,y=0)
    global us
    global bg1
    us=PhotoImage(file="login.png")
    lb=Label(Frame_login,image=us,bg="#C6FFFF").place(x=150,y=200)
    bg1=PhotoImage(file="admin_logo.png")
    lb=Label(win,image=bg1,bg="#C6FFFF").place(x=1300,y=600)
    global Frame1 
    Frame1=Frame(Frame_login,width=500,height=500,bg="#C6FFFF")
    Frame1.place(x=900,y=100)
    lb=Label(Frame1,text="Employee Login",font=("cambria",30),fg="blue",bg="#C6FFFF").place(x=80,y=50)
    lb=Label(Frame1,text="Username:",font=("cambria",18,'bold'),bg="#C6FFFF").place(x=60,y=150)
    lb=Label(Frame1,text="Password:",font=("cambria",18,'bold'),bg="#C6FFFF").place(x=60,y=250)
    global User
    global pswd
    
    user=Entry(Frame1,width=20,border=0,font=("cambria",18,'bold'),bg="#C6FFFF")
    user.place(x=185,y=150)
    pswd=Entry(Frame1,width=20,border=0,font=("cambria",18,'bold'),bg="#C6FFFF")
    pswd.place(x=185,y=250)
    user.focus_set()
    
    def enter_(e):
        pswd.focus_set()

    user.bind('<Return>',enter_)

    
    Frame(Frame1,width=400,height=2,bg='black').place(x=60,y=200)
    Frame(Frame1,width=400,height=2,bg='black').place(x=60,y=300)

    # Function to create the database and required tables
    
    def create_database():
        conn = sqlite3.connect("user_database.db")
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT)''')
        conn.commit()
        conn.close()

    # Function to create a new user in the database
    def register_user():
        username = user.get()
        password = pswd.get()
        # Check if the username or password is empty
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        else:
            # Connect to the SQLite database
            conn = sqlite3.connect("user_database.db")
            cursor = conn.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                messagebox.showerror("Error", "Username already exists. Choose a different one.")
            else:
                # Insert the new user into the database
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
                conn.close()

        
     # Function to handle login  
    def login(e):
        username = user.get()
        password = pswd.get()

        # Connect to the SQLite database
        conn = sqlite3.connect("user_database.db")
        cursor = conn.cursor()

        # Check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        authenticated_user = cursor.fetchone()

        if authenticated_user:
            messagebox.showinfo("Success", "Login successful!")
            afterlogin_gui()

        else:
            user.delete(0,END)
            pswd.delete(0,END)
            if username =="" and password =="":
                messagebox.showerror("Error","Please Enter Username & Password")
            else:
                messagebox.showerror("Error", "Please Register First")

        # Close the database connection
        conn.close()

    # Create the database and required tables
    create_database()
    pswd.bind('<Return>', login)

    b1=Button(Frame1,width=40,text="Sign in",command=login,fg="#C6FFFF",bg="blue",font=("cambria",15,'bold'),border=5)
    b1.place(x=20,y=350)
    b2=Button(win,width=10,text="admin login ",command=admin_login,fg="Black",bg="#C6FFFF",font=("cambria",15,'bold'),border=0)
    b2.place(x=1150,y=630)
    b3=Button(Frame1,width=30,text="Don't have account ? Register ",command=register_user,fg="red",bg="#C6FFFF",font=("cambria",15,'bold'),border=0)
    b3.place(x=150,y=420)

####----------------------------------------------------admin login -------------------------------------------###

def admin_login():
    Frame_admin=Frame(win,width=1550,height=780,bg="lightgreen")
    Frame_admin.place(x=0,y=0)
    global addm
    addm=PhotoImage(file="login.png")
    lb=Label(Frame_admin,image=addm,bg="lightgreen").place(x=150,y=200)
    Frame1=Frame(Frame_admin,width=500,height=500,bg="lightgreen")
    Frame1.place(x=900,y=100)
    lb=Label(Frame1,text="Admin Login",font=("cambria",30),fg="red",bg="lightgreen").place(x=80,y=50)
    lb=Label(Frame1,text="Username:",font=("cambria",18,'bold'),bg="lightgreen").place(x=60,y=150)
    lb=Label(Frame1,text="Password:",font=("cambria",18,'bold'),bg="lightgreen").place(x=60,y=250)
    user=Entry(Frame1,width=20,border=0,font=("cambria",18,'bold'))
    user.place(x=185,y=150)
    pswd=Entry(Frame1,width=20,border=0,font=("cambria",18,'bold'))
    pswd.place(x=185,y=250)
    user.focus_set()
    Frame(Frame1,width=400,height=2,bg='black').place(x=60,y=1300)
    Frame(Frame1,width=400,height=2,bg='black').place(x=60,y=300)

    def admin_authenticate():
        if user.get()=="admin" and pswd.get()=="admin@1234":
            messagebox.showinfo("Success","Admin login succesful...")
            after_adminlogin()
        else:
            user.delete(0,END)
            pswd.delete(0,END)
            messagebox.showerror("Error","Wrong Username or Password")

    
    
    b1=Button(Frame1,width=40,text="Sign in",command=admin_authenticate,fg="lightgreen",bg="red",font=("cambria",15,'bold'),border=5)
    b1.place(x=20,y=350)


def after_adminlogin():
    Frame_admin=Frame(win,width=1550,height=800,bg="lightblue")
    Frame_admin.place(x=0,y=0)
    global admin
    admin=PhotoImage(file="admin_logo1.png")
    lb=Label(Frame_admin,image=admin,bg="lightblue").place(x=110,y=100)
    lb=Label(Frame_admin,text="Welcome Admin..",font=("cambria",40),fg="black",bg="lightblue").place(x=110,y=500)

    def show_user():
        Frame_admin1=Frame(Frame_admin,width=900,height=550,bg="coral")
        Frame_admin1.place(x=600,y=200)
        conn=sqlite3.connect("user_database.db")
        cursor=conn.cursor()
        cursor.execute('SELECT username,password FROM users')
        rows = cursor.fetchall()
        conn.close()

        tree = ttk.Treeview(Frame_admin1,height=10)
        tree.place(x=20,y=40)
        tree['show']='headings'
        tree['columns'] = ('Sr.','Username','Password')

        s=ttk.Style()
        
        s.theme_use("clam")
        s.configure(".",font=("Cambria 14 bold"))
        s.configure("Treeview.Heading",font=("cambria 17 bold"))

        for column in tree['columns']:
            tree.heading(column, text=column)
        
        tree.column("Sr.",width=50)
        tree.column("Username",width=120)
        tree.column("Password",width=140)
        c=1
        for row in rows:
            row=(c,)+(row)
            c=c+1
            tree.insert('', 'end', values=row)

    def configure_values():
        Frame_admin2=Frame(Frame_admin,width=900,height=550,bg="silver")
        Frame_admin2.place(x=600,y=200)
        text="Note: This step should be done only once while\n first time installing Software"
        Label(Frame_admin2,text=text,font=("cambria",20,'bold'),bg="silver",fg="red").place(x=150,y=430)
        Label(Frame_admin2,text="Vehicle Type :",font=("cambria",20,'bold'),bg="silver",fg="black").place(x=150,y=200)
        entry1=ttk.Combobox(Frame_admin2,values=["CAR","BUS","TRUCK","BIKE"],width=20,font=("cambria",15,'bold'))
        entry1.place(x=150,y=250)
        Label(Frame_admin2,text="Slots :",font=("cambria",20,'bold'),bg="silver",fg="black").place(x=500,y=200)
        entry2=Entry(Frame_admin2,width=5,border=2,font=("cambria",15,'bold'))
        entry2.place(x=500,y=250)
        conn = sqlite3.connect("vehicle_database.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entryexit (
        vehicle_No TEXT UNIQUE,
        Owner_Name TEXT,
        Mob_No TEXT,Vehicle_Type TEXT,Date TEXT,Intime TEXT)''')
        conn.commit()
        conn.close()


        def conf_value():
            Type=entry1.get()
            slot_nos=entry2.get()
            conn=sqlite3.connect("vehicle_database.db")
            cursor=conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dashvalue (type TEXT,slots INTEGER)''')
            conn.commit()
            cursor.execute("INSERT INTO dashvalue(type,slots) VALUES ( ?, ?)",(Type,slot_nos))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Configuration Succesful..")
            entry1.delete(0,END)
            entry2.delete(0,END)

        Button(Frame_admin2,width=16,text="SUBMIT",command=conf_value,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=350,y=350)

    def update_values():
        Frame_admin3=Frame(Frame_admin,width=900,height=550,bg="lightcoral")
        Frame_admin3.place(x=600,y=200)
        Label(Frame_admin3,text="Vehicle Type :",font=("cambria",20,'bold'),bg="lightcoral",fg="black").place(x=150,y=200)
        entry4=ttk.Combobox(Frame_admin3,values=["CAR","BUS","TRUCK","BIKE"],width=20,font=("cambria",15,'bold'))
        entry4.place(x=150,y=250)
        Label(Frame_admin3,text="Slots :",font=("cambria",20,'bold'),bg="lightcoral",fg="black").place(x=500,y=200)
        entry5=Entry(Frame_admin3,width=5,border=2,font=("cambria",15,'bold'))
        entry5.place(x=500,y=250)


        def upd_value():
            Type=entry4.get()
            slot_nos=entry5.get()
            conn=sqlite3.connect("vehicle_database.db")
            cursor=conn.cursor()
            cursor.execute("UPDATE dashvalue SET slots=? WHERE type=?",(slot_nos,Type))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Update Succesful..")
            entry4.delete(0,END)
            entry5.delete(0,END)
        Button(Frame_admin3,width=16,text="SUBMIT",command=upd_value,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=350,y=350)

        
    Button(Frame_admin,width=16,text="EMPLOYEE DETAILS",command=show_user,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=610,y=130)
    Button(Frame_admin,width=16,text="CONFIGURE",command=configure_values,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=830,y=130)
    Button(Frame_admin,width=16,text="UPDATE",command=update_values,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=1060,y=130)
    Button(Frame_admin,width=16,text="LOGOUT",command=loginpage,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=1290,y=130)    

    

#####----------------------------------------------admin login end -----------------------------------#

def dashboard():

    global car
    global bus
    global truck
    global bike
    Frame2=Frame(win,width=1275,height=645,bg="springgreen")
    Frame2.place(x=270,y=150)
    Label(Frame2,text="DASHBOARD :",font=("cambria",40,'bold'),bg="springgreen").place(x=50,y=20)
     
    car=PhotoImage(file="car_logo.png",width=250,height=250)
    lb=Label(Frame2,image=car,bg="springgreen").place(x=100,y=130)
    Label(Frame2,text="CARS",font=("cambria",18,'bold'),bg="springgreen").place(x=200,y=380)
    

    bike=PhotoImage(file="bike_logo.png",width=250,height=250)
    lb=Label(Frame2,image=bike,bg="springgreen").place(x=400,y=130)
    Label(Frame2,text="BIKES",font=("cambria",18,'bold'),bg="springgreen").place(x=500,y=380)
    


    bus=PhotoImage(file="bus_logo.png",width=250,height=250)
    lb=Label(Frame2,image=bus,bg="springgreen").place(x=700,y=130)
    Label(Frame2,text="BUSES",font=("cambria",18,'bold'),bg="springgreen").place(x=800,y=380)
    

    truck=PhotoImage(file="truck_logo.png",width=250,height=250)
    lb=Label(Frame2,image=truck,bg="springgreen").place(x=1000,y=130)
    Label(Frame2,text="TRUCKS",font=("cambria",18,'bold'),bg="springgreen").place(x=1100,y=380)
    

    conn = sqlite3.connect("vehicle_database.db")
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BUS'")
    total_bus=cursor.fetchone()
    Label(Frame2,text=total_bus,font=("cambria",70,'bold'),bg="springgreen",fg="darkblue").place(x=780,y=410)


    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BIKE'")
    total_bike=cursor.fetchone()
    Label(Frame2,text=total_bike,font=("cambria",70,'bold'),bg="springgreen",fg="darkblue").place(x=480,y=410)

    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='CAR'")
    total_car=cursor.fetchone()
    Label(Frame2,text=total_car,font=("cambria",70,'bold'),bg="springgreen",fg="darkblue").place(x=180,y=410)


    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='TRUCK'")
    total_truck=cursor.fetchone()
    Label(Frame2,text=total_truck,font=("cambria",70,'bold'),bg="springgreen",fg="darkblue").place(x=1080,y=410)
    conn.close()


def addentry():

    Frame_addentry=Frame(win,width=1275,height=645,bg="#FFEC87")
    Frame_addentry.place(x=270,y=150)

    lblvdo1=Label(Frame_addentry)
    lblvdo1.place(x=270,y=240)
    player = tkvideo("carvdo1.mp4", lblvdo1,loop=1,size=(700,350))
    player.play()
    
    '''global back
    back=PhotoImage(file="car_entry.png",width=600,height=400)
    lb=Label(Frame_addentry,image=back,bg="#FFEC87").place(x=550,y=140)'''

    Label(Frame_addentry,text="Add new entry :",font=("cambria",40,'bold'),bg="#FFEC87",fg="red").place(x=50,y=20)
    Label(Frame_addentry,text="Vehicle No :",font=("cambria",20,'bold'),bg="#FFEC87",fg="black").place(x=50,y=120)
    vehno=Entry(Frame_addentry,width=20,border=2,font=("cambria",15,'bold'))
    vehno.place(x=230,y=125)
    Label(Frame_addentry,text="Owner Name :",font=("cambria",20,'bold'),bg="#FFEC87",fg="black").place(x=50,y=180)
    owname=Entry(Frame_addentry,width=20,border=2,font=("cambria",15,'bold'))
    owname.place(x=230,y=185)
   
    Label(Frame_addentry,text="Mobile No :",font=("cambria",20,'bold'),bg="#FFEC87",fg="black").place(x=550,y=120)
    mobno=Entry(Frame_addentry,width=20,border=2,font=("cambria",15,'bold'))
    mobno.place(x=730,y=125)
   
    Label(Frame_addentry,text="Vehicle Type :",font=("cambria",20,'bold'),bg="#FFEC87",fg="black").place(x=550,y=180)
    vtype = ttk.Combobox(Frame_addentry,values=["CAR","BUS","TRUCK","BIKE"],width=19,font=("cambria",15,'bold'))
    vtype.place(x=730,y=185)
    

    def insert_record():
        Vehicle_No=vehno.get()
        Owner_Name=owname.get()
        Mobile_No=mobno.get()
        Vehicle_Type=vtype.get()
        Intime=time.strftime("%H:%M:%S")
        Date=datetime.now().date()
        conn = sqlite3.connect("vehicle_database.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entryexit (
        vehicle_No TEXT UNIQUE,
        Owner_Name TEXT,
        Mob_No TEXT,Vehicle_Type TEXT,Date TEXT,Intime TEXT)''')

        
        if not Vehicle_No :
            messagebox.showwarning("error","please enter all details")
        else:
            
            cursor.execute("INSERT INTO entryexit (Vehicle_No,Owner_Name,Mob_No,Vehicle_Type,Date,Intime) VALUES (?, ?, ?, ?, ?, ?)", (Vehicle_No, Owner_Name, Mobile_No, Vehicle_Type, Date, Intime))
            conn.commit()
            conn.close()
            vehno.delete(0,END)
            owname.delete(0,END) 
            mobno.delete(0,END)
            vtype.delete(0,END)


            
            messagebox.showinfo("success","Entry Added Succesfully")
 
    
    Button(Frame_addentry,width=18,text="SUBMIT DETAILS",command=insert_record,bg="#96FF5B",font=("cambria",15,'bold'),border=5).place(x=1000,y=148)
   

def deleteentry():

    Frame_deleteentry=Frame(win,width=1275,height=645,bg="#737A87")
    Frame_deleteentry.place(x=270,y=150)
    Label(Frame_deleteentry,text="Delete entry :",font=("cambria",40,'bold'),bg="#737A87",fg="gold").place(x=50,y=20)
    Label(Frame_deleteentry,text="Enter Vehicle Number :",font=("cambria",20,'bold'),bg="#737A87",fg="cyan").place(x=50,y=150)
    veh_no=Entry(Frame_deleteentry,width=20,border=2,font=("cambria",15,'bold'))
    veh_no.place(x=355,y=153)
    
    lblvdo2=Label(Frame_deleteentry)
    lblvdo2.place(x=200,y=250)
    player = tkvideo("carvdo2.mp4", lblvdo2,loop=1,size=(800,350))
    player.play()
    
    '''global bg
    bg=PhotoImage(file="exit.png")
    lb=Label(Frame_deleteentry,image=bg,bg="#737A87").place(x=220,y=210)'''
    

    def delete_record():

        if not veh_no.get() :
            messagebox.showwarning("error","please enter Vehicle Number !!!")
        else:

            Vehicle_No1=veh_no.get()
            Date=datetime.now().date()
            Out_time=time.strftime("%H:%M:%S")
            conn = sqlite3.connect("vehicle_database.db")
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_history (
            vehicle_No TEXT UNIQUE,
            Owner_Name TEXT,
            Mob_No TEXT,Vehicle_Type TEXT,In_Date TEXT,Intime TEXT,Out_Date TEXT,Outtime TEXT)''')
            cursor.execute("SELECT * FROM entryexit WHERE vehicle_No='{}'".format(Vehicle_No1))
            row_to_copy=cursor.fetchone()
            final_row=(*row_to_copy,Date,Out_time)
            conn.commit()
            conn.close()
            conn = sqlite3.connect("vehicle_database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vehicle_history VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)",final_row)
            cursor.execute("DELETE FROM entryexit WHERE vehicle_No='{}'".format(Vehicle_No1))
            conn.commit()
            conn.close()
            veh_no.delete(0,END)
            messagebox.showinfo("success","Entry Deleted Succesfully")
    Button(Frame_deleteentry,width=20,text="DELETE",command=delete_record,bg="#FF5236",font=("cambria",15,'bold'),border=5).place(x=680,y=145)



def showdatabase():

    def show_current():
            Frame_showdatabase=Frame(win,width=1275,height=645,bg="#FFB49D")
            Frame_showdatabase.place(x=270,y=150)
            Label(Frame_showdatabase,text="Database:",font=("cambria",40,'bold'),bg="#FFB49D",fg="black").place(x=50,y=20)
            Button(Frame_showdatabase,width=15,text="Show History",command=show_history,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=950,y=50)
            conn=sqlite3.connect("vehicle_database.db")
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM entryexit')
            rows = cursor.fetchall()
            conn.close()

            tree = ttk.Treeview(Frame_showdatabase,height=20)
            tree.place(x=20,y=100)
            tree['show']='headings'
            tree['columns'] = ('Sr_No','Vehicle_No', 'Owner_Name', 'Mobile_No', 'Type', 'In-Date', 'In-Time')

            s=ttk.Style()
            
            s.theme_use("clam")
            s.configure(".",font=("Bahnschrift 14 bold"))
            s.configure("Treeview.Heading",font=("Bahnschrift 17 bold"))
            
 
            for column in tree['columns']:
                tree.heading(column, text=column)
            
            tree.column("Sr_No",width=72)
            tree.column("Type",width=100)
            tree.column("In-Date",width=120)
            tree.column("In-Time",width=110)
            tree.column("Mobile_No",width=135)
            tree.column("Owner_Name",width=235)
            tree.column("Vehicle_No",width=150)
            c=1
            for row in rows:
                row=(c,)+(row)
                c=c+1
                tree.insert('', 'end', values=row)
    
    
    
    
    def show_history():
        Frame_showdatabase=Frame(win,width=1275,height=645,bg="#FFB49D")
        Frame_showdatabase.place(x=270,y=150)
        Label(Frame_showdatabase,text="Database:",font=("cambria",40,'bold'),bg="#FFB49D",fg="black").place(x=50,y=20)
        Button(Frame_showdatabase,width=18,text="Show Current Data",command=show_current,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=950,y=50)
        conn=sqlite3.connect("vehicle_database.db")
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM vehicle_history')
        rows = cursor.fetchall()
        conn.close()

        tree = ttk.Treeview(Frame_showdatabase,height=20)
        tree.place(x=20,y=100)
        tree['show']='headings'
        tree['columns'] = ('Sr_No','Vehicle_No', 'Owner_Name', 'Mobile_No', 'Type', 'In-Date', 'In-Time', 'Out-Date','Out-Time')

        s=ttk.Style()
        
        s.theme_use("clam")
        s.configure(".",font=("Bahnschrift 14 bold"))
        s.configure("Treeview.Heading",font=("Bahnschrift 17 bold"))
        

        for column in tree['columns']:
            tree.heading(column, text=column)
        
        tree.column("Sr_No",width=72)
        tree.column("Type",width=100)
        tree.column("In-Date",width=120)
        tree.column("Out-Date",width=120)
        tree.column("In-Time",width=110)
        tree.column("Out-Time",width=110)
        tree.column("Mobile_No",width=140)
        tree.column("Owner_Name",width=220)
        tree.column("Vehicle_No",width=160)
        c=1
        for row in rows:
            row=(c,)+(row)
            c=c+1
            tree.insert('', 'end', values=row)
 
    show_current()


def parking_slot():
    Frame_parking=Frame(win,width=1275,height=645,bg="#A49EFF")
    Frame_parking.place(x=270,y=150)
    Label(Frame_parking,text="Remaining Slots :",font=("cambria",40,'bold'),bg="#A49EFF",fg="yellow").place(x=50,y=20)
   
    global car
    global bus
    global truck
    global bike
    
    car=PhotoImage(file="car_clipart.png")
    lb=Label(Frame_parking,image=car,bg="#A49EFF").place(x=50,y=170)
    Label(Frame_parking,text="CARS",font=("cambria",18,'bold'),bg="#A49EFF").place(x=150,y=370)
    

    bike=PhotoImage(file="bike_clipart.png")
    lb=Label(Frame_parking,image=bike,bg="#A49EFF").place(x=380,y=130)
    Label(Frame_parking,text="BIKES",font=("cambria",18,'bold'),bg="#A49EFF").place(x=480,y=370)
    


    bus=PhotoImage(file="bus_clipart.png")
    lb=Label(Frame_parking,image=bus,bg="#A49EFF").place(x=700,y=130)
    Label(Frame_parking,text="BUSES",font=("cambria",18,'bold'),bg="#A49EFF").place(x=800,y=370)
    


    truck=PhotoImage(file="truck_clipart.png")
    lb=Label(Frame_parking,image=truck,bg="#A49EFF").place(x=1000,y=130)
    Label(Frame_parking,text="TRUCKS",font=("cambria",18,'bold'),bg="#A49EFF").place(x=1070,y=370)
    conn = sqlite3.connect("vehicle_database.db")
    cursor=conn.cursor()


    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='CAR'")
    current_cars=cursor.fetchone()
    cursor.execute("SELECT slots FROM dashvalue WHERE type='CAR'")
    total_cars=cursor.fetchone()
    remain_cars=total_cars[0] - current_cars[0]
    Label(Frame_parking,text=remain_cars,font=("cambria",70,'bold'),bg="#A49EFF",fg="black").place(x=120,y=410)

    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BIKE'")
    current_bikes=cursor.fetchone()
    cursor.execute("SELECT slots FROM dashvalue WHERE type='BIKE'")
    total_bikes=cursor.fetchone()
    remain_bikes=total_bikes[0] - current_bikes[0]
    Label(Frame_parking,text=remain_bikes,font=("cambria",70,'bold'),bg="#A49EFF",fg="black").place(x=460,y=410)

    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='BUS'")
    current_buses=cursor.fetchone()
    cursor.execute("SELECT slots FROM dashvalue WHERE type='BUS'")
    total_buses=cursor.fetchone()
    remain_buses=total_buses[0] - current_buses[0]
    Label(Frame_parking,text=remain_buses,font=("cambria",70,'bold'),bg="#A49EFF",fg="black").place(x=770,y=410)

    cursor.execute("SELECT COUNT(Vehicle_Type) FROM entryexit WHERE Vehicle_Type='TRUCK'")
    current_trucks=cursor.fetchone()
    cursor.execute("SELECT slots FROM dashvalue WHERE type='TRUCK'")
    total_trucks=cursor.fetchone()
    remain_trucks=total_trucks[0] - current_trucks[0]
    Label(Frame_parking,text=remain_trucks,font=("cambria",70,'bold'),bg="#A49EFF",fg="black").place(x=1060,y=410)
    conn.close()



def convertxl():

    Frame_convertxl=Frame(win,width=1275,height=645,bg="mediumspringgreen")
    Frame_convertxl.place(x=270,y=150)
    Label(Frame_convertxl,text="Transfer Details to excel file:",font=("cambria",40,'bold'),bg="mediumspringgreen",fg="red").place(x=50,y=20)
    Label(Frame_convertxl,text="Enter File Name :",font=("cambria",20,'bold'),bg="mediumspringgreen",fg="black").place(x=50,y=150)
    file_name=Entry(Frame_convertxl,width=20,border=2,font=("cambria",15,'bold'))
    file_name.place(x=265,y=153)
    Label(Frame_convertxl,text="Select Details :",font=("cambria",20,'bold'),bg="mediumspringgreen",fg="black").place(x=50,y=200)
    ftype = ttk.Combobox(Frame_convertxl,values=["CURRENT VEHICLES","VEHICLE'S HISTORY"],width=16,font=("cambria",15,'bold'))
    ftype.place(x=265,y=200)
    
    def convert_to_xl():
        if ftype.get()=="CURRENT VEHICLES":
            table_name="entryexit"
        else:
            table_name="vehicle_history"
        if file_name.get=="":
            messagebox.showerror("Error","Please Enter File Name")
        else:
            conn=sqlite3.connect("vehicle_database.db")
            df=pd.read_sql_query("""select * from {}""".format(table_name),conn)
            path="C:Users\Arshad\Downloads\{}.xlsx".format(file_name.get())
            df.to_excel(path,index=False)
            messagebox.showinfo("Success","Your Excel file saved at downloads section..")
            conn.close()
            file_name.delete(0,END)

        
    Button(Frame_convertxl,width=18,text="SUBMIT",command=convert_to_xl,bg="yellow",font=("cambria",15,'bold'),border=5).place(x=550,y=150)



def afterlogin_gui():

    Frame2=Frame(win,width=1275,height=645,bg="springgreen")
    Frame2.place(x=260,y=150)
    Frame_top=Frame(win,width=1550,height=150,bg="Aqua")
    Frame_top.place(x=0,y=0)
    Frame_left=Frame(win,width=270,height=650,bg="#FFA7E8")
    Frame_left.place(x=0,y=149)

    lblvdo=Label(Frame_left)
    lblvdo.place(x=0,y=400)
    player = tkvideo("carvdo.mp4", lblvdo,loop=1,size=(260,250))
    player.play()
    dashboard()
    

    def digital_clock(): 
        label = Label(Frame_top, font=("cambria", 70, 'bold'),bg="Aqua") 
        label.place(x=1100,y=20)
        time_live = time.strftime("%H:%M:%S")
        label.config(text=time_live) 
        label.after(200, digital_clock)

    digital_clock()


    global bg5 
    global bg6
    global bg7
    global bg8
    #bg5=PhotoImage(file="carpark_logo.png",height=250,width=250)
    #lb=Label(Frame_left,image=bg5,bg="#FFB49D").place(x=0,y=370)
    bg6=PhotoImage(file="car1.png",height=150,width=450)
    lb=Label(Frame_top,image=bg6,bg="Aqua").place(x=0,y=0)
    bg7=PhotoImage(file="park_logo.png",height=150,width=150)
    lb=Label(Frame_top,image=bg7,bg="Aqua").place(x=460,y=0)
    bg8=PhotoImage(file="car2.png",height=150,width=450)
    lb=Label(Frame_top,image=bg8,bg="Aqua").place(x=610,y=0)

    Button(Frame_left,width=19,text="DASHBOARD",command=dashboard,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=15)   
    Button(Frame_left,width=19,text="ADD ENTRY",command=addentry,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=70)
    Button(Frame_left,width=19,text="DELETE ENTRY",command=deleteentry,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=125)
    Button(Frame_left,width=19,text="PARKING SLOT",command=parking_slot,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=180)
    Button(Frame_left,width=19,text="SHOW DATABASE",command=showdatabase,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=235)
    Button(Frame_left,width=19,text="CONVERT DATA",command=convertxl,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=290)
    Button(Frame_left,width=19,text="LOG OUT",command=loginpage,bg="yellow",font=("cambria",16,'bold'),border=5).place(x=10,y=345)
    Frame(Frame_top,width=1550,height=3,bg="black").place(x=0,y=146)
    Frame(Frame_left,width=3,height=645,bg="black").place(x=265,y=0)



loginpage()

win.mainloop()


