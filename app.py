from tkinter import *
from customtkinter import *
import pyperclip
from transcript1 import main_phonetic as phonetic
from transcript1 import main_phonematic as phonematic

func_lst = [phonetic, phonematic]

def transcribe():
    global func_lst
    global type_selected
    global output_field
    get_type = type_selected.get()
    picked_func = func_lst[get_type]
    user_input = input_field.get(1.0, END)
    transcription = picked_func(user_input)
    output_field.configure(state="normal")
    output_field.delete(1.0, END)
    output_field.insert(END, transcription)
    output_field.configure(state="disabled")
    copy_button.place(x = 1075, y=400, anchor=E)
    save_button.place(x = 1075, y=460, anchor=E)

def load():
    global func_lst
    global type_selected
    get_type = type_selected.get()
    picked_func = func_lst[get_type]
    result = ""
    load_path = filedialog.askopenfilename(filetypes=[("Текстовий файл", "*.txt")])
    if load_path:
        with open(load_path, "r", encoding="utf-8") as fp:
            text = fp.read()
            for word in text.split():
                transcription = picked_func(word)
                result += f'{word.strip()}: {transcription.strip()}\n'
            if result != "":
                save_path = filedialog.asksaveasfilename(initialfile=f"транскрипція.txt",
                                                         filetypes=[("Текстовий файл", "*.txt")])
                if save_path:
                    with open(save_path, "w+", encoding="utf-8") as fp:
                        fp.write(result)
        

def copy():
    global output_field
    pyperclip.copy(output_field.get(1.0, END))

def save():
    global input_field
    global output_field

    word = input_field.get(1.0, END)
    transcription = output_field.get(1.0, END)

    if transcription != "":
        directory = filedialog.asksaveasfilename(initialfile=f"{word.replace('!', '').strip()}_транскрипція.txt",
                                                 filetypes=[("Текстовий файл", "*.txt")])
        if directory:
            with open(directory, "w+", encoding="utf-8") as fp:
                fp.write(f'{word.strip()}: {transcription.strip()}')
                fp.close()

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
3. Наголошений голосний позначати знаком оклику після звуку (ро!ги, робо!та, ма!ма тощо).
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

