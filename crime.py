from tkinter import *
from tkinter import ttk, filedialog
import tkinter.messagebox
import sqlite3
import cv2
from PIL import Image, ImageTk

class Crime:
    def __init__(self, root):
        self.database = Database()
        self.database.connect()  # Changed 'conn' to 'connect'

        self.root = root
        self.root.title("Crime Record Management System")
        self.root.geometry("1200x750")
        self.root.config(bg="#f5f5f5")

        # Variables
        self.cId = StringVar()
        self.cName = StringVar()
        self.cStname = StringVar()
        self.cCrime = StringVar()
        self.cPlace = StringVar()
        self.cCitname = StringVar()
        self.photo_path = StringVar()

        # Configure styles
        self.configure_styles()

        # Create main container
        main_frame = Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Header Section
        self.create_header(main_frame)

        # Input Section
        input_frame = self.create_input_section(main_frame)

        # Button Panel
        self.create_buttons(main_frame)

        # Treeview Section
        self.create_treeview(main_frame)

        # Initialize default image and data
        self.display_default_image()
        self.showlist()
        self.crimeList.bind("<ButtonRelease-1>", self.crimerec)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), 
                       background="#2c3e50", foreground="white")
        style.configure("Treeview", font=('Arial', 10), rowheight=30)
        style.map("Treeview", background=[('selected', '#3498db')])
        style.configure("Custom.TButton", font=('Arial', 10, 'bold'), 
                       foreground="white")
        style.map("Custom.TButton",
                background=[('active', '#2c3e50'), ('disabled', '#bdc3c7')],
                foreground=[('active', 'white'), ('disabled', '#7f8c8d')])

    def create_header(self, parent):
        header_frame = Frame(parent, bg="#2c3e50", height=80)
        header_frame.pack(fill=X, pady=(0, 20))
        Label(header_frame, text="CRIME RECORD MANAGEMENT SYSTEM", 
             font=("Arial", 20, "bold"), bg="#2c3e50", fg="white").pack(side=LEFT, padx=20)

    def create_input_section(self, parent):
        input_frame = Frame(parent, bg="white", bd=2, relief=GROOVE)
        input_frame.pack(fill=X, pady=10)

        # Left Input Fields
        left_frame = Frame(input_frame, bg="white", padx=20, pady=15)
        left_frame.pack(side=LEFT)

        labels = ["Crime ID:", "Criminal Name:", "Station Name:", 
                 "Crime:", "Crime Place:", "Citizen Name:"]
        variables = [self.cId, self.cName, self.cStname, 
                    self.cCrime, self.cPlace, self.cCitname]
        self.entries = []

        for i, (label, var) in enumerate(zip(labels, variables)):
            row_frame = Frame(left_frame, bg="white")
            row_frame.grid(row=i, column=0, sticky=W, pady=5)
            Label(row_frame, text=label, font=("Arial", 11), 
                 bg="white", width=12, anchor=W).pack(side=LEFT)
            entry = ttk.Entry(row_frame, textvariable=var, 
                             font=("Arial", 11), width=30)
            entry.pack(side=LEFT, padx=5)
            self.entries.append(entry)

        # Right Photo Section
        right_frame = Frame(input_frame, bg="white", padx=20, pady=15)
        right_frame.pack(side=RIGHT)

        self.photo_label = Label(right_frame, bg="#ecf0f1", width=150, height=150)
        self.photo_label.pack()
        ttk.Button(right_frame, text="Upload Photo", command=self.upload_photo, 
                  style="Custom.TButton").pack(pady=10)

        return input_frame

    def create_buttons(self, parent):
        button_frame = Frame(parent, bg="#f5f5f5")
        button_frame.pack(fill=X, pady=10)

        buttons = [
            ("Add Record", "#27ae60", self.insert),
            ("Show Records", "#2980b9", self.showlist),
            ("Search", "#f39c12", self.search),
            ("Update", "#3498db", self.update),
            ("Delete", "#e74c3c", self.delete),
            ("Clear", "#95a5a6", self.clear),
            ("Exit", "#34495e", self.close)
        ]

        for text, color, cmd in buttons:
            style_name = f"{text.replace(' ', '')}.TButton"
            ttk.Style().configure(style_name, background=color)
            btn = ttk.Button(button_frame, text=text, command=cmd, 
                            style=style_name)
            btn.pack(side=LEFT, padx=5, ipadx=10, ipady=5)

    def create_treeview(self, parent):
        tree_frame = Frame(parent, bg="white", bd=2, relief=GROOVE)
        tree_frame.pack(fill=BOTH, expand=True)

        columns = ("Crime ID", "Criminal Name", "Station Name", 
                  "Crime", "Place", "Citizen Name", "Photo Path")
        self.crimeList = ttk.Treeview(tree_frame, columns=columns, 
                                    show="headings", selectmode=BROWSE)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", 
                           command=self.crimeList.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", 
                           command=self.crimeList.xview)
        self.crimeList.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.crimeList.grid(row=0, column=0, sticky=NSEW)
        vsb.grid(row=0, column=1, sticky=NS)
        hsb.grid(row=1, column=0, sticky=EW)

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        col_widths = [100, 150, 150, 150, 150, 150, 200]
        for col, width in zip(columns, col_widths):
            self.crimeList.heading(col, text=col)
            self.crimeList.column(col, width=width, anchor=W)

    # Database operations
    def insert(self):
        if self.cId.get():
            self.database.insert(
                self.cId.get(),
                self.cName.get(),
                self.cStname.get(),
                self.cCrime.get(),
                self.cPlace.get(),
                self.cCitname.get(),
                self.photo_path.get()
            )
            tkinter.messagebox.showinfo("Success", "Record inserted successfully!")
            self.showlist()
            self.clear()
        else:
            tkinter.messagebox.showerror("Error", "Crime ID is required!")

    def update(self):
        if self.cId.get():
            self.database.update(
                self.cId.get(),
                self.cName.get(),
                self.cStname.get(),
                self.cCrime.get(),
                self.cPlace.get(),
                self.cCitname.get(),
                self.photo_path.get()
            )
            tkinter.messagebox.showinfo("Success", "Record updated successfully!")
            self.showlist()
            self.clear()
        else:
            tkinter.messagebox.showerror("Error", "Select a record to update!")

    def showlist(self):
        self.crimeList.delete(*self.crimeList.get_children())
        for row in self.database.show():
            self.crimeList.insert("", END, values=row)

    def delete(self):
        if self.cId.get():
            self.database.delete(self.cId.get())
            tkinter.messagebox.showinfo("Success", "Record deleted successfully!")
            self.showlist()
            self.clear()
        else:
            tkinter.messagebox.showerror("Error", "Select a record to delete!")

    def search(self):
        self.crimeList.delete(*self.crimeList.get_children())
        for row in self.database.search(
            self.cId.get(),
            self.cName.get(),
            self.cStname.get(),
            self.cCrime.get(),
            self.cPlace.get(),
            self.cCitname.get()
        ):
            self.crimeList.insert("", END, values=row)

    # Image handling
    def upload_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            self.photo_path.set(file_path)
            self.display_image(file_path)

    def display_image(self, image_path):
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (150, 150))
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.photo_label.config(image=img)
            self.photo_label.image = img
        except Exception as e:
            print(f"Error loading image: {e}")
            self.display_default_image()

    def display_default_image(self):
        img = Image.new("RGB", (150, 150), "#ecf0f1")
        img = ImageTk.PhotoImage(img)
        self.photo_label.config(image=img)
        self.photo_label.image = img

    # Other functions
    def clear(self):
        for entry in self.entries:
            entry.delete(0, END)
        self.photo_path.set("")
        self.display_default_image()

    def close(self):
        if tkinter.messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def crimerec(self, event):
        selected = self.crimeList.focus()
        values = self.crimeList.item(selected, "values")
        if values:
            self.entries[0].delete(0, END)
            self.entries[0].insert(END, values[0])
            self.entries[1].delete(0, END)
            self.entries[1].insert(END, values[1])
            self.entries[2].delete(0, END)
            self.entries[2].insert(END, values[2])
            self.entries[3].delete(0, END)
            self.entries[3].insert(END, values[3])
            self.entries[4].delete(0, END)
            self.entries[4].insert(END, values[4])
            self.entries[5].delete(0, END)
            self.entries[5].insert(END, values[5])
            self.photo_path.set(values[6])
            self.display_image(values[6])


class Database:
    def __init__(self):
        self.connection = None  # Changed from 'conn' to 'connection'
        self.cursor = None

    def connect(self):  # Renamed 'conn' to 'connect'
        try:
            self.connection = sqlite3.connect("crime_records.db")
            self.cursor = self.connection.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS crime_records (
                    crime_id TEXT PRIMARY KEY,
                    criminal_name TEXT,
                    station_name TEXT,
                    crime TEXT,
                    crime_place TEXT,
                    citizen_name TEXT,
                    photo_path TEXT
                )'''
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, cid, cname, cstname, ccrime, cplace, ccitname, photo_path):
        query = '''INSERT INTO crime_records 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (cid, cname, cstname, ccrime, cplace, ccitname, photo_path))
        self.connection.commit()

    def update(self, cid, cname, cstname, ccrime, cplace, ccitname, photo_path):
        query = '''UPDATE crime_records SET
                   criminal_name = ?,
                   station_name = ?,
                   crime = ?,
                   crime_place = ?,
                   citizen_name = ?,
                   photo_path = ? 
                   WHERE crime_id = ?'''
        self.cursor.execute(query, (cname, cstname, ccrime, cplace, ccitname, photo_path, cid))
        self.connection.commit()

    def show(self):
        self.cursor.execute("SELECT * FROM crime_records")
        return self.cursor.fetchall()

    def delete(self, cid):
        self.cursor.execute("DELETE FROM crime_records WHERE crime_id = ?", (cid,))
        self.connection.commit()

    def search(self, cid, cname, cstname, ccrime, cplace, ccitname):
        query = '''SELECT * FROM crime_records 
                   WHERE crime_id LIKE ? 
                   AND criminal_name LIKE ? 
                   AND station_name LIKE ?
                   AND crime LIKE ? 
                   AND crime_place LIKE ? 
                   AND citizen_name LIKE ?'''
        params = (
            f"%{cid}%",
            f"%{cname}%",
            f"%{cstname}%",
            f"%{ccrime}%",
            f"%{cplace}%",
            f"%{ccitname}%"
        )
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    root = Tk()
    app = Crime(root)
    root.mainloop()
