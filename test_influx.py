#!/usr/bin/env python3
from kivy.metrics import dp

from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from datetime import date

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton

today = date.today()
store = JsonStore('json/hello.json')
service = JsonStore('json/maintenance.json')


service.put('oil change', interval = '3500', date = str(today))
service.put('transmission fluid',interval = '35000', date = str(today))
service.put('steering fluid',interval = '35000', date = str(today))
service.put('rotate tires',interval = '5000', date = str(today))
print(today)



# store.put('tito', name='Mathieu', org='kivy')
# store.put('tshirtman', name='Gabriel', age=27)

# # using the same index key erases all previously added key-value pairs
# store.put('tito', name='Mathieu', age=30)

# # get a value using a index key and key
# print('tito is', store.get('tito')['age'])

# # or guess the key/entry for a part of the key
# for item in store.find(name='Gabriel'):
#     print(f'tshirtmans index key is', item[0])
#     print(f'his key value pairs are', str(item[1]))


# def show_me(**kwargs):
#     print(kwargs)
#     for k,v in kwargs.items():
#         print(f'{k} = {v}')


# d1 = {'dog': 1, 'cat': 2, 'mouse': 3}

# print('\nPass a dictionary as keywords')
# show_me(**d1)

# print('\nPass Keywords')
# show_me(box=4, fox=5, eggs=6)

# store = JsonStore('json/test_1.json')
# store.put('color', red=1, white=2, blue=3)
# store.put('critters', **d1)
# print(f"\nstore.get('critters') = {store.get('critters')}")
 # for numbers in service.keys():
 #            self.lists.append(numbers)
 #            values = ''
 #            for k in service.get(numbers):
 #                values = (service.get(numbers)[k])
 #            print("Your", numbers, "is due at", values)





class Example(MDApp):
    data_tables = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        self.lists = []

        for numbers in service.keys():
            self.lists.append(numbers)
            print(self.lists[0])
            values = ''
            for k in service.get(numbers):
                values = (service.get(numbers)[k])
            print("Your", numbers, "is due at", values)



        layout = MDFloatLayout()  # root layout
        # Creating control buttons.
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Add row", "Remove row"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        # Create a table.
        self.data_tables = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=False,
            column_data=[
                ("Service", dp(30)),
                ("Interval", dp(40)),
            ],
            row_data=[("oil change", "2")]
        )
        # Adding a table and buttons to the toot layout.
        layout.add_widget(self.data_tables)
        layout.add_widget(button_box)

        return layout

    def on_button_press(self, instance_button: MDRaisedButton) -> None:
        '''Called when a control button is clicked.'''

        try:
            {
                "Add row": self.add_row,
                "Remove row": self.remove_row,
            }[instance_button.text]()
        except KeyError:
            pass

    def add_row(self) -> None:
        # last_num_row = int(self.data_tables.row_data[-1][0])
        self.data_tables.add_row(("TEST", "3"))

    def remove_row(self) -> None:
        if len(self.data_tables.row_data) > 1:
            self.data_tables.remove_row(self.data_tables.row_data[-1])


Example().run()
