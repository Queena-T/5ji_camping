from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5ji'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 使用者與餐別選項
users = ["🐻大熊小熊中熊🐻", "🐢穎妤🐢","🐶安鎂吉🐶"]
meal_types = ["Breakfast", "Night snack", "Dinner"]


# 菜單、注意事項數據庫
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    dish = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
def __repr__(self):
    return f"MenuItem('{self.name}', '{self.meal_type}', '{self.dish}')"
    
with app.app_context():
    db.create_all()

# 首頁
@app.route('/')
def index():
    return redirect(url_for('menu'))

# 總菜單
@app.route('/menu')
def menu():
    menu_items = Menu.query.order_by(Menu.meal_type).all()
    notes = Note.query.order_by(Note.name).all()
    return render_template('menu.html',
                           menu_items=menu_items,
                           meal_types=meal_types,
                           notes=notes,
                           users=users)
    
# 注意事項頁面
@app.route('/note')
def note():
    notes = Note.query.order_by(Note.name).all()
    return render_template('note.html', notes=notes, users=users)


# 表单：用来提交菜单数据
class MenuForm(FlaskForm):
    name = SelectField('姓名', coerce=str, validators=[DataRequired()])
    meal_type = SelectField('餐別',coerce=str, validators=[DataRequired()])
    dish = StringField('菜色', validators=[DataRequired()])
    note = TextAreaField('備料')
    submit = SubmitField('我要煮!')

@app.route('/update', methods=['POST'])
def update():
    item_id = request.form.get('id')
    name = request.form['name']
    meal_type = request.form['meal_type']
    dish = request.form['dish']
    note = request.form['note']

    if item_id:
        item = Menu.query.get(int(item_id))
        if item:
            item.name = name
            item.meal_type = meal_type
            item.dish = dish
            item.note = note
    else:
        new_item = Menu()
        new_item.name = name
        new_item.meal_type = meal_type
        new_item.dish = dish
        new_item.note = note
        db.session.add(new_item) 

    db.session.commit()
    return redirect(url_for('menu'))

# ✅ 刪除功能
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Menu.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('menu'))


# 新增 / 修改 注意事項
@app.route('/update-note', methods=['POST'])
def update_note():
        note_id = request.form.get('note-id')
        name = request.form['name']
        content = request.form['content']
    
        if note_id:
            note = Note.query.get(note_id)
            if note:
                note.name = name
                note.content = content
                db.session.commit()
        else:
            new_note = Note()
            new_note.name = name
            new_note.content = content
            db.session.add(new_note)
            db.session.commit()
    
        return redirect(url_for('note'))

# ✅ 刪除功能
@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    item = Note.query.get(note_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('note'))
    
if __name__ == '__main__':
    app.run(debug=True)