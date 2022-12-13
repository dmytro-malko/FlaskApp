from werkzeug.security import check_password_hash, generate_password_hash


from tecdoc import mysql

class ArticleInfo():

    def __init__(self):
        self.cursor = mysql.connection.cursor()
        self.close_connection = self.cursor.close

    def serch_article(self, article):
        self.cursor.execute("SELECT suppliers.id, suppliers.description, articles.DataSupplierArticleNumber,\
            articles.FoundString, articles.NormalizedDescription, suppliers.id as suppliers_id\
            FROM articles \
            LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
            WHERE FoundString = %s", ([article]))
        self.all_articles_suppliers = self.cursor.fetchall()
        return self.all_articles_suppliers

    def search_crosses(self, article, brand_id):
        self.cursor.execute("SELECT DISTINCT s.id, s.description as brand, c.PartsDataSupplierArticleNumber FROM article_oe a \
					JOIN manufacturers m ON m.id=a.manufacturerId\
					JOIN article_cross c ON c.OENbr=a.OENbr\
					JOIN suppliers s ON s.id=c.SupplierId\
					WHERE a.datasupplierarticlenumber=%s AND a.supplierid=%s  ORDER BY `brand` ASC", ([article,brand_id]))
        self.data_crosses = self.cursor.fetchall()
        return self.data_crosses

    def serch_article_info(self, article, brand_id):
        self.cursor.execute("SELECT articles.NormalizedDescription, suppliers.description, suppliers.id as suppliers_id,\
                        articles.DataSupplierArticleNumber FROM articles\
                        LEFT JOIN suppliers ON suppliers.id=articles.supplierId\
                        WHERE articles.DataSupplierArticleNumber=%s  AND articles.supplierId=%s LIMIT 1;" , ([article,brand_id]))
        self.article_info = self.cursor.fetchall()
        return self.article_info

    def get_article_img(self, article, brand_id):
        self.cursor.execute("SELECT PictureName FROM article_images WHERE DataSupplierArticleNumber=%s  AND supplierId=%s AND PictureName LIKE %s" , ([article,brand_id,'%.JPG']))
        self.article_img = self.cursor.fetchall()
        return self.article_img

    def serch_article_desc(self, article, brand_id):
        self.cursor.execute("SELECT id, description, displayvalue FROM article_attributes WHERE datasupplierarticlenumber=%s AND supplierid=%s;" , ([article,brand_id]))
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

    def get_list_manufacturers(self):
        self.cursor.execute("SELECT DISTINCT id, fulldescription FROM `manufacturers` ORDER BY `manufacturers`.`fulldescription` ASC;")
        self.list_manufacturers = self.cursor.fetchall()
        return self.list_manufacturers

    def get_article_applicability(self, article, brand_id):
        self.cursor.execute("SELECT DISTINCT models.fulldescription, models.constructioninterval FROM `article_li`\
                            JOIN cars ON cars.cars_id=article_li.linkageId JOIN models ON cars.model_id=models.id\
                            WHERE DataSupplierArticleNumber=%s AND supplierId=%s  ORDER BY `models`.`fulldescription` ASC", ([article,brand_id]))
        self.article_applicability = self.cursor.fetchall()
        return self.article_applicability
class UserData(ArticleInfo):
        
    def create_user(self, user_data):
        login = user_data['login']
        password = generate_password_hash(user_data['password'])
        if 'is-admin' in user_data:
            is_admin = user_data['is-admin']
        else:
            is_admin = 0
        first_name = user_data['first-name']
        last_name = user_data['last-name']
        email = user_data['email']
        phone = user_data['phone']
        if user_data['password'] == user_data['confirmPassword']:
            try:
                self.cursor.execute("INSERT INTO `users`(`login`, `password`, `is_admin`, `first_name`, `last_name`, `email`, `phone`)\
                                    VALUES (%s,%s,%s,%s,%s,%s,%s)" , (login, password, is_admin, first_name, last_name, email, phone))
                mysql.connection.commit()
                self.results = self.cursor.execute("SELECT * FROM users")
                users = self.cursor.fetchall()
                self.cursor.close()
                return users
            except:
                return "Произошла ошибка!!! Проверьте правильность заполнения формы!!!"
        else:
            return "Пароли не одинаковые!!!!"

    def update_user_data(self, user_data):
        user_id = user_data['user-id']
        login = user_data['login']
        if 'is-admin' in user_data:
            is_admin = user_data['is-admin']
        else:
            is_admin = 0
        first_name = user_data['first-name']
        last_name = user_data['last-name']
        email = user_data['email']
        phone = user_data['phone']
        self.cursor.execute(f"UPDATE `users` SET `login`='{login}',`is_admin`='{is_admin}',`first_name`='{first_name}',\
                             `last_name`='{last_name}',`email`='{email}',`phone`='{phone}' WHERE `id`='{user_id}'")
        mysql.connection.commit()
        self.cursor.close()

    def check_user_login(self, user_data):
        login = user_data['login']
        password = user_data['password']
        try:
            result = self.cursor.execute(f"SELECT * FROM users WHERE login='{login}'")
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

    def get_user_data(self, id):
        self.cursor.execute(f"SELECT * FROM users WHERE id={id}")
        user = self.cursor.fetchone()
        return user

    def delete_user(self, user_data):
        user_id = user_data['user-id']
        self.cursor.execute("DELETE FROM users WHERE id=%s" , ([user_id]))
        mysql.connection.commit()
        self.cursor.close()
        return "Данные успешно удалены"