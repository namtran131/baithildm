from pymongo import MongoClient

# ========================
# 1. CONNECT TO MONGODB
# ========================

client = MongoClient("mongodb://localhost:27017")   # hoặc URI Atlas
db = client["eShop"]
order_col = db["OrderCollection"]

# Xóa cũ cho sạch (không bắt buộc)
order_col.delete_many({})

# ========================
# 2. INSERT MANY DOCUMENTS
# ========================

orders = [
    {
        "orderid": 1,
        "products": [
            {"product_id": "quanau", "product_name": "quan au", "size": "XL", "price": 10, "quantity": 1},
            {"product_id": "somi",   "product_name": "ao so mi", "size": "XL", "price": 10.5, "quantity": 2}
        ],
        "total_amount": 31,
        "delivery_address": "Hanoi"
    },
    {
        "orderid": 2,
        "products": [
            {"product_id": "quanau", "product_name": "quan au", "size": "L", "price": 10, "quantity": 2}
        ],
        "total_amount": 20,
        "delivery_address": "HCM"
    }
]

order_col.insert_many(orders)
print("Inserted orders successfully!\n")

# ========================
# 3. EDIT DELIVERY ADDRESS
# ========================

order_col.update_one(
    {"orderid": 1},
    {"$set": {"delivery_address": "Hai Phong"}}
)
print("Updated delivery_address for orderid = 1\n")

# ========================
# 4. REMOVE AN ORDER
# ========================

order_col.delete_one({"orderid": 2})
print("Removed orderid = 2\n")

# ========================
# 5. READ ALL ORDERS AS TABLE
# ========================

orders = order_col.find()

print("No | Product name | Price | Quantity | Total")
no = 1
for order in orders:
    for p in order["products"]:
        total = p["price"] * p["quantity"]
        print(f"{no} | {p['product_name']} | {p['price']} | {p['quantity']} | {total}")
        no += 1
print()

# ========================
# 6. CALCULATE TOTAL AMOUNT
# ========================

pipeline = [
    {"$unwind": "$products"},
    {"$group": {"_id": None, "total": {"$sum": {"$multiply": ["$products.price", "$products.quantity"]}}}}
]

result = list(order_col.aggregate(pipeline))
print("Total amount of all orders:", result[0]["total"], "\n")

# ========================
# 7. COUNT PRODUCT_ID = 'somi'
# ========================

count = order_col.count_documents({"products.product_id": "somi"})
print("Total orders containing product_id = 'somi':", count)
