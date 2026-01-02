class Bogtable:
    def __init__(self, columns):
        self.__table = []
        if columns >= 0:
            self.__table = ['+']
        for i in range(columns):
            self.__table[0] += '---+'
        self.__columns = columns

    @property
    def raw_table(self):
        return self.__table

    @property
    def columns(self):
        return self.__columns

    def add_row(self, row):
        data_row = '|'
        for element in row:
            if element == 10:
                data_row += f' {element}|'
            else:
                data_row += f' {element} |'

        self.__table.append(data_row)
        self.__table.append(self.__table[0])

    def append_row(self, row):
        self.__table.append(row)

    def __str__(self):
        returned_string = ''
        for row in self.__table:
            returned_string += row + '\n'
        return returned_string

    def __add__(self, other):
        table1 = self.raw_table
        table2 = other.raw_table
        final_table = Bogtable(-1)
        if len(table1) != len(table2):
            return None

        for i in range(len(table1)):
            row = table1[i] + '     ' + table2[i]
            final_table.append_row(row)
        return final_table