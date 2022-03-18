import sqlite3


def check_table(table_name):
    if table_name == "Menu_Table":
        return True
    return False


def create_table(table_name):
    # connecting to the database
    connection = sqlite3.connect("restaurant.db")
    # cursor
    cursor = connection.cursor()
    # SQL command to create a table in the database
    if check_table(table_name):
        table = f'CREATE Table {table_name} (Pizza, Small, Medium, Large)'
    else:
        table = f'CREATE Table {table_name} (Pizza, Size, Name, id, Phone)'
    # execute the statement
    cursor.execute(table)
    connection.close()


def insert_menu(pizza, small, medium, large):
    sqliteConnection = sqlite3.connect('restaurant.db')
    cursor = sqliteConnection.cursor()
    try:
        sqlite_insert_with_param = f'INSERT INTO Menu_Table (Pizza, Small, Medium, Large) VALUES (?, ?, ?, ?)'
        data_tuple = (pizza, small, medium, large)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print(f'{pizza} أضيفت للقائمة ')

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def insert_booking(pizza, size, name, id, phone):
    sqliteConnection = sqlite3.connect('restaurant.db')
    cursor = sqliteConnection.cursor()
    try:
        sqlite_insert_with_param = f'INSERT INTO Booking_Table (Pizza, Size, Name, id, Phone) VALUES (?, ?, ?, ' \
                                   f'?, ?) '

        data_tuple = (pizza, size, name, id, phone)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        cursor.close()
        return 'الطلب اتحجز يا فندم.'

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def print_menu():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    print(f'Menu_Table:\nLarge    Medium    Small      Pizza')
    cur.execute(f'SELECT * FROM Menu_Table')
    for row in cur:
        print(row[0] + '    ', str(row[1]) + '        ', str(row[2]) + '      ', str(row[3]) + ' ')
    conn.commit()
    cur.close()


def get_prices(items):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    order = []
    print(f'Menu_Table:\nLarge    Medium    Small      Pizza')
    cur.execute(f'SELECT * FROM Menu_Table')
    for row in cur:
        if row[0] in items:
            order.append((row[0], row[1]))
    conn.commit()
    cur.close()
    return order


# create_table('Menu_Table')
# create_table('Booking_Table')
# insert_menu('بيتزا خضروات', 42, 53, 74)
# insert_menu('بيتزا مشروم', 48, 63, 84)
# insert_menu('بيتزا مارجاريتا', 42, 53, 74)
# insert_menu('بيتزا تشيز لافرز', 48, 63, 84)
# insert_menu('بيتزا هوت دوج', 48, 63, 84)
# insert_menu('بيتزا سلامى', 53, 69, 90)
# insert_menu('بيتزا بسطرمة', 53, 69, 90)
# insert_menu('بيتزا سوبر سوبريم', 58, 74, 100)
# insert_menu('بيتزا بيبرونى', 53, 69, 90)
# insert_menu('بيتزا تشيكن رانش', 58, 74, 100)
# insert_menu('بيتزا تشيكن باربيكيو', 58, 74, 100)
# insert_menu('بيتزا سموكد', 58, 74, 100)
# insert_menu('بيتزا تونة', 48, 63, 84)
# insert_menu('بيتزا سى رانش', 63, 84, 116)
print_menu()
