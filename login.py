import bcrypt

# _______________________________________________functions________________________________________________________
def does_not_have_account():
    frame_register.tkraise()

def does_not_remember_password():
    frame_recover.tkraise()

def hash_password(password):
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password


def register(ent_username, ent_password, ent_confirm_pass, ent_email, security_q):
    if ent_password != ent_confirm_pass:
        return
    if not re.search(r"[A-Z]", ent_password) or \
        not re.search(r"\d", ent_password) or \
        not re.search(r"[!@#$%^&*()_+{}|<>?]", ent_password):
        return
    hashed_password = hash_password(ent_password)
    connection = mysql.connector.connect(
        host="localhost",
        user="dladmin",
        password="QuincyMySQL",
        database="dldb"
    )
    cursor = connection.cursor()
    try:
        query = "SELECT COUNT(*) FROM user WHERE username = %s"
        cursor.execute(query, (ent_username,))
        result = cursor.fetchone()
        if result[0] > 0:
            return
        query = "INSERT INTO user (username, password, email, security_q) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (ent_username, hashed_password, ent_email, security_q))
        connection.commit()

        frame_login.tkraise()  # Raise the login frame
    finally:
        connection.close()

def reset_password(username, security_a, new_password, pass_confirm, frame_login):
    if new_password != pass_confirm:
        return
    if not re.search(r"[A-Z]", new_password) or \
        not re.search(r"\d", new_password) or \
        not re.search(r"[!@#$%^&*()_+{}|<>?]", new_password):
        return
    hashed_password = hash_password(new_password)
    connection = mysql.connector.connect(
        host="localhost",
        user="dladmin",
        password="QuincyMySQL",
        database="dldb"
    )
    cursor = connection.cursor()
    try:
        query = "SELECT security_q FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result[0] != security_a:
            return
        query = "UPDATE user SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_password, username))
        connection.commit()
    finally:
        connection.close()
        frame_login.tkraise()

def login(ent_username, ent_password, login_window):
    connection = mysql.connector.connect(
        host="localhost",
        user="dladmin",
        password="QuincyMySQL",
        database="dldb"
    )
    cursor = connection.cursor()
    try:
        query = "SELECT COUNT(*) FROM user WHERE username = %s"
        cursor.execute(query, (ent_username,))
        result = cursor.fetchone()
        if result[0] == 0:
            return False  # Username not found
        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (ent_username,))
        hashed_password = cursor.fetchone()[0].encode('utf-8')
        if bcrypt.checkpw(ent_password.encode('utf-8'), hashed_password):
            login_window.destroy()  # Close the login window
            query = "SELECT admin_ind FROM user WHERE username = %s"
            cursor.execute(query, (ent_username,))
            result = cursor.fetchone()
            if result[0] == 0:
                user_not_admin(ent_username)
            else:
                user_is_admin()
            return
        else:
            return
    finally:
        connection.close()
