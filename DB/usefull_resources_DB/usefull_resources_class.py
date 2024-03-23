import psycopg2

class UsefulResources:
    def __init__(self, res_name, article_name, res_url):
        self.res_name = res_name
        self.article_name = article_name
        self.res_url = res_url
        self.connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
        self.cursor = self.connection.cursor()

    def __str__(self):
        return f'{self.res_name} - {self.article_name} - {self.res_url}'

    def save(self):
        try:
            query = f"insert into usefull_resources(resource_name,article_name,resource_url) values('{self.res_name}','{self.article_name}','{self.res_url}');"
            self.cursor.execute(query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item saved successfully!")
        except psycopg2.Error as error:
            print(f"Error while saving item:", error)

    def delete(self):
        try:
            self.cursor.execute(f"DELETE from usefull_resources WHERE resource_name = '{self.res_name}';")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item deleted successfully!")
        except psycopg2.Error as e:
            print("Error while deleting item:", e)

    def update(self, res_name=None, res_url=None, article_name=None):
        try:
            if res_name is None:
                res_name = self.res_name
            if res_url is None:
                res_url = self.res_url
            if article_name is None:
                score = self.article_name
            update_query = f"UPDATE usefull_resources SET resource_name = '{res_name}', resource_url = '{res_url}', article_name = {article_name} WHERE resource_name = '{self.res_name}' and resource_url = '{self.res_url}';"
            self.cursor.execute(update_query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item updated successfully!")
        except psycopg2.Error as e:
            print("Error while updating item:", e)


if __name__ == '__main__':
    resource = UsefulResources('Anti Defamation League', 'TikTok Ban Feared, Antisemitic Conspiracy Theories Follow','https://www.adl.org/resources/blog/tiktok-ban-feared-antisemitic-conspiracy-theories-follow')
    resource.save()
    # resource.delete()
    # resource.update(score=9)



