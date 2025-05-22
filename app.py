from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

SKU_FILE = "sku_data.json"

def load_skus():
    with open(SKU_FILE, "r") as f:
        return json.load(f)

def save_skus(skus):
    with open(SKU_FILE, "w") as f:
        json.dump(skus, f)

@app.route("/assign", methods=["POST"])
def assign_sku():
    skus = load_skus()

    # 筛选出库存大于 0 的 SKU
    available_skus = [sku for sku in skus if len(sku["items"]) > 0]
    if not available_skus:
        return jsonify({"error": "No SKU with stock available"}), 400

    # 随机选择一个 SKU
    selected_sku = random.choice(available_skus)

    # 取该 SKU 下编号最小的一件
    selected_item = selected_sku["items"].pop(0)

    # 保存更新后的数据（减少库存）
    save_skus(skus)

    return jsonify({
        "assigned_sku": selected_item["id"],
        "image": selected_item["image"]
    })

@app.route("/", methods=["GET"])
def health_check():
    return "Blindbox service is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
