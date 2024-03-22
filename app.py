from flask import Flask, render_template, request

app = Flask(__name__)

users_list = [
    {
        'id':1,
        'name':'John Doe',
        'gender': 'M',
        'phone': '1234567890',
        'email': 'jonhdoe@gmail.com',
        'address': '123, Main Street, City, Country'
    },
    {
        'id':2,
        'name':'Soron',
        'gender': 'M',
        'phone': '1234567890',
        'email': 'jonhdoe@gmail.com',
        'address': '123, Main Street, City, Country'
    }
]   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('/admin/admin.html',active='admin')

@app.route('/admin/products')
def products():
    return render_template('/admin/products.html',active='products')

@app.route('/admin/categories')
def categories():
    return render_template('/admin/categories.html',active='categories')

@app.route('/admin/users')
def users():
    return render_template('/admin/users.html',active='users',users=users_list)

@app.route('/admin/view_user')  
def view_user():
    name = request.args.get('name',default='No Name',type=str)
    current_user = filter(lambda user:user['name'] == name,users_list)
    user = list(current_user)
    # return f"{user[0]}"
    return render_template('/admin/view_user.html',active='users',user=user[0])

@app.route('/admin/add_user')  
def add_user():
    # name = request.args.get('name',default='No Name',type=str)
    # current_user = filter(lambda user:user['name'] == name,users_list)
    # user = list(current_user)
    # return f"{user[0]}"
    return render_template('/admin/add_user.html',active='users')


@app.route('/admin/delete_uesr')  
def delete_user():
    name = request.args.get('name',default='No Name',type=str)
    current_user = filter(lambda user:user['name'] == name,users_list)
    user = list(current_user)
    # return f"{user[0]}"
    return render_template('/admin/delete_user.html',active='users',user=user[0])


@app.route('/admin/edit_user/<int:user_id>')
def edit_user(user_id):
    module = 'users'
    current_user = []
    for user in users_list:
        if user['id'] == user_id:
            current_user = user
    return render_template('/admin/edit_user.html',active=module,user=current_user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.route('/admin/brands')
def brands():
    return render_template('/admin/brands.html',active='brands')