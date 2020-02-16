import uuid,random,datetime
now = datetime.datetime.now()

from flask import Flask, jsonify, request
from flask_cors import CORS


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

#updated at_ options
updated = [5,10,15,30]

#daily energy stats
@app.route('/dailyStats', methods=['GET'])
def dailyStats():
    response_object = {'dailySolar': 0, 'dailyBattery': 0, 'dailyConS': 0, 'dailySave': 0, 'updated': 0}
    response_object['dailySolar'] = random.randint(100,200)
    response_object['dailyBattery'] = random.randint(0,100)
    response_object['dailyConS'] = random.randint(150,199)
    response_object['dailySave'] = random.randint(6,20)
    response_object ['updated'] = updated[random.randint(0,3)]
    return jsonify(response_object)



#daily energy consumption vs production
@app.route('/dailyCompare', methods=['GET'])
def dailyCons():
    #generate label
    label = []
    hour = now.hour
    for i in range(0,9): 
        label.append(hour) 
        hour -= 1
    label.reverse()

    #generate solor production and energy consumption series.
    # production   
    series0 = [0,0,0,0,0,0,0,0,0]
    #consumption
    series1 = [0,0,0,0,0,0,0,0,0]
    index = 0
    for i in label:
        if i in range(0,5):
            series0[index]= 0
            series1[index]= 0
            index += 1
        elif i in range(19,24):
            series0[index]= 0
            series1[index]= random.randint(5,70)
            index += 1
        else:
            series0[index]=random.randint(10,70)
            series1[index]=random.randint(5,70)
            index += 1

    #generate the return json object
    response_object = {"data":{"labels":[],"series":[[],[]]},"options":{"low":0, "high":0},"percentage":0,'updated':0}
    response_object['data']['labels'] = label
    response_object['data']['series'][0] = series0
    response_object['data']['series'][1] = series1
    response_object['options']['high'] = max(series0) + 50
    response_object['percentage'] = random.randint(5,20)
    response_object ['updated'] = updated[random.randint(0,3)]
    return jsonify(response_object)


# weekly energy consumption
@app.route('/weeklyCons', methods=['GET'])
def weeklyCons():
    #generate 
    series = [0,0,0,0,0,0,0]
    for i in range(0,7):
        series[i] = series[i] + random.randint(40,80)

    response_object = {"data":{"labels":["M","T","W","T","F","S","S"],"series":[[]]},"options":{"low":0, "high":0},"percentage":0,'updated':0}
    response_object['data']['series'][0] = series
    response_object['options']['high'] = max(series) + 50
    response_object['percentage'] = random.randint(5,20)
    response_object ['updated'] = updated[random.randint(0,3)]
    return jsonify(response_object)

# weekly energy consumption
@app.route('/weeklyProd', methods=['GET'])
def weeklyProd():
    return weeklyCons()


#consumption by devices
# @app.route('/byDevice', methods=['GET'])
# def byDevice:
#     items = []



#     response_object = {"item":[]}

# def getDevice():
    

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()