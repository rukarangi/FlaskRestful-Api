from peewee import *

db = SqliteDatabase("tasks.sqlite")

#Model Task
class Task(Model):
	i = IntegerField()
	uri = TextField()
	title = TextField()
	description = TextField(default="")
	done = BooleanField(default=False)

	class Meta:
		database = db

#Database Methods
#def dbDecorator(func):
#	def wrapper(*args, **kwargs):
#		db.connect()
#		func(*args, **kwargs)
#		db.close()
#	return wrapper

def listGet():
	db.connect()
	tasksM = Task.select()
	tasks = [taskMToDict(task) for task in tasksM]
	db.close()
	return tasks

def listAdd(title, description):
	db.connect()
	taskIds = [task.i for task in Task.select()]
	newId = (taskIds[-1] + 1) if len(taskIds) > 0 else 1

	task = Task(
		i = newId,
		uri = "/todo/api/v1.0/tasks/{}".format(newId),
		title = title,
		description = description
		)
	task.save()

	db.close()
	return taskMToDict(task)

#@dbDecorator
def taskGet(i):
	db.connect()
	try:
		task = taskMToDict(Task.get(Task.i == i))
		task["response"] = 200
	except DoesNotExist:
		task = {"i": 1, "title": "Not Found", "response": 404}
	db.close()
	return task

def taskRemove(i):
	pass

def taskMToDict(taskM):
	task = {
		"i": taskM.i,
		"uri": taskM.uri,
		"title": taskM.title,
		"description": taskM.description,
		"done": taskM.done
	}
	return task


#Database Init
def initialise():
	db.connect()
	db.create_tables([Task], safe=True)
	db.close()
