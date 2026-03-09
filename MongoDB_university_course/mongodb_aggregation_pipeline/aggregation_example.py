from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create / access database
db = client["company"]

# Create / access collection
collection = db["employees"]

# Insert sample data
employees = [
    {"name": "Alice", "department": "IT", "salary": 60000},
    {"name": "Bob", "department": "IT", "salary": 55000},
    {"name": "Charlie", "department": "HR", "salary": 50000},
    {"name": "David", "department": "HR", "salary": 52000},
    {"name": "Eve", "department": "Finance", "salary": 65000}
]

collection.delete_many({})   # clear old data
collection.insert_many(employees)

# Aggregation Pipeline
pipeline = [
    {
        "$group": {
            "_id": "$department",
            "average_salary": {"$avg": "$salary"},
            "total_employees": {"$sum": 1}
        }
    },
    {
        "$sort": {"average_salary": -1}
    }
]

# Execute aggregation
result = collection.aggregate(pipeline)

print("Department-wise Salary Analysis:")
for doc in result:
    print(doc)