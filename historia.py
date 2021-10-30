from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class form_historia(FlaskForm):
    id_paciente = IntegerField("Id Paciente",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    buscarp1 = SubmitField("Buscar", render_kw={"onmouseover":"buscar_pacienteh()"})
    nombre = StringField("Nombre: ")
    apellido = StringField("Apellido: ")
    estado_salud = StringField("Estado de Salud: ") 
