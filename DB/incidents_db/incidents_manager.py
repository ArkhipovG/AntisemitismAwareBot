import psycopg2


class IncidentsManager:
    @classmethod
    def get_by_name(cls, title):
        try:
            connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
            cursor = connection.cursor()
            select_query = f"SELECT * FROM incidents WHERE incedent_title = '{title}'"
            cursor.execute(select_query)
            item = cursor.fetchone()
            cursor.close()
            connection.close()
            title = item[1]
            info = item[2]
            date = item[3]
            is_online = item[4]
            stroke = f'Incident title: {title}\nIncident info: {info}\nDate of incident: {date}\nOnline: {is_online}\n'
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
            select_query = f"SELECT * FROM incidents"
            cursor.execute(select_query)
            items = cursor.fetchall()
            cursor.close()
            connection.close()
            item_str = ''
            for num,item in enumerate(items):
                item_str += f'Resource №{num+1}:\nIncident title: {str(item[1])}\nIncident info: {str(item[2])}\nDate of incident: {str(item[3])}\nOnline: {str(item[4])}\n'
                item_str += '\n'
            return item_str
        except psycopg2.Error as e:
            print("Error while fetching all items:", e)
            return None

if __name__ == '__main__':
    print(IncidentsManager.get_by_name('Bulling'))
    print(IncidentsManager.all_items())