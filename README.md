# MongoDB with Python — Learning Repo

A collection of Python scripts demonstrating MongoDB operations using **PyMongo**, built while following the [MongoDB University](https://learn.mongodb.com/) course.

## Topics Covered

| Topic | Files |
|---|---|
| **Connection** | `connection.py` |
| **Insert** | `insert_single.py`, `insert_multiple.py` |
| **Find / Read** | `find_single.py`, `find_multiple.py` |
| **Update** | `update_single.py`, `update_many.py` |
| **Delete** | `delete_single.py`, `delete_many.py` |
| **Transactions** | `transactions.py` |
| **Aggregation Pipelines** | `mongodb_aggregation_pipeline/` — `$match`, `$group`, `$sort`, `$project`, `$unwind`, `$skip`, `$limit` |
| **FastAPI + MongoDB** | `mongoDB_and_FastAPI/` — Full CRUD REST API |

## Prerequisites

- Python 3.8+
- A MongoDB instance (local or [MongoDB Atlas](https://www.mongodb.com/atlas))

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Vardhanch05/MongoDB-python.git
   cd MongoDB-python
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   # source .venv/bin/activate  # macOS / Linux
   pip install -r requirements.txt
   ```

3. **Configure your connection string**

   Create a `.env` file inside `MongoDB_university_course/`:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
   ```

4. **Run any script**
   ```bash
   cd MongoDB_university_course
   python connection.py
   python insert_single.py
   # etc.
   ```

## Running the FastAPI App

```bash
cd MongoDB_university_course/mongoDB_and_FastAPI
uvicorn myfirstapp:app --reload
```

Then visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
MongoDB_learn/
├── .gitignore
├── requirements.txt
├── README.md
├── test_mongo.py
└── MongoDB_university_course/
    ├── .env                          ← your connection string (not tracked by Git)
    ├── connection.py
    ├── insert_single.py / insert_multiple.py
    ├── find_single.py / find_multiple.py
    ├── update_single.py / update_many.py
    ├── delete_single.py / delete_many.py
    ├── transactions.py
    ├── mongoDB_and_FastAPI/
    │   ├── myfirstapp.py             ← FastAPI CRUD app
    │   └── serializer.py
    └── mongodb_aggregation_pipeline/
        ├── aggregation.txt           ← theory notes
        ├── aggregation1_match_n_group.py
        ├── aggregation2_sort_n_project.py
        ├── aggregation_example.py
        └── pipeline_eg.py
```
