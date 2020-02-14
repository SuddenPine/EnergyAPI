import uuid,random

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


#daily energy stats
@app.route('/dailyStats', methods=['GET'])
def dailyStats():
    updated = [5,10,15,30]
    response_object = {'dailySolar': 0, 'dailyBattery': 0, 'dailyConS': 0, 'dailySave': 0, 'updated': 0}
    response_object['dailySolar'] = random.randint(100,200)
    response_object['dailyBattery'] = random.randint(0,100)
    response_object['dailyConS'] = random.randint(150,199)
    response_object['dailySave'] = random.randint(6,20)
    response_object ['updated'] = updated[random.randint(0,3)]
    return jsonify(response_object)

# dailyConsumptionChart: {
#         data: {
#           labels: ["M", "T", "W", "T", "F", "S", "S"],
#           series: [[250, 300, 332, 311, 320, 450, 501]]
#         },
#         options: {
#           lineSmooth: this.chartist.Interpolation.cardinal({
#             tension: 0
#           }),
#           low: 0,
#           high: 600, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
#           chartPadding: {
#             top: 0,
#             right: 0,
#             bottom: 0,
#             left: 0
#           }
#         }
#       }

#daily energy production
@app.route('/dailyProd', methods=['GET'])
def dailyProd():
    #generate 
    series = [0,0,10,20,30,40,30,10,0]
    series[2] = series[2] + random.randint(5,10)
    for i in range(2,8):
        series[i] = series[i] + random.randint(5,10)
    response_object = {"data":{"labels":[],"series":[]},"options":{"low":0, "high":0}}
    response_object['data']['labels'] = [i for i in range(0,25,3)]
    response_object['data']['series'] = series
    response_object['options']['high'] = max(series) + 50
    return jsonify(response_object)


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