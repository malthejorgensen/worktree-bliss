import os

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    # conn = DatabaseConnection(os.getenv("DATABASE_URL"))
    print("Connecting to Postgres: %s" % os.getenv("DATABASE_URL"))
    print("Connecting to Redis: %s" % os.getenv("REDIS_URL"))
    app.run(port=os.getenv("PORT_LAST_DIGIT"))
