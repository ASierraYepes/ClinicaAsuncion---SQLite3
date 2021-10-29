from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class form_horariom(FlaskForm):
    fecha = IntegerField("Id Medico",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    hora_inicial = StringField("Nombre: ")
    hora_final = StringField("Apellido: ")
    actualizar = SubmitField("Acepta", render_kw={"onmouseover":"buscar_medico()"})