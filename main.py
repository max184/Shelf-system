from tkinter import simpledialog
from customtkinter import *
from CTkTable import *
import sqlite3

app = CTk()
app.geometry("950x500")
set_appearance_mode("dark")

TabView = CTkTabview(master=app)
TabView.pack(padx=20, pady=20)

TabView.add("Add Menu")
TabView.add("TableView")

frame = CTkFrame(master=TabView.tab("Add Menu"), fg_color="#8D6F3A", border_color="#FFCC70", border_width=2, width=450, height=450)
frame.pack(expand=True)

def GetValues():
    # Collecting values
    entered_values = (
        ItemName.get(),
        ItemInfo.get(),
        MacAdd.get(),
        JobNum.get(),
        Notes.get(),
        Shelf.get()
    )

    # Printing the entered values
    print(f"Entered Value: {entered_values}")

    # Connecting to SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Creating a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS your_table (
            item_name TEXT,
            item_info TEXT,
            mac_address TEXT,
            job_number TEXT,
            notes TEXT,
            shelf TEXT
        )
    ''')

    # Inserting values into the table
    cursor.execute('''
        INSERT INTO your_table (item_name, item_info, mac_address, job_number, notes, shelf)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', entered_values)

    # Committing the changes and closing the connection
    conn.commit()
    conn.close()

    # Load data to CTkTable after inserting into the database
    load_data_to_table()

lable = CTkLabel(master=TabView.tab("Add Menu"), text="Welcome to the smart inventory system", font=("Arial", 20), text_color="white", fg_color="transparent", bg_color="#8D6F3A")
lable.place(relx=0.5, rely=0.1, anchor="center")

ItemName = CTkEntry(master=TabView.tab("Add Menu"), placeholder_text="Enter Item Name", width=115, bg_color="#8D6F3A")
ItemName.place(relx=0.5, rely=0.2, anchor="center")

ItemInfo = CTkEntry(master=TabView.tab("Add Menu"), placeholder_text="Item Info", width=115, bg_color="#8D6F3A")
ItemInfo.place(relx=0.5, rely=0.3, anchor="center")

MacAdd = CTkEntry(master=TabView.tab("Add Menu"), placeholder_text="Mac Address", width=115, bg_color="#8D6F3A")
MacAdd.place(relx=0.5, rely=0.4, anchor="center")

JobNum = CTkEntry(master=TabView.tab("Add Menu"), placeholder_text="Related Job Number", width=130, bg_color="#8D6F3A")
JobNum.place(relx=0.5, rely=0.5, anchor="center")

Notes = CTkEntry(master=TabView.tab("Add Menu"), placeholder_text="Notes", width=115, bg_color="#8D6F3A")
Notes.place(relx=0.5, rely=0.6, anchor="center")

Shelf = CTkComboBox(master=TabView.tab("Add Menu"), values=["Shelf A", "Shelf B", "Shelf C"], bg_color="#8D6F3A")
Shelf.place(relx=0.5, rely=0.7, anchor="center")

ItemID = CTkLabel(master=TabView.tab("Add Menu"), text="ID:", font=("Arial", 20), text_color="white", bg_color="#8D6F3A")
ItemID.place(relx=0.5, rely=0.8, anchor="center")

btn = CTkButton(master=TabView.tab("Add Menu"), text="Submit", corner_radius=10, fg_color="black", hover_color="darkgray", border_color="white", border_width=2, font=("Arial", 20), text_color="white", command=GetValues, bg_color="#8D6F3A")
btn.place(relx=0.5, rely=0.9, anchor="center")

# CTkTable to display data from the database
table_frame = CTkFrame(master=TabView.tab("TableView"), width=450, height=450)
table_frame.pack(expand=True)

# Function to fetch data from the database and populate CTkTable
def load_data_to_table():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM your_table')
    rows = cursor.fetchall()
    conn.close()

    # Clear existing rows in the CTkTable
    table.update_values(rows)

# Button to load data into CTkTable
load_data_btn = CTkButton(master=TabView.tab("TableView"), text="Load Data", corner_radius=10, fg_color="black", hover_color="darkgray", border_color="white", border_width=2, font=("Arial", 20), text_color="white", command=load_data_to_table, bg_color="#8D6F3A")
load_data_btn.place(relx=0.5, rely=0.9, anchor="center")

# CTkTable widget
table = CTkTable(master=table_frame, row=5, column=6)
table.pack(expand=True, fill="both", padx=20, pady=20)

def search_by_id():
    search_id = simpledialog.askstring("Search", "Enter ID:")
    if search_id is not None:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM your_table WHERE rowid = ?', (search_id,))
        row = cursor.fetchone()

        conn.close()

        if row:
            # Display details in a dialog or highlight the row
            details = "\n".join([f"{label}: {value}" for label, value in zip(["Item Name", "Item Info", "Mac Address", "Job Number", "Notes", "Shelf"], row)])
            simpledialog.messagebox.showinfo("Search Result", details)
        else:
            simpledialog.messagebox.showinfo("Search Result", "ID not found")

# Search button
search_btn = CTkButton(master=TabView.tab("TableView"), text="Search", corner_radius=10, fg_color="black", hover_color="darkgray", border_color="white", border_width=2, font=("Arial", 20), text_color="white", command=search_by_id, bg_color="#8D6F3A")
search_btn.place(relx=0.3, rely=0.9, anchor="center")

# Function to delete a specific ID
def delete_by_id():
    delete_id = simpledialog.askstring("Delete", "Enter ID to delete:")
    if delete_id is not None:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT rowid FROM your_table WHERE rowid = ?', (delete_id,))
        row = cursor.fetchone()

        if row:
            # Confirm deletion
            confirmation = simpledialog.askstring("Confirmation", f"Do you want to delete item with ID {delete_id}? (yes/no)")
            if confirmation.lower() == 'yes':
                cursor.execute('DELETE FROM your_table WHERE rowid = ?', (delete_id,))
                conn.commit()
                simpledialog.messagebox.showinfo("Deletion", f"Item with ID {delete_id} deleted successfully.")
            else:
                simpledialog.messagebox.showinfo("Deletion", "Deletion canceled.")
        else:
            simpledialog.messagebox.showinfo("Deletion", "ID not found")

        conn.close()

# Delete button
delete_btn = CTkButton(master=TabView.tab("TableView"), text="Delete", corner_radius=10, fg_color="black", hover_color="darkgray", border_color="white", border_width=2, font=("Arial", 20), text_color="white", command=delete_by_id, bg_color="#8D6F3A")
delete_btn.place(relx=0.7, rely=0.9, anchor="center")

app.mainloop()
