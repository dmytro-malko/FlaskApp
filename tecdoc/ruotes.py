from functools import wraps
from flask import redirect, render_template, request, flash, session

from tecdoc import app
from .model import ArticleInfo, UserData


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("login"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")
    return decorated_func

def admin_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("is_admin"):
            return f(*args, **kwargs)
        else:
            flash('Нет доступа!!!', 'danger')
            return redirect("/")
    return decorated_func

@app.route('/', methods=['GET', 'POST'])
# @logged_in
def main():
    if request.method == 'GET' and request.args.get('search'):
        article = str(request.args.get('search'))
        article_from_model = ArticleInfo().search_article_from_model(article)
        return render_template('index.html', article_from_model=article_from_model)
    return render_template('index.html')

@app.route('/info', methods=['GET', 'POST'])
# @logged_in
def info():
    info = ArticleInfo()

    if request.method == 'GET' and request.args.get('article') and request.args.get('brand_id'):
        article = str(request.args.get('article'))
        brand = str(request.args.get('brand_id'))
        
        article_crosses = info.search_crosses(article, brand)
        article_info = info.serch_article_info(article, brand)
        article_desc = info.serch_article_desc(article, brand)
        article_img = info.get_article_img(article, brand)
        info.close_connection()

        return render_template('info.html', article_crosses=article_crosses, article_info=article_info, article_desc=article_desc, article_img=article_img)

    elif request.method == 'GET' and request.args.get('article'):
        article_dirty = str(request.args.get('article'))
        article = "".join(c for c in article_dirty if c.isalnum())
        
        all_articles_suppliers = info.serch_article(article)
        
        info.close_connection()
        return render_template('info.html', all_articles_suppliers=all_articles_suppliers)

    return render_template('info.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user_details = request.form
        user = UserData().check_user_login(user_details)
        if type(user)==str:
            flash(user, 'danger')
            return render_template('login.html')
        elif user:
            session['login'] = True
            session['user_id'] = user['id']
            session['user_name'] = user['login']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            if user['is_admin'] == 1:
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            return redirect('/')
        else:
            flash('Данные введены не верно', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin')
# @admin_in
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/users', methods=['GET', 'POST'])
# @admin_in
def users():
    if request.method=='POST':
        if 'user-id' in request.form:
            user_data = request.form
            delete_user = UserData().delete_user(user_data)
            flash(delete_user, 'success')
            return redirect('/admin/users')
        else:
            user_data = request.form
            users_data = UserData().create_user(user_data)
            #flash(add_user, 'success')
            return render_template('/admin/users.html', users_data=users_data)
    users_data = UserData().check_users_data()
    if type(users_data) == str:
        flash(users_data, 'danger')
        return render_template('/admin/users.html')
    else:
        return render_template('/admin/users.html', users_data=users_data)

@app.route('/admin/edit-user/<int:id>', methods=['GET','POST'])
# @admin_in
def edit_user(id):
    user = UserData().get_user_data(id)
    if request.method=='POST':
        user_data = request.form
        UserData().update_user_data(user_data)
        return redirect('/admin/users')
    return render_template('/admin/edit-user.html', user=user)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')