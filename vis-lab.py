import random
import tkinter as tk
from tkinter import *
import threading

bele_kuglice=3
crne_kuglice=7
broj_izvlacenja=2

def teorijsko_izracunavanje():
    broj_povoljnih_ishoda=1
    ukupan_broj_ishoda=1
    for i in range(broj_izvlacenja):
        ukupan_broj_ishoda*=(bele_kuglice+crne_kuglice)-i
    for i in range(broj_izvlacenja):
        if(i==0):
            broj_povoljnih_ishoda*=(bele_kuglice)
        else:
            broj_povoljnih_ishoda*=(crne_kuglice+bele_kuglice-i)
    return broj_povoljnih_ishoda/ukupan_broj_ishoda

def programsko_izracunavanje(n):
    ukupno=0
    for i in range(n):
        kutija = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        prvi=random.choice(kutija)
        kutija.remove(prvi)
        random_broj=random.choice(kutija)

        if random_broj==1:
            ukupno+=1
    return ukupno/n

STEP_SIZE = 2
DELAY_MS = 20
flag=0
brojac=0

def reset():
    for i in range(len(lista)):
        canvas.coords(lista[i], koordinate_x1[i], koordinate_y1[i],
                  koordinate_x2[i], koordinate_y2[i])
    window.update()


def move_circle(random_number):
    koordinate_y1copy=koordinate_y1.copy()
    koordinate_y2copy=koordinate_y2.copy()

    while koordinate_y1copy[random_number] > 80:
        koordinate_y1copy[random_number] -= STEP_SIZE
        koordinate_y2copy[random_number] -= STEP_SIZE

        canvas.coords(lista[random_number], koordinate_x1[random_number], koordinate_y1copy[random_number],
                      koordinate_x2[random_number], koordinate_y2copy[random_number])

        window.update()
        window.after(DELAY_MS)

    button.config(state="normal")


def button_click():
    global flag
    flag+=1

    if(flag==1):
        try:
            reset()
            global brojac
            brojac += 1
            counter_label.set(str(brojac))
            random_number = random.randint(0, 9)
            button.config(state="disabled")
            thread = threading.Thread(target=move_circle(random_number))
            thread.start()

            random_number2 = random.randint(0, 9)
            while (random_number2 == random_number):
                random_number2 = random.randint(0, 9)
            thread2 = threading.Thread(target=move_circle(random_number2))
            thread2.start()

            thread.join()
            thread2.join()
            flag = 0
        except Exception as e:
            print()

def close_window():
    window.destroy()
    window3.destroy()

def window_inicijalizacija():
    window.title("ANIMACIJA")
    window.resizable(False, False)

def canvas_inicijalizacija():
    canvas_width = 585
    canvas_height = 400

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
    canvas.pack()
    canvas.configure(background="#CCCCCC")

    canvas.create_rectangle(2, 50, 586, 140, fill="yellow")

    return canvas,canvas_width,canvas_height

def kreiranje_kuglica(canvas_width,canvas_height,lista,koordinate_x1,koordinate_x2,koordinate_y2,koordinate_y1):
    circle_radius = 20
    circle_spacing = 20

    start_x = canvas_width - (circle_radius + circle_spacing)
    start_y = canvas_height - (circle_radius + circle_spacing)

    for i in range(10):
        x1 = start_x - (i * (circle_radius * 2 + circle_spacing))
        y1 = start_y
        x2 = x1 + (circle_radius * 2)
        y2 = y1 + (circle_radius * 2)

        koordinate_x1.append(x1)
        koordinate_x2.append(x2)
        koordinate_y1.append(y1)
        koordinate_y2.append(y2)
        if (i < 3):
            lista.append(canvas.create_oval(x1, y1, x2, y2, fill="white"))
        else:
            lista.append(canvas.create_oval(x1, y1, x2, y2, fill="black"))

    return lista,koordinate_x1,koordinate_x2,koordinate_y2,koordinate_y1

def window_dodavanjeLabela(counter_label):
    labela2 = tk.Label(window, text="Brojac:")

    labela = tk.Label(window, textvariable=counter_label)
    labela2.pack(side="left")
    labela.pack(side="left")
    return labela,labela2

#ZA DRUGI PROZOR
def provera_number(number):
    if (number == '' or number.isnumeric()==0):return 0
    elif (int(number) >= 10000000):
        print("Broj je prevelik");return 0
    return 1

def ispisRacun_verovatnoca(number):
    programska_verovatnoca = programsko_izracunavanje(int(number))
    teorijska_verovatnoca = teorijsko_izracunavanje()
    print("Unet broj n: " + number)
    print("Teorijska verovatnoca dogadjaja A:", teorijska_verovatnoca)
    print("Programska verovatnoca dogadjaja A:", programska_verovatnoca)
    return teorijska_verovatnoca,programska_verovatnoca

def update_label():
    for lx in labels: lx.destroy()
    number = entry.get()
    if(provera_number(number)==0):return
    teorijska_verovatnoca,programska_verovatnoca= ispisRacun_verovatnoca(number)

    label.config(text="Za uneto n: " + number)
    l = tk.Label(window3, text="");l.pack()
    labels.append(l)
    l = tk.Label(window3, text="n: " + number); l.pack()
    labels.append(l)
    l = tk.Label(window3, text="Teorijska verovatnoca dogadjaja A: " + str(teorijska_verovatnoca))
    l.pack()
    labels.append(l)
    l = tk.Label(window3, text="Programska verovatnoca dogadjaja A: " + str(programska_verovatnoca))
    l.pack()
    labels.append(l)

def window3_dodavanjeLabela():
    l = tk.Label(window3, text="")  # za prazan red
    l.pack()
    label = tk.Label(window3, text="Unesite broj n:")
    label.pack()
    entry = tk.Entry(window3)
    entry.pack()
    l = tk.Label(window3, text="")
    l.pack()

    button = tk.Button(window3, text="Pokreni", command=update_label)
    button.pack()
    exit_button = Button(window3, text="Kraj", command=close_window)
    exit_button.pack(pady=20)

    return l,label,entry,button,exit_button

def window3_inicijalizacija():
    window3.title("rezultati")
    window3.geometry("450x300")
    window3.resizable(False, False)

try:
    if __name__ == "__main__":
        window = tk.Tk()
        window_inicijalizacija()
        canvas,canvas_width,canvas_height=canvas_inicijalizacija()

        lista = []
        koordinate_x1 = []
        koordinate_x2 = []
        koordinate_y2 = []
        koordinate_y1 = []

        lista,koordinate_x1,koordinate_x2,koordinate_y2,koordinate_y1=\
            kreiranje_kuglica(canvas_width,canvas_height,lista,koordinate_x1,koordinate_x2,koordinate_y2,koordinate_y1)


        counter_label = tk.StringVar()
        counter_label.set(str(brojac))

        labela,labela2=window_dodavanjeLabela(counter_label)

        exit_b = Button(window, text="Kraj", command=close_window)
        exit_b.pack(side="right")
        button = tk.Button(window, text="Click", command=button_click)
        button.pack(side="top")

        window.protocol("WM_DELETE_WINDOW", close_window)


        # ZA DRUGI PROZOR
        labels = []
        window3 = tk.Tk()
        window3_inicijalizacija()
        l, label, entry, button, exit_button = window3_dodavanjeLabela()

        window3.protocol("WM_DELETE_WINDOW", close_window)

        window.mainloop()
except Exception as e:
        print()

