# Current Available Settings
# | added: 7/6/2021 |save_directory setting -> will contain all clean data
# | added: 7/6/2021 | input_directory setting -> contains all the unclean data
# ---------------------------------------------------------
import re
from dataclasses import dataclass, field


@dataclass
class ShopeeIO:
    settings: field()

    def read_setting(self):
        """
        :param self:
        :return: line read from .txt
        """
        with open('settings.txt', 'r') as file_read:
            self.settings = list(file_read.readlines())
        file_read.close()
        return self.settings

        # Check for user input settings

    def check_setting(self):
        """
        :param self:
        :return:
        """
        def get_values():
            """Get setting input"""
            return re.split(' = ', items)[1]

        for items in self.settings:

            # Save directory setting | added: 7/6/2021
            if items.__contains__('SAVE_DIRECTORY'):
                save_dir = get_values()

            # Output Directory Setting | added: 7/6/2021
            if items.__contains__('INPUT_FILE_DIRECTORY'):
                input_dir = get_values()

        io_setting = {
            'save_dir': save_dir,
            'input_dir': input_dir}

        return io_setting
