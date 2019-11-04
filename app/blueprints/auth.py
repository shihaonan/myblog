from flask import Blueprint
auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login')
def login():
    return '登录成功'

@auth_bp.route('/logout')
def logout():
    pass

