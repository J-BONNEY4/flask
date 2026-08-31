# It has to have Routes: e.g., /login, /register, /, /dashboard?query=1.
# it has to have a method eg GET,POST,PUT,DELETE,OPTIONS,PATCH.
# It has to have a status code e.g 200,201,403,405
# it has to have transfer data in JSON (Key:value pairs).
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Product, User, Purchase,Sale,Sale_detail,Payment

app = Flask(__name__)

# create a connection to the database using sqlalchemy
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# create a session to do sql transactions
session = Session(engine)

user = {"id": "1",
        "full_name": "Bonney",
        "email": "bon@gmail.com",
        "password": "bonn0",
        }


@app.before_request
def before_request():
    try:
        print("A request is coming in")
        new_user = User(user)
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User added successfully}"}), 201
    except:
        print("Error found")


@app.route("/")
def home():
    if request.method == "GET":
        data = {"Flask API": "Version 1"}
        return jsonify(data), 200
    else:
        error = {"error": "Method not allowed"}
        return jsonify(error), 405

# PRODUCTS ROUTE.
@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        # fetch data from the database.
        query = select(Product)
        products = session.scalars(query)
        results = []
        for prod in products:
            p = {"id": prod.id, "product_name": prod.product_name,
                 "buying_price": prod.buying_price, 
                 "selling_price": prod.selling_price}
            results.append(p)
        return jsonify(results), 200

    elif request.method == "POST":
        data = request.get_json()
        if data["product_name"] == "" or data["buying_price"] == "" or data["selling_price"] == "":
            error = {"error": "Ensure all fields are set"}
            return jsonify(error), 403
        else:
            # store in the database
            new_product = Product(
                user_id=user["id"],
                product_name=data["product_name"],
                buying_price=float(data["buying_price"]),
                selling_price=float(data["selling_price"])
            )
            session.add(new_product)
            session.commit()
        return jsonify({"message": "A new product added successfully"}), 201
    else:
        error = {"error": "method not allowed"}
        return jsonify(error), 405

# PURCHASE ROUTE.
@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if request.method =="GET":
        # FETCH DATA FROM DATABASE.
        query= select (Purchase)
        purchases = session.scalars(query)
        results =[]
        for purch in purchases:
            pu= {"product_id" : purch.id,"quantity" : purch.quantity,"paid_amount" :purch.paid_amount,
                 "created_at": purch.created_at}
            results.append(pu)
        return jsonify(results),200
    elif request.method == "POST":
        data = request.get_json()
        if data ["quantity"] == "" or data ["paid_amount"] == "" or data["created_at"]=="":
            error={"error": "Ensure all fields are set"}
            return jsonify(error),403
        else:
            # STORE IN THE DATABASE.
            new_purchase=Purchase(
                product_id= data["product_id"],
                quantity= data["quantity"],
                paid_amount= data["paid_amount"],
                created_at =datetime.now()
            )
            session.add(new_purchase)
            session.commit()
        return jsonify ({"Message" :"A new purchase made successfully"}), 201
    else:
        error = {"error" : "Method not allowed"}
        return jsonify(error),405

# SALE ROUTE
@app.route("/sales", methods=["GET","POST"])
def sales():
    if request.method =="GET":
        # FETCH DATA FROM DATABASE.
        query= select (Sale)
        sales=session.scalars(query)
        results =[]
        for sal in sales:
            s={"id" :sal.id, "product_id" : sal.product_id,"created_at": sal.created_at}
            results.append(s)
        return jsonify(results),200
    elif request.method== "POST":
         data =request.get_json()
         if data ["product_id"] =="":
             error={"error" : "Ensure all the fields are set"}
             return jsonify(error),403
         else:
            #  STORE IN THE DATABASE.
            new_sale=Sale(
                product_id= data["product_id"],
                created_at =datetime.now()
            )
            session.add(new_sale)
            session.commit()
         return jsonify({"Message" : "New sale successfully made"}),201
    else:
        error={"error" : "Method not allowed"}
        return jsonify(error),405

#  SALE_DETAILS.
@app.route("/sale_details", methods = ["GET","POST"])
def sales_details():
          if request.method=="GET":
            #   FETCH DATA FROM DATABASE.
            query= select (Sale_detail)
            sale_details = session.scalars(query)
            results =[]
            for sald in sale_details:
                sd={"id" : sald.id, "product_id" :sald.product_id,"quantity":sald.quantity}
                results.append(sd)
            return jsonify(results),200
          elif request.method=="POST":
              data=request.get_json()
              if data ["product_id"] =="" or data ["quantity"] =="":
                  error={"error","Ensure all fields are set"}
                  return jsonify(error),403
              else:
                #   STORE IN THE DATABASE.
                new_sale_details=Sale_detail(
                    product_id=data["product_id"],
                    sale_id=data["sale_id"],
                    quantity=data["quantity"]
                )
                session.add(new_sale_details)
                session.commit()
                return jsonify ({"Message" :"Sale Details successfully added"})
          else:
              error={"error" : "Method not allowed"}
              return jsonify(error),405
              
# PAYMENTS.
@app.route("/payments",methods =["GET","POST"])
def payments():
    if request.method=="GET":
        # FETCH DATA FROM DATABASE.
        query=select (Payment)
        payments=session.scalars(query)
        results=[]
        for py in payments:
            py={"id":py.id,"amount":py.amount,"method" :py.method,"transcode" :py.trans_code,
                "status":py.status,"created_at":py.created_at}
            results.append(py)
        return jsonify(results),200
    elif request.method=="POST":
        data = request.get_json()
        if data ["amount"] == "" or data["method"]== "" or data["transcode"]=="" or data["status"]=="":
           error={"error":"Ensure all fields are set"}
           return jsonify(error),403
        else:
            # STORE IN THE DATABASE.
            new_payment=Payment(
                id=data["id"],
                amount=data["amount"],
                method= data["method"],
                trans_code=data["transcode"],
                status=data["status"],
                created_at=datetime.now()
            )
            session.add(new_payment)
            session.commit()
        return jsonify ({"Message":"payment successfully made"}),201
    else:
        error={"error" : "Method not allowed"}
        return jsonify(error),405
    


app.run(debug=True)
