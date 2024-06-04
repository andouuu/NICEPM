import sqlite3
import bcrypt
import secrets
from flask import jsonify
import json
from config import CONFIG

def dict_factory(cursor, row):
    fields = [ column[0] for column in cursor.description ]
    return {key: value for key, value in zip(fields, row)}

def get_db_connection():
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = dict_factory
    return db_conn

def get_user(session_token):
    if not session_token:
        return jsonify(message = "No user!"), 400
    
    db_conn=get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * from users WHERE session_token = ?",(session_token,))
    current_user = cursor.fetchone()
    db_conn.close()
    return {"user_id": current_user["user_id"], "username": current_user["username"]},200

def generate_session_token():
    return secrets.token_hex(16)

def register(username,password,email):

    if not (username and password and email):
        return jsonify(message = "Incomplete user registration data"), 400
    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        db_conn.close()
        return jsonify(message = "Username or email already exists"),400

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes,salt)

    cursor.execute("INSERT INTO users (username, password_hash, salt, email) VALUES (?, ?, ?, ?)",
                   (username, hashed_password, salt, email))
    db_conn.commit()
    new_user_id = cursor.lastrowid

    db_conn.close()
    return jsonify({"user_id": new_user_id, "username": username, "email": email}), 200

def login(username, password):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        db_conn.close()
        return jsonify("User not found"), 404
    login_pass_bytes=password.encode('utf-8')
    user_pass_bytes=user["password_hash"]
    check = bcrypt.checkpw(login_pass_bytes,user_pass_bytes)
    if not (check):
        db_conn.close()
        return jsonify("Incorrect password"), 401

    session_token = generate_session_token()
    cursor.execute("UPDATE users SET session_token = ? WHERE user_id = ?;", (session_token, user["user_id"]))
    db_conn.commit()

    db_conn.close()
    return {"user_id": user["user_id"], "username": user["username"], "email": user["email"], "session_token": session_token}, 200

def read_all(user_id):
    ALL_ACCOUNTS = "SELECT * FROM accounts WHERE account_user_id = ?"
    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(ALL_ACCOUNTS,(user_id,))
    resultset = cursor.fetchall()
    db_conn.close()

    return jsonify(resultset)

def create(account):
    username=account['username']
    password=account['password']
    website=account['website']
    account_user_id=account["account_user_id"]
    INSERT_ACCOUNT = "INSERT INTO accounts (account_name, account_password, account_website, account_user_id) VALUES (?, ?, ?, ?)"
    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(INSERT_ACCOUNT, (username, password, website, account_user_id))
    db_conn.commit()
    new_account_id = cursor.lastrowid
    db_conn.close()
    
    return new_account_id, 201

def logout(user_id):
    db_conn=get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute("UPDATE users SET session_token = null WHERE user_id = ?", (user_id,))
    db_conn.commit()
    db_conn.close()
    return jsonify(message = "Sucessfully logged out!"), 200

def read_one(account_id):
    GET_ACCOUNT = "SELECT * FROM accounts WHERE account_id = ?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(GET_ACCOUNT, (account_id, ) )
    resultset = cursor.fetchall()
    db_conn.close()

    if len(resultset) < 1:
        return "Not found", 404
    elif len(resultset) > 2:
        return "Too many results found.", 500

    return jsonify(resultset[0])

def update(id, account):
    UPDATE_ACCOUNT = """
    UPDATE accounts
    SET account_name = ?,
        account_password = ?,
        account_website = ?
    WHERE account_id = ?
    """

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(UPDATE_ACCOUNT, (account["username"], account["password"], account["website"], id) )
    db_conn.commit()

    return read_one(id)

def delete(account_id):
    DELETE_ACCOUNT = "DELETE FROM accounts WHERE account_id=?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(DELETE_ACCOUNT, (account_id, ) )
    db_conn.commit()

    return "Succesfully deleted.", 204
