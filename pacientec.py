from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class form_pacientec(FlaskForm):
    id_paciente = IntegerField("Id Paciente",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    buscarp = SubmitField("Buscar", render_kw={"onmouseover":"buscar_paciente()"})
    nombre = StringField("Nombre: ") #, validators=[DataRequired(message = "No dejar vacio, completar")])
    apellido = StringField("Apellido: ") #, choices=[("Cilco 1"),("Cilco 2"),("Cilco 3"),("Cilco 4")])
    estado_salud = StringField("Estado de Salud: ") #, validators=[DataRequired(message = "No dejar vacio, completar"), Length(max=1)])
    id_cita =  IntegerField("Id Cita",validators=[DataRequired(message="Por Favor Ingrese Solo Números")])
    calificacion =  SelectField("Calificacion Cita", choices=[("Excelente"),("Buena"),("Regular"),("Mala"),("Pesima")])
    actualizar = SubmitField("Grabar", render_kw={"onmouseover":"guardar_calificacion()"})  
    buscarpaciente = SubmitField("Buscar", render_kw={"onmouseover":"buscar_paciente1()"})
    resumenp = SubmitField("Resumen Estado salud", render_kw={"onmouseover":"resumen()"})  
    hclinicap = SubmitField("Historia Clinica", render_kw={"onmouseover":"hclinica()"}) 
    retornar = SubmitField("Retornar", render_kw={"onmouseover":"retornarp()"})
