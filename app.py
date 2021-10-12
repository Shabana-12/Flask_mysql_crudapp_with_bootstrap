from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import flash, request
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass@1New'
app.config['MYSQL_DB'] = 'librarysys'
mysql = MySQL(app)

@app.route('/')
def retrieve():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
 
    cursor.execute('SELECT * FROM books')
    data = cursor.fetchall()
  
    
    return render_template('list.html', books= data)

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
 
    if request.method == 'POST':
        book_id = request.form['book_id']
        bookname = request.form['bookname']
        total = request.form['total']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO books(BookId,BookName, total) VALUES(%s, %s,%s)",
                           (book_id,bookname,total))
        mysql.connection.commit()
        flash("You have successfully added books in library")
        return redirect(url_for('retrieve'))

@app.route('/detail/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM books WHERE BookId = %s', (id,))
    data = cursor.fetchall()
    
    
    return render_template('detail.html', book= data[0])
  
@app.route('/update/<id>',methods = ['GET','POST'])
def update(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM books WHERE BookId = %s', (id,))
    book = cursor.fetchone()
    if request.method == 'POST':
        if book:
            
            book_id = request.form['book_id']
            bookname = request.form['bookname']
            total = request.form['total']
        
            cursor.execute("""UPDATE books SET BookName = %s,total= %s WHERE BookId = %s""", (bookname,total,book_id))
            mysql.connection.commit()
            flash("Book details updated successfully")
            return redirect(url_for('retrieve'))
        else:
            flash("Book details are not available which you are trying to update")
            return redirect(url_for('create'))
 
    return render_template('update.html', book = book)

@app.route('/delete/<id>', methods = ['POST','GET'])
def delete_employee(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * FROM books WHERE BookId = {0}'.format(id))
    book=cursor.fetchall()
    if request.method == 'POST':
        if book:
        
            cursor.execute('DELETE FROM books WHERE BookId = {0}'.format(id))
    
            mysql.connection.commit()
            flash('Book details Removed Successfully')
            return redirect(url_for('retrieve'))
        else:
            flash('Book details are not present which you are trying to delete')
            return redirect(url_for('retrieve'))
    return render_template("delete.html")
        

if __name__ == "__main__":
    app.run()
