#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from functools import partial
import datetime
import time

class InvalidField(Exception):
    pass

def validateInput(nombre, edad, fecha, hora):
    if (nombre == "" or any(char.isdigit() for char in nombre)):
        raise InvalidField("Nombre Invalido")
    elif (edad == "" or not edad.isdigit()):
        raise InvalidField("Edad invalida")
    elif (not datetime.datetime.strptime(fecha, "%d-%m-%Y")):
        raise ValueError("Fecha invalida")
    elif (not time.strptime(hora, "%H:%M")):
        raise ValueError("Hora invalida")

def printTable(df, table):
    cols = list(df.columns)
    tree = ttk.Treeview(window)
    if table == "full":
        tree.pack(side="top")
    elif table == "esc":
        tree.pack(side="right")
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor="w")
        tree.heading(i, text=i, anchor='w')
    for index, row in df.iterrows():
        tree.insert("",0,text=index,values=list(row))
    
def plotEdad(df):
    try:
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, window)
        bar1.get_tk_widget().pack(side="left")
        df["edad"].value_counts().plot(kind='bar', ax=ax1)
        ax1.set_title('Frecuencia de Edad de Estudiantes')
        ax1.set_xlabel("Edad")
        ax1.set_ylabel("Frecuencia")
    except IndexError:
        print("Sin registros por graficar")

def getEscolaridades(df):
    count = df['escolaridad'].value_counts() 
    count = count.to_frame()
    count.rename(columns={"escolaridad": "Frecuencia de Escolaridad"}, inplace=True)
    printTable(count, "esc")

def validationCB(username, password, login_window):
    if username.get() == admin_user and password.get() == admin_password:
        login_window.destroy()
        return
    else:
        msg = tk.Message(login_window, text = "Credenciales incorrectas. Por favor intente de nuevo.")
        msg.config(bg='red', fg="white")
        login_window.after(5000, msg.destroy)
        msg.grid(row=0, column=2)

def enableExit():
    pass

def login():
    login_window = tk.Tk()
    login_window.protocol("WM_DELETE_WINDOW", enableExit)
    login_window.title('Inicie Sesion')

    #username label and text entry box
    usernameLabel = tk.Label(login_window, text="Usuario").grid(row=0, column=0)
    username = tk.StringVar()
    usernameEntry = tk.Entry(login_window, textvariable=username).grid(row=0, column=1)  

    #password label and password entry box
    passwordLabel = tk.Label(login_window,text="Password").grid(row=1, column=0)  
    password = tk.StringVar()
    passwordEntry = tk.Entry(login_window, textvariable=password, show='*').grid(row=1, column=1)

    validateLogin = partial(validationCB, username, password, login_window)

    #login button
    loginButton = tk.Button(login_window, text="Login", command=validateLogin, bg="green").grid(row=4, column=0)

    login_window.mainloop()

def deleteCB(df):
    window.withdraw()
    user_input = tk.simpledialog.askstring(title="Autenticacion", prompt="Ingrese password de admin para borrar los registros", show='*')
    if (user_input == admin_password):
        df = df[0:0]
        children = window.winfo_children()
        for child in children:
            child.destroy()
        showDashboard(df)
        window.deiconify()
    else:
        window.deiconify()
        msg = tk.Message(window, text = f"Password de administrador incorrecto.")
        msg.config(bg='red', font=('times', 24, 'italic'))
        window.after(5000, msg.destroy)
        msg.pack()

def deleteButton(df):
    delete = partial(deleteCB, df)
    B = tk.Button(window, text ="Eliminar todos los registros", command = delete, bg="orange")
    B.pack()

def submitCB(df, nombre, edad, escolaridad, fecha, hora, add_window):
    try:
        validateInput(nombre.get(), edad.get(), fecha.get(), hora.get())
        df.loc[len(df.index)] = [nombre.get(), edad.get(), escolaridad.get(), fecha.get(), hora.get()]
        df['fecha'] = pd.to_datetime(df['fecha'], format="%d-%m-%Y")
        df = df.sort_values(by=["fecha"])
        df["fecha"] = df["fecha"].dt.strftime("%d-%m-%Y")
        children = window.winfo_children()
        for child in children:
            child.destroy()
        showDashboard(df)
        window.deiconify()
        return
    except InvalidField as e:
        msg = tk.Message(add_window, text = e)
        msg.config(bg='red', fg="white")
        add_window.after(5000, msg.destroy)
        msg.grid(row=0, column=2)
    except ValueError:
        msg = tk.Message(add_window, text = "Formato de hora y/o fecha incorrecto. Formato correcto: \nHH:MM \ndd-mm-YYYY")
        msg.config(bg='red', fg="white")
        add_window.after(5000, msg.destroy)
        msg.grid(row=0, column=2)

def addCB(df):
    window.withdraw()
    add_window = tk.Toplevel()
    add_window.title('Agregar nuevo registro')

    niveles_escolaridad=[ 'Primaria' , 'Secundaria' , 'Preparatoria' , 'Universidad' , 'Posgrado']
    
    nombreLabel = tk.Label(add_window, text="Nombre")
    nombreLabel.grid(row=0, column=0)
    nombre = tk.StringVar()
    nombreEntry = tk.Entry(add_window, textvariable=nombre)
    nombreEntry.grid(row=0, column=1)

    edadLabel = tk.Label(add_window, text="Edad")
    edadLabel.grid(row=1, column=0)
    edad = tk.StringVar()
    edadEntry = tk.Entry(add_window, textvariable=edad)
    edadEntry.grid(row=1, column=1)
    
    escolaridadLabel = tk.Label(add_window, text="Escolaridad").grid(row=2, column=0)
    escolaridad = tk.StringVar()
    escolaridadEntry = tk.OptionMenu(add_window, escolaridad, *niveles_escolaridad)
    escolaridadEntry.grid(row=2, column=1)

    fechaLabel = tk.Label(add_window, text="Fecha").grid(row=3, column=0)
    fecha = tk.StringVar()
    fechaEntry = tk.Entry(add_window, textvariable=fecha)
    fechaEntry.grid(row=3, column=1)

    horaLabel = tk.Label(add_window, text="Hora").grid(row=4, column=0)
    hora = tk.StringVar()
    horaEntry = tk.Entry(add_window, textvariable=hora)
    horaEntry.grid(row=4, column=1)

    submit = partial(submitCB, df, nombre, edad, escolaridad, fecha, hora, add_window)

    submitButton = tk.Button(add_window, text="Ingresar", bg="green", command=submit)
    submitButton.grid(row=5, column=0)


def addButton(df):
    add = partial(addCB, df)
    B = tk.Button(window, text ="Agregar nuevo registro de alumno", command = add, bg="blue", fg="white")
    B.pack()

def saveCB(df):
    file_name = tk.simpledialog.askstring(title="Guardar registros", prompt="Ingrese el nombre del archivo JSON a generar")
    try:
        basePath = os.path.dirname(os.path.abspath(__file__))
        df.to_json(basePath + f"/{file_name}")
        msg = tk.Message(window, text = f"Registros guardados en: {basePath}/{file_name}")
        msg.config(bg='lightgreen', font=('times', 24, 'italic'))
        window.after(5000, msg.destroy)
        msg.pack()
    except Exception as e:
        print(e)
    

def saveButton(df):
    save = partial(saveCB, df)
    B = tk.Button(window, text ="Guardar registros en archivo JSON", command = save, bg="gray", fg="white")
    B.pack()

def loadCB(df, init):
    window.withdraw()
    file = tk.simpledialog.askstring(title="Cargar registros", prompt="Ingrese el nombre del archivo JSON a cargar (debe de encontrarse en el directorio actual)")
    try:
        basePath = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_json(basePath + f"/{file}", orient = "records")
        children = window.winfo_children()
        for child in children:
            child.destroy()
        if init == False:
            showDashboard(df)
        window.deiconify()
        msg = tk.Message(window, text = f"Archivo {file} cargado exitosamente")
        msg.config(bg='lightgreen', font=('times', 24, 'italic'))
        window.after(5000, msg.destroy)
        msg.pack()
        return df
    except Exception as e:
        window.deiconify()
        msg = tk.Message(window, text = f"El archivo {file} no existe")
        msg.config(bg='red', font=('times', 24, 'italic'))
        window.after(5000, msg.destroy)
        msg.pack()

def loadButton(df):
    load = partial(loadCB, df, False)
    B = tk.Button(window, text ="Cargar registros de archivo JSON", command = load, bg="gray", fg="white")
    B.pack()

def exitButton():
    B = tk.Button(window, text ="Salir", command = window.destroy, bg="red", fg="white")
    B.pack()

def showDashboard(df):
    printTable(df, "full")
    getEscolaridades(df)
    plotEdad(df)
    addButton(df)
    deleteButton(df)
    saveButton(df)
    loadButton(df)
    exitButton()

if __name__ == '__main__':
    global admin_user; admin_user = "root"
    global admin_password; admin_password = "toor"
    login()
    window = tk.Tk()
    df = pd.DataFrame()
    df = loadCB(df, True)
    showDashboard(df)
    window.mainloop()


