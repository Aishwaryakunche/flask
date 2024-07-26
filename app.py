from flask import Flask, render_template, request
from sentiments import second
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Define your secret key directly here
app.register_blueprint(second)

# Initialize database connection and cursor (if you are using a database for other purposes, adjust accordingly)
# Commented out as it's not needed for sentiment analysis alone

# conn = None
# cursor = None

# try:
#     conn = mysql.connector.connect(
#         host=db_host,
#         user=db_user,
#         password=db_password,
#         database=db_database
#     )
#     cursor = conn.cursor()
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#     exit(1)

@app.route('/')
def sentiment_analyzer():
    return render_template('sentiment_analyzer.html')

if __name__ == "__main__":
    app.run(debug=True)
