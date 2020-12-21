from app import app
from flask import Flask,jsonify,request,redirect,url_for,session, flash
from flask import render_template
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import time

from .configuraciones import *
import random as ran
#from app import configuraciones
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

app.secret_key = "super secret key"

@app.route('/')
@app.route('/index')
def index(): 
	return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

	return render_template('login.html')

@app.route('/validate', methods=['GET','POST'])
def validate():
	if request.method == "POST":
		try:
			correo = request.form['inputEmail']
			password = request.form['inputPassword']

			sql ="""select users.pass from users where users.correo = '%s';
			"""%(correo)
			cur.execute(sql)
			psswrd = cur.fetchone()

			if psswrd is None:
					adminPsswrd = ' '

			sql ="""select admins.pass from admins where admins.correo = '%s';
			"""%(correo)
			cur.execute(sql)
			adminPsswrd = cur.fetchone()

			if adminPsswrd is None:
					adminPsswrd = ' '

			if password == adminPsswrd[0]:
				return redirect(url_for('admindash'))

			if password == psswrd[0]:
				return redirect(url_for('dashboard'))

				

			return redirect(url_for('login'))

		except:
			pass
			return redirect(url_for('login'))

def dataGenerator():
	temp = [9.3, 12.5, 17.4, 20.1, 20.7, 21.4, 22.0, 27.1, 30.4]
	luz = [50,45, 5, 7, 60, 32, 93, 20, 26]
#0 sumergido en agua - 1023 en aire
#600-700 ligeramente humedo
#800-1023 suelo seco    
	hum_suelo = [0.100, 0.300, 0.500, 1.43, 0.650, 0.700, 0.750, 0.800, 1]    
	hum_ambiente = [0, 3, 7, 10, 11, 15, 17, 25, 40]    
	
	temperatura = np.random.choice(temp, p=[0.02,0.03,0.05,0.2,0.26,0.2,0.2,0.03,0.01])    
	luminosidad = np.random.choice(luz, p=[0.02,0.03,0.05,0.2,0.26,0.2,0.2,0.03,0.01])  
	humedad_sue = np.random.choice(hum_suelo, p=[0.02,0.03,0.05,0.2,0.26,0.2,0.2,0.03,0.01])      
	humedad_amb = np.random.choice(hum_ambiente, p=[0.02,0.03,0.05,0.2,0.26,0.2,0.2,0.03,0.01])    
	
	
	sql ="""insert INTO mediciones (artefacto_id, temp, luz, hum_suelo, hum_ambiente, date) 
			values ('1','%s','%s','%s','%s',now());
		 """%(temperatura,luminosidad,humedad_sue,humedad_amb)
	cur.execute(sql)
	conn.commit()

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

	while True:
		dataGenerator()
		if request.method == "POST":

			minTemp = request.form['minTemp']
			maxTemp = request.form['maxTemp']
			minLuz = request.form['minLuz']
			maxLuz = request.form['maxLuz']
			minHgnd = request.form['minHgnd']
			maxHgnd = request.form['maxHgnd']
			minHamb = request.form['minHamb']
			maxHamb = request.form['maxHamb']

			sql ="""update artefactos set limMinTemp = %s, limMaxTemp = %s, limMinLuz = %s, limMaxLuz = %s, limMinHgnd = %s, limMaxHgnd = %s, limMinHamb = %s, limMaxHamb = %s where artefactos.id = 1;
			"""%(minTemp, maxTemp, minLuz, maxLuz, minHgnd, maxHgnd, minHamb, maxHamb)
			cur.execute(sql)
			conn.commit()

			return redirect(url_for('dashboard'))

		sql ="""select mediciones.temp, mediciones.luz, mediciones.hum_suelo, mediciones.hum_ambiente from mediciones where mediciones.artefacto_id = 1 order by mediciones.date;"""
		cur.execute(sql)
		dataResultados = cur.fetchall()
		conn.commit()

		count = len(dataResultados)
		temperature = []
		luminosity = []
		hum_gnd = []
		hum_amb = []

		for i in range(len(dataResultados)):
			temperature.append(dataResultados[i][0])
			luminosity.append(dataResultados[i][1])
			hum_gnd.append(dataResultados[i][2])
			hum_amb.append(dataResultados[i][3])

		xScale = np.linspace(0, count, count, dtype = "int")
		yScale = temperature
		yScale2 = luminosity
		yScale3 = hum_gnd
		yScale4 = hum_amb

		# temperatura grafico
		trace = go.Scatter(
			x = xScale,
			y = yScale
		)

		# luminosidad grafico
		trace2 =go.Scatter(
			x = xScale,
			y = yScale2
		)

		# humedad suelo grafico
		trace3 =go.Scatter(
			x = xScale,
			y = yScale3
		)

		# humedad ambiente grafico
		trace4 =go.Scatter(
			x = xScale,
			y = yScale4
		)

		data = [trace]
		data2 = [trace2]
		data3 = [trace3]
		data4 = [trace4]

		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
		graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
		graphJSON3 = json.dumps(data3, cls=plotly.utils.PlotlyJSONEncoder)
		graphJSON4 = json.dumps(data4, cls=plotly.utils.PlotlyJSONEncoder)

		sql =""" select artefactos.limMinTemp, artefactos.limMaxTemp, artefactos.limMinLuz, artefactos.limMaxLuz, artefactos.limMinHgnd, artefactos.limMaxHgnd, artefactos.limMinHamb, artefactos.limMaxHamb from artefactos where artefactos.id = 1;
		"""
		cur.execute(sql)
		limites = cur.fetchall()
		conn.commit()

		alerta = False

		if temperature[len(dataResultados)-1] < limites[0][0]:
			alerta = True

		if temperature[len(dataResultados)-1] > limites[0][1]:
			alerta = True

		if luminosity[len(dataResultados)-1] < limites[0][2]:
			alerta = True

		if luminosity[len(dataResultados)-1] > limites[0][3]:
			alerta = True

		if hum_gnd[len(dataResultados)-1] < limites[0][4]:
			alerta = True

		if hum_gnd[len(dataResultados)-1] > limites[0][5]:
			alerta = True

		if hum_amb[len(dataResultados)-1] < limites[0][6]:
			alerta = True

		if hum_amb[len(dataResultados)-1] > limites[0][7]:
			alerta = True

		if alerta == True:
			flash("Parametro fuera de los límites establecidos","warning")

		return render_template('dashboard.html', graphJSON=graphJSON, graphJSON2=graphJSON2, graphJSON3=graphJSON3, graphJSON4=graphJSON4)


@app.route('/limits', methods=['GET','POST'])
def limits():
	return render_template('limits.html')

@app.route('/admindash', methods=['GET','POST'])
def admindash():

	sql ="""select artefactos.id, users.rut, users.nombre, users.correo, users.pass, artefactos.estado from users, artefactos where users.artefacto_id = artefactos.id and artefactos.estado = 'ACTIVO' order by artefactos.id;"""
	cur.execute(sql)
	usuarios = cur.fetchall()
	conn.commit()
	if request.method == "POST":
		
		minTemp = request.form['minTemp']
		maxTemp = request.form['maxTemp']
		minLuz = request.form['minLuz']
		maxLuz = request.form['maxLuz']
		minHgnd = request.form['minHgnd']
		maxHgnd = request.form['maxHgnd']
		minHamb = request.form['minHamb']
		maxHamb = request.form['maxHamb']
		name = request.form['nombre']
		rut = request.form['rut']
		email = request.form['email']
		contrasena = request.form['contrasena']

		
		sql ="""insert INTO artefactos (limMinTemp, limMaxTemp, limMinLuz, limMaxLuz, limMinHgnd, limMaxHgnd, limMinHamb, limMaxHamb, estado) values ('%s','%s','%s','%s','%s','%s','%s','%s','ACTIVO') returning artefactos.id;"""%(minTemp, maxTemp, minLuz, maxLuz, minHgnd, maxHgnd, minHamb, maxHamb)
		cur.execute(sql)
		newId = cur.fetchone()
		conn.commit()

		sql="""insert INTO users (rut, nombre, correo, pass, artefacto_id) values ('%s','%s','%s','%s','%s');
		"""%(rut, name, email, contrasena, newId[0])
		cur.execute(sql)
		conn.commit()
		return redirect(url_for('admindash'))
	return render_template('admindash.html',usuarios=usuarios)

@app.route('/crearUser', methods=['GET','POST'])
def crearUser():

	return render_template('crearUser.html')

@app.route('/admindash/<user_id>', methods=['GET'])
def deleteUser(user_id):

	sql=""" update artefactos set estado = 'DISPONIBLE' where artefactos.id = '%s';
	"""%(user_id)
	cur.execute(sql)
	conn.commit()
	return redirect(url_for('admindash'))








