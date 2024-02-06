from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

def is_friday_rush(order_datetime):
    return order_datetime.weekday() == 4 and 15 <= order_datetime.hour < 19

def calculate_base_delivery_fee():
    return 2

def calculate_small_order_surcharge(cart_value):
    return max(0, 10 - cart_value / 100)

def calculate_distance_surcharge(delivery_distance):
    remaining_distance = max(0, delivery_distance - 1000)
    return max(0, (remaining_distance + 499) // 500)

def calculate_item_surcharge(number_of_items):
    item_surcharge = max(0, number_of_items - 4) * 0.5
    bulk_item_surcharge = max(0, number_of_items - 13) * 1.2
    return item_surcharge + bulk_item_surcharge

def cap_delivery_fee(delivery_fee):
    return min(delivery_fee, 15)

def apply_friday_rush_multiplier(delivery_fee):
    return min(delivery_fee * 1.2, 15)

def is_delivery_free(cart_value):
    return cart_value >= 20000

def convert_to_cents(delivery_fee):
    return round(delivery_fee * 100)

def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, order_time):
    order_datetime = datetime.fromisoformat(order_time)

    friday_rush = is_friday_rush(order_datetime)

    delivery_fee = calculate_base_delivery_fee()
    delivery_fee += calculate_small_order_surcharge(cart_value)
    delivery_fee += calculate_distance_surcharge(delivery_distance)
    delivery_fee += calculate_item_surcharge(number_of_items)
    delivery_fee = cap_delivery_fee(delivery_fee)

    if friday_rush:
        delivery_fee = apply_friday_rush_multiplier(delivery_fee)

    if is_delivery_free(cart_value):
        return 0

    return convert_to_cents(delivery_fee)

@app.route('/calculate_delivery_fee', methods=['POST'])
def calculate_delivery_fee_endpoint():
    try:
        data = request.get_json()
        cart_value = data['cart_value']
        delivery_distance = data['delivery_distance']
        number_of_items = data['number_of_items']
        order_time = data['time']

        delivery_fee = calculate_delivery_fee(cart_value, delivery_distance, number_of_items, order_time)

        response = {'delivery_fee': delivery_fee}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)