import psycopg2

class HarmfulResources:
    def __init__(self, name, url, score):
        self.name = name
        self.url = url
        self.score = score
        self.connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
        self.cursor = self.connection.cursor()

    def __str__(self):
        return f'{self.name} - {self.url} - {self.score}'

    def save(self):
        try:
            query = f"insert into harmful_resources(resource_name,resource_url,harmful_score) values('{self.name}','{self.url}',{self.score});"
            self.cursor.execute(query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item saved successfully!")
        except psycopg2.Error as error:
            print(f"Error while saving item:", error)

    def delete(self):
        try:
            self.cursor.execute(f"DELETE from harmful_resources WHERE resource_name = '{self.name}';")
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item deleted successfully!")
        except psycopg2.Error as e:
            print("Error while deleting item:", e)

    def update(self, name=None, url=None, score=None):
        try:
            if name is None:
                name = self.name
            if url is None:
                url = self.url
            if score is None:
                score = self.score
            update_query = f"UPDATE harmful_resources SET resource_name = '{name}', resource_url = '{url}', harmful_score = {score} WHERE resource_name = '{self.name}' and resource_url = '{self.url}';"
            self.cursor.execute(update_query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item updated successfully!")
        except psycopg2.Error as e:
            print("Error while updating item:", e)


if __name__ == '__main__':
    resource = HarmfulResources('Vkontakte', 'https://www.vk.com',7)
    resource.save()
    # resource.delete()
    # resource.update(score=9)



