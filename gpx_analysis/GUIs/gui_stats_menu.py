"""
This script contains the playback menu sub frame class related to the tk GUI
The AppGUI class is the only one to use outside of this class
"""
# Pylint ignores
# pylint: disable=R0902
# pylint: disable=R0914

import tkinter as tk
from tkinter import ttk


class StatsMenuFrame:
    """
    This widget contains and abstracts the features of the stats menu
    """

    def __init__(self, parent_class):
        """
        Constructor for the StatsMenuFrame class

        :param parent_class: pass in the parent_class so we can access its window and
         other frames etc
        """
        self.__parent_class = parent_class
        self.__window = self.__parent_class.get_tk_window()

        # Create the surrounding frame
        self.__frm_stats_menu = None
        self.__frm_stats_menu = ttk.Frame(self.__window, relief=tk.RAISED, borderwidth=5)
        self.__frm_stats_menu.grid(row=1, column=0, sticky='nsew')
        self.__frm_stats_menu.grid_columnconfigure(0, weight=1)  # center it

        # Create the stats menu widgets
        # Create the title
        label_stats_menu = ttk.Label(master=self.__frm_stats_menu,
                                     text="Statistics Menu",
                                     font=('Minion Pro', 14, 'bold'))
        label_stats_menu.grid(row=0, column=0, sticky='s')
        self.__frm_stats_menu.rowconfigure(1, minsize=20)

        # Create a dropdown speed units menu
        self.__frm_stats_dropdown = None
        self.__value_speed_selected_option = None  # this is the value of the units
        self.__create_units_menu()

        # Create the checklist
        options = ['BoatA', 'BoatB', 'BoatC']
        self.__menu_choices = None
        self.__menubutton = None
        self.__menu = None
        self.__create_athlete_selection_menu(options)

        # Space in the grid
        self.__frm_stats_menu.rowconfigure(4, minsize=20)

        # Big label below to show all the stats
        test_data = {'Canford': {'dist': 1000000, 'spd': '1:53.2 s/500m', 'cad': 38},
                     'Winchester': {'dist': 900, 'spd': '1:55.6 s/500m', 'cad': 40},
                     'Emmanuel': {'dist': 1001, 'spd': '1:53.2 s/500m', 'cad': 38},
                     'Kew House': {'dist': 901, 'spd': '1:55.6 s/500m', 'cad': 40},
                     'Bryanston': {'dist': 800, 'spd': '1:59.8 s/500m', 'cad': 28}}
        self.__label_stats_text = None
        self.display_text(test_data)

    def display_text(self, data_in: dict) -> None:
        """
        Displays the stats text

        :param data_in: A dictionary where boat display name is key and data is the value
        :return: None
        """
        # Get the length of the longest name

        # Sort the athletes by highest dist, dodgy insertion sort
        modified_data = []
        while len(data_in):
            max_dist = -1  # no distance will not be greater than this
            max_key = None
            for key, value in data_in.items():
                test_val = value['dist']
                if test_val > max_dist:
                    max_dist = test_val
                    max_key = key

            # Make sure athlete distance renders correctly
            if max_dist > 100000:
                # if its over 100,000m (unrealistic number) say its finished
                new_dist = 'FIN'
            else:
                new_dist = f'{max_dist}m'
            modified_data.append({'name': max_key, 'dist': new_dist,
                                  'spd': data_in[max_key]['spd'],
                                  'cad': data_in[max_key]['cad']})
            del data_in[max_key]

        disp_text = ''

        max_athlete_dist_len = max(len(i['dist']) for i in modified_data) + 2

        for position, athlete_data in enumerate(modified_data):
            # make it so all the data starts lining up after names
            athlete_name = athlete_data['name']
            athlete_dist = athlete_data['dist']
            athlete_spd = athlete_data['spd']
            athlete_cad = athlete_data['cad']

            disp_text += (f'{position + 1}. ' + athlete_name + '\n' + '   ' +
                          athlete_dist + ' ' * (max_athlete_dist_len - len(
                        athlete_dist)) + athlete_spd + '   ' + f'{athlete_cad}s/m')

            disp_text += '\n'  # so it starts on a new line

        self.__label_stats_text = ttk.Label(master=self.__frm_stats_menu, text=disp_text,
                                            font='Courier')
        self.__label_stats_text.grid(row=5, column=0, sticky='w')

    def __create_athlete_selection_menu(self, options) -> None:
        """
        Creates the athlete selection menu

        :param options: The options for the list
        :return: None
        """
        self.__menubutton = tk.Menubutton(self.__frm_stats_menu,
                                          text="Choose Which athletes to show:",
                                          indicatoron=True)
        self.__menu = tk.Menu(self.__menubutton, tearoff=False)
        self.__menubutton.configure(menu=self.__menu)
        self.__menubutton.grid(row=3, column=0, sticky='w')
        self.__menu_choices = {}

        for choice in options:
            self.__menu_choices[choice] = tk.IntVar(value=0)
            self.__menu.add_checkbutton(label=choice, variable=self.__menu_choices[choice],
                                        onvalue=1, offvalue=0, command=self.__on_athlete_change)

    def __create_units_menu(self) -> None:
        """
        Create the frame with a units dropdown and button to confirm

        :return: None
        """
        # Encapsulate dropdown and dropdown label in a frame
        self.__frm_stats_dropdown = ttk.Frame(self.__frm_stats_menu, relief=tk.FLAT, borderwidth=0)
        self.__frm_stats_dropdown.grid(row=2, column=0, sticky='nsew')

        # Create the dropdown menu
        speed_options = ['s/500m', 'm/s', 'kmh', 'mph']  # options for it

        self.__value_speed_selected_option = tk.StringVar()
        self.__value_speed_selected_option.set(speed_options[0])  # s/500m is default unit

        # This doesn't need to be an instance var since we won't modify it again
        speed_dropdown = tk.OptionMenu(self.__frm_stats_dropdown,
                                       self.__value_speed_selected_option,
                                       *speed_options,
                                       command=self.__on_speed_option_change)
        speed_dropdown.grid(row=0, column=1, sticky='nsew')

        # Create the label for it
        label_stats_speed_choice = ttk.Label(master=self.__frm_stats_dropdown,
                                             text="Choose Speed Units:     ")
        label_stats_speed_choice.grid(row=0, column=0)

    def __on_athlete_change(self, *args) -> None:
        """
        This gets called when an athlete gets selected or deselected
        in the dropdown checklist

        :param args: *args
        :return: None
        """

        # *args is never used in this function but pylint will be upset it's not used
        # Do some random stuff to it
        if args == 1:
            pass

        print('change')
        for key, value in self.__menu_choices.items():
            print(key, value.get())

    def __on_speed_option_change(self, *args) -> None:
        """
        Called when speed option changes

        :return: None
        """

        # *args is never used in this function but pylint will be upset it's not used
        # Do some random stuff to it
        if args == 1:
            pass

        value = self.__value_speed_selected_option.get()
        print(value)
