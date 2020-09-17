import os
import openpyxl

class Writer:
    def __init__(self):
        pass

    def initialize(self):
        self.book = openpyxl.Workbook()
        self.book.remove(self.book.get_sheet_by_name('Sheet'))

    def append(self, pattern_dic, scripts_dic):
        
        for sheet_name, dic in [
                ['scripts', scripts_dic],
                ['patterns', pattern_dic]
            ]:
            
            tags = sorted(dic.keys())
            sheet = self.book.create_sheet(sheet_name)
            
            index = 0
            max_length_of_eng = 0
            max_length_of_kor = 0

            for tag in tags:
                for eng, kor in dic[tag]:
                    sheet['A{}'.format(index + 1)] = tag
                    sheet['B{}'.format(index + 1)] = eng
                    sheet['C{}'.format(index + 1)] = kor
                    index += 1

                    max_length_of_eng = max(max_length_of_eng, len(eng))
                    max_length_of_kor = max(max_length_of_kor, len(kor))
            
            sheet.column_dimensions['B'].width = max_length_of_eng
            sheet.column_dimensions['C'].width = max_length_of_kor
    
    def save(self, excel_path):
        self.book.save(excel_path)