from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from datetime import datetime
import sqlite3
app = Flask(__name__)

api = 'https://fakestoreapi.com'

cnn = sqlite3.connect('db.sqlite3')
cur = cnn.cursor()
student = cur.execute("""SELECT * FROM tbl_student""")
cnn.commit()
    
users_list = []   

for row in student: 
    users_list.append({
        'id': row[0],
        'name':row[1],
        'gender': row[2],
        'phone': row[4],
        'email': row[5],
        'address': row[3]
        
    },
    )

cur.close()

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
    cnn = sqlite3.connect('db.sqlite3')
    cur = cnn.cursor()
    student = cur.execute("""SELECT * FROM tbl_student""")
    cnn.commit()    
    users_list = []   

    for row in student: 
        users_list.append({
        'id': row[0],
        'name':row[1],
        'gender': row[2],
        'phone': row[4],
        'email': row[5],
        'address': row[3] 
    },
    )
    cur.close()
    return render_template('/admin/users.html',active='users',users=users_list)

@app.post('/create_user')
def create_user():
    name = request.form['name']
    gender = "M"

    form = {
        'name': name,
        'gender': gender
    }
    return form

@app.route('/admin/view_user/<int:id>')  
def view_user(id):
    current_user = []
    for user in users_list:
        if user['id'] == id:
            current_user = user
    # return f"{user[0]}"
    return render_template('/admin/view_user.html',active='users',user=current_user)

@app.route('/admin/add_user')  
def add_user():
    # name = request.args.get('name',default='No Name',type=str)
    # current_user = filter(lambda user:user['name'] == name,users_list)
    # user = list(current_user)
    # return f"{user[0]}"
    return render_template('/admin/add_user.html',active='users')

@app.route('/admin/save_user',methods=['POST'])
def save_user():
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        gender= "M"
        phone= request.form['phone']
        email= request.form['email']
        cnn = sqlite3.connect('db.sqlite3')
        cur=cnn.cursor()
        cur.execute("insert into tbl_student(name,gender,address,phone,email) values (?,?,?,?,?)",(name,gender,address,phone,email))
        cnn.commit()
        cur.close()

        # flash('User Added','success')
        return redirect(url_for("users"))
    return render_template("add_user.html")
    # return f"{name} {address} {gender} {phone} {email}"

@app.route('/admin/delete_user/<int:id>')  
def delete_user(id):
    module = 'users'
    cnn = sqlite3.connect('db.sqlite3')
    cur = cnn.cursor()
    student = cur.execute("""SELECT * FROM tbl_student""")
    cnn.commit()    
    users_list = []   

    for row in student: 
        users_list.append({
        'id': row[0],
        'name':row[1],
        'gender': row[2],
        'phone': row[4],
        'email': row[5],
        'address': row[3] 
    },
    )
    cur.close()
    return render_template('/admin/delete_user.html',active='users',user=users_list)



@app.route('/admin/confirm_delete/<int:id>',methods=['POST','GET'])  
def confirm_delete(id):
    cnn=sqlite3.connect("db.sqlite3")
    cur=cnn.cursor()
    cur.execute("delete from tbl_student where id=?",(uid,))
    cnn.commit()
    cur.close()
    # return f"{user[0]}"
    return redirect(url_for("users"))
    # return f"{uid}"

@app.route('/admin/edit_user/<int:user_id>')
def edit_user(user_id):
    module = 'users'
    current_user = []
    for user in users_list:
        if user['id'] == user_id:
            current_user = user
    return render_template('/admin/edit_user.html',active=module,user=current_user)


@app.route("/admin/confirm_edit/<int:id>",methods=['POST','GET'])
def confirm_edit(id):
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        gender= "M"
        phone= request.form['phone']
        email= request.form['email']
        cnn=sqlite3.connect("db.sqlite3")
        cur=cnn.cursor()
        cur.execute("update tbl_student set name=?, gender=?, address=?, phone=?, email=? where id=?",(name,gender,address,phone,email,id))
        cnn.commit()
        cur.close()
        # flash('User Updated','success')
        return redirect(url_for("users"))
    cnn=sqlite3.connect("db.sqlite3")
    cnn.row_factory=sqlite3.Row
    cur=cnn.cursor()
    cur.execute("select * from users where id=?",(id,))
    data=cur.fetchone()
    cur.close()
    return render_template("edit_user.html",datas=data)
    # return f"{id}"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.route('/admin/brands')
def brands():
    return render_template('/admin/brands.html',active='brands')


@app.route('/shop')
def shop():
    res = requests.get(api + '/products')
    return render_template('/shop/shop.html', data=res.json())
    
@app.route('/shop_now')
def shop_now():
    id = request.args.get('id')
    res = requests.get(api + '/products/'+id.__str__())
    return render_template('/shop/shop_now.html', product=res.json())   

@app.route('/checkout')
def checkout():
    id = request.args.get('id')
    res = requests.get(api + '/products/'+id.__str__())
    return render_template('/shop/checkout.html', product=res.json())

@app.post('/confirmBooking') 
def confirmBooking():
    product_id = request.form['id']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    data = requests.get(f"https://fakestoreapi.com/products/{product_id}")
    product= data.json()
    msg = (
        "<strong>New Confirm Booking </strong>\n"
        "<code>Name: {name}</code>\n"
        "<code>Phone: {phone}</code>\n"
        "<code>Email: {email}</code>\n"
        "<code>Address: {address}</code>\n"
        "<code>Booking Date: {date}</code>\n"
        "<code>=======================</code>\n"
        "<code>1. {product_name} 1x{price}</code>\n"
    ).format(
        name = name,
        phone = phone,
        email = email,
        address = address,
        date=datetime.today().strftime('%Y-%m-%d'),  # Format the date
        product_name = product['title'],
        price = product['price']
    )

    notify_res = sendNotify(msg)
    return notify_res  

def sendNotify(msg):
    bot_token = "6774243738:AAF9E60WjqEfYJYvGvYbWL9P3YwhJzE85eA"
    chat_id = "@DreamsLabBot2024"

    html = requests.utils.quote(msg)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
    res = requests.get(url)
    return res.json()

if __name__ == "__main__":
    app.run()