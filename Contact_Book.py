from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox
from sqlalchemy import *
from sqlalchemy.sql import *
import os
import sys

def on_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox('all'))


window =Tk()
engine = create_engine('sqlite:///database.db', echo=True)
metadata = MetaData()
contacts = Table('contacts', metadata,Column('id', Integer, primary_key=True),Column('name', String), Column('email', String),Column('phone', String))
conn = engine.connect()

main_canvas = Canvas(window)
main_canvas.place(relx=.5, rely=.5, anchor=CENTER,width=350,height=500)

scrollbar = Scrollbar(window, command=main_canvas.yview)
scrollbar.place(relx=1,rely=0.5,anchor=E,height=500)
#457

main_canvas.configure(yscrollcommand = scrollbar.set)
main_canvas.bind('<Configure>', on_configure)

main_frame = Frame(main_canvas)
main_frame_id = main_canvas.create_window((0,0), window=main_frame, anchor=NW)


contact_image = PhotoImage(file="contact.png")
back_image = PhotoImage(file='back.png')
name_image = PhotoImage(file="name.png")
phone_image = PhotoImage(file="phone-no.png")
email_image = PhotoImage(file="email.png")
add_image = PhotoImage(file="add.png")

select_contacts = select([contacts])
all_contacts_data = conn.execute(select_contacts)
all_contacts = []
email_data = []
phone_data = []
all_ids = []
for contact in all_contacts_data:
    all_contacts.append(contact[contacts.c.name])
    email_data.append(contact[contacts.c.email])
    phone_data.append(contact[contacts.c.phone])
    all_ids.append(contact[contacts.c.id])
#all_contacts = ['Divyansh','Nishay Malhan','Mithlesh Patankar','Chapati','Loggy','Hitesh Khangta','YesSmartypie','Mumbo Jumbo']

#email_data = ['divyansh@contact.com','nishay@collabx.in','Mythpat@youtube.com','Chapati@Youtube.com','Loggy@youtube.com','Smartypie@youtube.com','YesSmartypie@youtube.com','MumboJumbo@minecraft.net']

all_buttons = []

all_frames = {}


def add_contact():
    name = simpledialog.askstring("Enter Contact Name","Name: ")
    if name == None:
        messagebox.showerror(title="Error",message="Please Enter a Contact Name")
    else:
        email = simpledialog.askstring("Enter Email", "Email: ")
        if email == None:
            email = ''
        phone = simpledialog.askstring("Enter Phone","Phone: ")
        if phone == None:
            phone = ''
        global all_buttons,all_contacts,email_data,all_frames
        data_insert = contacts.insert().values(name=name, email=email,phone=phone)
        conn.execute(data_insert)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

menu_bar = Menu(window)
file_menu = Menu(menu_bar)
file_menu.add_command(label="Add",command=add_contact,accelerator="Command-A")
menu_bar.add_cascade(label="File", menu=file_menu)
window.config(menu=menu_bar)

def show_contact(event):
    name = all_contacts[all_buttons.index(event.widget)]
    email = email_data[all_buttons.index(event.widget)]
    phone = phone_data[all_buttons.index(event.widget)]
    all_frames["DetailsPage"].set_Values(name=name,email=email,phone=phone,contact_id=all_ids[all_buttons.index(event.widget)])
    all_frames["DetailsPage"].tkraise()
    main_canvas.yview_moveto('0')
    scrollbar.place_forget()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        for i in range(len(all_contacts)*2):
            if i%2 == 0:
                a = Label(self,text="  "+all_contacts[int(i/2)])
                a.configure(image=contact_image,compound=LEFT,width=350)
                a.grid(column=0,row=i,ipady=20)
                a.bind('<Button-1>',show_contact)
                all_buttons.append(a)
            else:
                Separator(self,orient=HORIZONTAL).grid(row=i, column=0,sticky=EW)

class DetailsPage(Frame):
    name = ''
    email = ''
    phone = ''
    contact_id = 0
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        back_label = Label(self,image=back_image,text="Back",compound=LEFT)
        back_label.grid(row=0, column=0, sticky="NW")
        back_label.bind('<Button-1>',self.go_back)
        self.name_label = Label(self,image=name_image,compound=LEFT,text="Name: "+self.name)
        self.name_label.grid(row=1,column=0,sticky="NW")
        self.phone_label = Label(self,image=phone_image,compound=LEFT,text="Phone: "+self.phone)
        self.phone_label.grid(row=2,column=0,sticky="NW")
        self.email_label = Label(self,image=email_image,compound=LEFT,text="Email: "+self.email)
        self.email_label.grid(row=3,column=0,sticky="NW")
        self.delete_button = Button(self,text="Delete Contact",command=self.delete)
        self.delete_button.grid(row=4,column=0,sticky="NW")


    def set_Values(self,name,phone,email,contact_id):
        self.name = name
        self.phone = phone
        self.email = email
        self.contact_id = contact_id
        self.name_label.configure(text="Name: "+self.name)
        self.phone_label.configure(text="Phone: "+self.phone)
        self.email_label.configure(text="Email: "+self.email)


    def go_back(self,event):
        all_frames["StartPage"].tkraise()
        scrollbar.place(relx=1,rely=0.5,anchor=E,height=500)
        main_canvas.configure(height=500)
    
    def delete(self):
        conn.execute(contacts.delete().where(contacts.c.id == self.contact_id))
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

all_frames["StartPage"] = StartPage(parent=main_frame,controller=window)
all_frames["StartPage"].grid(row=0,column=0,sticky="nsew")
all_frames["DetailsPage"] = DetailsPage(parent=main_frame,controller=window)
all_frames["DetailsPage"].grid(row=0,column=0,sticky="nsew")
all_frames["StartPage"].tkraise()


window.bind('<Down>',lambda down: main_canvas.yview_moveto('1'))
window.bind('<Up>',lambda up: main_canvas.yview_moveto('0'))
window.bind('<Command-a>',lambda add: add_contact())
window.bind('<Control-a>',lambda add: add_contact)
window.geometry('350x500+500+200')
window.resizable(False,False)
window.title('Contact Book')
window.mainloop()
