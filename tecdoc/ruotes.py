from flask import redirect, render_template, request

from tecdoc import app, mysql


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET' and request.args.get('search'):
        article = str(request.args.get('search'))
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT suppliers.description, articles.FoundString, articles.price,\
        articles.model, articles.NormalizedDescription, articles.quantity, suppliers.id as suppliers_id\
        FROM articles \
        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
        WHERE model = %s OR FoundString = %s LIMIT 20", ([article,article]))
        if result > 0:
            data = cursor.fetchall()
            return render_template('index.html', data=data)
    return render_template('index.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    cursor = mysql.connection.cursor()
    if request.method == 'GET' and request.args.get('submit')=='Поиск':
        article_dirty = str(request.args.get('article'))
        article = "".join(c for c in article_dirty if c.isalnum())
        
        cursor.execute("SELECT suppliers.description, articles.DataSupplierArticleNumber,\
            articles.FoundString, articles.NormalizedDescription, suppliers.id as suppliers_id\
            FROM articles \
            LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
            WHERE FoundString = %s", ([article]))
        all_articles_suppliers = cursor.fetchall()
        return render_template('info.html', all_articles_suppliers=all_articles_suppliers)
    if request.method == 'GET' and request.args.get('submit')=='Поиск кроссов':
        article = str(request.args.get('article'))
        brand = str(request.args.get('brand_id'))
        cursor.execute("SELECT DISTINCT s.description as brand, c.PartsDataSupplierArticleNumber FROM article_oe a \
					JOIN manufacturers m ON m.id=a.manufacturerId\
					JOIN article_cross c ON c.OENbr=a.OENbr\
					JOIN suppliers s ON s.id=c.SupplierId\
					WHERE a.datasupplierarticlenumber=%s AND a.supplierid=%s  ORDER BY `brand` ASC", ([article,brand]))
        data_crosses = cursor.fetchall()

        cursor.execute("SELECT article_images.Description, article_images.PictureName, articles.NormalizedDescription, suppliers.description, suppliers.id as suppliers_id,\
                        articles.DataSupplierArticleNumber FROM article_images\
                        LEFT JOIN articles ON articles.DataSupplierArticleNumber=article_images.DataSupplierArticleNumber AND articles.supplierId=article_images.supplierId\
                        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
                        WHERE article_images.DataSupplierArticleNumber=%s  AND article_images.supplierId=%s\
                        AND article_images.PictureName LIKE %s LIMIT 1;" , ([article,brand,'%.JPG']))
        data_image = cursor.fetchall()
        cursor.execute("SELECT description, displayvalue FROM article_attributes WHERE datasupplierarticlenumber=%s AND supplierid=%s;" , ([article,brand]))
        data_article = cursor.fetchall()
        return render_template('info.html', data_crosses=data_crosses, data_image=data_image, data_article=data_article)
    return render_template('info.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')