# from gevent import monkey
# monkey.patch_all()
from App import  create_app
from flask import Flask

app = create_app()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000)
