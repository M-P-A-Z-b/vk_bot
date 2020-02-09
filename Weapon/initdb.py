import sqlite3

connect = sqlite3.connect('cars.sqlite')
cursor = connect.cursor()

cursor.execute("""
CREATE table owners (
  id integer primary key,
  owner text,
  driver_card integer
);
""")

cursor.execute("""
CREATE table models (
  id integer primary key,
  mark text,
  model text,
  prod_country text
);
""")

cursor.execute("""
CREATE table cars (
  id integer primary key,
  number integer,
  color text,
  id_owner integer,
  id_model integer,
  FOREIGN KEY (id_owner) REFERENCES owners (id)
  FOREIGN KEY (id_model) REFERENCES models (id)
);
""")
cursor.execute("insert into owners values (1,'Вася','123')")
cursor.execute("insert into owners values (2,'Ира','124')")
cursor.execute("insert into owners values (3,'Игорь','122')")
cursor.execute("insert into owners values (4,'Виктор','121')")
cursor.execute("insert into owners values (5,'Андрей','126')")
cursor.execute("insert into models values (1,'Toyota','Camry','Japan')")
cursor.execute("insert into models values (2,'lada','Kalina','Russia')")
cursor.execute("insert into models values (3,'Сhevrolet','Camaro','USA')")
cursor.execute("insert into cars values (1,758,'red',1,1)")
cursor.execute("insert into cars values (2,176,'white',2,2)")
cursor.execute("insert into cars values (3,134,'yellow',3,3)")
cursor.execute("insert into cars values (4,777,'black',4,3)")
cursor.execute("insert into cars values (5,333,'brown',5,2)")
connect.commit()
# cursor.execute("SELECT * FROM owners")
# print(cursor.fetchall())
# cursor.execute("SELECT * FROM models")
# print(cursor.fetchall())
# cursor.execute("SELECT * FROM cars")
# print(cursor.fetchall())
cursor.execute("""
SELECT models.model,cars.color,owners.owner,owners.driver_card
FROM cars,owners, models
WHERE cars.id_owner=owners.id and cars.id_model=models.id and models.mark= 'Сhevrolet'
""")
print(cursor.fetchall())

connect.close()