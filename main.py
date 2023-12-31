import os
from datetime import date
import sqlite3
from kivy.app import StringProperty
from settingsjson import settings_json
from kivy.config import Config
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', '1')
Config.set('graphics','fullscreen','0')

# Import kivy requirements and KivyMD
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.settings import ScrollView, SettingOptions
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout

from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.list import IRightBodyTouch, IconRightWidget, MDList, TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton, MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivy import platform

if platform == "android":
    from android.permissions import request_permissions, Permission
    from android.activity import bind
    from android import activity
    # request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
    #                      Permission.READ_EXTERNAL_STORAGE])
    from android.storage import primary_external_storage_path
#==========================================================================#
#****************************** Variables *********************************#
#==========================================================================#
# variables that I want to initalize when program starts
screen_manager = ObjectProperty()
global file_save_path
file_save_path = "/home/rcjk/Videos/"
service_store = '/carApp/maintenance.json'
vehicle_store = '/carApp/vehicle.json'
mileage_store = '/carApp/miles.json'


#==========================================================================#
#*********************** Class Global Variables ***************************#
#==========================================================================#
class GlobalVar():
    miles = 0
    car_num = 0
    # results = ["Enter more recent data","Enter more recent data","Enter more recent data"]
    # flag = False
    # Hold date of service, set to today
    service_date = date.today()



    # Default save path
    file_save_path = '/home/rcjk/Videos/'
    # Json variables
    notes_store = f'{file_save_path}'

#==========================================================================#
#******************************* Classes **********************************#
#==========================================================================#

#==========================================================================#
# Class HomeScreen is a subclass of Screen
# __init__: Initalize the SQL connections
# on_enter: Set the label to todays date
#==========================================================================#

class HomeScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.connection = sqlite3.connect(f"{file_save_path}/carApp/carTracker.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars(vehicle TEXT, service TEXT, mileage INTEGER, date TEXT)")

    def on_enter(self):

        try:
            self.ids.date_label.text = str(GlobalVar.service_date)
        except:
            pass


    def service_list(self):

        self.service_save = JsonStore((f'{file_save_path}{service_store}'))

        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_service(x),
            } for i in (self.service_save).keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_service,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


    def car_list(self):

        self.vehicle_save = JsonStore((f'{file_save_path}{vehicle_store}'))

        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_vehicle(x),
            } for i in  (self.vehicle_save).keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_vehicle,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


    def set_service(self, text_item):
        self.ids.get_service.text = text_item
        self.menu.dismiss()

    def set_vehicle(self, text_vehicle):
        self.ids.get_vehicle.text = text_vehicle
        self.menu.dismiss()

    def open_snackbar(self):
        MDSnackbar(
            MDLabel(
                text="Saving Mileage",
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()

        #CALENDAR SECTION

    def on_save(self, instance, value, date_range):
            '''
            Events called when the "OK" dialog box button is clicked.

            :type instance: <kivymd.uix.picker.MDDatePicker object>;
            :param value: selected date;
            :type value: <class 'datetime.date'>;
            :param date_range: list of 'datetime.date' objects in the selected range;
            :type date_range: <class 'list'>;
            '''
            GlobalVar.service_date = value
            self.ids.date_label.text = str(value)
            print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


    def send_information(self):

        if (self.ids.get_vehicle.text != "Select Vehicle" and
            self.ids.mileage.text != "" and self.ids.date_label.text != ""):

            service = self.ids.get_service.text
            vehicle = self.ids.get_vehicle.text
            miles = self.ids.mileage.text
            dateValue = self.ids.date_label.text

            self.cursor.execute("INSERT INTO cars VALUES(?,?,?,?)",(vehicle, service, miles, dateValue))
            rows = self.cursor.execute("SELECT vehicle, service, mileage, date FROM cars").fetchall()
            print(rows)
            self.ids.mileage.error = False
            self.open_snackbar()

        elif self.ids.date_label.text != "":
            self.ids.date_label.text = "Enter a Date"

        else:
            self.ids.mileage.error = True

        self.connection.commit()

class ViewMileage(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.vehicle_list = []

        for cars in JsonStore((f'{file_save_path}{vehicle_store}')):
            self.vehicle_list.append(cars)

        self.connection = sqlite3.connect(f"{file_save_path}/carApp/carTracker.db")
        self.cursor = self.connection.cursor()

        self.rows = self.cursor.execute("SELECT vehicle, mileage, date FROM cars").fetchall()

       # self.filter_rows = self.cursor.execute("SELECT vehicle, service, mileage, date FROM cars WHERE vehicle = ?",("",),).fetchall()
        print(self.rows)

    def on_enter(self):

        self.__init__()
        self.setup_table(self.rows)


    def setup_table(self, data):
        data_tables = MDDataTable(
            size_hint=(1, 0.6),
            use_pagination=True,
            column_data=[
                ("", dp(1)),
                ("Vehicle", dp(30), self.sort_on_col_2),
                ("Mileage", dp(30)),
               # ("Service", dp(30)),
                ("Date", dp(50), self.sort_on_col_3),
            ],
            row_data=[
                # The number of elements must match the length
                # of the `column_data` list.
                ("",f"{i[0]}",f"{i[1]}",f"{i[2]}") for i in data ],
        )
        self.ids.box2.add_widget(data_tables)

    def sort_on_col_3(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][3]
            )
        )

    def sort_on_col_2(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][-1]
            )
        )

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    def load_data(self):

        print("loaded car")

    def on_leave(self):
        # for count in self.vehicle_list:
        self.ids.box1.remove_widget(self.ids.box1.children[0])
        self.ids.box2.remove_widget(self.ids.box2.children[0])

    def set_vehicle(self, text_vehicle):
        self.ids.get_vehicle.text = text_vehicle
        self.filter_rows = self.cursor.execute("SELECT vehicle, mileage, date FROM cars WHERE vehicle = ?",(text_vehicle,),).fetchall()
        self.ids.box2.remove_widget(self.ids.box2.children[0])
        self.setup_table(self.filter_rows)
        self.menu.dismiss()

    def car_list(self):
        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_vehicle(x),
            } for i in  self.vehicle_list
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_vehicle,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


class ViewService(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.vehicle_list = []

        for cars in JsonStore((f'{file_save_path}{vehicle_store}')):
            self.vehicle_list.append(cars)

        self.connection = sqlite3.connect(f"{file_save_path}/carApp/carTracker.db")
        self.cursor = self.connection.cursor()

        self.rows = self.cursor.execute("SELECT vehicle, service, mileage, date FROM cars").fetchall()

        self.filter_rows = self.cursor.execute("SELECT vehicle, service, mileage, date FROM cars WHERE service !='Select Service'",).fetchall()
        print(self.filter_rows)

    def on_enter(self):

        self.__init__()
        self.setup_table(self.filter_rows)


    def setup_table(self, data):
        data_tables = MDDataTable(
            size_hint=(1, 0.6),
            use_pagination=True,
            column_data=[
                ("", dp(1)),
                ("Vehicle", dp(30), self.sort_on_col_2),
                ("Mileage", dp(30)),
                ("Service", dp(30)),
                ("Date", dp(50), self.sort_on_col_3),
            ],
            row_data=[
                # The number of elements must match the length
                # of the `column_data` list.
                ("",f"{i[0]}",f"{i[2]}",f"{i[1]}",f"{i[3]}") for i in data ],
        )
        self.ids.box2.add_widget(data_tables)
        print("DING DONG")

    def sort_on_col_3(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][3]
            )
        )

    def sort_on_col_2(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: l[1][-1]
            )
        )

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    def load_data(self):

        print("loaded car")

    def on_leave(self):
        self.ids.box1.remove_widget(self.ids.box1.children[0])
        self.ids.box2.remove_widget(self.ids.box2.children[0])

    def set_vehicle(self, text_vehicle):
        self.ids.get_vehicle.text = text_vehicle
        self.filter_rows = self.cursor.execute("SELECT vehicle, service, mileage, date FROM cars WHERE vehicle = ?",(text_vehicle,),).fetchall()
        self.ids.box2.remove_widget(self.ids.box2.children[0])
        self.setup_table(self.filter_rows)
        self.menu.dismiss()

    def car_list(self):
        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_vehicle(x),
            } for i in  self.vehicle_list
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_vehicle,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


class SetUpAlerts(Screen):
    pass

class AddRemoveVehicle(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.vehicle_save = JsonStore((f'{file_save_path}{vehicle_store}'))

    def add_vehicle(self):

        if self.ids.vehicle.text != "":
            self.vehicle_save.put(self.ids.vehicle.text)
            self.ids.vehicle.error = False
        else:
            self.ids.vehicle.error = True

    def load_vehicle(self):

        try:

            for count in self.vehicle_save.keys():
               self.ids.car_menu.remove_widget(
               self.ids.car_menu.children[0])

        except:
            pass

        for vehicles in self.vehicle_save.keys():
            print(vehicles)
            self.ids.car_menu.add_widget(
                TwoLineAvatarIconListItem(
                    MinusSign(
                        MDIconButton(
                            icon = "minus",
                            ),
                        ),
                    text = f"{vehicles}",
                    )
                                                )

    def add_notes(self):

        if self.ids.vehicle.text != "":
            if self.ids.note.text == "":
               self.ids.note.helper_text = "Enter a note to record"
               self.ids.note.error = True
            else:
                note_location = f'{GlobalVar.file_save_path}/data/{self.ids.vehicle.text}_notes.json'
                JsonStore(note_location).put(self.ids.note.text, car = self.ids.vehicle.text)
                self.ids.note.error = False
        else:
            self.ids.note.helper_text = "Please enter a vehicle to add note to"
            self.ids.note.error = True

    def clear_screen(self):
        self.ids.vehicle.text = ""
        self.ids.note.text = ""


class MinusSign(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class AddRemoveService(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.service_save = JsonStore((f'{file_save_path}{service_store}'))


    def load_service_items(self):

        serviceList = ThreeLineAvatarIconListItem
        i = 0
        j = 0
        value1 = ""
        value2 = ""

        try:

            for count in self.service_save.keys():
               self.ids.scroll.remove_widget(
               self.ids.scroll.children[0])

        except:
            pass

        for service_items in self.service_save.keys():
            for interval in self.service_save.get(service_items):
                if j == 0:
                    value1 = (self.service_save.get(service_items)[interval])
                    j = 1


                else:
                    value2 = (self.service_save.get(service_items)[interval])
                    if value2 == "":
                        value2 = "N/A"
                    j = 0

                    self.ids.scroll.add_widget(
                        serviceList(
                            MinusSign(
                                IconRightWidget(
                                    icon = "minus",
                                    on_release= lambda x: self.trash(x.parent)
                                    ),
                                ),
                            text = f"{service_items}",
                            secondary_text = f"{value1} miles",
                            tertiary_text = f"{value2} months"
                             )
                                                        )

    def trash(self, thing):
        print(thing)
        print(thing.parent)
        self.ids.service_box.remove_widget(thing)

    def add_service(self):

        if self.ids.service.text != "" and self.ids.interval_miles.text != "":
            self.service_save.put(self.ids.service.text,
                                  interval_mileage = self.ids.interval_miles.text,
                                  interval_month = self.ids.interval_months.text)
            self.ids.service.error = False
            self.ids.service.error = False
        else:
            self.ids.service.error = True
            self.ids.interval_miles.error = True

class Setting(Screen):
    pass

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

# Build the app

class MyApp(MDApp):


    def build(self):

        global file_save_path
        # if self.config.get("example", "light_dark") == 1:

        #     print(self.config.get("example", "light_dark"))
        #     self.theme_cls.theme_style="Dark" # Set dark theme

        # else:

        #     print(self.config.get("example", "light_dark"))
        #     self.theme_cls.theme_style="Light" # Set dark them

        self.theme_cls.primary_palette = self.config.get("example","color")
        self.theme_cls.primary_hue= self.config.get("example","hue")
        LabelBase.register(name='Hack',
                           fn_regular='Hack-Bold.ttf')
        LabelBase.register(name='Domestic',
                           fn_regular='Domestic_Manners.ttf')
        # Custom Settings Menu
        self.options
        self.use_kivy_settings = False
        if platform == "android":
            self.request_permission()
            file_save_path = str(primary_external_storage_path())
            print(file_save_path)
            os.makedirs(f'{file_save_path}/carApp', exist_ok=True)

        else:
            file_save_path = (self.config.get("example", "path"))
            os.makedirs(f'{file_save_path}/carApp', exist_ok=True)


        # try:
        #     file_location = (self.config.get("example", "path") + '/data/maintenance.json')
        #     mkdir(f'{file_save_path}/data')
        # except:
        #     pass
        # print(file_location)
        # GlobalVar.service_store = JsonStore(file_location)
        my_string = StringProperty('')
        # setting = self.config.get('example', 'boolexample')
        KV = Builder.load_file('window_3.kv')
        return KV

    # Section to build the custom settings menu
    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'color': 'Green',
            'path': 'json/maintenance.json'})

    def build_settings(self, settings):
        settings.add_json_panel('Panel Name',
                                self.config,
                                data=settings_json)


    def on_config_change(self, config, section,
                         key, value):
        self.theme_cls.primary_palette = self.config.get("example","color")
        self.theme_cls.primary_hue= self.config.get("example","hue")
        file_save_path = self.config.get("example","path")
        os.makedirs(f'{file_save_path}/carApp', exist_ok=True)
        # if self.config.get("example", "light_dark") == 1:

        #     print(self.config.get("example", "light_dark"))
        #     self.theme_cls.theme_style="Dark" # Set dark theme

        # else:

        #     print(self.config.get("example", "light_dark"))
        #     self.theme_cls.theme_style="Light" # Set dark them
    def request_permission(self, *args):
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        activity.bind(on_request_permissions=self.on_request_permissions)

    def on_request_permissions(self, permissions, results):
        if Permission.WRITE_EXTERNAL_STORAGE in permissions:
            if all(result for result in results):
                self.show_permission_granted_message()
        else:
            self.show_permission_denied_message()

    def show_permission_granted_message(self):
        print("WRITE_EXTERNAL_STORAGE permission granted!")

    def show_permission_denied_message(self):
        print("WRITE_EXTERNAL_STORAGE permission denied!")


if __name__ == '__main__':

    MyApp().run()
