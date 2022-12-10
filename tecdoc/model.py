from tecdoc import mysql

class ArticleInfo():

    def __init__(self):
        self.cursor = mysql.connection.cursor()
    
    def serch_article(self, article):
        self.cursor.execute("SELECT suppliers.description, articles.DataSupplierArticleNumber,\
            articles.FoundString, articles.NormalizedDescription, suppliers.id as suppliers_id\
            FROM articles \
            LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
            WHERE FoundString = %s", ([article]))
        self.all_articles_suppliers = self.cursor.fetchall()
        return self.all_articles_suppliers

    def search_crosses(self, article, brand_id):
        self.cursor.execute("SELECT DISTINCT s.description as brand, c.PartsDataSupplierArticleNumber FROM article_oe a \
					JOIN manufacturers m ON m.id=a.manufacturerId\
					JOIN article_cross c ON c.OENbr=a.OENbr\
					JOIN suppliers s ON s.id=c.SupplierId\
					WHERE a.datasupplierarticlenumber=%s AND a.supplierid=%s  ORDER BY `brand` ASC", ([article,brand_id]))
        self.data_crosses = self.cursor.fetchall()
        return self.data_crosses

    def serch_article_info(self, article, brand_id):
        self.cursor.execute("SELECT article_images.Description, article_images.PictureName, articles.NormalizedDescription, suppliers.description, suppliers.id as suppliers_id,\
                        articles.DataSupplierArticleNumber FROM article_images\
                        LEFT JOIN articles ON articles.DataSupplierArticleNumber=article_images.DataSupplierArticleNumber AND articles.supplierId=article_images.supplierId\
                        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
                        WHERE article_images.DataSupplierArticleNumber=%s  AND article_images.supplierId=%s\
                        AND article_images.PictureName LIKE %s LIMIT 1;" , ([article,brand_id,'%.JPG']))
        self.article_info = self.cursor.fetchall()
        return self.article_info

    def serch_article_desc(self, article, brand_id):
        self.cursor.execute("SELECT description, displayvalue FROM article_attributes WHERE datasupplierarticlenumber=%s AND supplierid=%s;" , ([article,brand_id]))
        self.article_desc = self.cursor.fetchall()
        return self.article_desc

    def search_article_from_model(self, model):
        self.cursor.execute("SELECT suppliers.description, articles.FoundString, articles.price,\
        articles.model, articles.NormalizedDescription, articles.quantity, suppliers.id as suppliers_id\
        FROM articles \
        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
        WHERE model = %s", ([model]))
        self.article_from_model = self.cursor.fetchall()
        return self.article_from_model