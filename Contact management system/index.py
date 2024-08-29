from tkinter import *     #Tkinter is a GUI library for python 
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessagebox

root = Tk()
root.title("Contact List")
width = 800
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)                      #x and y calculate the coordinates to position the window in the center of the screen.
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0,0)
root.config(bg="#32012F")

def Database():
    conn = sqlite3.connect("contacts.db")        #if contacts.db doesn't exist then sqlite will create it
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Contact_list(sl_no INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, gender TEXT, age INTEGER, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM Contact_list ORDER BY first_name")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', value=(data))
    cursor.close()
    conn.close()


#variables
FIRST_NAME = StringVar()
LAST_NAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT =StringVar()


def AddNewContact():
    if FIRST_NAME.get() == "" or LAST_NAME.get() == "" or CONTACT.get() == "":
        result = tkMessagebox.showwarning('Incomplete Contact Details', 'Please enter the required details', icon="warning")
    else:
        tree.delete(*tree.get_children())
        first_name = FIRST_NAME.get()
        last_name = LAST_NAME.get()
        gender = GENDER.get()
        age = AGE.get()
        address = ADDRESS.get()
        contact = CONTACT.get()
    
        # Validate the inputs
        if not first_name or not last_name or not gender or not age or not address or not contact:
            tkMessagebox.showwarning("Input Error", "Please complete all required fields.")
            return
    
        try:
            # Convert age to an integer
            age = int(age)
        except ValueError:
            tkMessagebox.showwarning("Input Error", "Please enter a valid age.")
            return
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        # str(FIRST_NAME.get()), str(LAST_NAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(CONTACT.get())
        cursor.execute("INSERT INTO Contact_list (first_name, last_name, gender, age, address, contact) VALUES (?, ?, ?, ?, ?, ?)", (str(first_name), str(last_name), gender, age, str(address), contact))
        conn.commit()
        cursor.execute("SELECT * FROM 'Contact_list';")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', value=(data))
        cursor.close()
        conn.close()
        FIRST_NAME.set("")
        LAST_NAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

        NewWindow.destroy()

def DeleteContact():
    if not tree.selection():
        result = tkMessagebox.showwarning("Not selected", "Please select the contact you want to delete", icon="warning")
    else:
        result = tkMessagebox.showwarning('Confirmation', "Are you sure you want to delete the contact ", icon="warning")
        if result=="ok":
            currItem = tree.focus()
            contents = (tree.item(currItem))
            selectedItem = contents['values']
            tree.delete(currItem)
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Contact_list WHERE sl_no=%d" % selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()

def UpdateContact():
    if FIRST_NAME.get() == "" or LAST_NAME.get() == "" or CONTACT.get() == "":
        result = tkMessagebox.showwarning('Incomplete Contact Details', 'Please enter the required details', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Contact_list SET first_name = ?, last_name= ?, gender=?, age=?, address=?, contact=? WHERE sl_no=? ", (str(FIRST_NAME.get()), str(LAST_NAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(CONTACT.get()), int(sl_no)))
        conn.commit()
        cursor.execute("SELECT * FROM Contact_list ORDER BY first_name")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', value=(data))
        cursor.close()
        conn.close()
        FIRST_NAME.set("")
        LAST_NAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

        updateWindow.destroy()

def NewContactWindow():
    global NewWindow
    FIRST_NAME.set("")
    LAST_NAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Add new contact")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.geometry("%dx%d+%d+%d" % (width,height,x,y))
    NewWindow.resizable(0,0)
    if 'updateWindow' in globals():
        updateWindow.destroy()
    
    WindowTitle = Frame(NewWindow)
    WindowTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=("Calibri", 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=("Calibri", 14)).pack(side=LEFT)

    title_lbl = Label(WindowTitle, text="Add new Contact", font=("Calibri", 16), bg="#32012F", fg="white", width=300)
    title_lbl.pack(fill=X)
    fn_lbl = Label(ContactForm, text="First Name:", font=("Calibri", 14), bd=5)
    fn_lbl.grid(row = 0, sticky=W)
    ln_lbl = Label(ContactForm, text="Last Name:", font=("Calibri", 14), bd=5)
    ln_lbl.grid(row = 1, sticky=W)
    gender_lbl = Label(ContactForm, text="Gender:", font=("Calibri", 14), bd=5)
    gender_lbl.grid(row = 2, sticky=W)
    age_lbl = Label(ContactForm, text="Age:", font=("Calibri", 14), bd=5)
    age_lbl.grid(row = 3, sticky=W)
    address_lbl = Label(ContactForm, text="Address:", font=("Calibri", 14), bd=5)
    address_lbl.grid(row = 4, sticky=W)
    contact_lbl = Label(ContactForm, text="Contact:", font=("Calibri", 14), bd=5)
    contact_lbl.grid(row = 5, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRST_NAME, font=("Calibri",14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LAST_NAME, font=("Calibri", 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=("Calibri", 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS, font=("Calibri", 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=("Calibri", 14))
    contact.grid(row=5, column=1)

    add_btn = Button(ContactForm, text="Save", width = 50 , command=AddNewContact, bg="#524C42", fg="white")
    add_btn.grid(row=7, columnspan=2, pady=10)


def OnSelected(event):
    global sl_no, updateWindow
    currItem = tree.focus()
    contents = (tree.item(currItem))
    selectedItem = contents['values']
    sl_no = selectedItem[0]
    FIRST_NAME.set("")
    LAST_NAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    updateWindow = Toplevel()
    updateWindow.title("Update Contact")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width,height,x,y))
    updateWindow.resizable(0,0)
    if 'NewWindow' in globals():
        NewWindow.destroy()

    WindowTitle = Frame(updateWindow)
    WindowTitle.pack(side=TOP)
    ContactForm = Frame(updateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=("Calibri", 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=("Calibri", 14)).pack(side=LEFT)

    title_lbl = Label(WindowTitle, text="Update selected contact", font=("Calibri", 16), bg="#32012F", fg="white", width=300)
    title_lbl.pack(fill=X)
    fn_lbl = Label(ContactForm, text="First Name:", font=("Calibri", 14), bd=5)
    fn_lbl.grid(row = 0, sticky=W)
    ln_lbl = Label(ContactForm, text="Last Name:", font=("Calibri", 14), bd=5)
    ln_lbl.grid(row = 1, sticky=W)
    gender_lbl = Label(ContactForm, text="Gender:", font=("Calibri", 14), bd=5)
    gender_lbl.grid(row = 2, sticky=W)
    age_lbl = Label(ContactForm, text="Age:", font=("Calibri", 14), bd=5)
    age_lbl.grid(row = 3, sticky=W)
    address_lbl = Label(ContactForm, text="Address:", font=("Calibri", 14), bd=5)
    address_lbl.grid(row = 4, sticky=W)
    contact_lbl = Label(ContactForm, text="Contact:", font=("Calibri", 14), bd=5)
    contact_lbl.grid(row = 5, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRST_NAME, font=("Calibri",14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LAST_NAME, font=("Calibri", 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=("Calibri", 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS, font=("Calibri", 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=("Calibri", 14))
    contact.grid(row=5, column=1)

    update_btn = Button(ContactForm, text="Save", width = 50 , command=UpdateContact, bg="#524C42", fg="white")
    update_btn.grid(row=6, column=0, columnspan=2, pady=10)


Top = Frame(root, width=600, bd=2, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=600, bg="#32012F") 
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side = LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#32012F")
MidLeftPadding.pack(side= LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side = RIGHT, pady = 10)
TableMargin = Frame(root, width=550)
TableMargin.pack(side=TOP)

title_lbl = Label(Top, text= "Contact Management System", font=('Calibri',16), width=500, bg="#32012F", fg ="white")
title_lbl.pack(fill=X)

add_btn = Button(MidLeft, text=" (+) Add new ", bg="#E2DFD0", command=NewContactWindow, padx=10, pady=5)
add_btn.pack()
del_btn = Button(MidRight, text=" (-) Delect Contact", bg="#E72929", command=DeleteContact, padx=10, pady=5)
del_btn.pack(side=RIGHT)

scroll_hori = Scrollbar(TableMargin, orient=HORIZONTAL)
scroll_verti = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("sl_no", "first_name", "last_name", "gender", "age", "address", "contact"), selectmode="extended", height=400, yscrollcommand=scroll_verti.set, xscrollcommand=scroll_hori.set)
#TreeView from ttk is a versatile widget used to display tabular data, 3rd shows multiple select, 4th shows height that is no. of rows
scroll_hori.config(command=tree.xview)
scroll_hori.pack(side=BOTTOM, fill=X)
scroll_verti.config(command=tree.yview)
scroll_verti.pack(side=RIGHT, fill=Y)

style = ttk.Style()
# style.configure("Treeview", 
#                 background="#524C42",  # Background color of the Treeview
#                 foreground="white",      # Text color
#                 fieldbackground="#524C42")  # Background color of the fields
style.map("Treeview", 
          background=[('selected', '#6EACDA')],  # Background color when an item is selected
          foreground=[('selected', 'black')])

tree.heading('sl_no', text="SL.NO.", anchor=W) #w=west/left
tree.heading('first_name', text="First Name", anchor=W)
tree.heading('last_name', text="Last Name", anchor=W)
tree.heading('gender', text="Gender", anchor=W)
tree.heading('age', text="Age", anchor=W)
tree.heading('address', text="Address", anchor=W)
tree.heading('contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-1>', OnSelected)


if __name__ == "__main__":
    Database()
    root.mainloop()