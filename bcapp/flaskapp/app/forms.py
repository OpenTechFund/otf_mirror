from wtforms import (StringField, TextAreaField, SubmitField, 
                     BooleanField, SelectField, SelectMultipleField,
                     FileField, widgets)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email Address')
    active = BooleanField('Active?')
    admin = BooleanField('Admin?')
    password = StringField('New Password')
    domain_group_id = SelectField('Domain Group', coerce=int)
    submit = SubmitField('Edit User')

class DomainForm(FlaskForm):
    domain = StringField('Domain')
    ext_ignore = StringField('Extensions to ignore')
    paths_ignore = StringField('Paths to ignore')
    s3_storage_bucket = StringField('S3 Storage Bucket')
    submit = SubmitField('Edit Domain')

class DomainGroupForm(FlaskForm):
    name = StringField('Name')
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')