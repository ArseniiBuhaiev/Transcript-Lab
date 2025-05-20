from customtkinter import *
import json
import os
import sys
import pyperclip
from phonetics_lab_ua import phonetic_text
from phonetics_lab_ua import phonematic_text

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
    func_lst = [phonetic_text, phonematic_text]
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
        copy_button.configure(state="normal")
        save_button.configure(state="normal")
    else:
        copy_button.configure(state="disabled")
        save_button.configure(state="disabled")

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

# Функція визначення шляху до іконки
def get_icon_path():
    if getattr(sys, "frozen", False):
        icon_path = os.path.join(sys._MEIPASS, "newICON.ico")
    else:
        icon_path = "newICON.ico"
    return icon_path

# Функція застосування налаштувань
def apply_settings():
    global settings_json
    global pref_path
    pref_dir = os.path.join(os.path.expanduser("~"),
                             ".phoneticslabua")
    pref_path = f"{pref_dir}\\preferences.json"
    if os.path.exists(pref_path):
        with open(pref_path, "r") as file:
            settings_json = json.load(file)
        set_appearance_mode(settings_json["theme"])
        set_widget_scaling(settings_json["scale"])
        set_window_scaling(settings_json["scale"])
    else:
        os.makedirs(pref_dir, exist_ok=True)
        settings_json = {
            "theme": "light",
            "scale": 1.0
        }
        with open(pref_path, "w") as file:
            json.dump(settings_json, file)
        set_appearance_mode(settings_json["theme"])
        set_widget_scaling(settings_json["scale"])
        set_window_scaling(settings_json["scale"])

# Очищення основного фрейму від елементів попереднього інтерфейсу
def clear():
    for widget in main_area.winfo_children():
        widget.grid_forget()

# Створення інтерфейсу та конфігурація вікна програми
app = CTk()
app.title('Phonetics Lab UA')
app.iconbitmap(get_icon_path())
app.geometry("1353x500")
app.resizable(width=False, height=False)
set_default_color_theme("themes/rime.json")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)
apply_settings()

# Створення елементів інтерфейсу (панель, основна зона)
sidebar = CTkFrame(app, height=500, corner_radius=0)
sidebar.grid_propagate(False)
main_area = CTkFrame(app, width=1100, height=500, fg_color="transparent")
main_area.grid_propagate(False)

# Створення елементів інтерфейсу транскрибування тексту
input_frame = CTkFrame(main_area, fg_color="transparent")
input_label = CTkLabel(input_frame, text="ТЕКСТ ДЛЯ ТРАНСКРИБУВАННЯ:", font=('Segoe UI', 25))
input_field = CTkTextbox(input_frame, font=('Cambria', 22), wrap="word", corner_radius=20, border_color=["#b9c4c9", "#3e3e3e"], border_width=2, width=500, height=260)
load_button = CTkButton(input_frame, text="ЗАВАНТАЖИТИ З ФАЙЛУ .txt", font=("Segoe UI", 20), height=50, width=500, corner_radius=50, command=load)

type_selected = IntVar()
type_selected.set(0)
type_frame = CTkFrame(input_frame, fg_color="transparent")
radio_label = CTkLabel(type_frame, text="Оберіть тип транскрипції:", font=('Segoe UI', 25))
radio_1 = CTkRadioButton(type_frame, text="Фонетична", font=("Segoe UI", 20), variable=type_selected, value=0, command=transcribe)
radio_2 = CTkRadioButton(type_frame, text="Фонематична", font=("Segoe UI", 20), variable=type_selected, value=1, command=transcribe)

output_frame = CTkFrame(main_area, fg_color="transparent")
output_label = CTkLabel(output_frame, text="ТРАНСКРИБОВАНИЙ ТЕКСТ:", font=('Segoe UI', 25))
output_field = CTkTextbox(output_frame, font=('Cambria', 22), wrap="word", corner_radius=20, border_color=["#b9c4c9", "#3e3e3e"], border_width=2, width=500, height=260)
output_field.configure(state="disabled")

transcribe_button = CTkButton(output_frame, text="ТРАНСКРИБУВАТИ", font=("Segoe UI", 20), height=50, width=500, corner_radius=50, command=transcribe)
copy_button = CTkButton(output_frame, text="СКОПІЮВАТИ", font=("Segoe UI", 20), height=50, width=500, corner_radius=50, state="disabled", command=copy)
save_button = CTkButton(output_frame, text="ЗБЕРЕГТИ В .txt", font=("Segoe UI", 20), height=50, width=500, corner_radius=50, state="disabled", command=save)

# Створення елементів інтерфейсу налаштувань
theme_frame = CTkFrame(main_area, border_color=["#b9c4c9", "#3e3e3e"], border_width=2, fg_color="transparent")
theme_label = CTkLabel(theme_frame, text="Тема застосунку: ", font=("Segoe UI", 25))
theme_selected = StringVar()
theme_selected.set(settings_json["theme"])

# Функція оновлення налаштування теми
def theme_update():
    choice = theme_selected.get()
    settings_json["theme"] = choice
    set_appearance_mode(settings_json["theme"])
    with open(pref_path, "w") as file:
        json.dump(settings_json, file)

theme_radio1 = CTkRadioButton(theme_frame, text="Світла", font=("Segoe UI", 20), variable=theme_selected, value="light", command=theme_update)
theme_radio2 = CTkRadioButton(theme_frame, text="Темна", font=("Segoe UI", 20), variable=theme_selected, value="dark", command=theme_update)

scaling_frame = CTkFrame(main_area, border_color=["#b9c4c9", "#3e3e3e"], border_width=2, fg_color="transparent")

# Функція оновлення налаштування масштабування
def scaling_menu_callback(choice):
    choice = float(choice[:-1]) / 100
    settings_json["scale"] = choice
    set_window_scaling(choice)
    set_widget_scaling(choice)
    with open(pref_path, "w") as file:
        json.dump(settings_json, file)

scaling_menu = CTkOptionMenu(scaling_frame,
                             font=("Segoe UI", 20),
                             dropdown_font=("Segoe UI", 20),
                             values=["50%", "75%", "100%", "125%", "150%", "200%"],
                             command=scaling_menu_callback)
scaling_menu.set(f"{int(settings_json["scale"] * 100)}%")
scaling_label = CTkLabel(scaling_frame, text=f"Масштабування інтерфейсу:", font=("Segoe UI", 25))

# Виклик інтерфейсу транскрибування тексту
def text_ui():
    clear()

    input_frame.grid(row=0, column=0, sticky="nswe")
    input_label.grid(row=0, column=0, padx=25, pady=5, sticky="w")
    input_field.grid(row=1, column=0, padx=25, pady=5, sticky="ew")
    load_button.grid(row=2, column=0, padx=25, pady=5, sticky="w")
    type_frame.grid(row=3, column=0, padx=25, sticky="nswe")
    radio_label.grid(row=0, column=0, padx=25, pady=5, sticky = "w")
    radio_1.grid(row=1, column=0, padx=25, sticky = "nswe")
    radio_2.grid(row=2, column=0, padx=25, sticky = "nswe")

    output_frame.grid(row=0, column=1, sticky="nswe")
    output_label.grid(row=0, column=0, padx=25, pady=5, sticky="w")
    output_field.grid(row=1, column=0, padx=25, pady=5, sticky="ew")
    transcribe_button.grid(row=2, column=0, padx=25, pady=5, sticky="ew")
    copy_button.grid(row=3, column=0, padx=25, pady=5, sticky="ew")
    save_button.grid(row=4, column=0, padx=25, pady=5, sticky="ew")

# Виклик інтерфейсу налаштувань
def settings_ui():
    clear()
    theme_frame.grid_propagate(False)
    theme_frame.configure(width = 1050, height=120)
    theme_frame.grid(row=0, column=0, padx=25, pady=25)
    theme_label.grid(row=0, column=0, padx=10, pady=10)
    theme_radio1.grid(row=1, column=0, padx=50, sticky="w")
    theme_radio2.grid(row=2, column=0, padx=50, sticky="w")

    scaling_frame.grid_propagate(False)
    scaling_frame.configure(width = 1050, height=120)
    scaling_frame.grid(row=1, column=0, padx=25, pady=25)
    scaling_label.grid(row=0, column=0, padx=10, pady=10)
    scaling_menu.grid(row=1, column=0, padx=50, pady=10, sticky="w")

def placeholder_ui():
    clear()
    x = CTkLabel(main_area, text="This is a placeholder UI! The app is still in development")
    x.grid(row=0, column=0)

# Створення списку для вибору функції
text = CTkButton(sidebar, text="Транскрибування тексту", font=("Segoe UI", 20), height=50, width=250, corner_radius=0, hover_color=["#a3afb5", "#3e3e3e"], text_color=["#2A2C2F", "#F2F7FC"], fg_color="transparent", command=text_ui)
audio = CTkButton(sidebar, text="Транскрибування аудіо", font=("Segoe UI", 20), height=50, width=250, corner_radius=0, hover_color=["#a3afb5", "#3e3e3e"], text_color=["#2A2C2F", "#F2F7FC"], fg_color="transparent", command=placeholder_ui)
analysis = CTkButton(sidebar, text="Аналіз транскрипції", font=("Segoe UI", 20), height=50, width=250, corner_radius=0, hover_color=["#a3afb5", "#3e3e3e"], text_color=["#2A2C2F", "#F2F7FC"], fg_color="transparent", command=placeholder_ui)
settings = CTkButton(sidebar, text="Налаштування", font=("Segoe UI", 20), height=50, width=250, corner_radius=0, hover_color=["#a3afb5", "#3e3e3e"], text_color=["#2A2C2F", "#F2F7FC"], fg_color="transparent", command=settings_ui)

# Виклик результату по натисканню клавіші Enter та зміна його поведінки у вікні для вводу
input_field.bind('<Return>', enter_behaviour)

# Розміщення елементів інтерфейсу
sidebar.grid(row=0, column=0, sticky="nswe")
text.pack()
audio.pack()
analysis.pack()
settings.pack(side="bottom")
main_area.grid(row=0, column=1, sticky="nswe")

if __name__ == "__main__":
    text_ui()
    app.mainloop()