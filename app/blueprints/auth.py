from flask import Blueprint,render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user, login_required, current_user
from app.models import Admin
from app.forms import LoginForm

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin,form.remember.data)
            next = request.args.get('next')
            if next is None:
                next = url_for('admin.index')
            flash('欢迎来到后台~')
            return redirect(next)
        flash('错误的账号或密码')
    return render_template('auth/login.html',form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出')
    return redirect(url_for('blog.index'))

