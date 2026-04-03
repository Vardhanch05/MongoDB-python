# MongoDB Aggregation Pipeline — Complete Learning Guide

## What is an Aggregation Pipeline?

Think of it like an **assembly line in a factory**:
- Documents enter from one end
- Each **stage** transforms them in some way
- The final result comes out the other end

```
Documents → [Stage 1] → [Stage 2] → [Stage 3] → Results
              $match      $group       $sort
```

**Key rule:** Each stage takes input from the previous stage, NOT from the original collection.

---

## Stages You Already Know (Quick Recap)

| Stage | One-line Summary | You learned it in |
|-------|-----------------|-------------------|
| `$match` | Filter docs (like `WHERE` in SQL) | `aggregation1_match_n_group.py` |
| `$group` | Group + calculate (`SUM`, `AVG`) | `aggregation1_match_n_group.py` |
| `$sort` | Order results (1 = asc, -1 = desc) | `aggregation2_sort_n_project.py` |
| `$project` | Pick/rename/compute fields | `aggregation2_sort_n_project.py` |
| `$unwind` | Flatten arrays into separate docs | `pipeline_eg.py` |
| `$skip` | Skip N documents | `pipeline_eg.py` |
| `$limit` | Take only N documents | `pipeline_eg.py` |

---

## New Stages to Learn (in order)

### 1. `$addFields` / `$set` (add computed fields)

**What:** Adds new fields to documents WITHOUT removing existing ones.
**vs $project:** `$project` only keeps fields you mention. `$addFields` keeps everything + adds new ones.

```python
# $project — you LOSE fields you don't mention
{"$project": {"balance_inr": {"$multiply": ["$balance", 83.5]}}}
# Output: {balance_inr: 417500}  ← balance, name, etc. are GONE

# $addFields — keeps EVERYTHING + adds new field
{"$addFields": {"balance_inr": {"$multiply": ["$balance", 83.5]}}}
# Output: {name: "Vardhan", balance: 5000, balance_inr: 417500}  ← all fields preserved
```

`$set` is just an alias for `$addFields` — they do the exact same thing.

---

### 2. `$count` (count documents)

**What:** Counts documents at that point in the pipeline. Outputs a single document.

```python
pipeline = [
    {"$match": {"balance": {"$gt": 5000}}},
    {"$count": "high_balance_accounts"}
]
# Output: {"high_balance_accounts": 42}
```

---

### 3. `$lookup` (join collections)

**What:** Joins data from another collection — like SQL `JOIN`.

```
Collection A (orders)          Collection B (users)
┌──────────────────────┐      ┌──────────────────────┐
│ order_id: "ORD1"     │      │ _id: "U1"            │
│ user_id: "U1"    ────┼──────│ name: "Vardhan"      │
│ amount: 500          │      │ email: "v@email.com" │
└──────────────────────┘      └──────────────────────┘
```

```python
pipeline = [
    {
        "$lookup": {
            "from": "users",           # the OTHER collection to join
            "localField": "user_id",   # field in THIS collection
            "foreignField": "_id",     # field in the OTHER collection
            "as": "user_details"       # name for the joined data (comes as an array)
        }
    }
]
# Output: {order_id: "ORD1", user_id: "U1", amount: 500,
#          user_details: [{_id: "U1", name: "Vardhan", email: "v@email.com"}]}
```

**Important:** `$lookup` always returns an **array** in the `as` field, even if there's only one match. Use `$unwind` after to flatten it.

---

### 4. `$bucket` (group into ranges)

**What:** Groups documents into ranges/bins — perfect for histograms.

```python
pipeline = [
    {
        "$bucket": {
            "groupBy": "$balance",                           # field to bucket by
            "boundaries": [0, 1000, 5000, 10000, 50000],     # range edges
            "default": "Other",                               # bucket for out-of-range values
            "output": {                                       # what to compute per bucket
                "count": {"$sum": 1},
                "accounts": {"$push": "$account_holder"}
            }
        }
    }
]
# Output:
# {_id: 0,     count: 3, accounts: ["Alice", "Bob", "Charlie"]}     ← balance 0-999
# {_id: 1000,  count: 5, accounts: [...]}                           ← balance 1000-4999
# {_id: 5000,  count: 2, accounts: [...]}                           ← balance 5000-9999
# {_id: 10000, count: 1, accounts: [...]}                           ← balance 10000-49999
```

There's also `$bucketAuto` which automatically creates equal-sized buckets:
```python
{"$bucketAuto": {"groupBy": "$balance", "buckets": 4}}
```

---

### 5. `$facet` (multiple pipelines at once)

**What:** Runs multiple aggregation pipelines **in parallel** on the same data. Returns all results in one document.

```python
pipeline = [
    {
        "$facet": {
            # Pipeline 1: count by account type
            "by_type": [
                {"$group": {"_id": "$account_type", "count": {"$sum": 1}}}
            ],
            # Pipeline 2: get top 3 highest balances
            "top_3": [
                {"$sort": {"balance": -1}},
                {"$limit": 3}
            ],
            # Pipeline 3: get total count
            "total": [
                {"$count": "total_accounts"}
            ]
        }
    }
]
# Output (single document):
# {
#   by_type: [{_id: "Checking", count: 5}, {_id: "Savings", count: 3}],
#   top_3: [{name: "Eve", balance: 65000}, ...],
#   total: [{total_accounts: 8}]
# }
```

**Use case:** Dashboards where you need multiple stats from the same data in one query.

---

### 6. `$out` and `$merge` (save results)

**`$out`** — Writes the pipeline output to a NEW collection (replaces it if it exists).
```python
pipeline = [
    {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
    {"$out": "department_stats"}    # ← MUST be the LAST stage
]
# Creates/replaces the "department_stats" collection with the results
```

**`$merge`** — Smarter version of `$out`. Can merge into an existing collection instead of replacing.
```python
pipeline = [
    {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
    {
        "$merge": {
            "into": "department_stats",
            "whenMatched": "replace",      # what to do if doc already exists
            "whenNotMatched": "insert"     # what to do if doc is new
        }
    }
]
```

---

### 7. `$replaceRoot` (promote a sub-document)

**What:** Replaces the entire document with one of its sub-documents.

```python
# Before: {name: "Vardhan", address: {city: "Hyderabad", pin: "500001"}}
pipeline = [
    {"$replaceRoot": {"newRoot": "$address"}}
]
# After: {city: "Hyderabad", pin: "500001"}
```

---

### 8. `$sample` (random documents)

**What:** Randomly selects N documents. Great for testing or getting random samples.

```python
pipeline = [
    {"$sample": {"size": 5}}    # get 5 random documents
]
```

---

### 9. `$unionWith` (combine collections)

**What:** Like SQL `UNION` — combines documents from two collections.

```python
# Get all transactions from both "deposits" and "withdrawals" collections
pipeline = [
    {"$unionWith": "withdrawals"},
    {"$sort": {"date": -1}}
]
# Runs on "deposits" collection and combines with "withdrawals"
```

---

## Operators You Need to Learn

### Math Operators (use inside `$project` or `$addFields`)

```python
{"$add": ["$price", "$tax"]}                  # price + tax
{"$subtract": ["$price", "$discount"]}        # price - discount
{"$multiply": ["$price", "$quantity"]}         # price × quantity
{"$divide": ["$total", "$count"]}             # total ÷ count  (you know this one!)
{"$mod": ["$number", 2]}                      # number % 2 (remainder)
{"$abs": "$profit"}                           # absolute value
{"$round": ["$average", 2]}                   # round to 2 decimal places
```

### Conditional Operators

```python
# $cond — if/else
{"$cond": {
    "if": {"$gte": ["$balance", 10000]},
    "then": "Premium",
    "else": "Standard"
}}

# Short form:
{"$cond": [{"$gte": ["$balance", 10000]}, "Premium", "Standard"]}

# $switch — multiple conditions (like if/elif/else)
{"$switch": {
    "branches": [
        {"case": {"$gte": ["$score", 90]}, "then": "A"},
        {"case": {"$gte": ["$score", 80]}, "then": "B"},
        {"case": {"$gte": ["$score", 70]}, "then": "C"}
    ],
    "default": "F"
}}

# $ifNull — provide a default if field is null/missing
{"$ifNull": ["$nickname", "No nickname"]}
```

### String Operators

```python
{"$concat": ["$first_name", " ", "$last_name"]}    # "Vardhan" + " " + "C"
{"$toUpper": "$name"}                                # "VARDHAN"
{"$toLower": "$name"}                                # "vardhan"
{"$substr": ["$name", 0, 3]}                        # "Var" (start at 0, take 3 chars)
{"$strLenCP": "$name"}                               # 7 (length)
{"$trim": {"input": "$name"}}                        # remove whitespace
```

### Date Operators

```python
{"$year": "$created_at"}                             # 2026
{"$month": "$created_at"}                            # 4
{"$dayOfMonth": "$created_at"}                       # 3
{"$dayOfWeek": "$created_at"}                        # 5 (1=Sun, 7=Sat)
{"$hour": "$created_at"}                             # 14

# Format a date as string
{"$dateToString": {
    "format": "%Y-%m-%d",
    "date": "$created_at"
}}
# Output: "2026-04-03"
```

### Array Operators

```python
{"$size": "$skills"}                          # number of elements
{"$arrayElemAt": ["$skills", 0]}              # first element
{"$arrayElemAt": ["$skills", -1]}             # last element
{"$in": ["Python", "$skills"]}                # true if "Python" is in skills array

# $filter — keep only matching array elements
{"$filter": {
    "input": "$scores",
    "as": "score",
    "cond": {"$gte": ["$$score", 80]}         # keep scores >= 80
}}

# $map — transform each array element
{"$map": {
    "input": "$prices",
    "as": "price",
    "in": {"$multiply": ["$$price", 1.1]}     # add 10% to each price
}}
```

### Group Accumulator Operators (use inside `$group`)

```python
{"$group": {
    "_id": "$department",
    "total": {"$sum": "$salary"},             # you know this ✅
    "average": {"$avg": "$salary"},           # you know this ✅
    "highest": {"$max": "$salary"},           # NEW: maximum
    "lowest": {"$min": "$salary"},            # NEW: minimum
    "first_hire": {"$first": "$hire_date"},   # NEW: first value
    "last_hire": {"$last": "$hire_date"},     # NEW: last value
    "count": {"$sum": 1},                     # you know this ✅
    "all_names": {"$push": "$name"},          # NEW: collect into array
    "unique_skills": {"$addToSet": "$skill"}, # NEW: collect unique values
}}
```

---

## Pipeline Best Practices

1. **Put `$match` early** — filter first, process less data
2. **`$match` before `$group`** — reduces docs before grouping
3. **Limit fields with `$project`** — less data = faster
4. **Use `$match` after `$lookup`** — filter joined data early
5. **Use indexes** — `$match` and `$sort` at the start can use indexes

```python
# ✅ GOOD — filter first, less work for $group
[
    {"$match": {"status": "active"}},
    {"$group": {"_id": "$dept", "count": {"$sum": 1}}}
]

# ❌ BAD — groups ALL docs, then filters (wasted work)
[
    {"$group": {"_id": "$dept", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 5}}}
]
```

---

## Mental Model: When to Use What

| I want to... | Use stage |
|--------------|-----------|
| Filter documents | `$match` |
| Calculate totals/averages | `$group` |
| Sort results | `$sort` |
| Pick specific fields | `$project` |
| Add new fields (keep existing) | `$addFields` |
| Flatten an array | `$unwind` |
| Join another collection | `$lookup` |
| Count documents | `$count` |
| Group into ranges | `$bucket` |
| Run multiple pipelines | `$facet` |
| Save results to collection | `$out` / `$merge` |
| Get random docs | `$sample` |
| Combine collections | `$unionWith` |
| Paginate | `$skip` + `$limit` |
