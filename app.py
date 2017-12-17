from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__);

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify({'task': task})
    abort(404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            if not request.json:
                abort(400)
            if 'title' in request.json and type(request.json['title']) != unicode:
                abort(400)
            if 'description' in request.json and type(request.json['descripton']) != unicode:
                abort(400)
            if 'done' in request.json and type(request.json['done']) is not bool:
                abort(400)
            task['title'] = request.json.get('title', task['title'])
            task['description'] = request.json.get('description', task['description'])
            task['done'] = request.json.get('done', task['done'])
            return jsonify({'task': task})
    abort(404)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({'result': True})
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)