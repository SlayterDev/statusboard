from flask import render_template, flash, redirect, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from datetime import datetime
from config import ITEMS_PER_PAGE, MAX_SEARCH_RESULTS
from .forms import LoginForm, AddTodoForm, SearchForm, EventForm
from .models import Todo, User, Event
import pytz

@lm.user_loader
def load_user(id):
	return User()

def after_login(username, password):
	if username != 'Brad' and username != 'Kara':
		flash('Invalid login. Please Try again')
		return redirect(url_for('login'))
	if username == 'Brad' and password != 'potato':
		flash('Invalid login. Please Try again')
		return redirect(url_for('login'))
	user = User()
	user.username = username
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(url_for('todolist'))

@app.before_request
def before_request():
	g.user = current_user
	g.search_form = SearchForm()

@app.route('/')
@app.route('/index')
@login_required
def index():
	todos = reversed(Todo.query.all())
	events = Event.query.order_by(Event.date.desc())

	return render_template('index.html', title='Home', user=g.user,
							todos=todos, events=events)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return after_login(form.username.data, form.password.data)
	return render_template('login.html', title='Login', form=form)

@app.route('/todolist', methods=['GET', 'POST'])
@app.route('/todolist/<int:page>', methods=['GET', 'POST'])
@login_required
def todolist(page=1):
	todos = Todo.query.order_by(Todo.timestamp.desc())
	todos = todos.paginate(page, ITEMS_PER_PAGE, False)

	form = AddTodoForm()
	if form.validate_on_submit():
		assigned = ""
		if form.forBrad.data:
			assigned += "Brad "
		if form.forKara.data:
			if "Brad" in assigned:
				assigned += "and "
			assigned += "Kara "

		t = Todo(title=form.title.data, description=form.description.data,
				assigned=assigned, timestamp=datetime.utcnow(),
				creator=g.user.username, done=False)
		db.session.add(t)
		db.session.commit()
		flash('Your todo item has been added!')
		return redirect(url_for('todolist'))

	return render_template('todolist-client.html', title='Todo',
							user=g.user, todos=todos, form=form)

@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
	events = reversed(Event.query.all())

	form = EventForm()
	if form.validate_on_submit():
		assigned = ""
		if form.forBrad.data:
			assigned += "Brad "
		if form.forKara.data:
			if "Brad" in assigned:
				assigned += "and "
			assigned += "Kara "

		local = pytz.timezone("US/Central")
		date = datetime.combine(form.date.data, form.time.data)
		local_dt = local.localize(date, is_dst=None)
		date = local_dt.astimezone(pytz.utc)

		event = Event(title=form.title.data, date=date,
						assigned=assigned, 
						creator=g.user.username)
		db.session.add(event)
		db.session.commit()
		flash('Your event has been added')
		return redirect(url_for('calendar'))

	return render_template('calendar-client.html', title='Calendar',
							user=g.user, events=events,
							form=form)

@app.route('/markdone/<int:id>')
@login_required
def markdone(id):
	todo = Todo.query.get(id)
	if todo is None:
		flash('This item does not exist')
		return redirect(url_for('todolist'))
	todo.done = 1
	db.session.add(todo)
	db.session.commit()
	return redirect(url_for('todolist'))

@app.route('/deletetodo/<int:id>')
@login_required
def deletetodo(id):
	todo = Todo.query.get(id)
	if todo is None:
		flash('This item does not exist')
		return redirect(url_for('todolist'))
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('todolist'))

@app.route('/deleteevent/<int:id>')
@login_required
def deleteevent(id):
	event = Event.query.get(id)
	if event is None:
		flash('This event does not exist')
		return redirect(url_for('calendar'))
	db.session.delete(event)
	db.session.commit()
	return redirect(url_for('calendar'))

@app.route('/search', methods=['POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('todolist'))
	return redirect(url_for('search_results', 
							query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	results = Todo.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	return render_template('search_results.html', query=query,
							results=results)