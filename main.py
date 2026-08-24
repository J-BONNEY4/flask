# It has to have Routes: e.g., /login, /register, /, /dashboard?query=1.
# it has to have a method eg GET,POST,PUT,DELETE,OPTIONS,PATCH.
# It has to have a status code e.g 200,201,403,405
# it has to have transfer data in JSON (Key:value pairs).
from flask import Flask,request,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    if request.method=="GET":
        data={"Flask API" : "Version 1"}
        return jsonify(data),200
    else:
        error={"error" : "Method not allowed"}
        return jsonify(error),405

app.run(debug=True)