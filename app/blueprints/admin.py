from flask import Blueprint,url_for,flash,render_template,request,current_app,redirect
from flask_login import login_required
from app.models import Post,Category,Bloginfo,Admin
from app.extentions import db
from app.forms import PostForm,CategoryForm,BloginfoFrom,AdminForm

admin_bp = Blueprint('admin',__name__)

# admin下全部请求均需登录
@admin_bp.before_request
@login_required
def login_protect():
    pass

@admin_bp.route('/')
def index():
    posts_num = Post.query.count()
    categories_num = Category.query.count()
    return render_template('admin/index.html',posts_num=posts_num,categories_num=categories_num)

@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['APP_MANEGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html',pagination=pagination,posts=posts)

@admin_bp.route('/post/new',methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        body_html = request.form['fancy-editormd-html-code']
        category = Category.query.get(form.category.data)
        post = Post(title=title,body=body,body_html=body_html,category=category)
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功')
        return redirect(url_for('blog.show_post',post_id = post.id))
    return render_template('admin/new_post.html',form=form)


@admin_bp.route('/post/edit/<int:post_id>',methods=['GET','POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.body_html = request.form['fancy-editormd-html-code']
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('文章更新成功')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.body_html.data = post.body_html
    form.category.data = post.category_id
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/delete/<int:post_id>',methods=['POST'])
def delete_post(post_id):
    post= Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('.manage_post'))

@admin_bp.route('/category/new',methods=['GET','POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('添加分类成功')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html',form = form)


@admin_bp.route('/category/manage')
def manage_category():
    categories = Category.query.order_by(Category.id).all()
    return render_template('admin/manage_category.html',categories=categories)


@admin_bp.route('/category/edit/<int:category_id>',methods=['GET','POST'])
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name=form.name.data
        db.session.commit()
        flash('修改分类成功')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/delete/<int:category_id>',methods=['POST'])
def delete_category(category_id):
    if category_id == 1:
        flash('不能删除默认分类')
        return redirect(url_for('.manage_category'))
    category = Category.query.get_or_404(category_id)
    if category.posts:
        flash('该分类下有文章，不能直接删除')
        return redirect(url_for('.manage_category'))
    db.session.delete(category)
    db.session.commit()
    flash('删除分类成功')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/settings',methods=['GET','POST'])
def settings():
    form = BloginfoFrom()
    bloginfo = Bloginfo.query.first()
    if form.validate_on_submit():
        bloginfo.blog_title = form.blog_title.data
        bloginfo.blog_sub_title = form.blog_sub_title.data
        bloginfo.name = form.name.data
        bloginfo.about = form.about.data
        db.session.commit()
        flash('修改博客数据成功')
        return redirect(url_for('.index'))
    form.blog_title.data = bloginfo.blog_title
    form.blog_sub_title.data = bloginfo.blog_sub_title
    form.name.data = bloginfo.name
    form.about.data = bloginfo.about
    return render_template('admin/settings.html',form=form)

@admin_bp.route('/admininfo',methods=['GET','POST'])
def admininfo():
    form = AdminForm()
    admininfo = Admin.query.first()
    if form.validate_on_submit():
        admininfo.username = form.username.data
        admininfo.password = admininfo.set_password(form.password.data)
        db.session.commit()
        flash('修改管理员成功')
        return redirect(url_for('.index'))
    form.username.data = admininfo.username
    return render_template('admin/admininfo.html',form=form)






