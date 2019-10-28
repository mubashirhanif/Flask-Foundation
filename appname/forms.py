from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, FieldList, FormField
from wtforms import validators
import re
# from .models import User


# class LoginForm(Form):
#     username = TextField(u'Username', validators=[validators.required()])
#     password = PasswordField(u'Password', validators=[validators.optional()])

#     def validate(self):
#         check_validate = super(LoginForm, self).validate()

#         # if our validators do not pass
#         if not check_validate:
#             return False

#         # Does our the exist
#         user = User.query.filter_by(username=self.username.data).first()
#         if not user:
#             self.username.errors.append('Invalid username or password')
#             return False

#         # Do the passwords match
#         if not user.check_password(self.password.data):
#             self.username.errors.append('Invalid username or password')
#             return False

#         return True

# class InterfaceForm(FlaskForm):
#     ip = TextField(u'IP', validators=[validators.required()])
#     interface_name = TextField(u'Interface Name', validators=[validators.required()])

#     def validate(self):
#         check_validate = super(InterfaceForm, self).validate()

#         if not check_validate:
#             return False
#         _match_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",self.ip.data)

#         if not _match_ip:
#             self.ip.errors.append('IP address invalid')

class IPRegistrationForm(FlaskForm):
    
    username = TextField(u'Username', validators=[validators.required()])
    hostname = TextField(u'Hostname', validators=[validators.required()])
    # interface = FormField(InterfaceForm)
    ip = TextField(u'IP', validators=[validators.required()])
    interface_name = TextField(u'Interface Name', validators=[validators.required()])

    def validate(self):
        check_validate = super(IPRegistrationForm, self).validate()

        if not check_validate:
            return False
        _match_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",self.ip.data)

        if not _match_ip:
            self.ip.errors.append('IP address invalid')
            return False

        return True
