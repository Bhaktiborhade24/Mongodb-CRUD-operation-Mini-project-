import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# ----------------- MongoDB Connection -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["skincare_database"]
collection = db["skincare"]

# ----------------- Colors & Styles -----------------
BG_COLOR = "#4E342E"
FG_COLOR = "#FFFFFF"
BTN_COLOR = "#FFB300"
BTN_HOVER = "#FFA000"
ENTRY_BG = "#6D4C41"
FONT = ("Segoe UI", 10)

# ----------------- Functions -----------------
def create_skincare():
    skincare = get_form_data()
    if not all(skincare.values()):
        messagebox.showerror("Error", "All fields are required.")
        return
    if collection.find_one({"id": skincare["id"]}):
        messagebox.showerror("Error", "Item with this ID already exists.")
        return
    collection.insert_one(skincare)
    messagebox.showinfo("Success", "Skincare item added successfully!")
    clear_entries()
    read_skincare()

def read_skincare():
    listbox.delete(0, tk.END)
    header = f"{'ID':<10} {'Item':<20} {'Brand':<20} {'Amount':<10}"
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, "-" * 65)
    for item in collection.find():
        listbox.insert(
            tk.END,
            f"{item.get('id',''):<10} {item.get('item',''):<20} {item.get('brand',''):<20} {item.get('amount',''):<10}"
        )

def update_skincare():
    skincare_id = entry_id.get()
    if not skincare_id:
        messagebox.showerror("Error", "Skincare ID is required for update.")
        return
    new_values = get_form_data()
    result = collection.update_one({"id": skincare_id}, {"$set": new_values})
    if result.modified_count > 0:
        messagebox.showinfo("Success", "Skincare item updated successfully!")
    else:
        messagebox.showwarning("Warning", "No changes made or Item not found.")
    clear_entries()
    read_skincare()

def delete_skincare():
    skincare_id = entry_id.get()
    if not skincare_id:
        messagebox.showerror("Error", "Skincare ID is required for deletion.")
        return
    result = collection.delete_one({"id": skincare_id})
    if result.deleted_count > 0:
        messagebox.showinfo("Success", "Skincare item deleted successfully!")
    else:
        messagebox.showwarning("Warning", "Item not found.")
    clear_entries()
    read_skincare()

def clear_entries():
    for entry in (entry_id, entry_item, entry_brand, entry_amount):
        entry.delete(0, tk.END)

def get_form_data():
    return {
        "id": entry_id.get().strip(),
        "item": entry_item.get().strip(),
        "brand": entry_brand.get().strip(),
        "amount": entry_amount.get().strip()
    }

def on_listbox_select(event):
    selection = listbox.curselection()
    if selection and selection[0] > 1:
        data = listbox.get(selection[0]).split()
        clear_entries()
        entry_id.insert(0, data[0])
        entry_item.insert(0, data[1])
        entry_brand.insert(0, data[2])
        entry_amount.insert(0, data[3])

# ----------------- UI Setup -----------------
root = tk.Tk()
root.title("Skincare Management System")
root.geometry("600x500")
root.config(bg=BG_COLOR)

top_label = tk.Label(root, text="Bhakti Borhade 412 - CRUD Operation GUI (Skincare Database)",
                     bg=BG_COLOR, fg=FG_COLOR, font=("Segoe UI", 12, "bold"))
top_label.pack(anchor="w", padx=10, pady=5)

form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.pack(anchor="w", padx=10, pady=5)

def create_label_entry(text):
    label = tk.Label(form_frame, text=text, bg=BG_COLOR, fg=FG_COLOR, font=FONT, anchor="w")
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground="white", font=FONT, width=30)
    entry.pack(anchor="w", pady=5, ipady=3, ipadx=5)
    return entry

entry_id = create_label_entry("Skincare ID")
entry_item = create_label_entry("Skincare Item")
entry_brand = create_label_entry("Skincare Brand")
entry_amount = create_label_entry("Skincare Amount")

btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(anchor="w", padx=10, pady=5)

def create_button(text, command, color=BTN_COLOR):
    btn = tk.Button(btn_frame, text=text, command=command, bg=color, fg="black",
                    activebackground=BTN_HOVER, font=FONT, width=12, relief="flat")
    btn.pack(side=tk.LEFT, padx=5)
    return btn

create_button("Create", create_skincare)
create_button("Read", read_skincare)
create_button("Update", update_skincare)
create_button("Delete", delete_skincare, "#e53935")  # Red delete button
create_button("Clear", clear_entries, "#8E24AA")  # Purple clear button

listbox = tk.Listbox(root, width=70, height=15, bg="#8D6E63", fg=FG_COLOR,
                     font=FONT, selectbackground="#A1887F", selectforeground=FG_COLOR)
listbox.pack(anchor="w", padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", on_listbox_select)

read_skincare()
root.mainloop()