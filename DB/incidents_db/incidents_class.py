import psycopg2

class Incidents:
    def __init__(self, title, info, date, is_online):
        self.title = title
        self.info = info
        self.date = date
        self.is_online = is_online
        self.connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
        self.cursor = self.connection.cursor()
    #
    # def __str__(self):
    #     return f'{self.name} - {self.url} - {self.score}'

    def save(self):
        try:
            query = f"insert into incidents(incedent_title,incedent_info,incident_date,incident_online) values('{self.title}','{self.info}','{self.date}','{self.is_online}');"
            self.cursor.execute(query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item saved successfully!")
        except psycopg2.Error as error:
            print(f"Error while saving item:", error)

    def delete(self):
        try:
            self.cursor.execute(f"DELETE from incidents WHERE incedent_title = '{self.title}';")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item deleted successfully!")
        except psycopg2.Error as e:
            print("Error while deleting item:", e)

    def update(self, title=None, info=None, date=None, is_online=None):
        try:
            if title is None:
                title = self.title
            if info is None:
                info = self.info
            if date is None:
                date = self.score
            if is_online is None:
                is_online = self.is_online

            update_query = f"UPDATE incidents SET incedent_title = '{title}', incedent_info = '{info}', incedent_date = {date}, incident_online = {is_online} WHERE incedent_title = '{self.title}';"
            self.cursor.execute(update_query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item updated successfully!")
        except psycopg2.Error as e:
            print("Error while updating item:", e)


if __name__ == '__main__':
    resource = Incidents('Bulling', 'I faced with bulling in my school','2023-03-20',False)
    resource.save()
    # resource.delete()
    # resource.update(score=9)



