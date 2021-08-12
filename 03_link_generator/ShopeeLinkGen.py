import PySimpleGUI as sg
import pandas as pd
from GeneratorHelp import ShopeeScrape
from dataclasses import dataclass
from datetime import datetime
TODAY = datetime.now().strftime("%Y-%m-%d")


@dataclass
class EventsFunc:

    @staticmethod
    def export():
        """
        Compiles URL to navigate scraper
        """
        export_data = pd.DataFrame()
        export_data['product_itemid'] = data.product_itemid
        export_data['product_shopid'] = data.product_shopid
        export_data['product_links'] = product_link
        export_data['shop_review_links'] = review_links
        export_data['image_links'] = image_links
        export_data['shop_profile_links'] = shop_profile_links
        filename = f'{TODAY}_links(BASE).csv'
        return export_data.to_csv('../generated_links/' + filename)

# Event Object
eventfunc = EventsFunc()

# GUI Theme
sg.theme('DarkRed2')

# Window Layout
layout = [
    [sg.Text('Flat Filepath: ', size=(10, 1), auto_size_text=False, justification='left'),
     sg.InputText(''), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
    [sg.Button('Export Links')],
]

# Window
window = sg.Window('Shopee - Link Generator',
          layout,
          size=(500, 90),
          icon='gen.ico')

# Event Loop
while True:

    # Read User Events & Values
    event, values = window.read()

    # Create ShopeeScrape Object
    shs = ShopeeScrape(
        product_link='https://shopee.ph/',
        review_link='https://shopee.ph/api/v2/item/',
        image_link='https://cf.shopee.ph/file/',
        shop_link='https://shopee.ph/api/v4/product/get_shop_info?shopid=',
    )

    # Browsed & Read File
    try:
        if (event == 'Browse') is not None:
            data = pd.read_csv(values['Browse'], sep=',', engine='python')
    except ValueError:
        break

    except FileNotFoundError:
        data_not_found = sg.popup_error('File not Found')
        continue

    except PermissionError:
        sg.popup_error('File is in Use, Try Again')
        continue

    # Product Links

    if event == 'Export Links':

        product_link = shs.get_product(
            name=data.product_name,
            shop=data.product_shopid,
            product=data.product_itemid)

        image_links = shs.get_image(
            image_code=data.product_image_variation)

        review_links = shs.get_review(
            shop=data.product_shopid,
            product=data.product_itemid)

        shop_profile_links = shs.get_shop_profile_link(
            shop=data.product_shopid)

        try:
            eventfunc.export()
            sg.popup_auto_close('Links Done')

        except PermissionError:
            sg.popup_error('File is in use. Try Again.')

    # Event Close
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
            'Do you really want to quit?') == 'Yes':
        break

    window.close()
