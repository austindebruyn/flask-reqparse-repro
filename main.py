from flask import Flask, request
from flask_restplus import Resource, Api, reqparse, fields

app = Flask(__name__)
api = Api(app)

todos = {}

# --
# Using reqparse for args works for calling `parser.parse_args()` but does not
# generate proper swagger doc
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, help='Task to be completed', location='json')
parser.add_argument('priority', type=str, help='Priority of task', location='json')

# --
# Using task_fields generates proper swagger doc
task_fields = api.model('task_fields', {
    'task': fields.String,
    'priority': fields.String
})


@api.route('/<string:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    # @api.expect(parser)     # Use this line instead of L30 to see actual output
    @api.expect(task_fields)  # This produces expected output
    def put(self, todo_id):
        # todos[todo_id] = parser.parse_args(strict=True)
        # todos[todo_id] = request.form

        todos[todo_id] = request.json

        return {todo_id: todos[todo_id]}

if __name__ == '__main__':
    app.run(debug=True)
