# It has to have Routes: e.g., /login, /register, /, /dashboard?query=1.
# it has to have a method eg GET,POST,PUT,DELETE,OPTIONS,PATCH.
# It has to have a status code e.g 200,201,403,405
# it has to have transfer data in JSON (Key:value pairs).
from datetime import datetime
import sentry_sdk
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import create_engine, select
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session
from models import Base, Product, User, Purchase, Sale, Sale_detail, Payment

sentry_sdk.init(
    dsn="https://899e75018a56d49525f60a35ff6c86c4@o4512045998145536.ingest.us.sentry.io/4512046187151360",
    send_default_pii=True,
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] ="EXPLORE13"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# create a connection to the database using sqlalchemy
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# create a session to do sql transactions
session = Session(engine)

allowed_methods=["get","put","post","delete","patch","head","options"]


@app.route("/",methods=allowed_methods)
def home():
    if request.method == "GET":
        data = {"Flask API" : "Version 1"}
        return jsonify(data), 200
    else:
        error = {"error": "Method not allowed"}
        return jsonify(error), 405


#  REGISTER.
@app.route("/register",methods=allowed_methods)
def register():
    try:
        if request.method=="GET":
            error={"error":"Method not allowed"}
            return jsonify(error),405
        elif request.method=="POST":
            # FETCH DATA FROM REQUEST.
            data=request.get_json()
            # CHECK IF ALL FIELDS ARE SET.
            if not data or data.get("full_name")=="" or data.get("email")=="" or data.get("password")=="":
                error={"error":"Ensure all fields are set"}
                return jsonify(error),403
            else:
                # CHECK IF EMAIL EXISTS.
                query=select(User).where(User.email==data["email"])
                existing=session.scalars(query).first()
                if existing:
                    error={"error":"Email already exists"}
                    return jsonify(error),409
                elif not existing:
                    # HASH PASSWORD.
                    hashed_password=bcrypt.generate_password_hash(data["password"]).decode("utf-8")
                    # STORE DATA IN DATABASE.
                    new_user=User(
                        full_name=data["full_name"],
                        email=data["email"],
                        password=hashed_password
                    )
                    session.add(new_user)
                    session.commit()
                    # CREATE JWT TOKEN.
                    token=create_access_token(identity=data["email"])
                    message={
                        "message":"New user added successfully",
                        "id":new_user.id,
                        "token":token
                    }
                    return jsonify(message),201
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        error={"error":"Sorry, try again"}
        return jsonify(error),500


# LOGIN
@app.route("/login",methods=allowed_methods)
def login():
    try:
        if request.method=="GET":
            error={"error":"Method not allowed"}
            return jsonify(error),405
        elif request.method=="POST":
            # FETCH DATA FROM REQUEST.
            data=request.get_json()
            # CHECK IF ALL FIELDS ARE SET.
            if not data or data.get("email")=="" or data.get("password")=="":
                error={"error":"Email and password are required"}
                return jsonify(error),403
            else:
                # FIND USER FROM DATABASE.
                query=select(User).where(User.email==data["email"])
                user=session.scalars(query).first()
                # CHECK IF USER EXISTS.
                if not user:
                    error={"error":"Invalid email or password"}
                    return jsonify(error),401
                elif user:
                    # CHECK PASSWORD.
                    if not bcrypt.check_password_hash(user.password,data["password"]):
                        error={"error":"Invalid email or password"}
                        return jsonify(error),401
                    else:
                        # CREATE JWT TOKEN.
                        token=create_access_token(identity=user.email)
                        message={
                            "message":"Login successfully",
                            "id":user.id,
                            "full_name":user.full_name,
                            "email":user.email,
                            "token":token
                        }
                        return jsonify(message),200
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"something went wrong try again"}),500


# USERS ROUTE
@app.route("/users", methods=["GET"])
def users():

    # Get all users
    users = session.scalars(
        select(User)
    ).all()

    results = []

    for user in users:
        results.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        })

    return jsonify(results), 200


# PRODUCT
@app.route("/products",methods=allowed_methods)
@jwt_required()
def products():
    try:
        email=get_jwt_identity()
        if request.method=="GET":
            # FETCH DATA FROM THE DATABASE.
            query=select(Product)
            products=session.scalars(query)
            results=[]
            for prod in products:
                p={
                    "id":prod.id,
                    "product_name":prod.product_name,
                    "buying_price":prod.buying_price,
                    "selling_price":prod.selling_price
                }
                results.append(p)
            return jsonify(results),200
        elif request.method=="POST":
            data=request.get_json()
            if not data or data.get("product_name")=="" or data.get("buying_price")=="" or data.get("selling_price")=="":
                error={"error":"Ensure all fields are set"}
                return jsonify(error),403
            else:
                # STORE IN THE DATABASE.
                new_product=Product(
                    user_id=data["id"],
                    product_name=data["product_name"],
                    buying_price=float(data["buying_price"]),
                    selling_price=float(data["selling_price"])
                )
                session.add(new_product)
                session.commit()
                return jsonify({"message":"A new product added successfully"}),201
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"sorry try again"}),500
    

#PURCHASE.
@app.route("/purchases",methods=allowed_methods)
@jwt_required()
def purchases():
    try:
        email=get_jwt_identity()
        if request.method=="GET":
            # FETCH DATA FROM DATABASE.
            query=select(Purchase)
            purchases=session.scalars(query)
            results=[]
            for purch in purchases:
                pu={
                    "product_id":purch.id,
                    "quantity":purch.quantity,
                    "paid_amount":purch.paid_amount,
                    "created_at":purch.created_at
                }
                results.append(pu)
            return jsonify(results),200
        elif request.method=="POST":
            data=request.get_json()
            if not data or data.get("product_id")=="" or data.get("quantity")=="" or data.get("paid_amount")=="":
                error={"error":"Ensure all fields are set"}
                return jsonify(error),403
            else:
                # STORE IN THE DATABASE.
                new_purchase=Purchase(
                    product_id=data["product_id"],
                    quantity=data["quantity"],
                    paid_amount=data["paid_amount"],
                    created_at=datetime.now()
                )
                session.add(new_purchase)
                session.commit()
                return jsonify({"Message":"A new purchase made successfully"}),201
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"sorry try again"}),500


# SALE ROUTE
@app.route("/sales",methods=allowed_methods)
@jwt_required()
def sales():
    try:
        email=get_jwt_identity()
        if request.method=="GET":
            # FETCH DATA FROM DATABASE.
            query=select(Sale)
            sales=session.scalars(query)
            results=[]
            for sal in sales:
                s={"id":sal.id,"product_id":sal.product_id,
                   "created_at":sal.created_at}
                results.append(s)
            return jsonify(results),200
        elif request.method=="POST":
            data=request.get_json()
            if data["product_id"]=="":
                error={"error":"Ensure all the fields are set"}
                return jsonify(error),403
            else:
                # STORE IN THE DATABASE.
                new_sale=Sale(
                    product_id=data["product_id"],
                    created_at=datetime.now()
                )
                session.add(new_sale)
                session.commit()
            return jsonify({"Message":"New sale successfully made"}),201
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"sorry try again"}),500


#  SALE_DETAILS.
@app.route("/sale_details",methods=allowed_methods)
@jwt_required()
def sales_details():
    try:
        email=get_jwt_identity()
        if request.method=="GET":
            # FETCH DATA FROM DATABASE.
            query=select(Sale_detail)
            sale_details=session.scalars(query)
            results=[]
            for sald in sale_details:
                sd={"id":sald.id,"product_id":sald.product_id,
                    "quantity":sald.quantity}
                results.append(sd)
            return jsonify(results),200
        elif request.method=="POST":
            data=request.get_json()
            if data["product_id"]=="" or data["quantity"]=="":
                error={"error":"Ensure all fields are set"}
                return jsonify(error),403
            else:
                # STORE IN THE DATABASE.
                new_sale_details=Sale_detail(
                    product_id=data["product_id"],
                    sale_id=data["sale_id"],
                    quantity=data["quantity"]
                )
                session.add(new_sale_details)
                session.commit()
                return jsonify({"Message":"Sale Details successfully added"})
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"sorry try again"}),500

# PAYMENT
@app.route("/payments",methods=allowed_methods)
@jwt_required()
def payments():
    try:
        email=get_jwt_identity()
        if request.method=="GET":
            # FETCH DATA FROM DATABASE.
            query=select(Payment)
            payments=session.scalars(query)
            results=[]
            for py in payments:
                py={"id":py.id,"amount":py.amount,"method":py.method,"transcode":py.trans_code,"status":py.status,"created_at":py.created_at}
                results.append(py)
            return jsonify(results),200
        elif request.method=="POST":
            data=request.get_json()
            if data["amount"]=="" or data["method"]=="" or data["transcode"]=="" or data["status"]=="":
                error={"error":"Ensure all fields are set"}
                return jsonify(error),403
            else:
                # STORE IN THE DATABASE.
                new_payment=Payment(
                    id=data["id"],
                    amount=data["amount"],
                    method=data["method"],
                    trans_code=data["transcode"],
                    status=data["status"],
                    created_at=datetime.now()
                )
                session.add(new_payment)
                session.commit()
            return jsonify({"Message":"payment successfully made"}),201
        else:
            error={"error":"Method not allowed"}
            return jsonify(error),405
    except Exception as e:
        session.rollback()
        sentry_sdk.capture_exception(e)
        return jsonify({"error":"sorry try again"}),500


app.run(debug=True)
