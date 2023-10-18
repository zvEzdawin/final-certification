import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def open_search_dialog(self):
        Search()

    def search_records(self, name):
        name = ("%" + name + "%",)
        self.db.c.execute("""SELECT * FROM employees WHERE full_name LIKE ?""", name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(
                """DELETE FROM employees WHERE id=?""",
                (self.tree.set(selection_item, "#1"),)
            )
            self.db.conn.commit()
            self.view_records()

    def update_record(self, full_name, phone, email, salary):
        self.db.c.execute(
            """UPDATE employees SET full_name=?, phone=?, email=?, salary=?
            WHERE ID=?""",
            (full_name, phone, email, salary, self.tree.set(self.tree.selection()[0], "#1"))
        )
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def records(self, full_name, phone, email, salary):
        self.db.insert_data(full_name, phone, email, salary)
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="image\\add.png")
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=("ID", "full_name", "phone", "email", "salary"),
            height=45, show="headings"
        )
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("full_name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("full_name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Заработная плата")

        self.tree.pack(side=tk.LEFT)

        # создание кнопки изменения данных

        self.update_img = tk.PhotoImage(file="image/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления записи

        self.delete_img = tk.PhotoImage(file="image/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска

        self.search_img = tk.PhotoImage(file="image/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    def init_child(self):
        # Заголовок окна
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

    def open_dialog(self):
        Child()

    def view_records(self):
        self.db.c.execute("""SELECT * FROM employees """)

        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert("", "end", values=row) for row in self.db.c.fetchall()]


class Child(tk.Toplevel, Main):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить")

        self.geometry("400x220")

        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text="E-mail")
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text="Заработная плата")
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=300, y=190)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=220, y=190)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_phone.get(),
                self.entry_email.get(), self.entry_salary.get()
            ),
        )


class Update(Child):
    def __init__(self):
        super(Update, self).__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактировать позицию")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=190)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_record(
                self.entry_name.get(), self.entry_phone.get(),
                self.entry_email.get(), self.entry_salary.get()
            ),
        )
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute(
            """SELECT * FROM employees WHERE id=?""",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )

        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super(Search, self).__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Поиск")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            email TEXT,
            salary REAL);"""
        )
        self.conn.commit()

    def insert_data(self, full_name, phone, email, salary):
        self.c.execute(
            """INSERT INTO employees (full_name, phone, email, salary)
            VALUES (?,?,?,?)""",
            (full_name, phone, email, salary),
        )
        self.conn.commit()

if __name__ == "__main__":
    # создаем экран приложения
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()

    # Конфиг приложения
    root.title("Список сотрудников компании")
    root.resizable(False, False)
    root.geometry("1280x768+400+200")
    root.mainloop()