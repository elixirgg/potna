from flask import Flask, render_template, request, jsonify, url_for
import uuid

app = Flask(__name__)

pastes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create', methods=['POST'])
def create_paste():
    data = request.get_json()

    if 'text' in data:
        paste_id = str(uuid.uuid4())
        pastes[paste_id] = data['text']
        paste_url = url_for('read_paste', paste_id=paste_id, _external=True)
        return jsonify({'paste_url': paste_url}), 201
    else:
        return jsonify({'error': 'Text is required'}), 400

@app.route('/api/read/<paste_id>', methods=['GET'])
def read_paste(paste_id):
    paste_content = pastes.get(paste_id)

    if paste_content:
        return render_template('paste.html', paste_content=paste_content)
    else:
        return jsonify({'error': 'Paste not found'}), 404

@app.route('/api/read_raw/<paste_id>', methods=['GET'])
def read_raw_paste(paste_id):
    paste_content = pastes.get(paste_id)

    if paste_content:
        return paste_content
    else:
        return jsonify({'error': 'Paste not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
