import tkinter as tk
from tkinter import ttk, messagebox
from pandastable import Table
import pandas as pd
from functools import partial

class MainWindow:

    def __init__(self):
        self.df = pd.DataFrame(columns=['Player', 'Action', 'Team', 'Half', 'Index'], data=[])

        #initialize and configure the window
        self.root = tk.Tk()
        self.root.geometry('800x675')
        self.root.title('Rugby Event Coder')
        self.root.resizable(False, False)
        self.root.iconbitmap("rugby-ball.ico")

        # text box for the output file name
        self.file_name = tk.Entry(self.root)
        self.file_name.place(relx=0.17, rely=0.015)

        self.file_name_label = tk.Label(self.root, text='Output File Name:')
        self.file_name_label.place(relx=0.01, rely=0.015)

        # frame to allow the choice of possible file extensions
        self.extensions_frame = tk.Frame(self.root, bg='red')
        self.extensions_frame.columnconfigure(0, weight=1)
        self.extensions_frame.columnconfigure(1, weight=1)

        self.csv_state = tk.IntVar()
        self.extension_check_csv = tk.Checkbutton(self.extensions_frame, text='.csv', variable=self.csv_state, relief='groove')
        self.extension_check_csv.grid(row=0, column=0)

        self.json_state = tk.IntVar()
        self.extension_check_json = tk.Checkbutton(self.extensions_frame, text='.json', variable=self.json_state, relief='groove')
        self.extension_check_json.grid(row=0, column=1)

        #button to save file(s)
        self.button = tk.Button(self.root, text='Save Data', command=self.save_files, relief='groove')
        self.button.place(relx=0.9, rely=0.015)

        #separators
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.place(relx=0.01, rely=0.09, relwidth=0.98, relheight=1)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.place(relx=0.17, rely=0.55, relwidth=0.815, relheight=1)

        self.extensions_frame.place(relx=0.17, rely=0.05)

        #radiobuttons for player numbers
        self.radiobutton_state = tk.IntVar()

        self.number_frame_home = tk.Frame(self.root)
        self.number_frame_home.columnconfigure(0, weight=1)        

        for x in range(23):
            ttk.Radiobutton(self.number_frame_home, text=str(x+1), variable=self.radiobutton_state, value=x+1, command=self.selected_player).grid(row=x, column=0)
        self.number_frame_home.place(relx=0.01, rely=0.1)

        self.number_frame_away = tk.Frame(self.root)
        self.number_frame_away.columnconfigure(0, weight=1)

        for x in range(23):
            ttk.Radiobutton(self.number_frame_away, text=str(x+1), variable=self.radiobutton_state, value=(x+1)*-1, command=self.selected_player).grid(row=x, column=0)
        self.number_frame_away.place(relx=0.1, rely=0.1)

        #selection
        self.selection = tk.Label(text='H: #00', font=('Segoe UI', 25))
        self.selection.place(x=10, y=600)

        #event buttons
        self.event_frame = tk.Frame(self.root)
        self.event_frame.columnconfigure(0, weight=1)

        self.high_tackle = tk.Button(self.event_frame, text='HIGH TACKLE', width=20, relief='groove', command=partial(self.log_event, 'HIGH TACKLE')).grid(row=0, column=0)
        self.low_tackle = tk.Button(self.event_frame, text='LOW TACKLE', width=20, relief='groove', command=partial(self.log_event, 'LOW TACKLE')).grid(row=1, column=0, pady=10)
        self.forward_carry = tk.Button(self.event_frame, text='FORWARD CARRY', width=20, relief='groove', command=partial(self.log_event, 'FORWARD CARRY')).grid(row=2, column=0)
        self.backward_carry = tk.Button(self.event_frame, text='BACKWARD CARRY', width=20, relief='groove', command=partial(self.log_event, 'BACKWARD CARRY')).grid(row=3, column=0, pady=10)
        self.def_ruck_arrival = tk.Button(self.event_frame, text='DEF. RUCK ARRIVAL', width=20, relief='groove', command=partial(self.log_event, 'DEF. RUCK ARRIVAL')).grid(row=4, column=0)
        self.off_ruck_arrival = tk.Button(self.event_frame, text='OFF. RUCK ARRIVAL', width=20, relief='groove', command=partial(self.log_event, 'OFF. RUCK ARRIVAL')).grid(row=5, column=0, pady=10)
        self.lineout_throw = tk.Button(self.event_frame, text='LINEOUT THROWN', width=20, relief='groove', command=partial(self.log_event, 'LINEOUT THROWN')).grid(row=6, column=0)
        self.lineout_claim = tk.Button(self.event_frame, text='LINEOUT CLAIMED', width=20, relief='groove', command=partial(self.log_event, 'LINEOUT CLAIMED')).grid(row=7, column=0, pady=10)
        
        self.turnover_won = tk.Button(self.event_frame, text='TURNOVER WON', width=20, relief='groove', command=partial(self.log_event, 'TURNOVER WON')).grid(row=0, column=1, padx=10)
        self.scrum_feed = tk.Button(self.event_frame, text='SCRUM FEED', width=20, relief='groove', command=partial(self.log_event, 'SCRUM FEED')).grid(row=1, column=1, padx=10)
        self.scrum_won = tk.Button(self.event_frame, text='SCRUM WON', width=20, relief='groove', command=partial(self.log_event, 'SCRUM WON')).grid(row=2, column=1, padx=10)
        self.pen_conc = tk.Button(self.event_frame, text='PENALTY CONCEDED', width=20, relief='groove', command=partial(self.log_event, 'PENALTY CONCEDED')).grid(row=3, column=1, padx=10)
        self.free_kick_conc = tk.Button(self.event_frame, text='FREEKICK CONCEDED', width=20, relief='groove', command=partial(self.log_event, 'FREEKICK CONCEDED')).grid(row=4, column=1, padx=10)
        self.ruck_pass = tk.Button(self.event_frame, text='RUCK PASS', width=20, relief='groove', command=partial(self.log_event, 'RUCK PASS')).grid(row=5, column=1, padx=10)
        self.succesful_pass = tk.Button(self.event_frame, text='SUCCESSFUL PASS', width=20, relief='groove', command=partial(self.log_event, 'SUCCESSFUL_PASS')).grid(row=6, column=1, padx=10)
        self.unsuccessful_pass = tk.Button(self.event_frame, text='UNSUCCESSFUL PASS', width=20, relief='groove', command=partial(self.log_event, 'UNSUCCESSFUL_PASS')).grid(row=7, column=1, padx=10)

        self.conv_scored = tk.Button(self.event_frame, text='CONVERSION SCORED', width=20, relief='groove', command=partial(self.log_event, 'CONVERSION SCORED')).grid(row=0, column=2)
        self.conv_missed = tk.Button(self.event_frame, text='CONVERSION MISSED', width=20, relief='groove', command=partial(self.log_event, 'CONVERSION MISSED')).grid(row=1, column=2, pady=10)
        self.pen_scored = tk.Button(self.event_frame, text='PENALTY SCORED', width=20, relief='groove', command=partial(self.log_event, 'PENALTY SCORED')).grid(row=2, column=2)
        self.pen_missed = tk.Button(self.event_frame, text='PENALTY MISSED', width=20, relief='groove', command=partial(self.log_event, 'PENALTY MISSED')).grid(row=3, column=2, pady=10)
        self.box_kick = tk.Button(self.event_frame, text='BOX KICK', width=20, relief='groove', command=partial(self.log_event, 'BOX KICK')).grid(row=4, column=2)
        self.yellow_card = tk.Button(self.event_frame, text='YELLOW CARD', width=20, relief='groove', command=partial(self.log_event, 'YELLOW CARD')).grid(row=5, column=2, pady=10)
        self.red_card = tk.Button(self.event_frame, text='RED CARD', width=20, relief='groove', command=partial(self.log_event, 'RED CARD')).grid(row=6, column=2)
        self.kick_off = tk.Button(self.event_frame, text='KICK OFF', width=20, relief='groove', command=partial(self.log_event, 'KICK OFF')).grid(row=7, column=2)

        self.aerial_con = tk.Button(self.event_frame, text='AERIAL CONTESTED', width=20, relief='groove', command=partial(self.log_event, 'AERIAL CONTESTED')).grid(row=0, column=3)
        self.aerial_won = tk.Button(self.event_frame, text='AERIAL WON', width=20, relief='groove', command=partial(self.log_event, 'AERIAL WON')).grid(row=1, column=3, pady=10)
        self.touch_missed = tk.Button(self.event_frame, text='TOUCH MISSED', width=20, relief='groove', command=partial(self.log_event, 'TOUCH MISSED')).grid(row=2, column=3)
        self.touch_found = tk.Button(self.event_frame, text='TOUCH FOUND', width=20, relief='groove', command=partial(self.log_event, 'TOUCH FOUND')).grid(row=3, column=3, pady=10)
        self.fifty_22 = tk.Button(self.event_frame, text='50-22', width=20, relief='groove', command=partial(self.log_event, '50-22')).grid(row=4, column=3)
        self.mark = tk.Button(self.event_frame, text='MARK CALLED', width=20, relief='groove', command=partial(self.log_event, 'MARK')).grid(row=5, column=3, pady=10)
        self.ko = tk.Button(self.event_frame, text='KNOCK ON', width=20, relief='groove', command=partial(self.log_event, 'KNOCK ON')).grid(row=7, column=3, padx=10)
        self.missed_tackle = tk.Button(self.event_frame, text='MISSED TACKLE', width=20, relief='groove', command=partial(self.log_event, 'MISSED TACKLE')).grid(row=6, column=3, padx=10)

        self.event_frame.place(relx=0.18, rely=0.12)

        self.delete_last_row = tk.Button(self.root, text=' ROW \n DELETE', relief='groove', command=self.delete_last_row, width=7, height=3)
        self.delete_last_row.place(relx=0.9, rely=0.6)
        self.clear_dataframe = tk.Button(self.root, text=' CLEAR ', relief='groove', command=self.clear_dataframe, width=7, height=3)
        self.clear_dataframe.place(relx=0.9, rely=0.7)


        self.pandasframe = tk.Frame(self.root)
        self.table = pt = Table(self.pandasframe, dataframe=self.df, showtoolbar=False, showstatusbar=False, rows=5, cols=3, width=520, height=200)
        pt.show()

        self.pandasframe.place(relx=0.17, rely=0.58)

        #root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def delete_last_row(self):
        self.df.drop(self.df.tail(1).index,inplace=True)
        self.pandasframe = tk.Frame(self.root)
        self.table = pt = Table(self.pandasframe, dataframe=self.df, showtoolbar=False, showstatusbar=False, rows=5, cols=3, width=520, height=200)
        pt.show()

        self.pandasframe.place(relx=0.17, rely=0.58)

    def clear_dataframe(self):
        if messagebox.askyesno(title='Clear?', message='Are You Sure That You Want To Clear The Dataframe?'):
            self.df = pd.DataFrame(columns=['Player', 'Action', 'Team', 'Half', 'Index'], data=[])
            self.pandasframe = tk.Frame(self.root)
            self.table = pt = Table(self.pandasframe, dataframe=self.df, showtoolbar=False, showstatusbar=False, rows=5, cols=3, width=520, height=200)
            pt.show()

            self.pandasframe.place(relx=0.17, rely=0.58)

    def selected_player(self):
        multiplier=1
        self.string = ''

        if self.radiobutton_state.get() >= 0:
            self.string += 'H: #'
        else:
            self.string += 'A: #'
            multiplier *= -1

        try:
            self.selection.destroy()
        except:
            pass
        
        num = str(self.radiobutton_state.get()*multiplier)
        if len(num) == 1:
            self.string += '0'
        
        self.string += num

        self.selection = tk.Label(text=self.string, font=('Segoe UI', 25))
        self.selection.place(x=10, y=600)

    def log_event(self, event):
        player_selected = False
        try:
            len(self.string)
            player_selected = True
        except:
            self.no_string()

        if player_selected == True:
            self.df.loc[len(self.df)] = {'Player': self.string, 'Action': event, 'Team': self.string[0], 'Half': 1, 'Index': len(self.df)}

            try:
                self.pandasframe.destroy()
            except:
                pass
            
            self.pandasframe = tk.Frame(self.root)
            self.table = pt = Table(self.pandasframe, dataframe=self.df[-9:], showtoolbar=False, showstatusbar=False, rows=9, cols=3, width=520, height=200)
            pt.show()

            self.pandasframe.place(relx=0.17, rely=0.58)

    def no_string(self):
        messagebox.showerror(title='Select A Player', message='A Player Must Be Selected')

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
            self.df.to_csv(file_name+'.csv', index=False)
        if self.json_state.get() == 1 and file_name != '':
            self.df.to_csv(file_name+'.json', index=False)
        if self.json_state.get() == 0 and self.csv_state.get() == 0:
            self.extensionError()

    #function for when the close button is clicked
    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Are you sure that you want to close the program?'):
            self.root.destroy()

        self.root.destroy()

MainWindow()