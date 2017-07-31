''' first, I imported this Flask class from the Flask library. '''
from flask import Flask , render_template, request, redirect, url_for
''' next, I create an instance of this class with the name
of running application. Anytime we run an application in Python,
a special variable called name gets defined for the application
and all of the imports it uses.'''
app = Flask(__name__)

''' Add CRUD functionality  '''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

''' I have this thing that looks like a function, but starts
with an @ symbol. This is called a decorator in Python. This
decorator essentially wraps our function inside app.route
function that Flask has already created.'''

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	'''I will change my restaurantMenu function to get the first
	restaurant in data base  '''
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	''' list of all itens of menu and stored in a string called output '''
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('menu.html', restaurant=restaurant, items=items)

	'''
	output = ''
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description	
		output += '</br>'
		output += '</br>'
	#return the string for user could see the items of restaurant
	return output
	'''
# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

''' the application run by the Python interpreter gets a name
variable set to __main__.
The if statment here makes sure the server only runs if the
script is executed directly from the Python interpreter, and
not used as an imported module.
So basically, this line of code says, if you're executing
me with the Python interpreter, then do this '''
if __name__ == '__main__':
	''' If you enable debug support the server will reload
	itself each time it notices a code change. It will also
	provide you a helpful debugger in the browser if things 
	go wrong'''
	app.debug = True
	''' I use the run function to run the local server with
	our application - (host = '0.0.0.0', port = 5000) this
	tells the web server on my vagran machine to listen on 
	all public IP addresses'''
	app.run(host = '0.0.0.0', port = 5000)
