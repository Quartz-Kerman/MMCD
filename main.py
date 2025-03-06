from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('map.html')

@app.route('/technician_tools')
def technician_tools():
    return render_template('technician_tools.html')

@app.route('/foreman_tools')
def foreman_tools():
    return render_template('foreman_tools.html')

@app.route('/side_by_side')
def side_by_side_comparison():
    return render_template('side_by_side.html')

@app.route('/admin_tools')
def admin_tools():
    return render_template('admin_tools.html')

if __name__ == '__main__':
    app.run(debug=True)
