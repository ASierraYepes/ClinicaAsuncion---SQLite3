from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length

class form_comentario(FlaskForm):
    id_cita =  IntegerField("Id Cita",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    buscarcita = SubmitField("Buscar", render_kw={"onmouseover":"buscar_cita()"})
    comentario= StringField("Comentario : ")
    grabarc = SubmitField("Grabar", render_kw={"onmouseover":"grabarc()"})