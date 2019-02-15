# -*- coding: UTF-8 -*-
import os
import xlwt
import sys

path = "/Users/hengwei/PycharmProjects/python01/ML"

files= os.listdir(path)

i = 0

excelfile = xlwt.Workbook('test.xlsx')
table = excelfile.add_sheet("Sheet1",cell_overwrite_ok=False)

for file in files:
    if "-en.txt" in file:

        koreafilename = file[0:-7]+'.txt'
        with open(koreafilename,'r') as koreafile:
            krtext = koreafile.read()

        with open(file,'r') as cnfile:
            cntext = cnfile.read()

        table.write(i, 0, file[0:-7])
        table.write(i, 1, krtext)
        table.write(i, 2, cntext)
        i=i+1
excelfile.save('test.xlsx')
