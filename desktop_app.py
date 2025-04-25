from tkinter import *
from customtkinter import *
import os
import pyperclip
from transcript import phonetic
from transcript import phonematic

def write_to_file(text, fp):
    if os.path.exists(fp):
        with open(fp, 'a', encoding='utf-8') as file:
            file.write(f'\n{text}')
    else:
        with open(fp, 'w', encoding='utf-8') as file:
            file.write(text)

def read_from_file(fp):
    with open(fp, 'r', encoding='utf-8') as file:
        from_file = file.read()
        return from_file

def enter_behaviour(event):
    if event.state & (0x0001 | 0x0004):
        return
    else:
        transcribe()
        return 'break'

def transcribe():
    func_lst = [phonetic, phonematic]
    get_type = type_selected.get()
    picked_func = func_lst[get_type]
    user_input = input_field.get(1.0, END)
    transcription = picked_func(user_input)
    output_field.configure(state="normal")
    output_field.delete(1.0, END)
    output_field.insert(END, transcription)
    output_field.configure(state="disabled")
    show_buttons()

def show_buttons():
    transcription = output_field.get(1.0, END)
    if transcription != '' and 'ПОМИЛКА' not in transcription:
        copy_button.place(x = 1075, y=400, anchor=E)
        save_button.place(x = 1075, y=460, anchor=E)
    else:
        copy_button.place_forget()
        save_button.place_forget()

def load():
    load_path = filedialog.askopenfilename(filetypes=[("Текстовий файл", "*.txt")])
    if load_path:
        text = read_from_file(load_path)
        input_field.delete(1.0, END)
        input_field.insert(END, text)
        transcribe()
        
def copy():
    pyperclip.copy(output_field.get(1.0, END).strip())

def save():
    word = input_field.get(1.0, END)
    transcription = output_field.get(1.0, END)
    result = f'{word.replace('%', '').strip()}: {transcription.strip()}'
    save_path = filedialog.asksaveasfilename(initialfile=f"{word.replace('%', '').strip()}_транскрипція.txt",
                                             filetypes=[("Текстовий файл", "*.txt")])
    if save_path:
        write_to_file(result, save_path)

#Створення інтерфейсу
ui = Tk()
#Назва вікна
ui.title('Автоматичний транскриптор')
#Колір заднього фону
ui.configure(bg="#1e2838")
#Розмір вікна
ui.geometry("1100x500")
#Заборона змінити розмір вікна
ui.resizable(width=False, height=False)

#Створення текстового об'єкту із правилами користування
info_field = Text(ui, bg="#1e2838", fg="#d3e7e8", font=('Cambria', 18), bd=0, width=500, height=5)
info_field.insert(1.0,'''Правила користування транскриптором:

1. Введені слова складаються виключно з кириличних літер.
2. Транскриптор працює лише з одним словом.
3. Наголос, за потреби, позначати знаком відсотка після букви (ро%ги, робо%та, ма%ма тощо).
''')
info_field.configure(state=DISABLED)

#Створення елементів інтерфейсу (поле введення, виведення)
input_label = Label(ui, text="ТЕКСТ ДЛЯ ТРАНСКРИБУВАННЯ:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
output_label = Label(ui, text="ТРАНСКРИБОВАНИЙ ТЕКСТ:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
input_field = CTkTextbox(ui, fg_color="#161c26", font=('Cambria', 22), corner_radius=20, width=500, height=20)
output_field = CTkTextbox(ui, fg_color="#161c26", font=('Cambria', 22), corner_radius=20, width=500, height=20)
output_field.configure(state="disabled")

#Створення елементів інтерфейсу (вибір функції)
type_selected = IntVar()
type_selected.set(0)

radio_label = Label(ui, text="Оберіть тип транскрипції:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
radio_1 = CTkRadioButton(ui, text="Фонетична", font=("Cambria", 20), variable=type_selected, value=0)
radio_2 = CTkRadioButton(ui, text="Фонематична", font=("Cambria", 20), variable=type_selected, value=1)

#Створення елементів інтерфейсу (кнопки транскрибування, копіювання в буфер та збереження у файл)
transcribe_button = CTkButton(ui, text="ТРАНСКРИБУВАТИ", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=transcribe)
load_button = CTkButton(ui, text="ЗАВАНТАЖИТИ З ФАЙЛУ .txt", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=load)
copy_button = CTkButton(ui, text="СКОПІЮВАТИ", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=copy)
save_button = CTkButton(ui, text="ЗБЕРЕГТИ В .txt", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=save)
#Виклик результату по натисканню клавіші Enter та зміна його поведінки у вікні для вводу
input_field.bind('<Return>', enter_behaviour)


#Розміщення елементів інтерфейсу
info_field.place(x=25, y=25)
input_label.place(x=25, y=185)
output_label.place(x=575, y=185)
input_field.place(x=25, y=230)
output_field.place(x=1075, y=230, anchor=NE)
transcribe_button.place(x = 1075, y=340, anchor=E)
load_button.place(x = 25, y=340, anchor=W)
radio_label.place(x=25, y=390, anchor=W)
radio_1.place(x=45, y=430, anchor=W)
radio_2.place(x=45, y=460, anchor=W)

ui.mainloop()

