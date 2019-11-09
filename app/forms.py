from flask_wtf import FlaskForm
from wtforms import TextField,ValidationError,SelectField,StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField
from app.models import Category

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(1,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(1,60)])
    category = SelectField('分类',coerce=int,default=1)
    body = CKEditorField('内容',validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self):
        super(PostForm, self).__init__()
        self.category.choices = [(category.id,category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('分类名称',validators=[DataRequired(),Length(1,30)])
    submit = SubmitField()

    def validate_name(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类名称已存在')

class BloginfoFrom(FlaskForm):
    blog_title = StringField('博客标题',validators=[DataRequired(),Length(1,60)])
    blog_sub_title = StringField('博客副标题',validators=[DataRequired(),Length(1,100)])
    name = StringField('拥有者',validators=[Length(1,30)])
    about = CKEditorField('关于',validators=[DataRequired()])
    submit = SubmitField()

class AdminForm(FlaskForm):
    username = StringField('重设管理员账号',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('重设密码',validators=[DataRequired(),Length(1,128)])
    submit = SubmitField('提交')



