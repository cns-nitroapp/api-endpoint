from flask import Flask, request, jsonify
import logging
import json
from github import Github

from flask.wrappers import Response

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/v1/post', methods=['POST']) 
def post():
    data = request.get_json()
    agent = request.headers.get('User-Agent')

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

def getagent(agent):
    if (agent == 'got (https://github.com/sindresorhus/got)'):
        return 'Unknown author'
    elif(len(agent) < 1):
        return 'Unknown author'
    else:
        return agent


def write(data, agent):
    with open('../_posts/' + str(data['id']) + '.md', 'w') as fp:
        content = '---\nlayout: post\ntitle: "' + data['title'] + '"\nauthor: [' + agent + ']\nstart-date: "' + data['start-date'] + '"\nend-date: "' + data['end-date'] + '"\n---\n' + data['description']
        fp.write(content)
        github(str(data['id']), content, data['start-date'])

def github(id, content, start):
    g = Github('') #PERSONAL_ACCESS TOKEN HERE

    org = g.get_organization('cns-nitroapp')
    org.login
    repo = org.get_repo('blog')

    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    # Upload to github
    git_prefix = '_posts/'
    git_file = git_prefix + start + '-' + id + '.md'
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
