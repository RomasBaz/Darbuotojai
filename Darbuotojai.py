import tkinter
from tkinter import *
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tkinter import ttk
from dateutil.parser import parse
import sqlite3
import string

engine = create_engine('sqlite:///darbuotoju_duomenys.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Database_workers(Base):
    __tablename__ = 'darbuotoju_duomenys'
    id = Column(Integer, primary_key=True)
    name = Column('Vardas', String)
    last_name = Column('Pavardė', String)
    birth_date = Column('Gimimo_data', String)
    gender = Column('Lytis', String)
    address = Column('Adresas', String)
    zip_code = Column('Pašto_kodas', Integer)
    duties = Column('Pareigos', String)
    salary = Column('Atlyginimas', Integer)

    def __init__(self, name, last_name, birth_date, gender, address, zip_code, duties, salary):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.address = address
        self.zip_code = zip_code
        self.duties = duties
        self.salary = salary


    def __repr__(self):
        return f'{self.a} {self.id} {self.name} - {self.last_name} - {self.birth_date} - {self.gender} - {self.address} - {self.zip_code} - {self.duties} - {self.salary}'

# Base.metadata.create_all(engine)

class All_data():
    def __init__(self, window):

        self.window = window
        add_frame = Frame(window, width=200, height=200)
        add_frame.pack(pady=20, side='bottom', anchor='n', expand=1)

        scrollbar = ttk.Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree = ttk.Treeview(self.window, selectmode='browse')
        self.tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.a = LabelFrame(self.window, text='Example').pack(pady=20)
        self.style = ttk.Style(window)
        self.style.map('Treeview', foreground=self.fixed_map("foreground"), background=self.fixed_map("background"))

        self.tree["columns"] = ('ID', 'Name', 'Last Name', 'Birth date', 'Gender', 'Address', 'Zip code', 'Duties', 'Salary')

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column('ID', width=40, minwidth=30, anchor='center')
        self.tree.column("Name", width=80, minwidth=50)
        self.tree.column("Last Name", width=90, minwidth=50)
        self.tree.column("Birth date", width=80, minwidth=50, anchor='center')
        self.tree.column("Gender", width=80, minwidth=50)
        self.tree.column("Address", width=100, minwidth=50)
        self.tree.column("Zip code", width=80, minwidth=50, anchor='center')
        self.tree.column("Duties", width=100, minwidth=50)
        self.tree.column("Salary", width=80, minwidth=50, anchor='center')

        self.tree.heading('#0', text='ID')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Last Name', text='Last name')
        self.tree.heading('Birth date', text='Birth date')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Zip code', text='Zip code')
        self.tree.heading('Duties', text='Duties')
        self.tree.heading('Salary', text='Salary')
        self.tree.pack()

        self.add_record_button = Button(add_frame, text='Pridėti įrašą', command=lambda:[self.add_record()]).grid(row=4, column=0, pady=20)
        self.delete_button = Button(add_frame, text='Ištrinti įrašą', command=lambda:[self.delete_record()]).grid(row=4, column=1, pady=20)
        self.sselect_record = Button(add_frame, text='Pasirinkti įrašą', command=lambda:[self.select_record()]).grid(row=4, column=2, pady=20)
        self.update_record_button = Button(add_frame, text='Pakeisti įrašą', command=lambda:[self.update_record()]).grid(row=4, column=3, pady=20)

        self.error = Label(add_frame, text='')
        self.error.grid(row=5, columnspan=3, sticky=W)
        self.id = Label(add_frame, text='ID')
        self.id.grid(row=0, column=0)
        self.name = Label(add_frame, text='Name')
        self.name.grid(row=0, column=1)
        self.last_name = Label(add_frame, text='Last Name')
        self.last_name.grid(row=0, column=2)
        self.birth_date = Label(add_frame, text='Birth date')
        self.birth_date.grid(row=0, column=3)
        self.gender = Label(add_frame, text='Gender')
        self.gender.grid(row=0, column=4)
        self.address = Label(add_frame, text='Address')
        self.address.grid(row=2, column=0)
        self.zip_code = Label(add_frame, text='Zip code')
        self.zip_code.grid(row=2, column=1)
        self.duties = Label(add_frame, text='Duties')
        self.duties.grid(row=2, column=2)
        self.salary = Label(add_frame, text='Salary')
        self.salary.grid(row=2, column=3)

        self.field_id = Entry(add_frame)
        self.field_id.grid(row=1, column=0, padx=10, pady=5)
        self.field_name = Entry(add_frame)
        self.field_name.grid(row=1, column=1, padx=10, pady=5)
        self.field_last_name = Entry(add_frame)
        self.field_last_name.grid(row=1, column=2, padx=10, pady=5)
        self.field_birth_date = Entry(add_frame)
        self.field_birth_date.grid(row=1, column=3, padx=10, pady=5)
        self.field_gender = Entry(add_frame)
        self.field_gender.grid(row=1, column=4, padx=10, pady=5)
        self.field_address = Entry(add_frame)
        self.field_address.grid(row=3, column=0, padx=10, pady=5)
        self.field_zip_code = Entry(add_frame)
        self.field_zip_code.grid(row=3, column=1, padx=10, pady=5)
        self.field_duties = Entry(add_frame)
        self.field_duties.grid(row=3, column=2, padx=10, pady=5)
        self.field_salary = Entry(add_frame)
        self.field_salary.grid(row=3, column=3, padx=10, pady=5)

        global count
        count = 0

        conn = sqlite3.connect('darbuotoju_duomenys.db')
        c = conn.cursor()

        with conn:
            c.execute('SELECT * FROM darbuotoju_duomenys')
            a = c.fetchall()

        self.tree.tag_configure('nelyginiai', background='white')
        self.tree.tag_configure('lyginiai', background='lightgreen')

        list = [x for x in a]
        for x in list:
            if count % 2 == 0:
                self.tree.insert('', tkinter.END, value=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]), tags='lyginiai')
            else:
                self.tree.insert('', tkinter.END, value=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]), tags='nelyginiai')
            count += 1

    def fixed_map(self, option):
        return [a for a in self.style.map("Treeview", query_opt=option) if a[:2] != ("!disabled", "!selected")]

    def delete_field(self):
        return self.field_id.delete(0, END), self.field_name.delete(0, END), self.field_last_name.delete(0, END), self.field_birth_date.delete(0, END),\
                self.field_gender.delete(0, END), self.field_address.delete(0, END), self.field_zip_code.delete(0, END),self.field_duties.delete(0, END),\
                self.field_salary.delete(0, END)

    def is_date(self, fuzzy=False):
        try:
            self.error['text'] = ''
            parse(self.field_birth_date.get(), fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def add_record(self):
        id = self.field_id.get()
        name = self.field_name.get()
        last_name = self.field_last_name.get()
        birth_date = self.field_birth_date.get()
        gender = self.field_gender.get()
        address = self.field_address.get()
        zip_code = self.field_zip_code.get()
        duties = self.field_duties.get()
        salary = self.field_salary.get()

        if not (name.isalpha() and last_name.isalpha() and duties.isalpha() and\
            salary.isnumeric() and id.isnumeric() and zip_code.isnumeric() and\
                gender.isalpha() and self.is_date() == True):
            self.error['text'] = 'Neteisingu formatu įvedėte laukelius'
        else:
            if (id != '' and name != '' and last_name != '' and
                birth_date != '' and gender != '' and address != '' and
                    zip_code != '' and duties != '' and salary != ''):
                global count
                self.tree.insert(parent='', index='end', value=(id, name, last_name,
                                                                    birth_date, gender, address,
                                                                    zip_code, duties, salary))

                data = Database_workers(name, last_name, birth_date, gender, address, zip_code, duties, salary)
                session.add(data)
                session.commit()

                self.delete_field()


    def delete_record(self):
        self.error['text'] = ''
        try:
            selected = self.tree.selection()[0][3]
            conn = sqlite3.connect('darbuotoju_duomenys.db')
            c = conn.cursor()

            alphabet = string.ascii_lowercase
            if selected.isnumeric():
                selected = selected
            else:
                for a in [y for y in enumerate(alphabet.upper(), 10)]:
                    if selected == a[1]:
                        selected = a[0]

            with conn:
                c.execute(f'DELETE FROM darbuotoju_duomenys WHERE id = {selected}')

            self.tree.delete(self.tree.selection())
            self.delete_field()
        except IndexError:
            self.error['text'] = 'Nepasirinkote įrašo'


    def select_record(self):
        self.error['text'] = ''
        try:
            select = self.tree.focus()
            values = self.tree.item(select, 'values')

            if (self.field_id.get() == '' and self.field_name.get() == '' and self.field_last_name.get() == '' and
                    self.field_birth_date.get() == '' and self.field_gender.get() == '' and self.field_address.get() == '' and
                    self.field_zip_code.get() == '' and self.field_duties.get() == '' and self.field_salary.get() == ''):

                self.field_id.insert(0, values[0])
                self.field_name.insert(0, values[1])
                self.field_last_name.insert(0, values[2])
                self.field_birth_date.insert(0, values[3])
                self.field_gender.insert(0, values[4])
                self.field_address.insert(0, values[5])
                self.field_zip_code.insert(0, values[6])
                self.field_duties.insert(0, values[7])
                self.field_salary.insert(0, values[8])
        except IndexError:
            self.error['text'] = 'Nepasirinkote įrašo'

    def update_record(self):
        self.error['text'] = ''
        try:
            select = self.tree.focus()
            self.tree.item(select, values=(self.field_id.get(), self.field_name.get(), self.field_last_name.get(),
                                    self.field_birth_date.get(), self.field_gender.get(), self.field_address.get(),
                                    self.field_zip_code.get(), self.field_duties.get(), self.field_salary.get()))

            x = self.tree.selection()[0]
            conn = sqlite3.connect('darbuotoju_duomenys.db')
            c = conn.cursor()
            with conn:
                c.execute(f'UPDATE darbuotoju_duomenys SET Vardas="{self.field_name.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Pavardė="{self.field_last_name.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Gimimo_data="{self.field_birth_date.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Lytis="{self.field_gender.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Adresas="{self.field_address.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Pašto_kodas="{self.field_zip_code.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Pareigos="{self.field_duties.get()}" WHERE id={x[3]}')
                c.execute(f'UPDATE darbuotoju_duomenys SET Atlyginimas="{self.field_salary.get()}" WHERE id={x[3]}')

            self.delete_field()
        except IndexError:
            self.error['text'] = 'Nepasirinkote įrašo'


# window = Tk()
# All_data(window)
# window.mainloop()