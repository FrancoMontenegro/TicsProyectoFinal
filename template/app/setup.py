from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))


cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""

cur.execute(sql)

sql ="""
CREATE TABLE admins
		   (rut integer PRIMARY KEY,
		    nombre varchar(40),
		    correo varchar(40),
		    pass varchar(40));	
"""

cur.execute(sql)

sql ="""
CREATE TABLE artefactos
		   (id serial PRIMARY KEY,
		    limMinTemp decimal,
		    limMaxTemp decimal,
		    limMinLuz decimal,
		    limMaxLuz decimal,
		    limMinHgnd decimal,
		    limMaxHgnd decimal,
		    limMinHamb decimal,
		    limMaxHamb decimal,
		    estado varchar(40));
"""
cur.execute(sql)

sql ="""
CREATE TABLE users
		   (rut integer PRIMARY KEY,
		    nombre varchar(40),
		    correo varchar(40),
		    pass varchar(40),
		    artefacto_id integer,
		    FOREIGN KEY (artefacto_id) REFERENCES artefactos (id));	
"""

cur.execute(sql)



sql ="""
CREATE TABLE mediciones
		   (id serial PRIMARY KEY,
		    artefacto_id integer,
		    temp decimal,
		    luz decimal,
		    hum_suelo decimal,
		    hum_ambiente decimal,
			date timestamp,
		    FOREIGN KEY (artefacto_id) REFERENCES artefactos (id));	
"""
cur.execute(sql)


conn.commit()
cur.close()
conn.close()