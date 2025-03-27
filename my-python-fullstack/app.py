from flask import Flask, request, jsonify, render_template
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to establish a connection to MSSQL database
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-7UFPMB1\\SQLEXPRESS;'  # Adjust your server name if needed
        'DATABASE=krishna;' # Replace with your database name
        'UID=sa;'  # Replace with your database username
        'PWD=112233'  # Replace with your database password
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
            'id':user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3],
            'age': user[4]
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

@app.route('/delete/<email>', methods=['DELETE'])
def delete_user(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT * FROM REGISTER WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Delete the user
        cursor.execute('DELETE FROM REGISTER WHERE email = ?', (email,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User deleted successfully!'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred while deleting the user'}), 500


@app.route('/update/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    age = data.get('age')

    if not name or not password or not age:
        return jsonify({'error': 'Name, password, and age are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute('SELECT * FROM REGISTER WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        if not existing_user:
            return jsonify({'error': 'User not found'}), 404

        # Update user details
        cursor.execute('''
            UPDATE REGISTER 
            SET name = ?, password = ?, age = ? 
            WHERE email = ?
        ''', (name, password, age, email))

        conn.commit()
        conn.close()

        return jsonify({'message': 'User updated successfully!'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred while updating the user'}), 500

if __name__ == '__main__':
    app.run(debug=True)
