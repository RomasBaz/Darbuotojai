from tkinter import *
from sqlalchemy import Column, Integer, String, create_engine
from dateutil.parser import parse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///registracijos_duomenys.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Register_data(Base):
    __tablename__ = 'Registracijos_duomenys'
    id = Column(Integer, primary_key=True)
    name = Column('Vardas', String)
    last_name = Column('Pavardė', String)
    birth_date = Column('Gimimo data', String)
    username = Column('Vartotojas', String)
    password = Column('Slaptažodis', String)
    repeat_password = Column('Pakartotinis slaptažodis', String)

    def __init__(self, name, last_name, birth_date, username, password, repeat_password):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.username = username
        self.password = password
        self.repeat_password = repeat_password

    def __repr__(self):
        return f'{self.id} {self.name} - {self.last_name} - {self.birth_date} - {self.username} - {self.password} - {self.repeat_password}'

# Base.metadata.create_all(engine)
class Register:

    def __init__(self, root):
        self.root = root
        self.name = Label(self.root, text='Vardas').grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.last_name = Label(self.root, text='Pavardė').grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.birth_date = Label(self.root, text='Gimimo data\n(formatu: Y-m-d)').grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.username = Label(self.root, text='Naujas vartotojo vardas').grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.password = Label(self.root, text='Slaptažodis\n(Turi susidaryti bent iš 8 skaitmenų)').grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.repeat_password = Label(self.root, text='Pakartoti slaptažodį').grid(row=5, column=0, padx=5, pady=5, sticky=E)

        self.registration_button = Button(self.root, text='Registruoti', command=lambda:[self.matching_password(), self.is_date(), self.no_empty_fields(), self.values_are_True(), self.database()]).grid(row=6, column=1, padx=5, pady=5)

        self.error = Label(self.root, text='')
        self.error.grid(row=7, columnspan=3, sticky=W)

        self.error1 = Label(self.root, text='')
        self.error1.grid(row=8, columnspan=3, sticky=W)

        self.error2 = Label(self.root, text='')
        self.error2.grid(row=9, columnspan=3, sticky=W)

        self.error3 = Label(self.root, text='')
        self.error3.grid(row=10, columnspan=3, sticky=W)

        self.error4 = Label(self.root, text='')
        self.error4.grid(row=11, columnspan=3, sticky=W)

        self.field_name = Entry(self.root)
        self.field_name.grid(row=0, column=1, padx=5, pady=5)

        self.field_last_name = Entry(self.root)
        self.field_last_name.grid(row=1, column=1, padx=5, pady=5)

        self.field_birth_date = Entry(self.root)
        self.field_birth_date.grid(row=2, column=1, padx=5, pady=5)

        self.field_username = Entry(self.root)
        self.field_username.grid(row=3, column=1, padx=5, pady=5)

        self.field_password = Entry(self.root)
        self.field_password.grid(row=4, column=1, padx=5, pady=5)

        self.field_repeat_password = Entry(self.root)
        self.field_repeat_password.grid(row=5, column=1, padx=5, pady=5)

    def fields(self):
        return self.field_name.get(), self.field_last_name.get(), self.field_birth_date.get(), self.field_username.get(), self.field_password.get(), self.field_repeat_password.get()

    def matching_password(self):
        self.error['text'] = ''
        self.error4['text'] = ''
        true_password = self.fields()[4]
        repeat_password = self.fields()[5]
        if len(true_password) < 8:
            self.error['text'] = 'Slaptažodis turi susidaryti bent iš 8 skaitmenų'
            return False

        if true_password != repeat_password:
            self.error4['text'] = 'Neteisingai ivedėte pakartotinį slaptažodį!'
            return False
        else:
            return True

    def no_empty_fields(self):
        self.error1['text'] = ''
        if self.fields()[0] == '' or self.fields()[1] == '' or self.fields()[2] == '' or self.fields()[3] == '' or self.fields()[4] == '' or self.fields()[5] == '':
            self.error1['text'] = 'Neužpildėte visus laukus!'
            return False
        else:
            return True

    def values_are_True(self):
        self.error3['text'] = ''
        if not self.fields()[0].isalpha() or not self.fields()[1].isalpha():
            self.error3['text'] = 'Neteisingai įvedėte arba vardą arba pavardę'
            return False
        else:
            return True

    def is_date(self, fuzzy=False):
        try:
            self.error2['text'] = ''
            parse(self.fields()[2], fuzzy=fuzzy)
            return True
        except ValueError:
            self.error2['text'] = 'Neteisingai ivesta data'
            return False


    def database(self):
        if self.values_are_True() == True:
            if self.is_date() == True:
                if self.no_empty_fields() == True:
                    if self.matching_password() == True:
                        name = self.fields()[0]
                        last_name = self.fields()[1]
                        birth_date = self.fields()[2]
                        username = self.fields()[3]
                        password = self.fields()[4]
                        repeat_password = self.fields()[5]
                        data = Register_data(name, last_name, birth_date, username, password, repeat_password)
                        session.add(data)
                        session.commit()

                        self.field_name.delete(0, END)
                        self.field_last_name.delete(0, END)
                        self.field_birth_date.delete(0, END)
                        self.field_username.delete(0, END)
                        self.field_password.delete(0, END)
                        self.field_repeat_password.delete(0, END)

# window = Tk()
# Register(window)
# window.mainloop()