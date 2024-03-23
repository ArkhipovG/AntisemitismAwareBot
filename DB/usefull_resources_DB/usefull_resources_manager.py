import psycopg2


class ResourcesManager:
    @classmethod
    def get_by_name(cls, resource_name):
        try:
            connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
            cursor = connection.cursor()
            select_query = f"SELECT * FROM usefull_resources WHERE resource_name = '{resource_name}'"
            cursor.execute(select_query)
            item = cursor.fetchone()
            cursor.close()
            connection.close()
            res_name = item[1]
            article_name = item[2]
            resource_url = item[3]
            stroke = f'Resource name: {res_name}\nArticle: {article_name}\nURL: {resource_url}\n'
            if item:
                return stroke
            else:
                return None
        except psycopg2.Error as e:
            print("Error while fetching item by name:", e)
            return None

    @classmethod
    def all_items(cls):
        try:
            connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
            cursor = connection.cursor()
            select_query = f"SELECT * FROM usefull_resources"
            cursor.execute(select_query)
            items = cursor.fetchall()
            cursor.close()
            connection.close()
            item_str = ''
            for num,item in enumerate(items):
                item_str += f'Resource №{num+1}:\nResource name: {str(item[1])}\nArticle: {str(item[2])}\nURL: {str(item[3])}\n'
                item_str += '\n'
            return item_str
        except psycopg2.Error as e:
            print("Error while fetching all items:", e)
            return None

if __name__ == '__main__':
    print(ResourcesManager.get_by_name('Anti Defamation League'))
    print(ResourcesManager.all_items())