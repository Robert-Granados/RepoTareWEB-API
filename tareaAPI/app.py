from flask import Flask, request, jsonify
app = Flask(__name__)


items = []
next_id = 1

@app.route('/')
def hello():
    return 'API Funcionando!'

@app.route('/healthz')
def healthz():
    return 'OK', 200

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": items, "count": len(items)})

@app.route('/api/items', methods=['POST'])
def create_item():
    global next_id
    try:
        data = request.get_json()
        if data:
            data['id'] = next_id
            next_id += 1
            items.append(data)
            return jsonify({"message": "Item creado", "item": data}), 201
        return jsonify({"error": "Datos inválidos"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
