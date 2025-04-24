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


# 数据库模型：用来存储菜单和注意事项
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    dish = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200), nullable=True)

def __repr__(self):
        return f'<Menu {self.name}>'
    
with app.app_context():
    db.create_all()

# 表单：用来提交菜单数据
class MenuForm(FlaskForm):
    name = SelectField('姓名', coerce=str, validators=[DataRequired()])
    meal_type = SelectField('餐別',coerce=str, validators=[DataRequired()])
    dish = StringField('菜色', validators=[DataRequired()])
    note = TextAreaField('備料')
    submit = SubmitField('我要煮!')

# 路由：主页，显示所有菜单并允许用户选择并提交
@app.route('/', methods=['GET', 'POST'])
def index():
    # 模拟用户数据，实际可以从数据库获取
    users = ["🐶安鎂吉🐶", "🐢穎妤🐢", "🐻大熊小熊中熊🐻"]
    meal_types = ["Breakfast", "Night snack", "Dinner"]
    form = MenuForm(request.form)
    form.name.choices = [(user, user) for user in users]  # 下拉选择
    form.meal_type.choices = [(meal_type, meal_type) for meal_type in meal_types]
    
    if request.method == 'POST' and form.validate():
        # 将表单数据保存到数据库        
        menu_item = Menu()
        menu_item.name = form.name.data
        menu_item.meal_type = form.meal_type.data
        menu_item.dish = form.dish.data
        menu_item.note = form.note.data
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu successfully submitted!', 'success')
        return redirect(url_for('menu_list'))

    # 获取所有的菜单数据
    menus = Menu.query.all()
    return render_template('index.html', form=form, menus=menus)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu_list')
def menu_list():
    # 获取所有菜单项
    menus = Menu.query.all()
    return render_template('menu_list.html', menus=menus)

@app.route('/note')
def note():
    return render_template('note.html')

if __name__ == '__main__':
    app.run(debug=True)