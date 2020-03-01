import os
import re
import xlrd
import math
import components.event_object as event

from components.date_provider import DateProvider

EXCEL_HEADER_SCRAP = 3
EXCEL_DAY_LENGTH = 12
EXCEL_GROUP_COLUMN = 120
EXCEL_GROUP_SUBJECT_KIND_COLUMN = 121
EXCEL_GROUP_LOC_COLUMN = 123
EXCEL_TIMES = ['9:00-10:30', '10:40-12:10', '13:10-14:40', '14:50-16:20', '16:30-18:00', '18:10-19:40']

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

class ExcelWorker:
    def __init__(self, filename : str):
        self.workbook = xlrd.open_workbook(f'./files/data/{filename}')
        self.worksheet = self.workbook.sheet_by_index(0)
    
    def get_cell(self, i_index : int, j_index : int) -> str:
        return self.worksheet.cell(i_index - 1, j_index - 1).value

    def get_normalized_cell_data(self, i_index : int, j_index : int) -> [str]:
        cell_data = str(self.get_cell(i_index, j_index)).strip()
        result = re.findall(r'[\d,]*\d*\s*[н]*\s*[\D\s]*', cell_data, flags= re.IGNORECASE | re.DOTALL)

        return [item.strip() for item in result if item is not '']

    def get_row(self, column_index : int) -> [event.EventObject]:
        objects = []
        data = list(map(str.strip, self.get_normalized_cell_data(column_index, EXCEL_GROUP_COLUMN)))

        if any(data):
            location = self.get_cell(column_index, EXCEL_GROUP_LOC_COLUMN)
            if ExcelWorker.get_location(location) == 1:
                location = [item.strip() for item in re.split(r'[\n ]+', location.replace("В-78*", "")) if item is not '']

                for i in range(len(data)):
                    weeks = list(map(int, re.findall(r'\d+', data[i])))

                    if not any(weeks):
                        if (column_index - EXCEL_HEADER_SCRAP) % 2 == 0:
                            weeks = [i for i in range(2, 17, 2)]
                        else:
                            weeks = [i for i in range(1, 16, 2)]

                    data[i] = [item for item in re.split(r'[\d,]*\d*\s*[н]\s', data[i]) if item is not ''][0]
                    for week in weeks:
                        objects.append(event.EventObject(data[i], location[0], \
                                        ExcelWorker.get_double_time(column_index), self.get_subject_kind(column_index), \
                                            DateProvider.getDateFromWeek(2020, week, ExcelWorker.get_weekday(column_index))))
            else:
                location = str(int(location) if str(location).isdigit() else str(location))
                location = location.split("\n")
                for i in range(len(data)):
                    weeks = list(map(int, re.findall(r'\d+', data[i])))

                    if not any(weeks):
                        if (column_index - EXCEL_HEADER_SCRAP) % 2 == 0:
                            weeks = [i for i in range(2, 17, 2)]
                        else:
                            weeks = [i for i in range(1, 16, 2)]

                    data[i] = [item for item in re.split(r'[\d,]*\d*\s*[н]\s', data[i]) if item is not ''][0]
                    for week in weeks:
                        objects.append(event.EventObject(data[i], location[i], \
                                        ExcelWorker.get_double_time(column_index), self.get_subject_kind(column_index), \
                                            DateProvider.getDateFromWeek(2020, week, ExcelWorker.get_weekday(column_index))))

        return objects

    def get_subject_kind(self, column_index : int) -> int:
        kind = self.get_cell(column_index, EXCEL_GROUP_SUBJECT_KIND_COLUMN)

        if ExcelWorker.get_location(self.get_cell(column_index, EXCEL_GROUP_LOC_COLUMN)) == 1:
            return 3 if kind == "лаб" or kind == "лб" else 9
        else:
            return 4 if kind == "лаб" or kind == "лб" else 11

    @staticmethod
    def get_location(cl : str) -> int:
        cl = str(cl)
        return 1 if "В-78*" in cl else 0
        
    @staticmethod
    def get_double_number(column_index : int) -> int:
        column_index = column_index % EXCEL_DAY_LENGTH - EXCEL_HEADER_SCRAP
        double_number = normal_round(column_index / 2)

        return double_number

    @staticmethod
    def get_weekday(column_index : int) -> int:
        return (column_index - EXCEL_HEADER_SCRAP) // EXCEL_DAY_LENGTH

    @staticmethod
    def get_double_time(column_index : int) -> str:
        return EXCEL_TIMES[ExcelWorker.get_double_number(column_index) - 1]