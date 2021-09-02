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

    try:
        if ('authorization' in data):
            if (data['authorization'] == 'demo'):
                if ('id' in data):
                    with open('../_posts/' + data['id'] + '.json', 'w') as jsonFile:
                        json.dump(data, jsonFile)
                    print(data)
                    return data
                else:
                    return { "status": "403", "response": "Request cancelled - Missing Post ID" }, 403
            else:
                return { "status": "400", "response": "Request cancelled - Invalid API Key" }, 400
        else:
            return { "status": "403", "response": "Request cancelled - No API Key" }, 403
    except:
        return { "status": "500", "response": "Request cancelled - An error has occured. Please contact us at contact@constellate.pro"}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
