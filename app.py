from bson import ObjectId
from flask import Flask,render_template,url_for,redirect,request
from flask_pymongo import PyMongo

app=Flask(__name__)
mongo=PyMongo()
app.config['MONGO_URI']='mongodb+srv://n:n@cluster3.ejz92.mongodb.net/mydb?retryWrites=true&w=majority'
mongo.init_app(app)

@app.route('/')
def index():
    todos_collection=mongo.db.todos
    todos=todos_collection.find()
    t=todos_collection.find()
    results = list(t)
    if len(results)==0:
        print(len(results))
        checks=True
    else:
        checks=False
    
    return render_template('index.html',todos=todos,checks=checks)


@app.route("/add_todo", methods=['POST'])
def add_todo():
    todos_collection=mongo.db.todos
    todo_item=request.form.get('add-todo')
    todos_collection.insert_one({'text':todo_item,'complete':False})
    return redirect(url_for('index'))

@app.route('/comp/<oid>')
def comp(oid):
    todos_collection=mongo.db.todos
    todos_collection.update_one({'_id':{ '$eq': ObjectId(oid)}},{'$set' : {'complete':True}})
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos_collection=mongo.db.todos
    todos_collection.delete_many({'complete':True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos_collection=mongo.db.todos
    todos_collection.delete_many({})
    return redirect(url_for('index'))


if __name__=="__main__":
    app.run(debug=True)