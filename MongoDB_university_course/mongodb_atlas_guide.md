# MongoDB Atlas — Complete Setup & Reference Guide

A step-by-step reference for creating clusters, managing users, connecting, and common operations using both the **Atlas UI** and **mongosh** (MongoDB Shell).

---

## Table of Contents

1. [Creating a MongoDB Atlas Account](#1-creating-a-mongodb-atlas-account)
2. [Creating a Cluster](#2-creating-a-cluster)
3. [Creating Database Users](#3-creating-database-users)
4. [Configuring Network Access (IP Whitelist)](#4-configuring-network-access-ip-whitelist)
5. [Getting Your Connection String](#5-getting-your-connection-string)
6. [Connecting via mongosh](#6-connecting-via-mongosh)
7. [Connecting via Python (PyMongo)](#7-connecting-via-python-pymongo)
8. [Common mongosh Commands](#8-common-mongosh-commands)
9. [Managing Users via mongosh](#9-managing-users-via-mongosh)
10. [Managing Clusters via Atlas CLI](#10-managing-clusters-via-atlas-cli)
11. [Quick Reference Cheatsheet](#11-quick-reference-cheatsheet)

---

## 1. Creating a MongoDB Atlas Account

1. Go to [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Click **"Try Free"**
3. Sign up with email or Google/GitHub account
4. Verify your email address
5. You'll land on the Atlas dashboard — ready to create your first cluster

---

## 2. Creating a Cluster

### Via Atlas UI

1. In the Atlas dashboard, click **"Build a Database"** (or **"Create"** if you already have clusters)
2. Choose your tier:

   | Tier | Cost | Best For |
   |------|------|----------|
   | **M0 (Free/Shared)** | Free forever | Learning, small projects |
   | **M2/M5 (Shared)** | ~$9-$25/mo | Small production apps |
   | **M10+ (Dedicated)** | $57+/mo | Production workloads |

3. Select your **cloud provider** (AWS / Google Cloud / Azure)
4. Select your **region** (pick the closest to you for low latency)
   - For India: `ap-south-1` (Mumbai) on AWS
5. Name your cluster (e.g., `MyFirstCluster`)
6. Click **"Create Deployment"**
7. Wait 1-3 minutes for provisioning

### Via Atlas CLI (Command Line)

```bash
# Install Atlas CLI
# Windows (winget):
winget install -e --id MongoDB.MongoDBAtlasCLI

# macOS (Homebrew):
brew install mongodb-atlas-cli

# Login to Atlas
atlas auth login

# Create a free-tier cluster
atlas clusters create MyFirstCluster \
  --provider AWS \
  --region AP_SOUTH_1 \
  --tier M0

# Check cluster status
atlas clusters describe MyFirstCluster

# List all clusters
atlas clusters list
```

---

## 3. Creating Database Users

Database users are **separate from your Atlas account**. You need at least one to connect to your cluster.

### Via Atlas UI

1. Go to **"Database Access"** in the left sidebar
2. Click **"Add New Database User"**
3. Choose authentication method:
   - **Password** (most common)
   - **Certificate**
   - **AWS IAM**
4. Enter a **username** and **password**
   - ⚠️ Avoid special characters (`@`, `:`, `/`) in passwords — they cause issues in connection strings
   - Use the **"Autogenerate Secure Password"** button and save it somewhere safe
5. Set **Database User Privileges**:

   | Role | Access Level |
   |------|-------------|
   | `atlasAdmin` | Full admin access to everything |
   | `readWriteAnyDatabase` | Read/write to all databases |
   | `readAnyDatabase` | Read-only access to all databases |
   | `dbAdmin` | Admin for specific databases |
   | Custom role | Fine-grained access to specific collections |

6. Click **"Add User"**

### Via Atlas CLI

```bash
# Create a user with readWrite access to all databases
atlas dbusers create atlasAdmin \
  --username myUser \
  --password "MySecurePassword123"

# Create a read-only user
atlas dbusers create readAnyDatabase \
  --username readonlyUser \
  --password "ReadOnly456"

# List all database users
atlas dbusers list

# Delete a user
atlas dbusers delete myUser
```

### Via mongosh (once connected as admin)

```javascript
// Switch to the admin database
use admin

// Create a new user with readWrite access
db.createUser({
  user: "myAppUser",
  pwd: "SecurePassword789",    // or use passwordPrompt() for interactive input
  roles: [
    { role: "readWrite", db: "myDatabase" }
  ]
})

// Create an admin user
db.createUser({
  user: "adminUser",
  pwd: passwordPrompt(),       // prompts for password securely (recommended)
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})

// View all users
db.getUsers()

// Update a user's password
db.changeUserPassword("myAppUser", "NewPassword123")

// Update a user's roles
db.updateUser("myAppUser", {
  roles: [
    { role: "readWrite", db: "myDatabase" },
    { role: "read", db: "anotherDatabase" }
  ]
})

// Remove a user
db.dropUser("myAppUser")
```

---

## 4. Configuring Network Access (IP Whitelist)

Your cluster blocks all connections by default. You must whitelist IPs.

### Via Atlas UI

1. Go to **"Network Access"** in the left sidebar
2. Click **"Add IP Address"**
3. Options:
   - **"Add Current IP Address"** — adds your current machine's IP
   - **"Allow Access from Anywhere"** — adds `0.0.0.0/0` (⚠️ not recommended for production)
   - **Enter a specific IP** — e.g., `203.0.113.50/32`
4. Optionally add a comment (e.g., "Vardhan's laptop")
5. Click **"Confirm"**

### Via Atlas CLI

```bash
# Add your current IP
atlas accessLists create --currentIp

# Add a specific IP
atlas accessLists create "203.0.113.50/32" --comment "Office network"

# Allow access from anywhere (use with caution)
atlas accessLists create "0.0.0.0/0" --comment "Allow all"

# List all whitelisted IPs
atlas accessLists list

# Remove an IP
atlas accessLists delete "203.0.113.50/32"
```

---

## 5. Getting Your Connection String

### Via Atlas UI

1. Go to **"Database"** in the left sidebar
2. Click **"Connect"** on your cluster
3. Choose your connection method:

#### Option A: mongosh (Shell)
```
mongosh "mongodb+srv://<cluster-name>.xxxxx.mongodb.net/" --apiVersion 1 --username <username>
```

#### Option B: Application (Driver)
```
mongodb+srv://<username>:<password>@<cluster-name>.xxxxx.mongodb.net/?retryWrites=true&w=majority&appName=MyFirstCluster
```

#### Option C: MongoDB Compass (GUI)
Same connection string as Option B, paste it into Compass.

### Connection String Anatomy

```
mongodb+srv://vardhan:Xpassword123@mycluster.abc123.mongodb.net/myDatabase?retryWrites=true&w=majority
│              │       │             │                              │         │
│              │       │             │                              │         └── Query parameters
│              │       │             │                              └── Default database (optional)
│              │       │             └── Cluster hostname
│              │       └── Password
│              └── Username
└── Protocol (srv = DNS seedlist, handles replica set discovery automatically)
```

---

## 6. Connecting via mongosh

### Install mongosh

```bash
# Windows (winget)
winget install -e --id MongoDB.MongoDBShell

# macOS (Homebrew)
brew install mongosh

# Verify installation
mongosh --version
```

### Connect to Atlas

```bash
# Method 1: Connection string inline
mongosh "mongodb+srv://mycluster.abc123.mongodb.net/myDatabase" --username vardhan

# Method 2: Full connection string with password
mongosh "mongodb+srv://vardhan:MyPassword@mycluster.abc123.mongodb.net/"

# Method 3: Connect to local MongoDB
mongosh "mongodb://localhost:27017"
# or simply:
mongosh
```

### Verify Connection

```javascript
// Once connected, you'll see a prompt like:
// Atlas atlas-xxxxx-shard-0 [primary] myDatabase>

// Test the connection
db.runCommand({ ping: 1 })
// Output: { ok: 1 }

// Show current database
db
// Output: myDatabase

// Show server status
db.serverStatus().version

// Show connection info
db.getMongo()
```

---

## 7. Connecting via Python (PyMongo)

### Basic Connection

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect
client = MongoClient(MONGODB_URI)

# Verify connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection failed: {e}")

# List databases
for db_name in client.list_database_names():
    print(db_name)

client.close()
```

### .env File Format

```env
MONGODB_URI=mongodb+srv://vardhan:MyPassword@mycluster.abc123.mongodb.net/?retryWrites=true&w=majority&appName=MyFirstCluster
```

### Async Connection (Motor + FastAPI)

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database("myDatabase")
collection = db.get_collection("myCollection")
```

---

## 8. Common mongosh Commands

### Database Operations

```javascript
// Show all databases
show dbs

// Switch to / create a database
use myDatabase

// Drop (delete) current database
db.dropDatabase()

// Show current database stats
db.stats()
```

### Collection Operations

```javascript
// Show all collections in current database
show collections

// Create a collection explicitly
db.createCollection("users")

// Drop a collection
db.users.drop()

// Get collection stats
db.users.stats()

// Count documents
db.users.countDocuments({})
db.users.estimatedDocumentCount()  // faster, approximate
```

### CRUD Operations

```javascript
// --- INSERT ---
// Insert one document
db.users.insertOne({
  name: "Vardhan",
  age: 22,
  email: "vardhan@example.com"
})

// Insert multiple documents
db.users.insertMany([
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 }
])

// --- FIND (READ) ---
// Find all documents
db.users.find()

// Find with filter
db.users.find({ age: { $gt: 20 } })

// Find one document
db.users.findOne({ name: "Vardhan" })

// Find with projection (select specific fields)
db.users.find({}, { name: 1, age: 1, _id: 0 })

// Find with sort, limit, skip
db.users.find().sort({ age: -1 }).limit(5).skip(0)

// --- UPDATE ---
// Update one document
db.users.updateOne(
  { name: "Vardhan" },
  { $set: { age: 23 } }
)

// Update many documents
db.users.updateMany(
  { age: { $lt: 25 } },
  { $set: { status: "young" } }
)

// Replace entire document
db.users.replaceOne(
  { name: "Vardhan" },
  { name: "Vardhan", age: 23, email: "new@example.com" }
)

// --- DELETE ---
// Delete one document
db.users.deleteOne({ name: "Alice" })

// Delete many documents
db.users.deleteMany({ age: { $lt: 18 } })

// Delete all documents in a collection
db.users.deleteMany({})
```

### Indexing

```javascript
// Create a single-field index
db.users.createIndex({ email: 1 })         // ascending
db.users.createIndex({ age: -1 })          // descending

// Create a unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Create a compound index
db.users.createIndex({ name: 1, age: -1 })

// Create a text index (for text search)
db.users.createIndex({ name: "text", bio: "text" })

// List all indexes
db.users.getIndexes()

// Drop an index
db.users.dropIndex("email_1")

// Drop all indexes (except _id)
db.users.dropIndexes()
```

### Aggregation

```javascript
// Simple aggregation pipeline
db.users.aggregate([
  { $match: { age: { $gt: 20 } } },
  { $group: { _id: "$status", count: { $sum: 1 }, avgAge: { $avg: "$age" } } },
  { $sort: { avgAge: -1 } }
])

// $lookup (join between collections)
db.orders.aggregate([
  {
    $lookup: {
      from: "users",            // the other collection
      localField: "userId",     // field in orders
      foreignField: "_id",      // field in users
      as: "userDetails"         // output array field
    }
  }
])
```

---

## 9. Managing Users via mongosh

```javascript
// Must be connected as an admin user and switched to admin db
use admin

// --- VIEW USERS ---
db.getUsers()                                       // all users
db.getUser("vardhan")                               // specific user

// --- CREATE USERS ---
// Read/write user for a specific database
db.createUser({
  user: "appUser",
  pwd: passwordPrompt(),
  roles: [{ role: "readWrite", db: "myApp" }]
})

// Admin user
db.createUser({
  user: "superAdmin",
  pwd: passwordPrompt(),
  roles: ["root"]
})

// --- UPDATE USERS ---
// Change password
db.changeUserPassword("appUser", passwordPrompt())

// Add/change roles
db.grantRolesToUser("appUser", [
  { role: "read", db: "analytics" }
])

// Remove roles
db.revokeRolesFromUser("appUser", [
  { role: "read", db: "analytics" }
])

// --- DELETE USERS ---
db.dropUser("appUser")
```

### Common Built-in Roles Reference

| Role | Scope | Description |
|------|-------|-------------|
| `read` | Database | Read-only access |
| `readWrite` | Database | Read + write access |
| `dbAdmin` | Database | Admin tasks (indexes, stats, etc.) |
| `userAdmin` | Database | Create/modify users for that database |
| `readAnyDatabase` | Cluster | Read all databases |
| `readWriteAnyDatabase` | Cluster | Read/write all databases |
| `userAdminAnyDatabase` | Cluster | Manage users across all databases |
| `dbAdminAnyDatabase` | Cluster | Admin all databases |
| `clusterAdmin` | Cluster | Manage cluster configuration |
| `root` | Cluster | Superuser — full access to everything |

---

## 10. Managing Clusters via Atlas CLI

```bash
# --- CLUSTER LIFECYCLE ---
# Create a cluster
atlas clusters create MyCluster --provider AWS --region AP_SOUTH_1 --tier M0

# List all clusters
atlas clusters list

# Describe a cluster (get details)
atlas clusters describe MyCluster

# Pause a cluster (M10+ only, saves money)
atlas clusters pause MyCluster

# Resume a paused cluster
atlas clusters start MyCluster

# Delete a cluster (⚠️ irreversible)
atlas clusters delete MyCluster

# --- CONFIGURATION ---
# Upgrade cluster tier
atlas clusters update MyCluster --tier M10

# Change disk size
atlas clusters update MyCluster --diskSizeGB 20

# --- BACKUPS ---
# List snapshots
atlas backups snapshots list MyCluster

# Create an on-demand snapshot
atlas backups snapshots create MyCluster --desc "Before migration"

# Restore from snapshot
atlas backups restores start automated \
  --clusterName MyCluster \
  --snapshotId <snapshot-id> \
  --targetClusterName MyCluster
```

---

## 11. Quick Reference Cheatsheet

### Connection Strings

```bash
# Atlas (SRV — recommended)
mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<database>

# Local MongoDB
mongodb://localhost:27017/<database>

# With auth on local
mongodb://<user>:<password>@localhost:27017/<database>?authSource=admin

# Replica set (non-SRV)
mongodb://<user>:<pwd>@host1:27017,host2:27017,host3:27017/<db>?replicaSet=myRS
```

### mongosh One-Liners

```bash
# Quick connect + run a command
mongosh "mongodb+srv://cluster.abc.mongodb.net/" --username admin --eval "db.stats()"

# Export a collection to JSON
mongosh --eval "JSON.stringify(db.users.find().toArray())" > users.json

# Run a script file
mongosh "mongodb+srv://cluster.abc.mongodb.net/" --username admin script.js
```

### Useful Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equal | `{ age: { $eq: 25 } }` |
| `$ne` | Not equal | `{ status: { $ne: "inactive" } }` |
| `$gt` / `$gte` | Greater than / ≥ | `{ balance: { $gt: 1000 } }` |
| `$lt` / `$lte` | Less than / ≤ | `{ age: { $lt: 30 } }` |
| `$in` | In array | `{ status: { $in: ["A", "B"] } }` |
| `$nin` | Not in array | `{ status: { $nin: ["X"] } }` |
| `$exists` | Field exists | `{ email: { $exists: true } }` |
| `$regex` | Regex match | `{ name: { $regex: /^V/i } }` |
| `$and` | Logical AND | `{ $and: [ {a: 1}, {b: 2} ] }` |
| `$or` | Logical OR | `{ $or: [ {a: 1}, {b: 2} ] }` |

### Update Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$set` | Set field value | `{ $set: { age: 25 } }` |
| `$unset` | Remove a field | `{ $unset: { temp: "" } }` |
| `$inc` | Increment by value | `{ $inc: { balance: 100 } }` |
| `$push` | Add to array | `{ $push: { tags: "new" } }` |
| `$pull` | Remove from array | `{ $pull: { tags: "old" } }` |
| `$addToSet` | Add unique to array | `{ $addToSet: { tags: "vip" } }` |
| `$rename` | Rename a field | `{ $rename: { old: "new" } }` |
| `$min` / `$max` | Update if less/greater | `{ $min: { low: 5 } }` |

---

> **Tip:** Bookmark this file and come back whenever you need a quick refresher. For official docs, visit [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/).
