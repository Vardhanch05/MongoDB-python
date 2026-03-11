# MongoDB Aggregation Pipeline Example using PyMongo

from pymongo import MongoClient

# Connect to MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Create / access database
db = client["company"]

# Create / access collection
collection = db["employees"]

# Remove existing documents (to avoid duplicates)
collection.delete_many({})

# Insert sample employee data
employees = [
    {"name": "Alice", "department": "IT", "salary": 60000, "skills": ["Python", "MongoDB"]},
    {"name": "Bob", "department": "IT", "salary": 55000, "skills": ["Java", "SQL"]},
    {"name": "Charlie", "department": "HR", "salary": 50000, "skills": ["Communication"]},
    {"name": "David", "department": "HR", "salary": 52000, "skills": ["Management"]},
    {"name": "Eve", "department": "Finance", "salary": 65000, "skills": ["Accounting", "Excel"]}
]

collection.insert_many(employees)

# Pipeline stages for aggregation
pipeline = [

    # $match stage: filter employees with salary greater than 50000
    {"$match": {"salary": {"$gt": 50000}}},

    # $unwind stage: split the skills array into separate documents
    {"$unwind": "$skills"},

    # $group stage: group employees by department and calculate statistics
    {
        "$group": {
            "_id": "$department",
            "average_salary": {"$avg": "$salary"},
            "total_employees": {"$sum": 1}
        }
    },

    # $project stage: format the output fields
    {
        "$project": {
            "_id": 0,
            "department": "$_id",
            "average_salary": 1,
            "total_employees": 1
        }
    },

    # $sort stage: sort departments by highest average salary
    {"$sort": {"average_salary": -1}},

    # $skip stage: skip the first document (for pagination example)
    {"$skip": 0},

    # $limit stage: limit results to top 5 records
    {"$limit": 5}
]

# Execute the aggregation pipeline
result = collection.aggregate(pipeline)

# Print the results
print("Aggregation Pipeline Result:\n")
for doc in result:
    print(doc)

# Output:
'''
Aggregation Pipeline Result:

{'average_salary': 65000.0, 'total_employees': 2, 'department': 'Finance'}
{'average_salary': 57500.0, 'total_employees': 4, 'department': 'IT'}
{'average_salary': 52000.0, 'total_employees': 1, 'department': 'HR'}
'''