from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, IntegerField
from wtforms.validators import Required, Length
import Utilidades


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class SaludarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('Saludar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class ClientesFiltroForm(FlaskForm):	
    """
    Funcion para inicializar formulario de ventas
    se requiere que
    		el producto tenga longitud de 5 caracteres como mínimo (letras)
			el cliente tenga longitud de 3 caracteres como mínimo (letras, por ejemplo, SOL
			el precio unitario tenga longitud de 1 caracter como mínimo (numerico)
			la cantidad tenga longitud de 1 caracter como mínimo (numerico)
    """
    txtPais = StringField('País', validators=[Length(min=15)], render_kw={"placeholder": "Buscar Clientes"})
    btnBuscar = SubmitField('Buscar Clientes')
    