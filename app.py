from pymongo import MongoClient
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["eShop"]
order_collection = db["OrderCollection"]

print("=== HỆ THỐNG QUẢN LÍ ĐƠN HÀNG ===")

def show_orders():
    orders = list(order_collection.find())
    if not orders:
        print("CHƯA CÓ ĐƠN HÀNG NÀO !")
        return

    print("{:<3} {:<15} {:<10} {:<8}".format("STT", "Tên Sản Phẩm____", "Giá____","Số Lượng"))
    for i, order in enumerate(orders, start=1):
        for product in order["products"]:
            print("{:<3} {:<15} {:<10} {:<8}".format(
                i, product["product_name"], product["price"], product["quantity"]
            ))

def total_amount():
    orders = list(order_collection.find())
    total = sum(order["total_amount"] for order in orders)
    print("Tổng Tiền Tất Cả Đơn Hàng:", total)

def count_product(product_id):
    orders = list(order_collection.find())
    total_count = 0
    for order in orders:
        for product in order["products"]:
            if product["product_id"] == product_id:
                total_count += product["quantity"]
    print(f"Tổng số lượng sản phẩm '{product_id}':", total_count)

while True:
    print("\nCHỌN CHỨC NĂNG TRONG CÁC CHỨC NĂNG SAU:")
    print("1 - Thêm đơn hàng")
    print("2 - Sửa địa chỉ giao hàng")
    print("3 - Xóa đơn hàng")
    print("4 - Hiển thị tất cả đơn hàng")
    print("5 - Tính tổng tiền")
    print("6 - Đếm số lượng sản phẩm theo product_id")
    print("0 - Thoát")

    choice = input("Nhập lựa chọn: ")

    if choice == "1":
        orderid = int(input("Nhập orderid: "))
        num_products = int(input("Số Sản Phẩm Trong Đơn : "))
        products = []
        total = 0
        for _ in range(num_products):
            pid = input("Nhập product_id: ")
            pname = input("Nhập tên sản phẩm: ")
            size = input("Nhập size: ")
            price = float(input("Nhập giá: "))
            quantity = int(input("Nhập số lượng: "))
            total += price * quantity
            products.append({
                "product_id": pid,
                "product_name": pname,
                "size": size,
                "price": price,
                "quantity": quantity
            })
        address = input("Nhập địa chỉ giao hàng: ")
        order_collection.insert_one({
            "orderid": orderid,
            "products": products,
            "total_amount": total,
            "delivery_address": address
        })
        print("Đã thêm đơn hàng!")

    elif choice == "2":
        orderid = int(input("Nhập orderid cần sửa: "))
        new_address = input("Nhập địa chỉ mới: ")
        order_collection.update_one(
            {"orderid": orderid},
            {"$set": {"delivery_address": new_address}}
        )
        print(f"Đã cập nhật địa chỉ giao hàng cho đơn {orderid}")

    elif choice == "3":
        orderid = int(input("Nhập orderid cần xóa: "))
        order_collection.delete_one({"orderid": orderid})
        print(f"Đã xóa đơn hàng {orderid}")

    elif choice == "4":
        show_orders()

    elif choice == "5":
        total_amount()

    elif choice == "6":
        pid = input("Nhập product_id cần đếm: ")
        count_product(pid)

    elif choice == "0":
        print("Thoát chương trình.")
        break

    else:
        print("Lựa chọn không hợp lệ!")