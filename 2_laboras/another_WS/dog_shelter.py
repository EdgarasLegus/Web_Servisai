from flask import Flask
from flask import request
from flask import jsonify
from flask import abort

import os

app = Flask(__name__)

dogs_db = [
	{'id' : '1', 'breed' : 'French bulldog', 'name' : 'Doggo', 'temporary guardian ID' : 'NONE'},
	{'id' : '2', 'breed' : 'Chow Chow', 'name' : 'Sir Pup', 'temporary guardian ID' : 'NONE'},
	{'id' : '3', 'breed' : 'Spaniel', 'name' : 'Coco', 'temporary guardian ID' : 'NONE'},
	{'id' : '4', 'breed' : 'French bulldog', 'name' : 'Olive', 'temporary guardian ID' : 'NONE'},
	{'id' : '5', 'breed' : 'German Shepherd', 'name' : 'Rex', 'temporary guardian ID' : 'NONE'}
]

@app.route('/')
def hello():
	return'Welcome to the puppy shelter'

# GET information about all dogs from database as JSON
@app.route('/dogs', methods=['GET'])
def get_all_dogs():
	return jsonify(dogs_db)

# GET any dog by any parameter
@app.route('/dogs/<parameter>', methods=['GET'])
def get_dog(parameter):
	my_dog = [ dog for dog in dogs_db if (dog['id'] == parameter or 
		dog['breed'] == parameter or dog['name'] == parameter or
		dog['temporary guardian ID'] == parameter)]
	if len(my_dog) == 0:
		abort(404)
	return jsonify(my_dog[0])



# DELETE a dog from a database by ID (adopt)
@app.route('/dogs/<dog_id>', methods=['DELETE'])
def adopt_dog(dog_id):
	adopted_dog = [ dog for dog in dogs_db if (dog['id'] == dog_id )]
	if len(adopted_dog) == 0:
		abort(404)
	dogs_db.remove(adopted_dog[0])
	return jsonify(adopted_dog[0]), 200

# POST a dog to a database (give away)
# Name is in url, id and breed have to be provided as JSON
@app.route('/dogs', methods=['POST'])
def give_away_dog():
	current_id = int(dogs_db[len(dogs_db) - 1]['id']) + 1
	new_dog = {
	'id' : str(current_id),
	'breed' : request.json['breed'],
	'temporary guardian ID' : request.json['temporary guardian ID'],
	'name' : request.json['name']
	}
	dogs_db.append(new_dog)
	
	return jsonify(new_dog), 201
	

# PUT change a dog
# Any parameter in URL
@app.route('/dogs/<dog_id>', methods = ['PUT'])
def change_dog(dog_id):
	changed_dog = [ dog for dog in dogs_db if (dog['id'] == dog_id )]
	if len(changed_dog) == 0:
		abort(404)
	if 'name' in request.json:
		changed_dog[0]['name'] = request.json['name']
	if 'breed' in request.json:
		changed_dog[0]['breed'] = request.json['breed']
	if 'temporary guardian ID' in request.json:
		changed_dog[0]['temporary guardian ID'] = request.json['temporary guardian ID']

	return jsonify(changed_dog[0])


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
