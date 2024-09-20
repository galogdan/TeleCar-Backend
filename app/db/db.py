from pymongo import MongoClient

uri = "mongodb+srv://galogdan321:TeleCar111@telecar.mrp67e9.mongodb.net/?retryWrites=true&w=majority&appName=TeleCar"
client = MongoClient(uri)
db = client["TeleCar"]
users_collection = db["Users"]
forum_collection = db["Forum"]
auctions_collection = db["Auctions"]
tickets_collection = db["Tickets"]
messages_collection = db ["Messagess"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
