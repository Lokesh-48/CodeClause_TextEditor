import os
from tkinter import *
from tkinter import filedialog, colorchooser, font, ttk
from tkinter.messagebox import showinfo, askyesno

def change_color():
    color = colorchooser.askcolor(title="Pick a color...or else")
    text_area.config(fg=color[1])

def change_font(*args):
    text_area.config(font=(font_name.get(), size_box.get()))

def new_file():
    if askyesno("New File", "Are you sure you want to start a new file?"):
        window.title("Untitled")
        text_area.delete(1.0, END)

def open_file():
    file = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )

    if file:
        try:
            window.title(os.path.basename(file))
            text_area.delete(1.0, END)

            with open(file, "r") as f:
                text_area.insert(1.0, f.read())
        except Exception:
            showinfo("Error", "Couldn't read file")

def save_file():
    file = filedialog.asksaveasfilename(
        initialfile='untitled.txt',
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )

    if file:
        try:
            window.title(os.path.basename(file))
            with open(file, "w") as f:
                f.write(text_area.get(1.0, END))
        except Exception:
            showinfo("Error", "Couldn't save file")

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def toggle_text_format(tag_name, font_style):
    current_tags = text_area.tag_names("sel.first")
    if tag_name in current_tags:
        text_area.tag_remove(tag_name, "sel.first", "sel.last")
    else:
        text_area.tag_add(tag_name, "sel.first", "sel.last")
        text_area.tag_configure(tag_name, font=(font_name.get(), font_size.get(), font_style))

def bold_text():
    toggle_text_format("bold", "bold")

def italic_text():
    toggle_text_format("italic", "italic")

def underline_text():
    toggle_text_format("underline", "underline")

def about():
    showinfo("About", "This is a program written by YOU!")

def quit_editor():
    if askyesno("Quit", "Are you sure you want to quit?"):
        window.destroy()

window = Tk()
window.title("Text Editor Program")
file = None

window_width = 500
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

font_name = StringVar(window)
font_name.set("Arial")

font_size = StringVar(window)
font_size.set("25")

text_area = Text(window, font=(font_name.get(), font_size.get()))

scroll_bar = Scrollbar(text_area)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
text_area.grid(sticky=N + E + S + W)
scroll_bar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroll_bar.set)

frame = Frame(window)
frame.grid()

color_button = Button(frame, text="Color", command=change_color)
color_button.grid(row=0, column=0)

font_box = OptionMenu(frame, font_name, *font.families(), command=change_font)
font_box.grid(row=0, column=1)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)
size_box.grid(row=0, column=2)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_editor, accelerator="Ctrl+Q")

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Bold", command=bold_text, accelerator="Ctrl+B")
edit_menu.add_command(label="Italic", command=italic_text, accelerator="Ctrl+I")
edit_menu.add_command(label="Underline", command=underline_text, accelerator="Ctrl+U")

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

window.bind("<Control-n>", lambda event: new_file())
window.bind("<Control-o>", lambda event: open_file())
window.bind("<Control-s>", lambda event: save_file())
window.bind("<Control-q>", lambda event: quit_editor())
window.bind("<Control-x>", lambda event: cut())
window.bind("<Control-c>", lambda event: copy())
window.bind("<Control-v>", lambda event: paste())
window.bind("<Control-b>", lambda event: bold_text())
window.bind("<Control-i>", lambda event: italic_text())
window.bind("<Control-u>", lambda event: underline_text())

window.mainloop()
