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
    agent = request.headers.get('User-Agent')

    try:
        if ('authorization' in data):
            if (data['authorization'] == 'demo'):
                if ('id' in data):
                    if (type(data['id']) == int):
                        if (len(data['title']) >= 1):
                            if (len(data['description']) >= 1):
                                if (len(data['start-date']) >= 1):
                                    if (len(data['end-date']) >= 1):
                                        write(data, getagent(agent))
                                        return { "status": 200, "content": "OK" }, 200
                                    else:
                                        return { "status": 403, "type": "invalid.end.date" }, 403
                                else:
                                    return { "status": 403, "type": "invalid.start.date" }, 403
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
    except:
        return { "status": 500, "content": "Request cancelled - An error has occured. Please contact us at contact@constellate.pro"}, 500

def getagent(agent):
    if (agent == 'got (https://github.com/sindresorhus/got)'):
        return 'Unknown author'
    elif(len(agent) < 1):
        return 'Unknown author'
    else:
        return agent


def write(data, agent):
    with open('../_posts/' + str(data['id']) + '.md', 'w') as fp:            
            fp.write('---\nlayout: post\ntitle: "' + data['title'] + '"\ndescription: "' + data['description'] + '"\ntags: [' + agent + ']\n---')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
