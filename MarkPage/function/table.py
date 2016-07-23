#coding=utf8
import xlrd
import xlwt
import json

class Table:
    def __init__(self, table, row_num, col_num):
        self.table = table
        self.row_num = row_num
        self.col_num = col_num
    def __getitem__(self, i):
        return self.table[i]

    def getMentionContext(self, r, c):
        res = []
        for i in range(self.row_num):
            if i == r:
                continue
            res.append(self.table[i][c])

        for j in range(self.col_num):
            if j == c:
                continue
            res.append(self.table[r][j])
        return res

class tableManager:
    def __init__(self):
        self.excel = xlrd.open_workbook('table_data.xls')
    def getTable(self):
        table = self.excel.sheet_by_name('table')
        tables = []

        nrows = table.nrows
        ncols = table.ncols

        # 按列存储
        r = 0
        down_flag = False
        while True:
            r += 1

            # 获取当前表格的行数
            next_r = r
            while True:
                if next_r == nrows:
                    down_flag = True
                    break
                if table.cell(next_r,0).value != '':
                    next_r += 1
                else:
                    break

            # 获取当前表格的列数
            next_c = 0
            while True:
                if next_c == ncols:
                    break
                if table.cell(r,next_c).value != '':
                    next_c += 1
                else:
                    break

            t = []
            for rr in range(r, next_r):
                row = []
                for cc in range(0,next_c):
                    row.append(table.cell(rr,cc).value)
                t.append(row)
            tables.append(Table(t, next_r - r, next_c))
            if down_flag:
                break
            else:
                r = next_r + 1

        return tables
          
            



