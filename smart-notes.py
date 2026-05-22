import customtkinter as ct
from database_for_smart_note import NoteDatabase

db = NoteDatabase()

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("You smart note")
        self.Tab = ct.CTkTabview(self)
        self.Tab.pack(padx=10, pady=10, ipadx=25, ipady=35)
        self.Tab.add('Добавить')
        self.Tab.add('Все заметки')

        self.notes = Notes(master=self.Tab.tab('Все заметки'))
        self.add_button = ButtonAdd(master=self.Tab.tab('Добавить'), notes_screen = self.notes)

class ButtonAdd:
    def __init__(self, master, notes_screen):
        self.frame = ct.CTkFrame(master)
        self.but_add = ct.CTkButton(self.frame, text='добавить', fg_color='#359af0', text_color='white', width=200,font=('Arial', 17, 'bold'), command=lambda: self.add())
        self.entry_name = ct.CTkEntry(self.frame, placeholder_text="Введите название", font=('Arial', 14, 'bold'), width=150)
        self.entry = ct.CTkEntry(self.frame, placeholder_text="Введите текст", font=('Arial', 14, 'bold'),width=150)
        self.notes_screen = notes_screen

        self.frame.pack(padx=20, pady=20)
        self.entry_name.pack(padx=20, pady=20)
        self.entry.pack(padx=20, pady=20)
        self.but_add.pack(padx=20, pady=20)

    def add(self):
        enter = self.entry.get()
        name = self.entry_name.get()
        try:
            db.add(name,enter)
            print('заметка добавлена')
        except Exception as e:
            print(e)
        self.notes_screen.refresh()

class Notes:
    def __init__(self, master):
        self.main_frame = ct.CTkFrame(master)
        self.delete_but = ct.CTkButton(master, text='Удалить заметку', command=lambda: self.delete())
        self.current_note_name = None
        self.frame_left = ct.CTkFrame(self.main_frame)
        self.frame_right = ct.CTkFrame(self.main_frame)
        self.list = ct.CTkScrollableFrame(self.frame_left)
        self.textbox = ct.CTkTextbox(self.frame_right)

        self.main_frame.pack(padx=5, pady=5)
        self.frame_left.pack(side="left", padx=10,pady=10)
        self.frame_right.pack(side="right", padx=10,pady=10)
        self.list.pack(side="left", padx=5,pady=5)
        self.textbox.pack(side="top", padx=5,pady=5,ipadx=50)
        self.delete_but.pack(side="bottom", padx=5,pady=5)
        try:
            self.data = db.get_all()
            #print(self.data)
        except Exception as e:
            print(e)
        if self.data:
            for i in self.data:
                self.but_note = ButtonNote(name=i[0],
                                           master=self.list,
                                           text=i[1],
                                           textbox = self.textbox,
                                           notes_screen =self)

    def refresh(self):
        # 1. Удаляем все старые кнопки из скролл-фрейма
        for widget in self.list.winfo_children():
            widget.destroy()

            try:
                self.data = db.get_all()
            except Exception as e:
                print(e)

            if self.data:
                for i in self.data:
                    ButtonNote(name=i[0], master=self.list, text=i[1], textbox=self.textbox, notes_screen=self)

    def delete(self):
        db.delete(self.current_note_name)
        self.refresh()

class ButtonNote:
    def __init__(self, master,name,text,textbox,notes_screen):
        self.notes_screen = notes_screen
        self.text = text
        self.name = name
        self.but = ct.CTkButton(master, text=name, fg_color='#359af0', text_color='white', width=200,font=('Arial', 17, 'bold'), command=lambda: self.show())
        self.textbox = textbox

        self.but.pack(padx=20, pady=20)
    def show(self):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("0.0", self.text)
        self.notes_screen.current_note_name = self.name

app = App()
app.mainloop()