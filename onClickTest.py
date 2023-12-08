import tkinter as tk
from tkinter import ttk


def on_cell_click(event):
    item = tree.identify('item', event.x, event.y)
    column = tree.identify('column', event.x, event.y)
    print(f"Click on item: {item}, column: {column}")
    cell_value = tree.item(item, 'values')[int(column.split('#')[-1]) - 1]

    close_popup_window()

    popup_window = tk.Toplevel(root)
    popup_window.configure(bg="#e0e0e0")

    label = tk.Label(popup_window, text=f"{cell_value}", bg="#e0e0e0")
    label.pack(padx=10, pady=10)

    x, y, _, _ = tree.bbox(item, column)
    x_root, y_root = root.winfo_rootx(), root.winfo_rooty()
    popup_window.geometry(f"+{x_root + x}+{y_root + y}")

    popup_window.overrideredirect(True)
    popup_window.bind('<Leave>', lambda event: popup_window.destroy())
    popup_window.bind('<B1-Motion>', lambda e: drag_window(popup_window, e))

    global current_popup_window
    current_popup_window = popup_window


def drag_window(window, event):
    x, y = event.x_root, event.y_root
    window.geometry(f"+{x - drag_start_x}+{y - drag_start_y}")


def on_press(event):
    global drag_start_x, drag_start_y
    drag_start_x, drag_start_y = event.x, event.y


def close_popup_window(window=None):
    global current_popup_window
    if window:
        window.destroy()
    elif current_popup_window:
        current_popup_window.destroy()
    current_popup_window = None


def on_cell_motion(event):
    if getattr(on_cell_motion, 'time_running', False):
        return
    # x, y = event.x, event.y
    # item = tree.identify_row(y)
    # column = tree.identify_column(x)
    x_global, y_global = root.winfo_pointerxy()
    x_tree, y_tree = tree.winfo_rootx(), tree.winfo_rooty()
    x, y = x_global - x_tree, y_global - y_tree
    item = tree.identify_row(y)
    column = tree.identify_column(x)
    if item and column:
        if column == "#1":
            return
        # item = tree.identify('item', event.x, event.y)
        # column = tree.identify('column', event.x, event.y)
        print(f"Mouse on item: {item}, column: {column}")
        cell_value = tree.item(item, 'values')[int(column.split('#')[-1]) - 1]

        close_popup_window()

        popup_window = tk.Toplevel(root)
        popup_window.configure(bg="#e0e0e0")

        label = tk.Label(popup_window, text=f"{cell_value}", bg="#e0e0e0")
        label.pack(padx=10, pady=10)

        x, y, _, _ = tree.bbox(item, column)
        x_root, y_root = root.winfo_rootx(), root.winfo_rooty()
        popup_window.geometry(f"+{x_root + x}+{y_root + y}")

        popup_window.overrideredirect(True)
        popup_window.bind('<Leave>', lambda e: on_cell_leave(e, item))
        popup_window.bind('<Button>', lambda e: on_cell_leave(e, item))
        # popup_window.bind('<B1-Motion>', lambda e: drag_window(popup_window, e))

        global current_popup_window
        current_popup_window = popup_window

        on_cell_motion.time_running = True
        root.after(500, lambda: setattr(on_cell_motion, 'time_running', False))
        # root.after(3000, show_popup, item, column, cell_value)


def show_popup(item, column, cell_value):
    close_popup_window()

    popup_window = tk.Toplevel(root)
    popup_window.configure(bg="#e0e0e0")

    label = tk.Label(popup_window, text=f"{cell_value}", bg="#e0e0e0", font=('Arial', 50))
    label.pack(padx=50, pady=50)

    x, y, _, _ = tree.bbox(item, column)
    x_root, y_root = root.winfo_rootx(), root.winfo_rooty()
    popup_window.geometry(f"+{x_root + x}+{y_root + y}")

    popup_window.overrideredirect(True)
    popup_window.bind('<Leave>', lambda e: on_cell_leave(e, item))
    popup_window.bind('<Button>', lambda e: on_cell_leave(e, item))
    # popup_window.bind('<B1-Motion>', lambda e: drag_window(popup_window, e))

    global current_popup_window
    current_popup_window = popup_window

    on_cell_motion.event_triggered = True


def on_cell_leave(event, current_item):
    on_cell_motion.event_triggered = False
    x_global, y_global = root.winfo_pointerxy()
    x_tree, y_tree = tree.winfo_rootx(), tree.winfo_rooty()
    x, y = x_global - x_tree, y_global - y_tree
    leave_item = tree.identify_row(y)
    if current_item == leave_item:
        close_popup_window()


root = tk.Tk()
root.title("Click Event")
tree = ttk.Treeview(root, columns=('Column1', 'Column2'), show='headings')
tree.heading('Column1', text='Column1')
tree.heading('Column2', text='Column2')

for i in range(5):
    if i == 4:
        tree.insert('', 'end', values=(f'Data {i}', f'DataDataDataDataDataDataDataDataDataDataDataData {i + 1}'))
    else:
        tree.insert('', 'end', values=(f'Data {i}', f'Data {i + 1}'))

tree.bind('<Motion>', on_cell_motion)
tree.bind('<Leave>', lambda e: on_cell_leave(e, None))
# tree.bind('<ButtonRelease-1>', on_cell_click)

current_popup_window = None

tree.pack()
root.mainloop()
