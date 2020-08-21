import json, flask
from google.cloud import firestore

def countrygame_highscore(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        #'Access-Control-Allow-Headers': 'Accept, X-Requested-With, Content-Type', #Content-Type
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, HEAD',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'content-type':'application/json;charset=utf-8'
    }

    if request.method == 'GET':
        return (get_highscore(), 200, headers)
    if request.method == 'POST':
        #return (save_highscore(request), 201, headers)
        return save_highscore(request)

def save_highscore(request):
    print(request)
    req = request.get_json()
    print(req)
    if req:
        data = {"name":req['name'], "score":req['score'], "date":req['date']}
        print(data)
        # Add a new document
        db = firestore.Client()
        doc_ref = db.collection(u'highscores').add(data)
        print("Added recored to db successfully: %s"%(data))
        response = flask.jsonify({"success":"ok"})
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
        return response


def get_highscore():
    resp = []
    # Then query for documents
    db = firestore.Client()
    for doc in db.collection(u'highscores').order_by(u'score').stream():
        resp.append(doc.to_dict())
    return json.dumps({"data":resp})