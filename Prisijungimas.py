import Registracija
import Darbuotojai
from tkinter import *
import sqlite3


conn = sqlite3.connect('registracijos_duomenys.db')
c = conn.cursor()

with conn:
    c.execute('SELECT VARTOTOJAS, Slaptažodis FROM Registracijos_duomenys')
    a = c.fetchall()

window1 = Tk()
window1.title('Prisijungimas')
window1.minsize(240, 190)
window1.maxsize(240, 190)
window1.geometry('250x200')

def registracijos_atidarymas():
    window = Tk()
    Registracija.Register(window)
    window.title('Registracija')
    window.minsize(380, 400)
    window.maxsize(380, 400)
    window.mainloop()

def matching_database():
    username = field_username.get()
    password = field_password.get()
    for x in a:
        if x[0] == username and x[1] == password:
            window1.destroy()
            window = Tk()
            window.title('Darbuotojai')
            window.minsize(760, 450)
            window.maxsize(760, 450)
            Darbuotojai.All_data(window)
            window.mainloop()
            break
    else:
        info['text'] = 'Nepavyko prisijungti'

username = Label(window1, text='Vartotojas').grid(row=0, column=0, padx=5, pady=5, sticky=E)
password = Label(window1, text='Slaptažodis').grid(row=1, column=0, padx=5, pady=5, sticky=E)

button_connect = Button(window1, text='Prisijungti', command=matching_database).grid(row=3, column=1, padx=5, pady=5)
button_registration = Button(window1, text='Registruotis', command=registracijos_atidarymas).grid(row=4, column=1, padx=5, pady=5)

info = Label(window1, text='')
info.grid(row=2, column=1, padx=5, pady=5)

field_username = Entry(window1)
field_username.grid(row=0, column=1, padx=5, pady=5)

field_password = Entry(window1, show='*')
field_password.grid(row=1, column=1, padx=5, pady=5)

window1.mainloop()
