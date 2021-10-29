from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length

class form_registrop(FlaskForm):
    id_paciente = IntegerField("Id Paciente",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    buscarr = SubmitField("Buscar", render_kw={"onmouseover":"buscar_pacienter()"})
    nombre = StringField("Nombre: ")
    apellido = StringField("Apellido: ")
    estado_salud = StringField("Estado de Salud: ")
    id_cita =  IntegerField("Id Cita",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    fecha = StringField("Fecha")
    hora_cita = StringField("Hora: ")
    id_medico = IntegerField("Id Medico")
    nombrem = StringField("nombre: ")
    apellidom = StringField("apellido: ")
    especialidad = StringField("especialidad: ")
    eleccion = RadioField("")
    actualizarr = SubmitField("Grabar", render_kw={"onmouseover":"guardar_registro()"})
    Nroturno =  StringField("Numero Turno: ")
    retorno = SubmitField("Asignar", render_kw={"onmouseover":"regresar()"})