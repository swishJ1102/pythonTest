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


def create_file_detail_treeview(parent):

    file_tree_frame = tk.Frame(parent, bg="#e0e0e0")
    file_tree_frame.pack(pady=5, padx=(10, 50))


def create_result_detail_treeview(parent):
    result_tree_frame = tk.Frame(parent, bg="#e0e0e0")
    result_tree_frame.pack(pady=5, padx=(10, 50))

    tree = ttk.Treeview(result_tree_frame, columns=('Line', 'Info'), show='headings', height=20)
    tree.heading('Line', text='行目')
    tree.heading('Info', text='内容')
    tree.column('Line', width=50, anchor='center')
    tree.column('Info', width=1000, anchor='w')
    tree.pack()


class App:
    def __init__(self, root):
        self.output_label = None
        self.tree = None
        self.entry_after = None
        self.entry_before = None
        self.root = root
        self.root.title("転換ツール　V1.0.0")
        self.create_widgets()

    def create_widgets(self):
        window_width = 800
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.root.configure(bg="#e0e0e0")
        # self.root.resizable(False, False)
        font_style = ('Arial', 10)

        frame_before = tk.Frame(self.root, bg="#e0e0e0")
        frame_before.pack(pady=15)

        label_before_text = tk.Label(frame_before, text="入力パ   ス：", font=font_style, bg="#e0e0e0")
        label_before_text.grid(row=0, column=0, padx=1)

        entry_before = tk.Entry(frame_before, width=50, font=font_style)
        entry_before.bind("<FocusOut>", on_leave)
        entry_before.grid(row=0, column=1, padx=15)

        browse_button_before = tk.Button(frame_before, text="入力選択", command=lambda: (
            clear_before_entry(), entry_before.insert(tk.END, filedialog.askopenfilename())), bg='#DDDDDD', fg='black',
                                         font=font_style)
        browse_button_before.grid(row=0, column=2, padx=(10, 30))

        frame_after = tk.Frame(self.root, bg="#e0e0e0")
        frame_after.pack(pady=15)

        label_after_text = tk.Label(frame_after, text="出力パ   ス：", font=font_style, bg="#e0e0e0")
        label_after_text.grid(row=0, column=0, padx=1)

        entry_after = tk.Entry(frame_after, width=50, font=font_style)
        entry_after.grid(row=0, column=1, padx=15)

        browse_button_after = tk.Button(frame_after, text="出力選択", command=lambda: (
            clear_after_entry(), entry_after.insert(tk.END, filedialog.askopenfilename())), bg='#DDDDDD', fg='black',
                                        font=font_style)
        browse_button_after.grid(row=0, column=2, padx=(10, 30))

        frame_button = tk.Frame(self.root, bg="#e0e0e0")
        frame_button.pack(pady=10)
        convert_button = tk.Button(frame_button, text="実行する", command=self.convert_text, bg='#2ECC40', fg="white",
                                   # relief=tk.FLAT,
                                   font=('Arial', 13))
        convert_button.pack(side=tk.LEFT, padx=(100, 10))

        exit_button = tk.Button(frame_button, text="退出する", command=exit_app, bg='#AAAAAA', fg="white",
                                # relief=tk.FLAT,
                                font=('Arial', 13))
        exit_button.pack()
        exit_button.pack(side=tk.LEFT, padx=(10, 50))

        list_button = tk.Button(frame_button, text="詳細内容", command=show_hidden_preview, bg='#e0e0e0',
                                relief=tk.FLAT,
                                font=font_style)
        list_button.pack(side=tk.RIGHT, padx=(0, 1))

        output_label = tk.Label(self.root, text="", bg="#e0e0e0", fg='black')
        output_label.pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True, fill='both')

        file_detail_tab = ttk.Frame(notebook)
        notebook.add(file_detail_tab, text='ファイル一覧')
        create_file_detail_treeview(file_detail_tab)

        result_detail_tab = ttk.Frame(notebook)
        notebook.add(result_detail_tab, text='結果内容')
        create_result_detail_treeview(result_detail_tab)

    def convert_text(self):
        input_file_path = self.entry_before.get()
        output_file_path = self.entry_after.get()
        try:
            with open(input_file_path, 'r') as file:
                input_text = file.read()
                converted_text = input_text.replace('a', 'A')
            with open(output_file_path, 'w') as file:
                file.write(converted_text)
                tmp = ['a',
                       'b']
                self.tree.insert('', 'end', values=tmp)
                # self.tree_scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
                # self.tree_scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
                # self.tree.configure(yscrollcommand=tree_scrollbary.set)
                # self.tree.configure(xscrollcommand=tree_scrollbarx.set)
                # self.tree.pack()
                self.output_label.config(text="転換成功！", fg="green", font=('Arial', 15))
        except FileNotFoundError:
            self.output_label.config(text="ファイルは見つかりません。", fg="red", font=('Arial', 15))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    # root.geometry("800*650")
    root.mainloop()
