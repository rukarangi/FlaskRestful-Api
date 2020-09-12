from flask import Flask 
from flask_restful import Api, Resource, reqparse


#Setup App and Api objects

app = Flask(__name__)
api = Api(app)

#Api classes and routes

class TaskListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument("title", type = str, required = True,
			help = "No task title provided", location = "json")
		self.reqparse.add_argument("description", type = str, default = "",
			location = "json")
		super(TaskListAPI, self).__init__()

	def get(self):
		pass

	def post(self):
		pass

class TaskAPI(Resource):
	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass

api.add_resource(TaskListAPI, "/todo/api/v1.0/tasks", endpoint = "tasks")
api.add_resource(TaskAPI, "/todo/api/v1.0/tasks/<int:id>", endpoint = "task")