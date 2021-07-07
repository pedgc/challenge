import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class App():
    def __init__(self):
        # super().__init__()
        pass

        # root window
        window = ThemedTk(theme="arc")
        window.title('Theme Demo')
        window.geometry('400x300')
        window.style = ttk.Style(self)

        # label
        label = ttk.Label(window, text='Name:')
        label.grid(column=0, row=0, padx=10, pady=10,  sticky='w')
        # entry
        textbox = ttk.Entry(window)
        textbox.grid(column=1, row=0, padx=10, pady=10,  sticky='w')
        # button
        btn = ttk.Button(window, text='Show')
        btn.grid(column=2, row=0, padx=10, pady=10,  sticky='w')

        # radio button
        window.selected_theme = ttk.StringVar()
        theme_frame = ttk.LabelFrame(self, text='Themes')
        theme_frame.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky='w')

        for theme_name in window.style.theme_names():
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                variable=window.selected_theme,
                command=window.change_theme)
            rb.pack(expand=True, fill='both')

    def change_theme(self):
        window.style.theme_use(window.selected_theme.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()
