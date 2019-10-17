import xlrd
import os

class ExcelWorker:
    def __init__(self, filename : str):
        self.workbook = xlrd.open_workbook(os.path.join(os.getcwd(), f'files\\data\\{filename}'))
        self.worksheet = self.workbook.sheet_by_index(0)
    
    def get_cell(self, i_index : int, j_index : int):
        print(self.worksheet.cell(i_index, j_index))

worker = ExcelWorker('KBiSP-3-kurs-1-sem.xlsx')

worker.get_cell(7, 119)