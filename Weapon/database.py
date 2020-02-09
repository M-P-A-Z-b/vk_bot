import sqlite3


def init_db():
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("""
    CREATE table phrases (
        id integer primary key,
        phrase text,
        answer text
        );
    """)
    connect.close()


def insert_db(phrase, answer):
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM phrases")
    new_id = str(cursor.fetchall()[-1][0] + 1)
    cursor.execute("insert into phrases values(" +
                   new_id+", '"+phrase+"', '"+answer+"')")
    connect.commit()
    connect.close()


def get_db():
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM phrases")
    result = cursor.fetchall()
    print(result)
    connect.close()
    return result


def init2_db():
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("""
    CREATE table groups (
        id integer primary key autoincrement,
        groups_name text
    );
    """)

    cursor.execute("""
    CREATE table user (
        id integer primary key,
        chat_id integer,
        id_group integer,
        FOREIGN KEY (id_group) REFERENCES groups (id)
    );
    """)

    cursor.execute("insert into groups values (1,'gunshot')")
    cursor.execute("insert into groups values (2,'cold')")
    cursor.execute("insert into groups values (3,'all')")
    connect.commit()

    connect.close()


def get_member(group):
    if group == 'gunshot':
        group_id = 1
    elif group == 'cold':
        group_id = 2
    elif group == 'all':
        group_id = 3
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT chat_id FROM user WHERE id_group="+str(group_id))
    result = cursor.fetchall()
    connect.close()
    for i in range(0, len(result)):
        result[i] = result[i][0]
    return result


def get_groups():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT groups_name FROM groups")
    result = cursor.fetchall()
    print(result)
    conn.close()
    for i in range(0, len(result)):
        result[i] = result[i][0]
    return result


def add_member(group, chat_id):
    if group == '{"command":"gunshot"}':
        group_id = 1
    if group == '{"command":"cold"}':
        group_id = 2
    if group == '{"command":"all"}':
        group_id = 3
    connect = sqlite3.connect('database.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT id from user")
    if not cursor.fetchall():
        new_id = "1"
    else:
        new_id = str(cursor.fetchall()[-1][0]+1)
    print(new_id)
    print(chat_id)
    print(group_id)
    cursor.execute("insert into user values ("+new_id +
                   ","+str(chat_id)+","+str(group_id)+")")
    connect.commit()
    connect.close()

# connect = sqlite3.connect('database.sqlite')
# cursor=connect.cursor()
# cursor.execute("insert into user values('1','0','0')")
# connect.commit()
# connect.close()

# conn = sqlite3.connect('database.sqlite')
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM groups")
# result = cursor.fetchall()
# print(result)
# conn.close()
