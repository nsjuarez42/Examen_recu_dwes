from entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, user):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT * FROM user WHERE username = %s'

            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                password = User.check_password(row[2], user.password)
                fullname = row[3]

                user = User(id, username, password, fullname)

                return user
            else:
                return None

        except Exception as e:

            raise Exception(e)
        
    @classmethod
    def create_user(cls,db,cursor,username,password,fullname):

        try:
            sentence = "INSERT INTO users(id,username,password,fullname) VALUES(NULL,%s,%s,%s)"
            cursor.execute(sentence,(username,password,fullname))
            db.commit()
            print("User inserted succesfully")
        
        except Exception as e:
            raise Exception(e)



    @classmethod
    def get_by_id(cls,db,id):

        try:
            cursor = db.cursor()
            sql = 'SELECT id, username, fullname FROM users WHERE id = %s'

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                fullname = row[2]

                logged_user = User(id, username, None, fullname)

                return logged_user
            else:
                return None

        except Exception as e:

            raise Exception(e)
    
    @classmethod
    def get_by_username(cls,db,username):

        try:
            cursor = db.cursor()
            sql = 'SELECT id, username, fullname, password FROM users WHERE username = %s'

            cursor.execute(sql, (username,))
            row = cursor.fetchone()

            if row:
                print(row)
                id = row[0]
                username = row[1]
                fullname = row[2]
                password = row[3]

                return User(id,username,password,fullname)
            
            else:
                return None

        except Exception as e:

            raise Exception(e)