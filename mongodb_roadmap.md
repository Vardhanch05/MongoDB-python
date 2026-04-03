# MongoDB + Python — Learning Roadmap

## ✅ What You've Already Covered

Based on your repo, you've completed these topics:

| # | Topic | Files | Status |
|---|-------|-------|--------|
| 1 | **Connecting to Atlas** | `connection.py` | ✅ Done |
| 2 | **Insert One** | `insert_single.py` | ✅ Done |
| 3 | **Insert Many** | `insert_multiple.py` | ✅ Done |
| 4 | **Find One** | `find_single.py` | ✅ Done |
| 5 | **Find Many** (with query operators `$gt`) | `find_multiple.py` | ✅ Done |
| 6 | **Update One** (`$inc`) | `update_single.py` | ✅ Done |
| 7 | **Update Many** (`$set`) | `update_many.py` | ✅ Done |
| 8 | **Delete One** | `delete_single.py` | ✅ Done |
| 9 | **Delete Many** (with `$lt`) | `delete_many.py` | ✅ Done |
| 10 | **Transactions** (multi-doc ACID) | `transactions.py` | ✅ Done |
| 11 | **Aggregation: `$match` + `$group`** | `aggregation1_match_n_group.py` | ✅ Done |
| 12 | **Aggregation: `$sort` + `$project` + `$divide`** | `aggregation2_sort_n_project.py` | ✅ Done |
| 13 | **Aggregation: `$unwind` + `$skip` + `$limit`** | `pipeline_eg.py` | ✅ Done |
| 14 | **FastAPI + MongoDB** (async CRUD with Motor) | `myfirstapp.py` | ✅ Done |
| 15 | **Serializer** (ObjectId → string) | `serializer.py` | ✅ Done |

**Summary:** CRUD is solid. Aggregation is **partially done** — you've covered 7 stages out of 18+. Transactions and a basic FastAPI app are in place.

---

## 🟡 Aggregation Pipeline — Detailed Progress

Here's every aggregation stage and where you stand:

| Stage | What It Does | Status |
|-------|-------------|--------|
| `$match` | Filter documents (like SQL `WHERE`) | ✅ Done |
| `$group` | Group + aggregate (`$sum`, `$avg`) | ✅ Done |
| `$sort` | Order results | ✅ Done |
| `$project` | Reshape docs, include/exclude fields | ✅ Done |
| `$unwind` | Flatten arrays into separate docs | ✅ Done |
| `$skip` | Skip N documents (pagination) | ✅ Done |
| `$limit` | Return only N documents | ✅ Done |
| | | |
| `$lookup` | **Join** two collections (SQL `JOIN`) | ❌ Not covered |
| `$addFields` / `$set` | Add computed fields to documents | ❌ Not covered |
| `$replaceRoot` | Replace the entire document with a sub-doc | ❌ Not covered |
| `$count` | Count documents in pipeline | ❌ Not covered |
| `$out` | Write pipeline results to a new collection | ❌ Not covered |
| `$merge` | Merge results into an existing collection | ❌ Not covered |
| `$bucket` | Group into ranges (histograms) | ❌ Not covered |
| `$facet` | Run multiple pipelines in parallel | ❌ Not covered |
| `$graphLookup` | Recursive/tree lookups (org charts, etc.) | ❌ Not covered |
| `$redact` | Field-level access control in pipeline | ❌ Not covered |
| `$sample` | Randomly select N documents | ❌ Not covered |
| `$unionWith` | Combine results from two collections | ❌ Not covered |
| `$setWindowFields` | Window functions (running totals, ranks) | ❌ Not covered |
| `$densify` | Fill gaps in time-series data | ❌ Not covered |

### Aggregation operators you've used vs not used:

**Used:** `$avg`, `$sum`, `$divide`

**Not used yet:**
| Operator | What It Does |
|----------|--------------|
| `$min` / `$max` | Min/max value in a group |
| `$first` / `$last` | First/last value in a group |
| `$push` / `$addToSet` | Collect values into an array |
| `$count` | Count items in a group |
| `$multiply` / `$subtract` / `$add` | Math operations |
| `$cond` / `$switch` | Conditional logic (if/else) |
| `$dateToString` / `$year` / `$month` | Date operations |
| `$concat` / `$toUpper` / `$toLower` | String operations |
| `$arrayElemAt` / `$filter` / `$size` | Array operations |

---

## ❌ What's Missing (Topics You Should Cover Next)

### 🔴 Phase 1: Essential Gaps (Learn These First)

These are core MongoDB concepts you need to cover next.

#### 1. Finish Aggregation Pipeline
> You've covered the basics but there are important stages left. **Focus on these first:**

**Must-learn stages (high priority):**

| Stage | Why It Matters | Suggested File |
|-------|---------------|----------------|
| `$lookup` | Joins between collections — used everywhere | `aggregation3_lookup.py` |
| `$addFields` | Add computed fields without removing existing ones | `aggregation4_addfields.py` |
| `$count` | Simple document counting in pipeline | (combine with others) |
| `$out` / `$merge` | Save pipeline results to a collection | `aggregation5_out_merge.py` |
| `$bucket` | Create histogram-style groupings | `aggregation6_bucket.py` |
| `$facet` | Run multiple pipelines at once | `aggregation7_facet.py` |

```python
# Example: $lookup — join accounts with their transfers
pipeline = [
    {
        "$lookup": {
            "from": "transfers",
            "localField": "account_id",
            "foreignField": "from_account",
            "as": "transfer_history"
        }
    }
]

# Example: $addFields — add a computed field
pipeline = [
    {"$addFields": {"balance_in_inr": {"$multiply": ["$balance", 83.5]}}}
]

# Example: $bucket — group balances into ranges
pipeline = [
    {
        "$bucket": {
            "groupBy": "$balance",
            "boundaries": [0, 1000, 5000, 10000, 50000],
            "default": "50000+",
            "output": {"count": {"$sum": 1}}
        }
    }
]

# Example: $facet — multiple pipelines at once
pipeline = [
    {
        "$facet": {
            "by_type": [{"$group": {"_id": "$account_type", "count": {"$sum": 1}}}],
            "high_balance": [{"$match": {"balance": {"$gt": 10000}}}],
            "total": [{"$count": "total_accounts"}]
        }
    }
]
```

**Nice-to-know stages (lower priority):**
- `$graphLookup` — recursive lookups (org charts, social graphs)
- `$replaceRoot` — promote a nested doc to the top level
- `$sample` — random document selection
- `$setWindowFields` — window functions (advanced analytics)

**Operators to practice:**
- Math: `$multiply`, `$subtract`, `$add`, `$mod`
- Conditional: `$cond`, `$switch`, `$ifNull`
- String: `$concat`, `$toUpper`, `$substr`
- Date: `$dateToString`, `$year`, `$month`, `$dayOfWeek`
- Array: `$filter`, `$size`, `$arrayElemAt`, `$in`

#### 2. Indexing
> Without indexes, MongoDB scans every document. This is the #1 performance topic.

```python
# Topics to cover:
# - createIndex() — single field, compound, unique
# - explain() — how to check if queries use indexes
# - TTL indexes — auto-delete documents after time
# - Text indexes — full-text search
```

**What to build:** Create `indexing.py` — create indexes on your `accounts` collection, then use `.explain()` to compare query performance with and without indexes.

#### 3. `$lookup` (Joins) — covered in aggregation above
> MongoDB's way of joining two collections — equivalent to SQL JOIN.

```python
# Join 'orders' collection with 'users' collection
pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user_info"
        }
    }
]
```

**What to build:** Create two collections (e.g., `accounts` and `transfers`), then use `$lookup` to join them.

#### 4. Schema Validation
> MongoDB is schemaless, but you can enforce rules on what documents look like.

```python
db.create_collection("users", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email", "age"],
        "properties": {
            "name": {"bsonType": "string"},
            "email": {"bsonType": "string"},
            "age": {"bsonType": "int", "minimum": 0}
        }
    }
})
```

**What to build:** Create `schema_validation.py` — set up a validated collection and try inserting valid and invalid documents.

#### 5. Data Modeling (Embedding vs Referencing)
> The most important design decision in MongoDB — when to nest documents vs link them.

```python
# EMBEDDED (denormalized) — good for 1:few, read-heavy
{
    "name": "Vardhan",
    "addresses": [
        {"city": "Hyderabad", "pin": "500001"},
        {"city": "Bangalore", "pin": "560001"}
    ]
}

# REFERENCED (normalized) — good for 1:many, write-heavy
# users collection
{"_id": "user1", "name": "Vardhan"}
# orders collection
{"_id": "order1", "user_id": "user1", "amount": 500}
```

**What to build:** Create `data_modeling.py` — implement both patterns and compare query complexity.

---

### 🟡 Phase 2: Intermediate (Build Real Things)

#### 5. Cursor Methods & Pagination
```python
# sort, skip, limit for pagination
page = 1
per_page = 10
results = collection.find().sort("name", 1).skip((page-1) * per_page).limit(per_page)
```

#### 6. Bulk Operations
```python
from pymongo import InsertOne, UpdateOne, DeleteOne

operations = [
    InsertOne({"name": "Alice"}),
    UpdateOne({"name": "Bob"}, {"$set": {"age": 30}}),
    DeleteOne({"name": "Charlie"})
]
result = collection.bulk_write(operations)
```

#### 7. Change Streams (Real-time)
> Watch a collection for live changes — like a database event listener.

```python
with collection.watch() as stream:
    for change in stream:
        print(change)  # fires on every insert/update/delete
```

#### 8. GridFS (File Storage)
> Store files larger than 16MB in MongoDB.

```python
import gridfs
fs = gridfs.GridFS(db)
file_id = fs.put(b"file content", filename="report.pdf")
```

#### 9. Geospatial Queries
```python
# Find locations near a point
collection.find({
    "location": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [78.4, 17.4]},
            "$maxDistance": 5000  # meters
        }
    }
})
```

---

### 🟢 Phase 3: Advanced (Production-Ready Skills)

#### 10. Full-Text Search / Atlas Search
> Powerful search engine built into Atlas — like Elasticsearch but integrated.

#### 11. Beanie ODM
> A modern async ODM for MongoDB (like Mongoose for Node.js, but for Python + FastAPI).

```python
from beanie import Document

class User(Document):
    name: str
    age: int

    class Settings:
        name = "users"
```

#### 12. Replica Sets & Sharding (Theory)
> Understand how MongoDB scales horizontally — important for system design interviews.

#### 13. Security & Auth
> Roles, field-level encryption, audit logs.

#### 14. Backup & Restore
```bash
# Export
mongodump --uri="mongodb+srv://..." --out=./backup

# Import
mongorestore --uri="mongodb+srv://..." ./backup
```

---

## 🗺️ Suggested Learning Order

```
YOU ARE HERE
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  Phase 1: Fill the Gaps (2-3 weeks)                 │
│                                                     │
│  1. Finish Aggregation             ← DO THIS FIRST  │
│     • $lookup, $addFields, $count                   │
│     • $out/$merge, $bucket, $facet                  │
│     • Operators: $cond, $multiply, dates, strings   │
│  2. Indexing + explain()                            │
│  3. Schema Validation                               │
│  4. Data Modeling patterns                          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Phase 2: Build Projects (2-3 weeks)                │
│                                                     │
│  5. Pagination & Cursors                            │
│  6. Bulk Operations                                 │
│  7. Change Streams                                  │
│  8. GridFS                                          │
│  9. Geospatial Queries                              │
│                                                     │
│  🔨 PROJECT: Build a full REST API with             │
│     FastAPI + MongoDB covering all of the above     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Phase 3: Go Pro (2-3 weeks)                        │
│                                                     │
│  10. Atlas Search                                   │
│  11. Beanie ODM                                     │
│  12. Replica Sets & Sharding (theory)               │
│  13. Security & Encryption                          │
│  14. Backup & Restore                               │
│                                                     │
│  🔨 PROJECT: Build a production-grade app with      │
│     Beanie + FastAPI + auth + search                │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Suggested Folder Structure Going Forward

```
MongoDB_university_course/
├── connection.py                    ✅
├── insert_single.py                 ✅
├── insert_multiple.py               ✅
├── find_single.py                   ✅
├── find_multiple.py                 ✅
├── update_single.py                 ✅
├── update_many.py                   ✅
├── delete_single.py                 ✅
├── delete_many.py                   ✅
├── transactions.py                  ✅
├── indexing.py                      ← NEW: create next
├── schema_validation.py             ← NEW
├── data_modeling.py                 ← NEW
├── pagination.py                    ← NEW
├── bulk_operations.py               ← NEW
├── change_streams.py                ← NEW
├── mongodb_aggregation_pipeline/    🟡 Partial
│   ├── aggregation3_lookup.py       ← NEW (priority)
│   ├── aggregation4_addfields.py    ← NEW
│   ├── aggregation5_out_merge.py    ← NEW
│   ├── aggregation6_bucket.py       ← NEW
│   └── aggregation7_facet.py        ← NEW
├── mongoDB_and_FastAPI/             ✅
└── mongodb_atlas_guide.md           ✅
```

---

## 📚 Resources

| Resource | Link | Best For |
|----------|------|----------|
| MongoDB University (Free) | [learn.mongodb.com](https://learn.mongodb.com) | Structured courses with certs |
| PyMongo Docs | [pymongo.readthedocs.io](https://pymongo.readthedocs.io) | API reference |
| MongoDB Manual | [mongodb.com/docs/manual](https://www.mongodb.com/docs/manual) | Deep dives |
| Beanie ODM Docs | [beanie-odm.dev](https://beanie-odm.dev) | Async ODM for FastAPI |
| MongoDB Design Patterns | [mongodb.com/blog/post/building-with-patterns-a-summary](https://www.mongodb.com/blog/post/building-with-patterns-a-summary) | Data modeling |
