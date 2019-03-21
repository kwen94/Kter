import xlrd
import sys
import os
import re


class myexcel:

    def __init__(self, path):
        self.path = path
        self.book = xlrd.open_workbook(path)

    def get(self, obj):
        dic = {}
        if isinstance(obj, str):
             dic[obj] = self._get_item(obj)
        elif isinstance(obj, list):
            for i in obj:
                dic[i] = self._get_item(i)
        return dic

    def _get_item(self, name):
            sheet = self.book.sheet_by_name(name)
            if sheet:
                record = []
                nrows = sheet.nrows 
                for i in range(nrows):
                    record.append(sheet.row_values(i))
            else:
                raise ValueError
            return record

