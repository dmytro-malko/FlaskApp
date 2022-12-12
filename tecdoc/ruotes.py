from flask import redirect, render_template, request, flash, session

from tecdoc import app
from .model import ArticleInfo, UserData


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET' and request.args.get('search'):
        article = str(request.args.get('search'))
        article_from_model = ArticleInfo().search_article_from_model(article)
        return render_template('index.html', article_from_model=article_from_model)
    return render_template('index.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'GET' and request.args.get('submit')=='Поиск':
        article_dirty = str(request.args.get('article'))
        article = "".join(c for c in article_dirty if c.isalnum())
        
        all_articles_suppliers = ArticleInfo().serch_article(article)

        return render_template('info.html', all_articles_suppliers=all_articles_suppliers)
    
    if request.method == 'GET' and request.args.get('submit')=='Поиск кроссов':
        article = str(request.args.get('article'))
        brand = str(request.args.get('brand_id'))

        article_crosses = ArticleInfo().search_crosses(article, brand)
        article_info = ArticleInfo().serch_article_info(article, brand)
        article_desc = ArticleInfo().serch_article_desc(article, brand)

        return render_template('info.html', article_crosses=article_crosses, article_info=article_info, article_desc=article_desc)
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
            session['login'] = user['login']
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
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/users', methods=['GET', 'POST'])
def users():
    if request.method=='POST':
        if 'user-id' in request.form:
            user_data = request.form
            delete_user = UserData().delete_user(user_data)
            flash(delete_user, 'success')
            return render_template('/admin/users.html')
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
def edit_user(id):
    user = UserData().get_user_data(id)
    if request.method=='POST':
        user_data = request.form
        UserData().update_user_data(user_data)
        return users()
    return render_template('/admin/edit-user.html', user=user)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')