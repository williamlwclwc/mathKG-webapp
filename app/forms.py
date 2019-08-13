from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                    Form, TextField, TextAreaField, IntegerField, SelectField, validators)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sys
sys.path.append('../utils/')
from utils.login_util import query_user


class node_form(Form):
    node_name = TextField("node_name", [validators.InputRequired()])
    category = SelectField(
        "category", validators=[validators.Optional()],
        choices=[("", ""), ("0", "0"), ("1", "1")])
    url = TextField("url", [validators.Optional()])
    content = TextAreaField("content", [validators.Optional()])
    notes = TextAreaField("notes", [validators.Optional()])
    add_node = SubmitField("Add Node")
    edit_node = SubmitField("Edit Node")
    delete_node = SubmitField("Delete Node")


class edge_form(Form):
    key_num = TextField("key_num", [validators.Optional()])
    source_name = TextField("source_name", [validators.InputRequired()])
    target_name = TextField("target_name", [validators.InputRequired()])
    relationship = SelectField(
        "relationship", validators=[validators.Optional()],
        choices=[("", ""), ("contain", "contain"), ("arithmetic operation", "arithmetic operation"),
        ("property", "property"), ("algorithm", "algorithm"), ("application", "application"), 
        ("example", "example"), ("expression", "expression"), ("theorem", "theorem"), 
        ("conjecture", "conjecture"), ("proof", "proof"), ("proof methods", "proof methods"),
        ("corollary", "corollary"), ("formula", "formula")])
    content = TextAreaField("content", [validators.Optional()])
    notes = TextAreaField("notes", [validators.Optional()])
    add_edge = SubmitField("Add Edge")
    edit_edge = SubmitField("Edit Edge")
    delete_edge = SubmitField("Delete Edge")


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = query_user(username)
        if user is not None:
            raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')