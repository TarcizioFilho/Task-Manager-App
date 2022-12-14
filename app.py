from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
print('initializing app')
db.init_app(app)


class Create_task(db.Model):
        __tablename__ = 'tarefas'
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(200))
        tasks_done = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    all_tasks = Create_task.query.all() #variável all_tasks guarda todas as informções/tarefas criadas pelo user
    return render_template('index.html',tasks_list=all_tasks)#carregar o template index.html

@app.route('/<id>')
def get_task_by_id(id):
    task_by_id = Create_task.query.get(id)
    return render_template('index.html', task_by_id=task_by_id)

@app.route('/task-edit-id/<id>')
def get_task_by_id_edit(id):
    task_by_id_edit = Create_task.query.get(id)
    return render_template('index.html', task_by_id_edit=task_by_id_edit)

@app.route('/create-task', methods=['POST'])
def criar():
    task = Create_task(content=request.form['content_tasks'], tasks_done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))# redirecionar a função home para que o seja mostrada a página atualizada quando o conteudo for alterado

@app.route('/remove-task/<id>')
def remove(id):
    task = Create_task.query.filter_by(id=int(id)).delete() #procurar na base de dados o id correspondente ao id que vem da página web, e depois faz delete
    db.session.commit()
    return redirect(url_for('home'))
    
@app.route('/task-done/<id>')
def task_done(id):
    task = Create_task.query.filter_by(id=int(id)).first()
    task.tasks_done = not(task.tasks_done)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update-task/<id>', methods=['GET', 'POST'])
def update_task(id):
    task_to_update = Create_task.query.filter_by(id=int(id)).first()
    if request.method == 'POST':
        task_to_update.content = request.form['new_content_task']
        db.session.commit()
    return(redirect(url_for('home')))

    
if __name__ == '__main__':
    app.run(debug=True)