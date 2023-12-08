import tkinter as tk
from tkinter import ttk


def on_checkbox_change(event):
    item = tree.identify_row(event.y)
    values = tree.item(item, 'values')
    current_state = values[0]
    new_state = not current_state
    tree.item(item, values=(new_state, values[1]))


root = tk.Tk()
root.title("CheckBox in TreeView")

tree = ttk.Treeview(root, columns=('Checkbox', 'Data'), show='headings')
tree.heading('Checkbox', text='Checkbox')
tree.heading('Data', text='Data')

for i in range(5):
    tree.insert('', 'end', values=(False, f'Data {i}'))

tree.bind('<Button-1>', on_checkbox_change)

tree.pack()
root.mainloop()
