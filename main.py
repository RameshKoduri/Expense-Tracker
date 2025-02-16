from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home Page - Add Expense
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']

        new_expense = Expense(name=name, amount=float(amount), date=datetime.strptime(date, '%Y-%m-%d'))
        db.session.add(new_expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('index.html')

# Statement Page - View & Delete Expenses
@app.route('/statement', methods=['GET', 'POST'])
def statement():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')

    if from_date and to_date:
        expenses = Expense.query.filter(Expense.date.between(from_date, to_date)).all()
    else:
        expenses = Expense.query.all()

    total_amount = sum(exp.amount for exp in expenses)

    return render_template('statement.html', expenses=expenses, total_amount=total_amount)

# Delete Expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    
    return redirect(url_for('statement'))

if __name__ == '__main__':
    app.run(debug=True)
