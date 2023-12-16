import csv
from pymongo import MongoClient
import pymongo
#Connecting to MongoDB
mongo_client = pymongo.MongoClient("mongodb+srv://SSP:Surya123@cluster0.fkaowh5.mongodb.net/?retryWrites=true&w=majority")
mongo_db = mongo_client['sample_airbnb']
mongo_listingsAndReviews = mongo_db['listingsAndReviews']

# 3. Query MongoDB (retrieve all documents)
data_from_mongodb = mongo_client['sample_airbnb']

# 4. Convert MongoDB Data to a List of Dictionaries
data_list = []

for doc in data_from_mongodb:
    row = {
        "id": doc["_id"],
        "listing_title": doc["name"],
        "listing_description": doc["description"],
        "unique_host_id": doc["host_id"],
        "host_name": doc["host_name"],
        "neighbourhood_name": doc["neighbourhood"],
        "longitude": doc["location"]["coordinates"][0],
        "latitude": doc["location"]["coordinates"][1],
        "listing_price": doc["price"],
        "start_date": doc["availability"]["start_date"],
        "end_date": doc["availability"]["end_date"],
        "amenities": ", ".join(doc["amenities"]),  # Convert the list to a comma-separated string
        "average_rating": doc["rating"]
    }
    data_list.append(row)

# 5. Write to CSV File
with open("data.csv", "w", newline="") as csv_file:
    fieldnames = [
        "id", "listing_title", "listing_description", "unique_host_id",
        "host_name", "neighbourhood_name", "longitude", "latitude",
        "listing_price", "start_date", "end_date", "amenities", "average_rating"
    ]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in data_list:
        csv_writer.writerow(row)
