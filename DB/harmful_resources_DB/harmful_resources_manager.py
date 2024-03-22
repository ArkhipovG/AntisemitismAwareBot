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
                return item
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
            return items
        except psycopg2.Error as e:
            print("Error while fetching all items:", e)
            return None

if __name__ == '__main__':
    print(*ResourcesManager.get_by_name('Vkontakte'))
    for item in ResourcesManager.all_items():
        print(*item)