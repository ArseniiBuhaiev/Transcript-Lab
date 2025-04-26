from tkinter import *
from customtkinter import *
import os
import pyperclip
from phonetics_lab_ua import phonetic
from phonetics_lab_ua import phonematic

# Функція запису до файлу
def write_to_file(text, fp):
    if os.path.exists(fp):
        with open(fp, 'a', encoding='utf-8') as file:
            file.write(f'\n{text}')
    else:
        with open(fp, 'w', encoding='utf-8') as file:
            file.write(text)

# Функція читання з файлу
def read_from_file(fp):
    with open(fp, 'r', encoding='utf-8') as file:
        from_file = file.read()
        return from_file

# Функція зміни поведінки клавіші Enter
def enter_behaviour(event):
    if event.state & (0x0001 | 0x0004):
        return
    else:
        transcribe()
        return 'break'

# Функція транскрибування слова
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

# Функція появи/зникнення кнопок для збереження результату в залежності від його наявності
def show_buttons():
    transcription = output_field.get(1.0, END)
    if transcription.strip() != '' and 'ПОМИЛКА' not in transcription:
        copy_button.place(x = 1075, y=240, anchor=E)
        save_button.place(x = 1075, y=300, anchor=E)
    else:
        copy_button.place_forget()
        save_button.place_forget()

# Функція завантаження слова з текстового файлу для транскрибування
def load():
    load_path = filedialog.askopenfilename(filetypes=[("Текстовий файл", "*.txt")])
    if load_path:
        text = read_from_file(load_path)
        input_field.delete(1.0, END)
        input_field.insert(END, text)
        transcribe()

# Функція копіювання результату в буфер обміну        
def copy():
    pyperclip.copy(output_field.get(1.0, END).strip())

# Функція збереження транскрипції у файл
def save():
    word = input_field.get(1.0, END)
    transcription = output_field.get(1.0, END)
    result = f'{word.replace('%', '').strip()}: {transcription.strip()}'
    save_path = filedialog.asksaveasfilename(initialfile=f"{word.replace('%', '').strip()}_транскрипція.txt",
                                             filetypes=[("Текстовий файл", "*.txt")])
    if save_path:
        write_to_file(result, save_path)

# Створення інтерфейсу та конфігурація вікна програми
ui = Tk()
ui.title('Автоматичний транскриптор')
ui.configure(bg="#1e2838")
ui.geometry("1100x350")
ui.resizable(width=False, height=False)

# Створення елементів інтерфейсу (поле введення, виведення)
input_label = Label(ui, text="ТЕКСТ ДЛЯ ТРАНСКРИБУВАННЯ:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
output_label = Label(ui, text="ТРАНСКРИБОВАНИЙ ТЕКСТ:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
input_field = CTkTextbox(ui, fg_color="#161c26", font=('Cambria', 22), corner_radius=20, width=500, height=20)
output_field = CTkTextbox(ui, fg_color="#161c26", font=('Cambria', 22), corner_radius=20, width=500, height=20)
output_field.configure(state="disabled")

# Створення елементів інтерфейсу (вибір функції)
type_selected = IntVar()
type_selected.set(0)

# Створення елементів для вибору типу транскрипції
radio_label = Label(ui, text="Оберіть тип транскрипції:", bg="#1e2838", fg="#d3e7e8", font=('Cambria', 20))
radio_1 = CTkRadioButton(ui, text="Фонетична", font=("Cambria", 20), variable=type_selected, value=0, command=transcribe)
radio_2 = CTkRadioButton(ui, text="Фонематична", font=("Cambria", 20), variable=type_selected, value=1, command=transcribe)

# Створення елементів інтерфейсу (кнопки транскрибування, копіювання в буфер та збереження у файл)
transcribe_button = CTkButton(ui, text="ТРАНСКРИБУВАТИ", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=transcribe)
load_button = CTkButton(ui, text="ЗАВАНТАЖИТИ З ФАЙЛУ .txt", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=load)
copy_button = CTkButton(ui, text="СКОПІЮВАТИ", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=copy)
save_button = CTkButton(ui, text="ЗБЕРЕГТИ В .txt", font=("Cambria", 20), height=50, width=500, corner_radius=5, command=save)

# Виклик результату по натисканню клавіші Enter та зміна його поведінки у вікні для вводу
input_field.bind('<Return>', enter_behaviour)

# Розміщення елементів інтерфейсу
#info_field.place(x=25, y=25)
input_label.place(x=25, y=25)
output_label.place(x=575, y=25)
input_field.place(x=25, y=70)
output_field.place(x=1075, y=70, anchor=NE)
transcribe_button.place(x =1075, y=180, anchor=E)
load_button.place(x=25, y=180, anchor=W)
radio_label.place(x=25, y=230, anchor=W)
radio_1.place(x=45, y=270, anchor=W)
radio_2.place(x=45, y=310, anchor=W)

ui.mainloop()

