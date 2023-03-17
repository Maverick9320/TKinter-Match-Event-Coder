import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

df = pd.DataFrame(columns=['Col1', 'Col2'], data=[[1, 2], [3, 4]])

class MyGui:

    def __init__(self):

        #initialize and configure the window
        self.root = tk.Tk()
        self.root.geometry('800x900')
        self.root.title('Rugby Event Coder')
        self.root.resizable(False, False)
        self.root.iconbitmap("rugby-ball.ico")

        # text box for the output file name
        self.file_name = tk.Entry(self.root)
        self.file_name.place(x=120, y=10)

        self.file_name_label = tk.Label(self.root, text='Output File Name:')
        self.file_name_label.place(x=10, y=10)

        # frame to allow the choice of possible file extensions
        self.extensions_frame = tk.Frame(self.root)
        self.extensions_frame.columnconfigure(0, weight=1)
        self.extensions_frame.columnconfigure(1, weight=1)

        self.csv_state = tk.IntVar()
        self.extension_check_csv = tk.Checkbutton(self.extensions_frame, text='.csv', variable=self.csv_state)
        self.extension_check_csv.grid(row=0, column=0)

        self.json_state = tk.IntVar()
        self.extension_check_json = tk.Checkbutton(self.extensions_frame, text='.json', variable=self.json_state)
        self.extension_check_json.grid(row=0, column=1)

        #button to save file(s)
        self.button = tk.Button(self.root, text='Save Data', command=self.save_files)
        self.button.place(x=730, y=10)

        #separators
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.place(relx=0.01, rely=0.07, relwidth=0.98, relheight=1)

        self.extensions_frame.place(x=120, y=30)

        #radiobuttons for player numbers
        self.radiobutton_state = tk.IntVar()

        self.number_frame_home = tk.Frame(self.root)
        self.number_frame_home.columnconfigure(0, weight=1)        

        for x in range(23):
            ttk.Radiobutton(self.number_frame_home, text=str(x+1), variable=self.radiobutton_state, value=x+1, command=self.selected_color).grid(row=x, column=0, ipady=5.5)
        self.number_frame_home.place(x=15, y=100)

        self.number_frame_away = tk.Frame(self.root)
        self.number_frame_away.columnconfigure(0, weight=1)

        for x in range(23):
            ttk.Radiobutton(self.number_frame_away, text=str(x+1), variable=self.radiobutton_state, value=(x+1)*-1, command=self.selected_color).grid(row=x, column=0, ipady=5.5)
        self.number_frame_away.place(x=120, y=100)

        #selection
        self.selection = tk.Label(text='H: #00', font=('Segoe UI', 25, 'Roman'))
        self.selection.place(x=680, y=75)

        #root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def selected_color(self):
        multiplier=1
        string = ''

        if self.radiobutton_state.get() >= 0:
            string += 'H: #'
        else:
            string += 'A: #'
            multiplier *= -1

        try:
            self.selection.destroy()
        except:
            pass
        
        num = str(self.radiobutton_state.get()*multiplier)
        if len(num) == 1:
            string += '0'
        
        string += num

        self.selection = tk.Label(text=string, font=('Segoe UI', 25))
        self.selection.place(x=680, y=75)

    #error messages
    def file_nameError(self):
        #error message for if the file_name entry has been left blank
        messagebox.showerror(title='Input A File Name', message='File Name Cannot Be Left Blank')

    def extensionError(self):
        #error message for if no file extensions have been checked
        messagebox.showerror(title='Choose A File Extension', message='Choose At Least One File Extension')

    #function for the save files button
    def save_files(self):
        file_name = self.file_name.get()

        if file_name == '':
            self.file_nameError()
        if self.csv_state.get() == 1 and file_name != '':
            df.to_csv(file_name+'.csv', index=False)
        if self.json_state.get() == 1 and file_name != '':
            print(True)
            df.to_csv(file_name+'.json', index=False)
        if self.json_state.get() == 0 and self.csv_state.get() == 0:
            self.extensionError()

    def shortcut(self, event):
        if event.state == 4 and event.keysym == 'Return':
            self.show_message()

    #function for when the close button is clicked
    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Are you sure that you want to close the program?'):
            self.root.destroy()

MyGui()