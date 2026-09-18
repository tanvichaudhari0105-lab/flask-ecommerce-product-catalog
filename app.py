from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app =Flask(__name__)#cretes our flask application
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", 3306))
)
@app.route("/")
def home():#first page
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()

    return render_template("index.html", products=products)

@app.route("/add-product",methods=["GET", "POST"])
def add_product():
    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]
        category = request.form["category"]

        cursor = db.cursor()

        query ="""
        INSERT INTO products
        (name,description, price ,stock, category)
        VALUES(%s, %s, %s, %s, %s)
        """
        values =(name, description, price, stock, category)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return "Product added successfully!"
    return render_template("add_product.html")

@app.route("/update-product/<int:id>",methods=["GET", "POST"])
def update_product(id):
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE id = %s",(id,))

    product = cursor.fetchone()

    cursor.close()

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]
        category = request.form["category"]

        cursor =db.cursor()

        query = """
        UPDATE products
        SET name =%s,
        description = %s,
        price = %s,
        stock = %s,
        category =%s
        WHERE id = %s
        """

        values= (name, description, price, stock, category, id)

        cursor.execute(query, values)
        db.commit()

        cursor.close()

        return "Product updated successfully!"

    return render_template("update_product.html",product=product)
@app.route("/delete-product/<int:id>", methods=["POST"])
def delete_product(id):
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )
    db.commit()

    cursor.close()

    return "Product deleted successfully"

@app.route('/api/products', methods=['GET'])
def get_products():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()

    return jsonify(products)  

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM products WHERE id = %s",
        (id,)
    )

    product = cursor.fetchone()

    cursor.close()

    if product is None:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product)
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    name = data['name']
    description = data['description']
    price = data['price']
    stock = data['stock']
    category = data['category']

    cursor = db.cursor()

    query = """
    INSERT INTO products
    (name, description, price, stock, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (name, description, price, stock, category)

    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({"message": "Product created successfully"}), 201 

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product_api(id):
    data = request.get_json()

    name = data['name']
    description = data['description']
    price = data['price']
    stock = data['stock']
    category = data['category']

    cursor = db.cursor()

    query = """
    UPDATE products
    SET name = %s,
        description = %s,
        price = %s,
        stock = %s,
        category = %s
    WHERE id = %s
    """

    values = (name, description, price, stock, category, id)

    cursor.execute(query, values)
    db.commit()

    cursor.close()

    return jsonify({"message": "Product updated successfully"})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product_api(id):
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )

    db.commit()
    cursor.close()

    return jsonify({"message": "Product deleted successfully"})  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)#starts flask development server and relods when we chance our code