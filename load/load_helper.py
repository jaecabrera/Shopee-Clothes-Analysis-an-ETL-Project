import pandas
import pathlib
from dataclasses import dataclass
from datetime import datetime
import os
pandas.set_option('display.max_columns', 10)


@dataclass
class LoadHelper:
    filepath: str
    date: str

    def data_directory(self):
        try:
            for dirname, _, filenames in os.walk(self.filepath):
                for filename in filenames:

                    if os.path.join(filename).endswith('.csv'):
                        yield str(os.path.join(filename))

                    if os.path.join(filename).endswith('.json'):
                        yield str(os.path.join(filename))

        except NotADirectoryError:
            return print("The directory does not exist.")

        except PermissionError:
            return print("The directory is in read-only")

    def time(self):
        today = datetime.now()
        today_format = today.strftime('%Y-%m-%d')
        self.date = today_format

        return self.date

    def load_frame(self):
        filepath = pathlib.PureWindowsPath(str(self.filepath) + '\\' + self.date)
        data = pandas.read_csv(filepath)

        return data

# df = LoadHelper(filepath='../extracted_files', date=None)
# print([files for files in df.data_directory()])
