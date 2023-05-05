import psycopg2

# создание таблиц БД
def get_create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS client (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL);
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS e_mail (
    mail_name VARCHAR(50) UNIQUE NOT NULL,
    id INTEGER PRIMARY KEY REFERENCES client(id)
    );''')

    cur.execute('''CREATE TABLE IF NOT EXISTS phone_number (
    id SERIAL PRIMARY KEY,
    number VARCHAR(13) UNIQUE,
    client_id INTEGER REFERENCES  client(id)
    );''')

# наполнение имя фамилия
def append_client(cursor, FirstName: str, LastName: str):
    cursor.execute('''INSERT INTO client (first_name, last_name)
    VALUES (%s, %s) RETURNING id, first_name, last_name;''', (FirstName, LastName))

# наполнение телефон
def append_phone(cursor, id_client, client_number='NULL'):
    cursor.execute(''' INSERT INTO phone_number (client_id, number)
    VALUES (%s, %s) RETURNING id, client_id, number;''', (id_client, client_number))


# наполнение email
def append_e_mail(cursor, client_id, mail):
    cursor.execute(""" INSERT INTO e_mail (id, mail_name)
    VALUES (%s, %s) RETURNING id, mail_name """, (client_id, mail))

# изменение данных
def update_client(cursor, first_name, last_name, id):
    cursor.execute(""" UPDATE client SET first_name=%s,
    last_name=%s WHERE id=%s;
    """, (first_name, last_name, id))

# удаление номера телефона
def del_phone(cursor, id):
    cursor.execute(""" DELETE FROM phone_number WHERE id=%s ; """, (id,))

# удаление клиента
def del_client(cursor, id):
    cursor.execute("""DELETE FROM e_mail WHERE e_mail.id=%s;""", (id,))
    cursor.execute("""DELETE FROM phone_number WHERE client_id=%s ; """, (id,))
    cursor.execute("""DELETE FROM client WHERE client.id=%s;""", (id,))

# поиск клиента по фамилии
def get_client(cursor, LastName):
    cur.execute("""SELECT first_name, last_name, em."mail_name", number FROM client c
    JOIN e_mail em ON c.id = em.id
    JOIN phone_number pn ON pn.client_id = c.id
    WHERE last_name = %s;""", (LastName,))
    print(cur.fetchall())

with psycopg2.connect(database='personal_info', user='postgres', password='') as conn:# в параметрe password укажите пароль пользователья postgres
    with conn.cursor() as cur:
        cur.execute('''DROP TABLE phone_number;
        DROP TABLE e_mail;
        DROP TABLE client;''')

        get_create_table(cur)
        append_client(cur, 'Ivan', 'Ivanov')
        append_client(cur, 'Petr', 'Petrov')
        append_e_mail(cur, 1, 'I.Ivanov@mails.rg')
        append_e_mail(cur, 2, 'P.Petrov@Cmail.rf')

        append_phone(cur, 1, 796093)
        append_phone(cur, 1, 232090)
        append_phone(cur, 2, 456678)
        append_phone(cur, 2, 567788)

        del_phone(cur, 3)
        del_client(cur, 1)
        get_client(cur, 'Petrov')
        update_client(cur, 'Sergey', 'Petrov', 2)
        get_client(cur, 'Petrov')

        conn.commit()

