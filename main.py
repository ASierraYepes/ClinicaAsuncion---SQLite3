from flask import Flask, render_template, request, redirect, url_for, session, flash  #Importamos el framework flask
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import sqlite3
import os
from medicoh import form_medicoh
from pacientec import form_pacientec
from historia import form_historia
from registro import form_registrop
from comentario import form_comentario

app = Flask(__name__)             #ejecutamos para obtener un objeto que vamos a configurar
app.secret_key = os.urandom(24)

username = None
rol = None
identificacion = None
xid_medico = None
nameM = None

    #--Pagina de inicio--#
@app.route("/")
def home():
    return render_template("index.html")

    #---Ingreso paciente---#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        username = escape(request.form["username"])
        password = escape(request.form["password"])

        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            cur= con.cursor()
            sql = cur.execute("SELECT Password FROM registerUser where email = ?",[username]).fetchone()
            global rol
            rol = cur.execute("SELECT rol FROM registerUser where email = ?",[username]).fetchone() #Registro se lo doy a la variable
            global nameM
            nameM = cur.execute("SELECT name FROM registerUser where email = ?",[username]).fetchone() #Registro se lo doy a la variable
            global identificacion
            identificacion = cur.execute("SELECT identification FROM registerUser where email = ?",[username]).fetchone()

            if sql!=None:
                clavehash = sql[0]
                session.clear()
                if check_password_hash(clavehash,password):
                    session["loginsuccess"] = True
                    session['email'] = username

                    if rol[0]=="Paciente":
                        return redirect(url_for("patients", username = username))
                        #return render_template("patientProfile.html", datosuser = sql2[0], session = session)
                    if rol[0]=="Medico":
                        return redirect(url_for("medic", username = username))
                    else:
                        return redirect(url_for("admin", username = username)) 
                        #render_template("dashboard.html", datosadmin = sql2[0], session = session)
                else:
                    return redirect(url_for('login'))
            else:
                flash("EL Usuario que ingreso o la contraseña es incorrecta. Por favor ingrese datos válidos!!")
                return redirect(url_for('login'))

    return render_template("login.html")

    #---Registro paciente---#
@app.route('/regitroP', methods=["GET", "POST"])
def newUser():
    if request.method == "POST":
        name = escape(request.form["one"])
        email = request.form["two"]
        password = escape(request.form["three"])
        hash_pass = generate_password_hash(password)
        identification = escape(request.form["cedula"])
        sex = request.form["four"]
        bloodType = request.form["five"]
        birthday = request.form["six"]
        age = request.form["age"]
        addres = request.form["seven"]
        city = request.form["eight"]
        phone = request.form["nine"]
        rol = request.form["rol"]

        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            sql = con.cursor() #Manipula la conexion a la base de datos
            session['name'] = name
            if rol=="Paciente":
                sql.execute("INSERT INTO registerUser(name, email, password, identification, sex, bloodType, birthday, age, addres, city, phone, rol) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, email, hash_pass, identification, sex, bloodType, birthday, age, addres, city, phone, rol))
                sql.execute("INSERT INTO paciente(id_paciente, nombre, estado, estado_salud) values (?, ?, ?, ?)",(identification, name, 'True', 'Aún no se ha comprobado el estado de salud'))
            if rol=="Medico":
                sql.execute("INSERT INTO registerUser(name, email, password, identification, sex, bloodType, birthday, age, addres, city, phone, rol) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, email, hash_pass, identification, sex, bloodType, birthday, age, addres, city, phone, rol))
                sql.execute("INSERT INTO Medico(id_medico, estado, nombre) values (?, ?, ?)",(identification, 'True', name))
            if rol=="Administrador":
                sql.execute("INSERT INTO registerUser(name, email, password, identification, sex, bloodType, birthday, age, addres, city, phone, rol) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(name, email, hash_pass, identification, sex, bloodType, birthday, age, addres, city, phone, rol))
            con.commit() #Confirma la Transacción SQL
        return redirect(url_for("login"))    
    return redirect(url_for("newUser"))

    #---Perfil paciente---#
@app.route('/perfilP/<username>', methods=['GET'])
def patients(username):
    #if session['loginsuccess'] == True:   
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            cur= con.cursor()
            sql2 = cur.execute("SELECT * FROM registerUser where email = ?", [username]).fetchall() 
        return render_template('patientProfile.html', datosuser = sql2[0], session = session)

    #---Sistema del Administrador---#
@app.route('/sistema/', methods=['GET']) 
def dashboard():
    url = '/sistema/perfilA/'+username
    return render_template('dashboard.html', url = url) 

    #---Perfil Administrador---#
@app.route('/sistema/perfilA/<username>', methods=['GET'])
def admin(username):
    url = '/sistema/perfilA/'+username
    with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
         cur= con.cursor()
         sql2 = cur.execute("SELECT * FROM registerUser where email = ?", [username]).fetchall()
    return render_template('adminProfile.html', datosuser = sql2[0], url = url) 

    #---Asignar roles por usuario---#
@app.route("/sistema/asignarRol", methods=['GET', 'POST'])
def Roles():
    return "asignar roles"

    #---Perfil medico---#
@app.route('/perfilM/<username>', methods=['GET'])
def medic(username):
    with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
         cur= con.cursor()
         sql2 = cur.execute("SELECT * FROM registerUser where email = ?", [username]).fetchall()
    return render_template('medicProfile.html', datosuser = sql2[0])

    #---Menu de citas---#
@app.route('/menuCita')
def menucitas():
    with sqlite3.connect("clinica_la_asuncion.db") as con: #creo la conexion
        cur = con.cursor() #Manipula la conexion a la base de datos
        if rol[0]=="Paciente":
            row = cur.execute("SELECT * FROM Citas where id_paciente = ?", [identificacion[0]])
            return render_template('menucitas.html', datos=row)
        if rol[0]=="Medico":
            row = cur.execute("SELECT * FROM Citas where Medico = ?", [nameM[0]])
            return render_template('menucitas.html', datos=row)
        else:
            row = cur.execute("select* from Citas")
            return render_template('menucitas.html', datos=row)

    #---Crear citas---#
@app.route('/aCita', methods=['GET', 'POST'])
def crearCita():
    if request.method == 'POST':
        id_pac = request.form['identificacion']
        medico = request.form['medico']
        horacita = request.form['hora_cita']
        fecha = request.form['fecha']
        area = request.form['area']
        with sqlite3.connect("clinica_la_asuncion.db") as con: #creo la conexion
            cur = con.cursor() #Manipula la conexion a la base de datos
            estado = 0
            id_medico = cur.execute("SELECT id_medico FROM Medico where nombre = ?",[medico]).fetchone()
            cur.execute("insert into Citas(id_paciente, medico, hora_cita, fecha, area) values(?,?,?,?,?)", (id_pac, medico, horacita, fecha, area))
            cur.execute("insert into cita(id_paciente, fecha, hora_cita, hora_llegada, calificacion, id_medico,estado) values(?,?,?,?,?,?,?)", (id_pac, fecha, horacita, horacita, "---",id_medico[0],estado))
            con.commit() #confirma la transaccion sql
        flash('Cita Creada con Exito!!')
    return redirect(url_for('menucitas'))

    #---Editar citas---#
@app.route('/eCita/<id_paciente>')
def editar_cita(id_paciente):
    with sqlite3.connect("clinica_la_asuncion.db") as con: #creo la conexion
        con.row_factory=sqlite3.Row #convertir la respuesta de la base de datos en un diccionario
        cur = con.cursor() #Manipula la conexion a la base de datos
        cur.execute("select* from Citas where id_paciente = {0}".format(id_paciente))
        cita = cur.fetchall() #trae un solo registro de la base de datos
        return render_template('editarCita.html', cita=cita[0])

    #---Actualizar citas---#
@app.route('/update/<id_paciente>', methods=['POST'])
def update(id_paciente):
    if request.method == 'POST':
        id_pac = request.form['identificacion']
        med = request.form['medico']
        horacita = request.form['hora_cita']
        fecha = request.form['fecha']
        area = request.form['area']
        with sqlite3.connect("clinica_la_asuncion.db") as con: #creo la conexion
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("update Citas set medico = ?, hora_cita = ?, fecha = ?, area = ? where id_paciente = ?;",[med,horacita,fecha,area,id_paciente])
            con.commit()
        flash("Cita Actualizada Satisfactoriamente!!")
    return redirect(url_for("menucitas"))
    
@app.route('/dCita/<id_paciente>')
def eliminar_cita(id_paciente):
    with sqlite3.connect("clinica_la_asuncion.db") as con: #creo la conexion
        cur = con.cursor() #Manipula la conexion a la base de datos
        cur.execute("delete from Citas where id_paciente = ?;",[id_paciente])
        cur.execute("delete from cita where id_paciente = ?;",[id_paciente])
        con.commit()
    flash('Cita eliminada satisfactoriamente!!')
    return redirect(url_for('menucitas'))

   #---Asigna Horario de Atención por Médico---#
@app.route('/asignarH', methods=['GET','POST'])
def asignarH(): 
    form = form_medicoh()
    return render_template("asignarHM.html", form=form)

    #---Consultar Horario de Atención por Médico---#
@app.route('/consulta_medico',methods=["POST"])
def consultam():   
    form = form_medicoh()
    if request.method=="POST":
        xid_medico = form.id_medico.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory = sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from medico where id_medico = ?",[xid_medico])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("La identificación ingresada no pertene a un Medico!")
            return render_template("asignarHM.html", row = row, form=form )
    return render_template("asignarHM.html")

    #---Crea Horario de Atención Medico---#
@app.route('/agregar_horario' ,methods=["GET","POST"])
def grabarh():
    form = form_medicoh() # Creo la Instancia del Formulario
    if request.method=="POST": # Pregunto Metodo de la Petición
        xfecha        = form.fecha.data #.data para traer lo que tiene la caja de texto
        xhora_inicial = form.hora_inicial.data # Recupero cada una da las cajas de texto
        xhora_final   = form.hora_final.data
        xid_medico    = form.id_medico.data  
        if ( xhora_inicial < xhora_final):
            try:
            # Validar que no Exista Horario creado en esa fecha para ese Medico
                with sqlite3.connect("clinica_la_asuncion.db") as con0: #Creo la conexión - with manejador de contexto
                    con0.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                    cur0 = con0.cursor()
                    xsql = "select * from horario_medico where fecha = ? and hora_inicial >= ? and hora_final <= ? and id_medico = ?;"
                    cur0.execute(xsql,(xfecha, xhora_inicial, xhora_final, xid_medico))
                    row0 = cur0.fetchone() #Trae de la Base de DAtos 1 solo registro
                    if row0 is None:
                        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
                            cur = con.cursor() #Manipula la conexion a la base de datos
                            cur.execute("insert into horario_medico(fecha, hora_inicial,hora_final,id_medico) values (?, ?, ?, ?);",(xfecha, xhora_inicial, xhora_final, xid_medico))
                            con.commit() #Confirma la Transacción SQL
                        with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto                            
                            con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                            cur1 = con1.cursor()
                            cur1.execute("select * from horario_medico where id_medico = ?;",[xid_medico])
                            row1 = cur1.fetchall()
                        return render_template("asignarHM.html", form=form, row1=row1)                        
                    else:
                        flash ("Horario mal Asignado, se cruza con otro horario del mismo medico")
                        return render_template("asignarHM.html", form=form)    
            except:
                con0.rollback()
        else:        
             flash ("Horario Invalido")
    flash ("Horario mal Asignado, se cruza con otro horario del mismo medico")         
    return render_template("asignarHM.html", form=form) 

    #---Calificar citas cumplicas---#
@app.route('/ccita' ,methods=["GET","POST"])
def citai1():
    form = form_pacientec()
    return render_template("calificarcita.html", form=form)

    #---Menu de consultas Paciente---#
@app.route('/consulta_paciente',methods=["POST"])
def consultap():   
    form = form_pacientec()

    if request.method=="POST":
        xid_paciente = form.id_paciente.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from paciente where id_paciente = ?",[xid_paciente])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("No se Encuentra en la Base de Datos")
                return render_template("calificarcita.html", form=form)        
            return render_template("calificarcita.html", form=form, row = row)
    return render_template("calificarcita.html")

@app.route('/calificacionp',methods=["POST"])
def calificarp():
    form = form_pacientec()
    if request.method=="POST":
        xid_cita = form.id_cita.data
        xcalificacion = form.calificacion.data
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from cita where id_cita = ?",[xid_cita])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:        
                flash ("El id de la cita no existe!!")
                return render_template("calificarcita.html", form=form)  
            else:
                if (row["estado"] == 1 ):    
                   with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
                        cur = con.cursor() #Manipula la conexion a la base de datos
                        cur.execute("update cita set calificacion = ?, estado = 2 where id_cita = ?;",[xcalificacion,xid_cita])
                        con.commit() #Confirma la Transacción 
                   flash ("Grabo calificacion Exitosa")     
                else:
                    if (row["estado"] == 1 ):
                        flash ("La cita no se ha realizado no se puede calificar, no ha sido atendido")                
                    else:
                        flash ("La cita fue calificada exitosamente!")                
                return render_template("calificarcita.html", form=form) 
    return "Error al Actualizar"
        
@app.route('/cpaciente' ,methods=["GET","POST"])
def cpaciente1():
    form = form_pacientec()
    return render_template("consultap.html", form=form)

@app.route('/consulta_p' ,methods=["GET","POST"])
def cpaciente2():
    form = form_pacientec()
    if request.method=="POST":
        xid_paciente = form.id_paciente.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from paciente where id_paciente = ?",[xid_paciente])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("La identificación ingresada no pertenece a la de un paciente -  "+str(xid_paciente))
            return render_template("consultap.html", form=form, row = row)
    return render_template("consultap.html", form=form)

    #---Historia Clinica---#
@app.route('/clinicah' ,methods=["GET","POST"])
def cpaciente5():
    form = form_historia()
    if request.method=="POST":
        xid_paciente = form.id_paciente.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from paciente where id_paciente = ?",[xid_paciente])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("La identificación ingresada no pertenece a la de un paciente -  "+str(xid_paciente))
        with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto
            con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur1 = con1.cursor() #Manipula la conexion a la base de datos
            cur1.execute("select * from historia_clinica where id_paciente = ?",[xid_paciente])   
            row1 = cur1.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row1 is None:
                flash ("No se Encuentra en la Base de Datos la historia clinica del paciente con id: "+str(xid_paciente))        
        with sqlite3.connect("clinica_la_asuncion.db") as con2: #Creo la conexión - with manejador de contexto
            con2.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur2 = con2.cursor()
            cur2.execute("select * from comentario where id_paciente = ?",[xid_paciente])
            row2 = cur2.fetchall()                
        return render_template("historiaclinica.html", form=form, row = row, row1=row1, row2=row2)
    flash ("Fallo Consulta de Historia Clinica")
    return render_template("historiaclinica.html", form=form)

    #---Resumen de Estado de Paciente---#
@app.route('/presumen' ,methods=["GET","POST"])
def cpaciente4():
    form = form_pacientec()
    if request.method=="POST":
        xid_paciente = form.id_paciente.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from paciente where id_paciente = ?",[xid_paciente])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
            return render_template("consultaep.html", form=form, row = row)
    return render_template("consultaep.html", form=form)

    #---Registro de llegada de paciente a la cita---#
@app.route('/registro' ,methods=["GET","POST"])
def cpaciente6():
    form = form_registrop()
    return render_template("registrop.html", form=form)

@app.route('/registroc' ,methods=["GET","POST"])
def cpaciente7():
    form = form_registrop()
    if request.method=="POST":
        xid_paciente = form.id_paciente.data #.data para traer lo que tiene la caja de texto
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            cur.execute("select * from paciente where id_paciente = ?",[xid_paciente])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro           
            if row is None:
                flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
        with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto
            con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur1 = con1.cursor() #Manipula la conexion a la base de datos
            xsql = "select id_cita,fecha,hora_cita,m.id_medico,m.nombre,m.especialidad from cita c ,medico m where m.id_medico = c.id_medico and c.id_paciente = ?"
            cur1.execute(xsql,[xid_paciente])   
            row1 = cur1.fetchall() #Trae de la Base de DAtos 1 solo registro
            matriz =[]
            for i in range(len(row1)):
                matriz.append("")
                for j in range(len(row1[i])):
                    if j == 0  or j== 3:
                        matriz[i]= matriz[i]+" "+str(row1[i][j])
                    else:
                        matriz[i]= matriz[i]+" "+row1[i][j]
            form.eleccion.choices = matriz
            if row1 is None:
                flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
            return render_template("registrop.html", form=form, row1 = row1, row=row)
    return "Fallo Consulta de paciente"

@app.route('/registrop' ,methods=["GET","POST"])
def cpaciente8():
    form = form_registrop()
    xeleccion = form.eleccion.data
    flash ("Eligió "+str(xeleccion))
    vector = xeleccion.split(" ")
    xid_cita = int(vector[1])
    with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            xsql1 = "select id_paciente,id_cita,fecha,hora_cita,m.id_medico,m.nombre,m.especialidad from cita c ,medico m where m.id_medico = c.id_medico and c.id_cita = ?"
            cur.execute(xsql1,[xid_cita])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            if row is None:
                flash ("No se Encuentra en la Base de Datos Cita "+str(row[0]))
            else:    
                with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto
                    xid_paciente = row[0]
                    con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                    cur1 = con1.cursor() #Manipula la conexion a la base de datos
                    xsql1 = "select * from paciente where id_paciente = ?"
                    cur1.execute(xsql1,[xid_paciente])   
                    row1 = cur1.fetchone() #Trae de la Base de DAtos 1 solo registro
                    if row1 is None:
                        flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
                    else: 
                        with sqlite3.connect("clinica_la_asuncion.db") as con2: #Creo la conexión - with manejador de contexto
                            xid_medico = row[4]
                            con2.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                            cur2 = con1.cursor() #Manipula la conexion a la base de datos
                            xsql2 = "select * from turno where id_medico = ?"
                            cur2.execute(xsql2,[xid_medico])   
                            row2 = cur2.fetchall()
                            if row1 is None:
                               form.Nroturno.data = str(xid_medico)+"1"
                            else:
                                form.Nroturno.data = str(xid_medico)+str(len(row2)+1)
                            xid_medico   = row[4]
                            xNroturno    = form.Nroturno.data
                            xestado      = True
                            xid_cita     = row[1]
                            xid_paciente = row[0]
                            xfecha       = row[2]
                            xhora        = row[3]
                            with sqlite3.connect("clinica_la_asuncion.db") as con3: #Creo la conexión - with manejador de contexto
                                cur3 = con3.cursor() #Manipula la conexion a la base de datos
                                cur3.execute("insert into turno(id_medico, turno, estado, id_cita, id_paciente, fecha, hora) values (?, ?, ?, ?, ?, ?, ?)",(xid_medico, xNroturno, xestado, xid_cita, xid_paciente, xfecha, xhora))
                                con3.commit() #Confirma la Transacción SQL
            return render_template("turno.html", form=form, row1 = row1, row=row, row2=row2)
    return "Eligio "+str(xeleccion)+" vector "+vector[1]

    #---Grabar comentarios---#
@app.route('/comentario' ,methods=["GET","POST"])
def cpaciente9():
    form = form_comentario()
    return render_template("comentario.html", form=form)

@app.route('/pcomentario' ,methods=["GET","POST"])
def cpaciente10(): 
    form = form_comentario()
    if request.method=="POST":
       xid_cita = form.id_cita.data     
       with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            xsql1 = "select * from cita where id_cita = ?"
            cur.execute(xsql1,[xid_cita])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro          
            if row is None:
                flash ("No se Encuentra en la Base de Datos Cita "+str(row[0]))
            else:    
                with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto
                    xid_paciente = row[1]
                    con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                    cur1 = con1.cursor() #Manipula la conexion a la base de datos
                    xsql1 = "select * from paciente where id_paciente = ?"
                    cur1.execute(xsql1,[xid_paciente])   
                    row1 = cur1.fetchone() #Trae de la Base de DAtos 1 solo registro
                    if row1 is None:
                        flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
                    else: 
                        with sqlite3.connect("clinica_la_asuncion.db") as con2: #Creo la conexión - with manejador de contexto
                            xid_medico = row[6]
                            con2.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                            cur2 = con1.cursor() #Manipula la conexion a la base de datos
                            xsql2 = "select * from medico where id_medico = ?"
                            cur2.execute(xsql2,[xid_medico])   
                            row2 = cur2.fetchone()
                            if row2 is None:
                               flash ("La identificación ingresada no pertenece a la de un paciente - "+str(xid_paciente))
                            else:
                                return render_template("comentario.html", form=form, row=row, row1=row1, row2=row2)
       return render_template("comentario.html", form=form)

@app.route('/grabarc' ,methods=["GET","POST"])
def cpaciente11():
    form = form_comentario()
    Nro_registros = 0
    if request.method=="POST":
        xid_cita = form.id_cita.data 
        xcomentario = form.comentario.data
        with sqlite3.connect("clinica_la_asuncion.db") as con: #Creo la conexión - with manejador de contexto
            con.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
            cur = con.cursor() #Manipula la conexion a la base de datos
            xsql1 = "select * from cita where id_cita = ?"
            cur.execute(xsql1,[xid_cita])   
            row = cur.fetchone() #Trae de la Base de DAtos 1 solo registro
            xid_paciente = row["id_paciente"]
            xid_medico   = row["id_medico"]
            xsql1 = "select * from historia_clinica where id_paciente = ?"
            cur.execute(xsql1,[xid_paciente])   
            row = cur.fetchone()        
            if row is None:
                xsql1 = "select * from historia_clinica"
                cur.execute(xsql1)   
                row = cur.fetchall()
                if row is None:
                   xid_historia = 1
                else:
                    xid_historia = len(row[0]) + 1           
                xsql1 = "insert into historia_clinica(id_historia, id_paciente, estado) values (?, ?, ?)"
                cur.execute(xsql1,(xid_historia,xid_paciente,1))
                con.commit() #Confirma la Transacción SQL
            else:
                xid_historia = row[0]                   
            with sqlite3.connect("clinica_la_asuncion.db") as con1: #Creo la conexión - with manejador de contexto
                con1.row_factory=sqlite3.Row #Convertir la respuesta de la BD en un diccionario
                cur1 = con1.cursor() #Manipula la conexion a la base de datos
                xsql1 = "select * from historia_clinica"
                cur1.execute(xsql1)   
                row1 = cur1.fetchall() #Trae de la Base de DAtos 1 solo registro
                if row1 is None:
                    Nro_registros = 1
                else:
                    Nro_registro = len(row1[0]) + 1   
                with sqlite3.connect("clinica_la_asuncion.db") as con2:
                     cur2 = con2.cursor() #Manipula la conexion a la base de datos
                     cur2.execute("insert into comentario(id_comentario, id_cita, id_paciente, id_medico, id_historia, comentario) values (?, ?, ?, ?, ?, ?)",(Nro_registro,xid_cita,xid_paciente,xid_medico,xid_historia,xcomentario))
                     con2.commit() #Confirma la Transacción SQL
                flash("Comentario realizado con Exito!!")
    return render_template("comentario.html", form=form)

    #---Cerrar sesion---#
@app.route('/logout')
def logout():
    session.pop('email', None)   #--Destruir despues de cerrar--
    return redirect(url_for('login'))

@app.before_request #Se ejecuta antes de cualquier petición que se va a hacer
def comienzo(): #No deja entrar a otra ruta diferente a la del login
    if "email" not in session and request.endpoint in["comentario","registro","consulta_medico","patients","dashboard","admin","Roles","medic","asignarH","consultam","grabarh","menucitas","crearCita","editar_cita","update","eliminar_cita","citai1","consultap","calificarp","cpaciente1","cpaciente2","registroLlegada"]:
        return redirect(url_for("home"))
        
if __name__ == '__main__':
    app.run(debug = True)
 