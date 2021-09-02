from flask import Flask, request, jsonify
import logging
import json

from flask.wrappers import Response

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/v1/post', methods=['POST']) 
def post():
    data = request.get_json()

    if ('authorization' in data):
        if (data['authorization'] == 'demo'):
            if ('id' in data):
                if (type(data['id']) == int):
                    if (len(data['title']) >= 1):
                        if (len(data['description']) >= 1):
                            with open('../_posts/' + str(data['id']) + '.json', 'w') as jsonFile:
                                json.dump(data, jsonFile)
                            print(data)
                            return { "status": 200, "content": "OK" }, 200
                        else:
                            return { "status": 403, "type": "invalid.description" }, 403
                    else:
                        return { "status": 403, "type": "invalid.title" }, 403
                else:
                    return { "status": 403, "type": "invalid.post.id" }, 403
            else:
                return { "status": 403, "type": "missing.post.id" }, 403
        else:
            return { "status": 400, "type": "invalid.api.key" }, 400
    else:
        return { "status": 403, "type": "missing.api.key" }, 403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
