from flask import Flask, render_template, request, redirect, url_for, session
import uuid # For generating unique, secure user/session IDs
import os # For securely generating the secret key

app = Flask(__name__)

# --- Security & Configuration ---
# Generate a secure secret key for session management
app.secret_key = os.urandom(24) 

# Simple in-memory "database"
books = [
    {"id": 1, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams"},
    {"id": 2, "title": "Pride and Prejudice", "author": "Jane Austen"}
]
next_book_id = 3

# A simple authentication placeholder
# NOTE: In a real app, never store passwords like this. Use hashing (e.g., bcrypt)!
USERS = {"secure_user": "secure_pass"}

# --- Routes ---

@app.route('/')
def index():
    """Renders the home page with the list of books."""
    # Using Flask's built-in templating (Jinja2) automatically handles secure rendering 
    # and prevents XSS by escaping output.
    if 'username' not in session:
        return redirect(url_for('login'))
        
    return render_template('index.html', books=books, current_user=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple password check (again, use hashing in a real app)
        if username in USERS and USERS[username] == password:
            session['username'] = username # Secure session management
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """Adds a new book (requires login)."""
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        global next_book_id
        title = request.form.get('title')
        author = request.form.get('author')
        
        # Input Validation (Good Practice: prevents logic bugs)
        if not title or not author:
            return "Title and Author are required!", 400

        new_book = {"id": next_book_id, "title": title, "author": author}
        books.append(new_book)
        next_book_id += 1
        return redirect(url_for('index'))
        
    return render_template('add_book.html')


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Deletes a book by ID (securely implemented as a POST request)."""
    if 'username' not in session:
        return redirect(url_for('login'))
        
    global books
    # Secure ID check and deletion logic
    books = [book for book in books if book['id'] != book_id]
    return redirect(url_for('index'))


# --- Run the App ---
if __name__ == '__main__':
    # Flask requires a 'templates' folder for rendering HTML
    # We will need to create those files
    print("Starting Flask application. Ensure you have a 'templates' folder with index.html, login.html, and add_book.html.")
    print("Test User: secure_user / secure_pass")
    app.run(debug=True)
