
import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Adjust Settings Here'},
    {'type': 'bool',
     'title': 'Set Light/Dark Mode',
     'desc': 'Toggle Light/Dark mode on and off',
     'section': 'example',
     'key': 'light_dark'},
    {'type': 'options',
     'title': 'Select Color',
     'desc': 'Choose from one of the options',
     'section': 'example',
     'key': 'color',
     'options': ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']},
    {'type': 'options',
     'title': 'Select Hue',
     'desc': 'Choose hue color',
     'section': 'example',
     'key': 'hue',
     'options': ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', 'A100', 'A200', 'A400', 'A700']},
    {'type': 'path',
     'title': 'Save Path',
     'desc': 'Location for saved information',
     'section': 'example',
     'key': 'path'}])
