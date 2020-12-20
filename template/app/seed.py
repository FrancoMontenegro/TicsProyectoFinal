from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


sql =""" insert INTO admins (rut, nombre, correo, pass)
					 values (197479493, 'franco montenegro', 'franco@gmail.com', 'password');
"""
cur.execute(sql)
conn.commit()

sql =""" insert INTO artefactos (estado)
					 values ('ACTIVO');
"""
cur.execute(sql)
conn.commit()

sql =""" insert INTO users (rut, nombre, correo, pass, artefacto_id)
					 values (111111111, 'nombre apellido', 'correo@gmail.com', 'password', 1);
"""
cur.execute(sql)
conn.commit()





cur.close()
conn.close()
