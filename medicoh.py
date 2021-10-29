from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class form_medicoh(FlaskForm):
    id_medico = IntegerField("Id Medico",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    consultar = SubmitField("Acepta", render_kw={"onmouseover":"buscar_medico()"})
    nombre = StringField("Nombre: ")
    apellido = StringField("Apellido: ")
    especialidad = StringField("Especialidad: ")
    fecha =  StringField("Fecha",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    hora_inicial = StringField("Hora Inicial: ",validators=[DataRequired(message = "No dejar vacio, completar")])
    hora_final = StringField("Hora Final: ",validators=[DataRequired(message = "No dejar vacio, completar")])
    actualizar = SubmitField("Grabar", render_kw={"onmouseover":"guardar_horario()"})  