
import psycopg2
from flask import Flask, request, jsonify


with open('api-key.txt', 'r') as f:
    api_key = f.read()
    
conn = psycopg2.connect("")
cursor = conn.cursor()
    
    
# CREATE TABLE user_ip ( ip VARCHAR(15) NOT NULL, create_date TIMESTAMPTZ NOT NULL, fingerprint VARCHAR(255), country_code CHAR(2), region VARCHAR(255), city VARCHAR(255), isp VARCHAR(255), asn INTEGER, organization VARCHAR(255), fraud_score INTEGER, is_crawler BOOLEAN, mobile BOOLEAN, proxy BOOLEAN, vpn BOOLEAN, tor BOOLEAN, active_vpn BOOLEAN, active_tor BOOLEAN, recent_abuse BOOLEAN, bot_status BOOLEAN, PRIMARY KEY (ip, create_date) )


app = Flask(__name__)

@app.route('/get-user-ip', methods=['GET'])
def get_user_ip():
    headers = request.headers
    auth = headers.get('X-Api-Key')
    if auth != api_key:
        return 'Unauthorized', 401
    username = request.args.get('username')
    count = request.args.get('count', 'NULL')
    print(username, count)
    return 'Ok.', 200
    cursor.execute('SELECT * FROM user_ip WHERE username = %s ORDER BY last_used_date DESC LIMIT %s', (ip, count))
    result = cursor.fetchall()
    if len(result) == 0:
        return 'User not found in the database.', 404
    return jsonify(result), 200
    
@app.route('/get-ip-score', methods=['GET'])
def get_ip_score():
    headers = request.headers
    auth = headers.get('X-Api-Key')
    if auth != api_key:
        return 'Unauthorized', 401
    ip = request.args.get('ip')
    count = request.args.get('count', 'NULL')
    print(ip, count)
    cursor.execute('SELECT * FROM ip_score WHERE ip = %s ORDER BY create_date DESC LIMIT %s', (ip, count))
    result = cursor.fetchall()
    if len(result) == 0:
        return 'IP score not found in the database.', 404
    return jsonify(result), 200
    
@app.route('/set-user-ip', methods=['POST'])
def set_user_ip():
    headers = request.headers
    auth = headers.get('X-Api-Key')
    if auth != api_key:
        return 'Unauthorized', 401
    content = request.json
    print(content)
    return 'Ok.', 200
    cursor.execute('SELECT COUNT(*) FROM user_ip WHERE username = %s AND ip = %s', (username, ip))
    if (cursor.fetchone() is not None):
        print('INSERT')
    else:
        print('UPDATE')
    result = cursor.fetchone()
    if len(result) == 0:
        return 'An unknown error ocurred.', 500
    return jsonify(result), 200
        
@app.route('/set-ip-score', methods=['POST'])
def set_ip_score():
    headers = request.headers
    auth = headers.get('X-Api-Key')
    if auth != api_key:
        return 'Unauthorized', 401
    content = request.json
    content['create_date'] = content['timestamp']
    keys = ['ip', 'create_date', 'fingerprint', 'country_code', 'region', 'city', 'isp', 'asn', 'organization', 'fraud_score', 'is_crawler', 'mobile', 'proxy', 'vpn', 'tor', 'active_vpn', 'active_tor', 'recent_abuse', 'bot_status']
    values = [content.get(key, None) for key in keys]
    print(keys)
    print(values)
    cursor.execute('INSERT INTO ip_score VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', values)
    result = cursor.fetchone()
    print(result)
    if len(result) == 0:
        return 'An unknown error ocurred.', 500
    conn.commit()
    return jsonify(result), 200
        
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)
