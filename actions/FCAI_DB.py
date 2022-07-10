import os
import sqlite3

import pandas as pd

folder_path = 'D:\\FCAI_CU_Chatbot\\DB'


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

        if len(temp) == 4:
            # split file name form its extension
            table_name = temp[0]

        else:
            table_name = table_name.split('.')
            table_name = table_name[0]


        if not self.check_table('xGPAx'):
            gpa_table = f'CREATE Table xGPAx (id, gpa, year, department)'
            self.cursor.execute(gpa_table)

        if not self.check_table('schedule'):
            schedule_table = f'CREATE Table schedule (g1, g2, cs3, cs4, ai3, ai4, it3, it4, is3, is4, ds3, ds4)'
            self.cursor.execute(schedule_table)
        if not self.check_table(f'x{table_name}x'):
            if table_name.isdigit():
                table = f'CREATE Table x{table_name}x (subject, grades, hours)'
            else:
                table = f'CREATE Table x{table_name}x (subject, prerequisites,	priority)'
            # execute the statement

            self.cursor.execute(table)

    def insert_data(self, table_name, data):
        """
            parameters:
                table_name: string consists of id_gpa_year_department
                data: csv file to convert it to sqlite
        """
        department = []
        try:
            temp = table_name.split('_')

            if len(temp) == 4:
                # split file name form its extension
                department = temp[3].split('.')
                table_name = temp[0]

            else:
                table_name = table_name.split('.')
                table_name = table_name[0]

            if self.check_table(f'x{table_name}x'):
                if table_name.isdigit():

                    insert_values = f'INSERT INTO xGPAx (id, gpa, year, department) VALUES (?, ?, ?, ?)'
                    data_tuple = (temp[0], temp[1], temp[2], department[0])
                    self.cursor.execute(insert_values, data_tuple)
                    data.to_sql(f'x{table_name}x', self.connection, if_exists='replace', index=False)
                    self.connection.commit()

                else:
                    df = pd.read_csv('D:\\FCAI_CU_Chatbot\\DB\\schedule.csv')
                    df.to_sql(f'schedule', self.connection, if_exists='replace', index=False)
                    data.to_sql(f'x{table_name}x', self.connection, if_exists='replace', index=False)
                    self.connection.commit()

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

    @staticmethod
    def get_data(data):
        data_list = []
        for row in data:
            data_list.append(list(row))
        return data_list

    @staticmethod
    def convert_to_dictionary(data, table_name):
        """
            Parameters:
                data: query returned from database
                table_name: its name of the table which query was returned from it

            Returns:
                data: dictionary of the query
        """
        if table_name == '':
            data = pd.DataFrame(data, columns=['subject', 'grades', 'hours'])
            cumulative_hours = sum(data['hours'])
            data = data.drop(['hours'], axis=1)
            grades = set(data['grades'])
            results = {}

            student_subject = []
            for i in grades:
                subjects = []

                for subject, grade in zip(data['subject'], data['grades']):
                    if grade == i:

                        student_subject.append(subject.lower())
                        subjects.append(subject.lower())
                results[i] = subjects

            return results, student_subject, cumulative_hours

        if table_name == 'GPA':
            data = {data[0]: data[1:] for data in data}
            return data

        data = {data[0].lower(): [data[1:][0].split('^'), data[1:][1]] for data in data}
        return data

    def get_tables(self, table_name):
        """
            parameter:
                table_name: string name of the wanted table

            returns:
                results: list of student grades and subjects
                         OR list of bylaw
                         OR list of students id and gpa
        """

        data = self.cursor.execute(f'SELECT * FROM x{table_name}x').fetchall()
        results = self.get_data(data)
        self.connection.commit()

        if table_name.isdigit():
            return self.convert_to_dictionary(results, '')

        elif table_name == "bylaw":
            return self.convert_to_dictionary(results, 'bylaw')

        return self.convert_to_dictionary(results, 'GPA')

    def get_schedule(self):
        data = self.cursor.execute(f'SELECT * FROM schedule').fetchall()
        results = self.get_data(data)
        df = pd.DataFrame(results, columns=['g1', 'g2', 'cs3', 'cs4', 'ai3', 'ai4', 'it3', 'it4', 'is3', 'is4', 'ds3',
                                            'ds4'])
        self.connection.commit()
        return df.to_dict(orient='list')

    def create_DB(self):
        for file in os.listdir(folder_path):
            if file == 'schedule.csv':
                continue

            self.create_table(file)
            data = pd.read_csv(f'{folder_path}\\{file}')
            self.insert_data(file, data)

    def close_DB(self):
        self.connection.close()
        self.cursor.close()
