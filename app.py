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
app.config['MYSQL_DB'] = 'mypracticedatabase'
mysql = MySQL(app)


@app.route('/')
def Index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM employee')
    data = cursor.fetchall()

    return render_template('list.html', employee=data)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
 
    if request.method == 'POST':
        # id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        salary = request.form['salary']
        gender = request.form['gender']
        etype = request.form['etype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("INSERT INTO employee(name,age,address,salary,gender,type) VALUES(%s, %s,%s,%s,%s,%s)",
                           (name,age,address,salary,gender,etype))
        mysql.connection.commit()
        flash("You have successfully added Employee in the list")
        return redirect(url_for('Index'))

@app.route('/detail/<id>', methods=['POST', 'GET'])
def detail(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee WHERE id = %s', (id,))
    data = cursor.fetchall()

    return render_template('detail.html', employee=data[0])


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee WHERE id = %s', (id,))
    data = cursor.fetchone()
    if request.method == 'POST':
        if data:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            name = request.form['name']
            age = request.form['age']
            address = request.form['address']
            salary = request.form['salary']
            gender = request.form['gender']
            etype = request.form['etype']
            cursor.execute("""UPDATE employee SET name = %s,age= %s ,address=%s ,salary=%s,gender=%s,type=%s WHERE id = %s""",
                           (name, age, address, salary, gender, etype, id,))
            mysql.connection.commit()
            flash("Employee details updated successfully")
            return redirect(url_for('Index'))

    return render_template('update.html', employee=data)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("DELETE FROM employee WHERE id=%s", (id,))

    mysql.connection.commit()
    flash('Employee details Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run()
