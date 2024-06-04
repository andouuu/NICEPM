import json
import requests
from config import CONFIG
from passmanager import register,login,get_user,logout

def add_account(session_token, account_name, account_password, account_website, account_user_id):
    new_account = {
        "username": account_name,
        "password": account_password,
        "website": account_website,
        "account_user_id": account_user_id
    }
    headers = {"Authorization": f"Bearer {session_token}"}
    response = requests.post(f"{CONFIG['api']['url']}/add-account", json=new_account, headers=headers)
    
    return response.status_code

def list_of_accounts(session_token):
    user = get_current_user(session_token)
    headers = {"Authorization": f"Bearer {session_token}"}
    params = {"user_id": user["user_id"]}  # Pass user_id as a query parameter
    results = requests.get(f"{CONFIG['api']['url']}/saved-accounts", params=params, headers=headers)
    accounts = json.loads(results.text)

    return accounts

def get_account(session_token, account_id):
    headers = {"Authorization": f"Bearer {session_token}"}
    result = requests.get(f"{CONFIG['api']['url']}/saved-accounts/{account_id}", headers=headers)
    account = json.loads(result.text)

    return account

def update_account(session_token, account):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {session_token}"}
    response = requests.put(f"{CONFIG['api']['url']}/change-details/{account['id']}", json=account, headers=headers)
    account = json.loads(response.text)

    return account['account_id']

def delete_account(session_token, account_id):
    headers = {"Authorization": f"Bearer {session_token}"}
    requests.delete(f"{CONFIG['api']['url']}/delete-data/{account_id}", headers=headers)

def user_login(username, password):
    response = login(username, password)

    if response[1] == 200:
        user_data=response[0]
        return user_data['session_token']
    return None

def user_register(username, password, email):
    response = register(username,password,email)
    if response[1] == 200:
        return True, response[0]
    else:
        return False, response[0]

def get_current_user(session_token):
    response = get_user(session_token)
    if response[1]== 200:
        user=response[0]
        return user

def logout_user(user_id):
    response = logout(user_id)
    return response[1]