from flask import redirect, render_template, request

from tecdoc import app, mysql
from .model import ArticleInfo


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
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')