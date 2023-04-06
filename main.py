from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os


def create_tree(directory):
    """
    Create a dictionary representation of the directory tree
    """
    tree = {'name': os.path.basename(directory)}
    if os.path.isdir(directory):
        tree['type'] = "directory"
        tree['children'] = [create_tree(os.path.join(
            directory, x)) for x in os.listdir(directory)]
    else:
        tree['type'] = "file"
    return tree


def print_gui_tree(tree, text_area, keyword='', indent=0):
    """
    Print the directory tree in GUI with nodes containing the keyword
    """
    if keyword.lower() in tree['name'].lower():
        text_area.insert(tk.END, ' ' * indent + '- ' +
                         tree['name'] + '/' if tree['type'] == 'directory' else ' ' * indent + '- ' + tree['name'] + '\n')
    if tree['type'] == 'directory':
        for child in tree['children']:
            print_gui_tree(child, text_area, keyword, indent=indent+2)


def clear(entry):
    entry.delete(0, tk.END)


def open_directory_dialog(root, text_area, entry, search_button):
    entry.config(state='normal')  # enable entry widget
    search_button.config(state='normal')  # enable search button
    directory = filedialog.askdirectory(parent=root)
    if not directory:
        print("No directory selected")
        return

    if not os.path.isdir(directory):
        print("Error: Invalid directory path")
        return

    # print new directory tree
    tree = create_tree(directory)

    # clear text area and insert new directory tree
    text_area.delete(1.0, tk.END)
    print_gui_tree(tree, text_area)


def search_directory(entry, text_area):
    """
    Search the current directory tree for a keyword and print the results
    """
    text_area.delete(1.0, tk.END)   # clear the text area

    # get the current directory tree
    directory = filedialog.askdirectory()
    if not directory:
        print("No directory selected")
        return

    if not os.path.isdir(directory):
        print("Error: Invalid directory path")
        return

    tree = create_tree(directory)

    # get the keyword from the entry widget
    keyword = entry.get()

    # print the directory tree with matching nodes
    print_gui_tree(tree, text_area, keyword)


def main():
    root = tk.Tk()
    root.style = ttk.Style()  # type: ignore
    root.style.theme_use("vista")  # type: ignore
    root.title("Directory Tree Generator")

    # Create text area and scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_area = Text(root, yscrollcommand=scrollbar.set)
    text_area.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=text_area.yview)

    # Create entry widget
    entry = ttk.Entry(root, width=30)
    entry.insert(0, "Enter keyword(s) here")
    entry.bind("<FocusIn>", lambda args: entry.delete('0', 'end'))
    entry.pack(side=LEFT, padx=5, pady=5, fill=X)

    # Create search button
    search_button = ttk.Button(
        text="Search Directory", command=lambda: search_directory(entry, text_area))
    search_button.pack(side=LEFT, pady=5)

    # Button to clear input
    clear_input = ttk.Button(
        root, text="Clear", command=lambda: clear(entry))
    clear_input.pack(side=LEFT)

    root.mainloop()


if __name__ == '__main__':
    main()
