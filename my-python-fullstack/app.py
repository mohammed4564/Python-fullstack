from flask import Flask, request, jsonify, render_template
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to establish a connection to MSSQL database
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-2BCQ0PO\\SQLEXPRESS01;'  # Adjust your server name if needed
        'DATABASE=UMAR_DB;'  # Replace with your database name
        'UID=sa;'  # Replace with your database username
        'PWD=12345678'  # Replace with your database password
    )
    return conn

@app.route('/')
def dashboard():
    return render_template('dashboard.html')  # Render dashboard page when accessing "/"

# Route to display registration form
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')  # Render registration form page

# GET endpoint to retrieve all users from the REGISTER table
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM REGISTER')
    users = cursor.fetchall()
    conn.close()

    # Convert the rows into a list of dictionaries
    users_list = []
    for user in users:
        users_list.append({
            'name': user[0],
            'email': user[1],
            'password': user[2],
            'age': user[3]
        })

    return jsonify(users_list)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()  # Get the JSON data from the request body
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute('SELECT * FROM REGISTER WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        # Insert the new user into the REGISTER table
        cursor.execute(''' 
            INSERT INTO REGISTER (name, email, password, age)
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, age))

        conn.commit()
        conn.close()

        return jsonify({'message': 'User registered successfully!'}), 201

    except Exception as e:
        # Handle specific error (like database error)
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred while registering the user'}), 500


if __name__ == '__main__':
    app.run(debug=True)
