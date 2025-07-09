# love-crush-app/app.py
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
import certifi

app = Flask(__name__)

# MongoDB connection
ca = certifi.where()
client = MongoClient("mongodb+srv://arulselvamarun0602:Ar%4006012001@lovecluster.oc9jwjd.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true", tlsCAFile=ca)
db = client["loveApp"]
collection = db["responses"]

# Show the form page
@app.route("/")
def form():
    return render_template("form.html")

# Save form data to MongoDB
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    print("📨 Received form data:", data)

    try:
        result = collection.insert_one(data)
        print("✅ Inserted to MongoDB:", result.inserted_id)
        return jsonify({"message": "Saved!", "id": str(result.inserted_id)})
    except Exception as e:
        print("🔥 ERROR inserting to MongoDB:", type(e).__name__, str(e))
        return jsonify({"error": str(e)}), 500

# Serve the crush response page
@app.route("/love/<id>", methods=["GET"])
def love_page(id):
    try:
        doc = collection.find_one({"_id": ObjectId(id)})
        if not doc:
            return "Link not found 😢"
        return render_template("crush.html", sender=doc["sender"], crush=doc["crush"], id=id)
    except Exception as e:
        print("Error loading love page:", e)
        return "Server error 😢"

# Save crush's response
@app.route("/respond/<id>/<choice>", methods=["POST"])
def respond(id, choice):
    try:
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"response": choice}})
        return jsonify({"status": "saved", "response": choice})
    except Exception as e:
        print("Error saving response:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
