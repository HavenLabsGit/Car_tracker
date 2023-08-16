from kivy import config
from car_query import Write_to_db
from maintenance import Maintenance
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
from kivy.uix.settings import ScrollView, SettingsWithSidebar

from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView

#==========================================================================#
#****************************** Variables *********************************#
#==========================================================================#

screen_manager = ObjectProperty()
# Globals
class GlobalVar():
    miles = 0
    car_num = 0
    results = ["Enter more recent data","Enter more recent data","Enter more recent data"]
    # list of vehicles I want to track
    vehicles = ("Honda", "Tundra", "T-100")
    vehicle = "car"
    flag = False
    service = "mileage"

#==========================================================================#
#****************************** Functions *********************************#
#==========================================================================#

def initalize_list(x):
    init_list = Write_to_db()
    tester = init_list.build_query(x)
    return tester
#
#==========================================================================#
#******************************* Classes **********************************#
#==========================================================================#

class HomeScreen(Screen):

    #initialize class
    write_car = Write_to_db()
    red = (0.96, 0.43, 0.01, 0.5)
    green = (0.29, 0.67, 0.31)
    # Function called when check box is clicked

    def on_checkbox_active(self, checkbox, value):
        if value:
            GlobalVar.flag = True
            print('The checkbox is ' + str(GlobalVar.flag))
        else:
            GlobalVar.flag = False
            print('The checkbox is ' + str(GlobalVar.flag))

    def service_list(self):
        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in Maintenance
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_service,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


    def car_list(self):
        menu_items = [
            {
                "text":f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in Maintenance
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.get_vehicle,
            items=menu_items,
            width_mult=4,
            border_margin=dp(24)
        )

        self.menu.open()


    def set_item(self, text__item):
        self.ids.label_service.text = text__item
        GlobalVar.service = self.ids.label_service.text
        self.menu.dismiss()

    # /* Name: selected_tundra
#  * Parameter: none
#  * Return: none
#  * Description: Changes the button color when selected. Also sets the variable tundra true for writing to correct field
#  */

    def selected_tundra(self):

        self.ids.tundra.md_bg_color = self.red
        self.ids.t100.md_bg_color = self.green
        self.ids.honda.md_bg_color = self.green
        GlobalVar.vehicle = "Tundra"
        print(GlobalVar.vehicle)

    # /* Name: selected_t100
#  * Parameter: none
#  * Return: none
#  * Description: Changes the button color when selected. Also sets the variable tundra true for writing to correct field
#  */
    def selected_t100(self):

        self.ids.tundra.md_bg_color = self.green
        self.ids.t100.md_bg_color = self.red
        self.ids.honda.md_bg_color = self.green
        GlobalVar.vehicle = "T-100"
        print(GlobalVar.vehicle)


    # /* Name: selected_honda
#  * Parameter: none
#  * Return: none
#  * Description: Changes the button color when selected. Also sets the variable tundra true for writing to correct field
#  */
    def selected_honda(self):

        self.ids.tundra.md_bg_color = self.green
        self.ids.t100.md_bg_color = self.green
        self.ids.honda.md_bg_color = self.red
        GlobalVar.vehicle = "Honda"
        print(GlobalVar.vehicle)

    # /* Name: send_miles
#  * Parameter: none
#  * Return: none
#  * Description: reads the test box value and send to the database
#  */
    def send_miles(self):

        write_car = Write_to_db() # Initalize object
        GlobalVar.miles = self.ids.mileage.text # Load test input into variable miles

        # Error handling if text field is blank or vehicle is not selected
        try:
             x = self.set_mileage()  # Figure out which vehicle we want to write mileage for
             GlobalVar.results[x] = str(GlobalVar.miles) # write mileage
             write_car.write_influx(GlobalVar.vehicle, GlobalVar.service, GlobalVar.miles)  # influxdb query to write values to database.
             self.ids.mileage.error = False # If error message was present, clear it now

             MDSnackbar(
             MDLabel(
                 text="Wrote to database",
             ),
             y=dp(24),
             pos_hint={"center_x": 0.5},
             size_hint_x=0.5,
             ).open()

        # Uh oh, something went wrong!
        except:
            # set error message
            self.ids.mileage.error = True

    def set_mileage(self):
        if GlobalVar.vehicle == "Honda":
            self.value = 0
        elif GlobalVar.vehicle == "Tundra":
            self.value = 1
        elif GlobalVar.vehicle == "T-100":
            self.value = 2
        return self.value


        # /* Name: grab_mileage
    #  * Parameter: none
    #  * Return: none
    #  * Description: Pulls value from global list and sends information to the screen
    #  */


    def grab_mileage(self):

        try:
            self.manager.get_screen('information').ids.honda.text = "Honda " + str(GlobalVar.results[0]) + " miles"
        except:
            self.manager.get_screen('information').ids.honda.text = "Enter more recent data"
        try:
            self.manager.get_screen('information').ids.tundra.text = "Tundra " + str(GlobalVar.results[1]) + " miles"
        except:
            self.manager.get_screen('information').ids.tundra.text = "Enter more recent data"
        try:
            self.manager.get_screen('information').ids.t100.text = "T-100 " + str(GlobalVar.results[2]) + " miles"
        except:
            self.manager.get_screen('information').ids.t100.text = "Enter more recent data"

    def open_snackbar(self):
        MDSnackbar(
            MDLabel(
                text="Saving Mileage",
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()

class ViewMileage(Screen):
    pass

class ViewService(Screen):
    pass

class SetUpAlerts(Screen):
    pass

class AddRemoveVehicle(Screen):
    pass

class AddRemoveService(Screen):
    pass

class Setting(Screen):
    pass

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

# Build the app

class MyApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = self.config.get("example","color")
        LabelBase.register(name='Hack',
                           fn_regular='Hack-Bold.ttf')
        LabelBase.register(name='Domestic',
                           fn_regular='Domestic_Manners.ttf')
        # Custom Settings Menu
        self.theme_cls.accent_palette = "Red"
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        # setting = self.config.get('example', 'boolexample')
        KV = Builder.load_file('window_3.kv')
        return KV



    # Section to build the custom settings menu
    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'color': 'Green',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.add_json_panel('Panel Name',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        self.theme_cls.primary_palette = self.config.get("example","color")
        print(config, section, key, value)

    def on_checkbox_active(self, checkbox, value):
        if value:
            print(value)
            print('The checkbox', checkbox, 'is active', 'and', checkbox, 'state')
            self.theme_cls.theme_style="Dark" # Set dark theme
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox, 'state')
            print(value)
            self.theme_cls.theme_style="Light" # Set dark them

    for x in GlobalVar.vehicles:      # For how many vehilce
       results = initalize_list(GlobalVar.vehicles[GlobalVar.car_num])
       GlobalVar.results[GlobalVar.car_num] = str(results)
       GlobalVar.car_num+=1

if __name__ == '__main__':

    MyApp().run()
