from flask import Flask, render_template, request, redirect, url_for
from retrieve import whole_quadrant, whole_quadrant_red, sites_ordered
from map import route_query, get_coords, get_map_embed
import bcrypt
import json

with open("passwords.json", "r") as file:
  data = json.load(file)
  
def hash_password(password):
  salt = b'2b$12$ra36kQz0toY.Dj4CPXOx8e'
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

def technician_login(technician_input):
  technician_input = hash_password(technician_input)
  print(technician_input)
  saved_password = data["users"]["technician"]["password"]
  print(saved_password)
  if str(technician_input) == str(saved_password):
    return True
  return False

def foreman_login(foreman_input):
  foreman_input = hash_password(foreman_input)
  saved_password = data["users"]["foreman"]["password"]
  if str(foreman_input) == str(saved_password):
    return True
  return False

def admin_login(admin_input):
  admin_input = hash_password(admin_input)
  saved_password = data["users"]["admin"]["password"]
  if str(admin_input) == str(saved_password):
    return True
  return False

def update_password(user_type, new_password):
    hashed_password = hash_password(new_password)
    data["users"][user_type]["password"] = str(hashed_password)
    with open("passwords.json", "w") as file:
        json.dump(data, file)

#_______________________________________________________________________________________________________________________

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    password = request.form['password']
    if user_type == 'technician' and technician_login(password):
        return redirect(url_for('technician_tools'))
    elif user_type == 'foreman' and foreman_login(password):
        return redirect(url_for('foreman_tools'))
    elif user_type == 'admin' and admin_login(password):
        return redirect(url_for('admin_tools'))
    else:
        print('Invalid login')
        return redirect(url_for('home'))

@app.route('/technician_tools', methods=['GET', 'POST'])
def technician_tools():
    if request.method == 'POST':
        grid_square = request.form['grid_square']
        site_ids = []
        for i in range(1, 11):
            site_id = request.form.get(f'site_{i}')
            if site_id:
                site_ids.append(f"{grid_square}-{site_id}")
        print("SITE IDS:", site_ids)
        nodes = sites_ordered(site_ids)
        print("NODES:", nodes)
        formatted_locations = []
        for loc in nodes:
            formatted_locations.append({
                "address": str(loc["site_name"]),
                "lat": loc["latitude"],
                "lng": loc["longitude"]
            })
        print("FORMATTED LOCATIONS:", formatted_locations)
        route_response = route_query(formatted_locations)
        coords = get_coords(formatted_locations, route_response)
        map_url = get_map_embed(coords)
        return render_template('technician_tools.html', map_url=map_url)
    return render_template('technician_tools.html')



@app.route('/foreman_tools', methods=['GET', 'POST'])
def foreman_tools():
    if request.method == 'POST':
        site_code = int(request.form['site_code'])
        mode = request.form['mode']
        if mode == 'normal':
            nodes = whole_quadrant(site_code)
        else:
            nodes = whole_quadrant_red(site_code)
        formatted_locations = []
        for loc in nodes[:10]:
            formatted_locations.append({
                "address": str(loc["site_name"]),
                "lat": loc["latitude"],
                "lng": loc["longitude"]
            })
        route_response = route_query(formatted_locations)
        coords = get_coords(formatted_locations, route_response)
        map_url = get_map_embed(coords)
        return render_template('foreman_tools.html', map_url=map_url)
    return render_template('foreman_tools.html')

@app.route('/side_by_side')
def side_by_side_comparison():
    return render_template('side_by_side.html')

@app.route('/admin_tools', methods=['GET', 'POST'])
def admin_tools():
    if request.method == 'POST':
        user_type = request.form['user_type']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            update_password(user_type, new_password)
            return redirect(url_for('admin_tools'))
    return render_template('admin_tools.html')

@app.route('/update_password', methods=['POST'])
def update_password_route():
    user_type = request.form['user_type']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    if new_password == confirm_password:
        update_password(user_type, new_password)
        return redirect(url_for('admin_tools'))
    return redirect(url_for('admin_tools'))


if __name__ == '__main__':
    app.run(debug=True)
