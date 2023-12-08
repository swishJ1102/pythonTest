import os
import tkinter as tk
from configparser import ConfigParser
from tkinter import filedialog
from tkinter import ttk


def get_program_directory():
    return os.path.dirname(os.path.abspath(__file__))


def get_config_file_path():
    return os.path.join(get_program_directory(), ".config.ini")


def save_file_paths(input_file_path, output_file_path):
    config = ConfigParser()
    config['Paths'] = {'input_file_path': input_file_path, 'output_file_path': output_file_path}
    with open(get_config_file_path(), 'w') as configfile:
        config.write(configfile)


def load_file_paths():
    config = ConfigParser()
    config.read(get_config_file_path())
    return config['Paths'] if 'Paths' in config else {}


def update_from_config_paths(entry_before, entry_after, config_path):
    if config_path:
        entry_before.insert(tk.END, config_path.get('input_file_path'))
        entry_after.insert(tk.END, config_path.get('output_file_path'))


def convert_text():
    input_file_path = entry_before.get()
    output_file_path = entry_after.get()
    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
            converted_text = input_text.replace('a', 'A')
        with open(output_file_path, 'w') as file:
            file.write(converted_text)
            tmp = ['a',
                   'b']
            tree.insert('', 'end', values=tmp)
            tree_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
            tree_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
            tree.configure(yscrollcommand=tree_scrollbary.set)
            tree.configure(xscrollcommand=tree_scrollbarx.set)
            tree.pack()
            output_label.config(text="転換成功！", fg="green", font=('Arial', 15))
    except FileNotFoundError:
        output_label.config(text="ファイルは見つかりません。", fg="red", font=('Arial', 15))


def clear_before_entry():
    convert_button.config(state=tk.NORMAL)
    entry_before.delete(0, tk.END)
    output_label.config(text="")


def clear_after_entry():
    convert_button.config(state=tk.NORMAL)
    entry_after.delete(0, tk.END)
    output_label.config(text="")


def on_leave(event):
    if entry_before.get().replace(" ", "") == "":
        return
    else:
        if os.path.exists(entry_before.get()):
            convert_button.config(state=tk.NORMAL)
            output_label.config(text="")
        else:
            convert_button.config(state=tk.DISABLED)
            output_label.config(text=f"ファイル['{entry_before.get()}']はシステムに存在しません。", fg="red",
                                font=('Arial', 13))
            entry_before.focus_set()


def exit_app():
    save_file_paths(entry_before.get(), entry_after.get())
    root.destroy()


def show_hidden_preview():
    if tree.winfo_ismapped():
        tree.delete(*tree.get_children())
        tree.pack_forget()
        tree_scrollbary.pack_forget()
        tree_scrollbarx.pack_forget()
    else:
        tree_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(yscrollcommand=tree_scrollbary.set)
        tree.configure(xscrollcommand=tree_scrollbarx.set)
        tree.pack(pady=15)


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_before.delete(0, tk.END)
        entry_before.insert(tk.END, folder_path)
        show_files_in_tree(folder_path)


def show_files_in_tree(folder_path):
    try:
        file_list = os.listdir(folder_path)
        tree.delete(*tree.get_children())

        for index, file_name in enumerate(file_list, start=1):
            file_path = os.path.join(folder_path, file_name)
            tmp = [str(index), file_path]
            tree.insert('', 'end', values=tmp)

        tree_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(yscrollcommand=tree_scrollbary.set)
        tree.configure(xscrollcommand=tree_scrollbarx.set)
        tree.pack()

        tree.heading('#0', text='CheckBox')
        tree.column('#0', width=50, anchor='center')
        # tree.tag_configure('unchecked', background='white')
        # tree.tag_configure('checked', background='#D3F1FF')
        for item in tree.get_children():
            tree.tag_configure('unchecked', background='white')
            canvas = tk.Canvas(tree, width=25, height=25, highlightthickness=0)
            canvas.create_rectangle(5, 5, 20, 20, outline='black', fill='white', tags='checkbox')
            canvas.tag_bind('checkbox', '<Button-1>', lambda event, i=item: on_checkbox_change(i))
            # tree.tag_bind(item, '<Button-1>', lambda event, i=item: on_checkbox_change(i))

        output_label.config(text="ファイル表示成功。", fg="green", font=('Arial', 13))
    except FileNotFoundError:
        output_label.config(text="ファイルは見つかりません。", fg="red", font=('Arial', 15))


def on_checkbox_change(item):
    values = tree.item(item, 'values')
    current_state = values[0]
    new_state = not current_state
    tree.item(item, values=(new_state, values[1], values[2]))


root = tk.Tk()
root.title("転換ツール　V1.0.0")

# root.overrideredirect(True)

window_width = 800
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.configure(bg="#e0e0e0")
# root.resizable(False, False)
font_style = ('Arial', 10)

frame_before = tk.Frame(root, bg="#e0e0e0")
frame_before.pack(pady=15)

label_before_text = tk.Label(frame_before, text="入力パ   ス：", font=font_style, bg="#e0e0e0")
label_before_text.grid(row=0, column=0, padx=1)

entry_before = tk.Entry(frame_before, width=50, font=font_style)
entry_before.bind("<FocusOut>", on_leave)
entry_before.grid(row=0, column=1, padx=15)

browse_button_before = tk.Button(frame_before, text="入力選択", command=lambda: (
    clear_before_entry(), browse_folder()), bg='#DDDDDD',
                                 fg='black', font=font_style)
browse_button_before.grid(row=0, column=2, padx=(10, 30))

frame_after = tk.Frame(root, bg="#e0e0e0")
frame_after.pack(pady=15)

label_after_text = tk.Label(frame_after, text="出力パ   ス：", font=font_style, bg="#e0e0e0")
label_after_text.grid(row=0, column=0, padx=1)

entry_after = tk.Entry(frame_after, width=50, font=font_style)
entry_after.grid(row=0, column=1, padx=15)

browse_button_after = tk.Button(frame_after, text="出力選択", command=lambda: (
    clear_after_entry(), entry_after.insert(tk.END, filedialog.askopenfilename())), bg='#DDDDDD', fg='black',
                                font=font_style)
browse_button_after.grid(row=0, column=2, padx=(10, 30))

frame_button = tk.Frame(root, bg="#e0e0e0")
frame_button.pack(pady=10)
convert_button = tk.Button(frame_button, text="実行する", command=convert_text, bg='#2ECC40', fg="white",
                           # relief=tk.FLAT,
                           font=('Arial', 13))
convert_button.pack(side=tk.LEFT, padx=(100, 10))

exit_button = tk.Button(frame_button, text="退出する", command=exit_app, bg='#AAAAAA', fg="white",  # relief=tk.FLAT,
                        font=('Arial', 13))
exit_button.pack()
exit_button.pack(side=tk.LEFT, padx=(10, 50))

list_button = tk.Button(frame_button, text="詳細内容", command=show_hidden_preview, bg='#e0e0e0', relief=tk.FLAT,
                        font=font_style)
list_button.pack(side=tk.RIGHT, padx=(0, 1))

output_label = tk.Label(root, text="", bg="#e0e0e0", fg='black')
output_label.pack(pady=10)

tree_frame = tk.Frame(root, bg="#e0e0e0")
tree_frame.pack(pady=5, padx=(20, 20))
tree = ttk.Treeview(tree_frame, columns=('Line', 'Info'), show='headings', height=20)
tree.heading('Line', text='行目')
tree.heading('Info', text='内容')
tree.column('Line', width=50, anchor='center')
tree.column('Info', width=1000, anchor='w')

# sizegrip_tree = ttk.Sizegrip(tree_frame)
# sizegrip_tree.pack(side=tk.BOTTOM, anchor='se')
tree_scrollbary = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree_scrollbarx = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
tree_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
tree_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(yscrollcommand=tree_scrollbary.set)
tree.configure(xscrollcommand=tree_scrollbarx.set)

tree.pack()

config_path = load_file_paths()
update_from_config_paths(entry_before, entry_after, config_path)

root.mainloop()
