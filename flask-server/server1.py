from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def handle_request():
    # 리액트에서 보낸 데이터 받기
    print(request)
    data = request.get_json()
    print(data)
    
    # 데이터 처리 (예시: 데이터를 그대로 반환)
    processed_data = {"message1": f"Received: {data['message']}"}
    print(processed_data)

    processed_data = {
        "FK_result" : data["message"],
        "FK_choice" : "O",
        "FK_name" : "제품이름입니다",
        "FK_open" : "2025-03-01",
        "FK_country" : "China",
        "FK_fake" : 45,
        "FK_sname" : "Shop3493847384"
        }
    
    # 리액트에 결과 반환
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)