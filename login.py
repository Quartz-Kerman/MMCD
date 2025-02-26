import bcrypt
import json
from main import technician_tools, foreman_tools, admin_tools

with open("passwords.json", "r") as file:
  data = json.load(file)
  
# _______________________________________________functions________________________________________________________
def hash_password(password):
  salt = b'2b$12$ra36kQz0toY.Dj4CPXOx8e'
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

def technician_login(technician_input):
  technician_input = hash_password(technician_input)
  saved_password = data["users"]["technician"]["password"]
  if str(technician_input) == str(saved_password):
    technician_tools()

def foreman_login(foreman_input):
  foreman_input = hash_password(foreman_input)
  saved_password = data["users"]["foreman"]["password"]
  if str(foreman_input) == str(saved_password):
    foreman_tools()

def admin_login(admin_input):
  admin_input = hash_password(admin_input)
  saved_password = data["users"]["admin"]["password"]
  if str(admin_input) == str(saved_password):
    admin_tools()