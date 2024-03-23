import psycopg2

class UsefulResources:
    def __init__(self, res_name, res_title, res_url):
        self.res_name = res_name
        self.res_title = res_title
        self.res_url = res_url
        self.connection = psycopg2.connect('postgres://ljegpnle:s52KtrB_NVDjrDKJM4qPGF8T1nSSkERE@flora.db.elephantsql.com/ljegpnle')
        self.cursor = self.connection.cursor()

    # def __str__(self):
    #     return f'{self.res_name} - {self.res_title} - {self.res_url}'

    def save(self):
        try:
            query = f"insert into usefull_resources(resource_name,resource_title,resource_url) values('{self.res_name}','{self.res_title}','{self.res_url}');"
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

    def update(self, res_name=None, res_title=None, res_url=None):
        try:
            if res_name is None:
                res_name = self.res_name
            if res_url is None:
                res_url = self.res_url
            if res_title is None:
                res_title = self.res_title
            update_query = f"UPDATE usefull_resources SET resource_name = '{res_name}', resource_url = '{res_url}', resource_title = {res_title} WHERE resource_name = '{self.res_name}' and resource_url = '{self.res_url}';"
            self.cursor.execute(update_query)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            print("Item updated successfully!")
        except psycopg2.Error as e:
            print("Error while updating item:", e)


if __name__ == '__main__':
    resource = UsefulResources('Museum of Jewish Heritage - A Living Memorial to the Holocaust', 'Their website offers a wealth of educational resources, including online exhibitions, lesson plans, and articles about antisemitism and the Holocaust.','https://mjhnyc.org/')
    #resorce2 = UsefulResources('Anti-Defamation League (ADL)','The ADL is a leading organization in the fight against antisemitism and other forms of hate. Their website provides educational resources, reports, and tools for combating antisemitism.','https://www.adl.org/')
    # resorce3 = UsefulResources('United States Holocaust Memorial Museum (USHMM)','The USHMM offers extensive educational resources about the Holocaust, including materials on antisemitism, propaganda, and resistance. Their website features online exhibitions, survivor testimonies, and teaching materials.','https://www.ushmm.org/')
    #resorce4 = UsefulResources('Simon Wiesenthal Center','This organization is dedicated to preserving the memory of the Holocaust and confronting contemporary antisemitism. Their website offers educational resources, news updates, and information about ongoing initiatives.','https://www.wiesenthal.com/')
    #resorce5 = UsefulResources('Yad Vashem','The World Holocaust Remembrance Center in Jerusalem provides educational materials, research, and documentation about the Holocaust and antisemitism. Their website features online exhibitions, educational programs, and resources for teachers.','https://www.yadvashem.org/')
    #resorce6 = UsefulResources(' Facing History and Ourselves','This educational organization provides resources and professional development for teachers to address difficult topics like antisemitism, racism, and prejudice. Their website offers lesson plans, videos, and articles for educators and students.','https://www.facinghistory.org/')
    #resorce7 = UsefulResources('Holocaust Educational Trust','Based in the UK, this organization provides educational resources and programs to promote understanding of the Holocaust and combat antisemitism. Their website offers teaching materials, survivor testimonies, and educational initiatives.','https://www.het.org.uk/')
    #resorce8 = UsefulResources('European Union Agency for Fundamental Rights (FRA)','The FRA conducts research and collects data on various forms of discrimination, including antisemitism. Their website offers reports, surveys, and resources related to antisemitism and discrimination in Europe.','https://fra.europa.eu/en')
    # resource.save()
    # resorce2.save()
    # resorce3.save()
    # resorce4.save()
    #resorce5.save()
    # resorce6.save()
    #resorce7.save()
    #resorce8.save()
    # # resource.delete()
    # # resource.update(score=9)



