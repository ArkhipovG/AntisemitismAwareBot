import psycopg2


class ResourcesManager:
    @classmethod
    def get_by_name(cls, resource_name):
        try:
            connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
            cursor = connection.cursor()
            select_query = f"SELECT * FROM harmful_resources WHERE resource_name = '{resource_name}'"
            cursor.execute(select_query)
            item = cursor.fetchone()
            cursor.close()
            connection.close()
            if item:
                return item[1:]
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
            select_query = f"SELECT * FROM harmful_resources"
            cursor.execute(select_query)
            items = cursor.fetchall()
            cursor.close()
            connection.close()
            item_str = ''
            for item in items:
                item_str += str(item[1]) + ' ' + str(item[2]) + ' ' + str(item[3])
                item_str += '\n'
            return item_str
        except psycopg2.Error as e:
            print("Error while fetching all items:", e)
            return None

if __name__ == '__main__':
    print(*ResourcesManager.get_by_name('Vkontakte'))
    print(ResourcesManager.all_items())