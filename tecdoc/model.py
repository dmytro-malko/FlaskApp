from werkzeug.security import check_password_hash, generate_password_hash


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
        self.cursor.close()
        return self.all_articles_suppliers

    def search_crosses(self, article, brand_id):
        self.cursor.execute("SELECT DISTINCT s.description as brand, c.PartsDataSupplierArticleNumber FROM article_oe a \
					JOIN manufacturers m ON m.id=a.manufacturerId\
					JOIN article_cross c ON c.OENbr=a.OENbr\
					JOIN suppliers s ON s.id=c.SupplierId\
					WHERE a.datasupplierarticlenumber=%s AND a.supplierid=%s  ORDER BY `brand` ASC", ([article,brand_id]))
        self.data_crosses = self.cursor.fetchall()
        self.cursor.close()
        return self.data_crosses

    def serch_article_info(self, article, brand_id):
        self.cursor.execute("SELECT article_images.Description, article_images.PictureName, articles.NormalizedDescription, suppliers.description, suppliers.id as suppliers_id,\
                        articles.DataSupplierArticleNumber FROM article_images\
                        LEFT JOIN articles ON articles.DataSupplierArticleNumber=article_images.DataSupplierArticleNumber AND articles.supplierId=article_images.supplierId\
                        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
                        WHERE article_images.DataSupplierArticleNumber=%s  AND article_images.supplierId=%s\
                        AND article_images.PictureName LIKE %s LIMIT 1;" , ([article,brand_id,'%.JPG']))
        self.article_info = self.cursor.fetchall()
        self.cursor.close()
        return self.article_info

    def serch_article_desc(self, article, brand_id):
        self.cursor.execute("SELECT description, displayvalue FROM article_attributes WHERE datasupplierarticlenumber=%s AND supplierid=%s;" , ([article,brand_id]))
        self.article_desc = self.cursor.fetchall()
        self.cursor.close()
        return self.article_desc

    def search_article_from_model(self, model):
        self.cursor.execute("SELECT suppliers.description, articles.FoundString, articles.price,\
        articles.model, articles.NormalizedDescription, articles.quantity, suppliers.id as suppliers_id\
        FROM articles \
        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
        WHERE model = %s", ([model]))
        self.article_from_model = self.cursor.fetchall()
        self.cursor.close()
        return self.article_from_model

class UserData(ArticleInfo):
        
    def create_user(self, user_data):
        login = user_data['login']
        password = generate_password_hash(user_data['password'])
        is_admin = user_data['is-admin']
        first_name = user_data['first-name']
        last_name = user_data['last_name']
        email = user_data['email']
        phone = user_data['phone']
        try:
            self.cursor.execute("INSERT INTO `users`(`login`, `password`, `is_admin`, `first_name`, `last_name`, `email`, `phone`)\
                                VALUES (%s,%s,%s,%s,%s,%s,%s)" , (login, password, is_admin, first_name, last_name, email, phone))
            mysql.connection.commit()
            self.cursor.close()
            return "Пользователь успешно добавлен"
        except:
            pass

    def update_user_data(self, user_data):
        user_id = user_data['user_id']
        login = user_data['login']
        password = generate_password_hash(user_data['password'])
        is_admin = user_data['is-admin']
        first_name = user_data['first-name']
        last_name = user_data['last_name']
        email = user_data['email']
        phone = user_data['phone']
        self.cursor.execute(f"UPDATE `users` SET `login`={login},`password`={password},`is_admin`={is_admin},`first_name`={first_name},\
                             `last_name`={last_name},`email`={email},`phone`={phone} WHERE `id`={user_id}")

    def check_user_data(self, user_data):
        login = user_data['login']
        password = generate_password_hash(user_data['password'])
        try:
            result = self.cursor.execute(f"SELECT * FROM users WHERE login={login}")
            if result > 0:
                user = self.cursor.fetchone()
                if check_password_hash(user['password'], password):
                    return user
                else:
                    self.cursor.close()
                    return 'Не верный пароль'
        except:
            self.cursor.close()
            return 'Не верный логин'


    def check_users_data(self):
        self.results = self.cursor.execute("SELECT * FROM users")
        if self.results > 0:
            users = self.cursor.fetchall()
            self.cursor.close()
            return users
        else:
            self.cursor.close()
            return "Пользователей не найденно"

    def delete_user(self, user_data):
        user_id = user_data['user_id']
        self.cursor.execute("DELETE FROM users WHERE id=%s" , ([user_id]))
        mysql.connection.commit()
        self.cursor.close()
        return "Данные успешно удалены"