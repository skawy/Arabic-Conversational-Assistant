import os
import sqlite3

import pandas as pd


class FCAI_DB:
    def __init__(self):
        self.database_name = "FCAI Subjects.db"
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def check_row(self, table_name, row):
        column = ['subject', 'prerequisite']
        student_columns = ['subject', 'grades', 'hours']

        if len(row) == 2:
            columns_list = column
        else:
            columns_list = student_columns

        id = []
        for i in range(len(columns_list)):
            self.cursor.execute(f"SELECT rowid FROM {table_name} WHERE {column[i]} = ?", (row[i],))
            data = self.cursor.fetchall()

            if len(data) != 0:
                id.append(data)

        if len(id) != 0 and len(id) != 1:
            if id[0] == id[1]:
                return True
        return False

    def check_table(self, table_name):
        try:
            self.cursor.execute(
                f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')
            if self.cursor.fetchone()[0] == 1:
                return True
        except sqlite3.Error:
            print('Table is not exist')
        return False

    def create_table(self, table_name):
        # SQL command to create a table in the database
        temp = table_name.split('_')
        table_name = table_name.split('.')
        if not self.check_table(f'x{table_name[0]}x'):
            if temp[0].isdigit():
                print('fjbjsfbjsfkvn', table_name)
                table = f'CREATE Table x{table_name[0]}x (subject, grades, hours)'
            else:
                table = f'CREATE Table x{table_name[0]}x (subject, prerequisites,	priority)'
            # execute the statement
            print(table)
            self.cursor.execute(table)

    def insert_data(self, table_name, data):
        try:
            temp = table_name.split('_')
            table_name = table_name.split('.')
            if self.check_table(f'x{table_name[0]}x'):
                if temp[0].isdigit():
                    data.to_sql(f'x{table_name[0]}x', self.connection, if_exists='append', index=False)
                    self.connection.commit()
                else:
                    data.to_sql(f'x{table_name[0]}x', self.connection, if_exists='append', index=False)
                    self.connection.commit()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

    @staticmethod
    def get_data(data):
        data_list = []
        for row in data:
            data_list.append(list(row))
        return data_list

    def get_tables(self, table_name):
        result = []
        bylaw = []
        temp = table_name.split('_')
        table_name = table_name.split('.')
        data = self.cursor.execute(f'SELECT * FROM x{table_name[0]}x').fetchall()
        if temp[0].isdigit():
            result = self.get_data(data)
        else:
            bylaw = self.get_data(data)

        self.connection.commit()
        return result, bylaw

    def create_DB(self):
        for file in os.listdir('D:\\FCAI_Chatbot\\DB'):
            self.create_table(file)
            data = pd.read_csv('D:\\FCAI_Chatbot\\DB\\' + file)
            self.insert_data(file, data)
            # print(self.get_tables(file))
        self.connection.close()

    def close_DB(self):
        self.connection.close()
        self.cursor.close()


# db = FCAI_DB()
# db.create_DB()
