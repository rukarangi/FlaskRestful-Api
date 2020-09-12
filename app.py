from flask import Flask, url_for
from flask_restful import Api, Resource, reqparse, marshal, fields

from databaseControl import initialise, Task, db, listGet, listPost, taskGet, taskPut, taskDelete

#Setup App and Api objects

DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

app = Flask(__name__)
api = Api(app)

#Api classes and routes

taskGuide = {
	"uri": fields.Url("task"),
	"title": fields.String,
	"description": fields.String,
	"done": fields.Boolean
}

class TaskListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument("title", type = str, required = True,
			help = "No task title provided", location = "json")
		self.reqparse.add_argument("description", type = str, default = "",
			location = "json")
		super(TaskListAPI, self).__init__()

	def get(self):
		print("get list")
		tasks = listGet()
		return {"tasks": [marshal(task, taskGuide) for task in tasks]}

	def post(self):
		args = self.reqparse.parse_args()
		task = listPost(args["title"], args["description"])
		return {"task": marshal(task, taskGuide)}

class TaskAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument("title", type = str, location = "json")
		self.reqparse.add_argument("description", type = str, location = "json")
		self.reqparse.add_argument("done", type = bool, location = "json")
		super(TaskAPI, self).__init__()

	def get(self, i):
		args = self.reqparse.parse_args()
		task = taskGet(i)
		return {"task": marshal(task, taskGuide)}, task["response"]

	def put(self, i):
		args = self.reqparse.parse_args()
		print(args["done"])
		task = taskPut(i, args["done"])
		return {"task": marshal(task, taskGuide)}, task["response"]

	def delete(self, i):
		task = taskDelete(i)
		return {"task": task}, task["response"]

api.add_resource(TaskListAPI, "/todo/api/v1.0/tasks", endpoint = "tasks")
api.add_resource(TaskAPI, "/todo/api/v1.0/tasks/<int:i>", endpoint = "task")

if __name__ == "__main__":
	initialise()
	app.run(debug=DEBUG, host=HOST, port=PORT)