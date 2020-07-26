import json
from bs4 import BeautifulSoup


from flask import abort, request, Flask
from flask_cors import CORS

from disambiguate_NE import disambiguate_NE

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def preprocess_sent_html(sent_html):
    soup = BeautifulSoup(sent_html)
    tokens = []
    for span in soup.find_all("span", "entity"):
        tokens.append([int(v) for v in span['data-start_end'].split(" ")])
    
    return {'sent': soup.text, 'entity': tokens}


@app.route('/api/get_entity', methods=['POST'])
def post_handler():
    
    data = request.get_json()
    text = data.get("sent", "")
    sent_data = preprocess_sent_html(text)
    
    sent = sent_data['sent']
    spans = sent_data['entity']
    
    if not spans:
        return json.dumps({'entity': []})
    
    
    result = [disambiguate_NE(sent[token_start:token_end]) for token_start, token_end in spans]
    result = [[idx, title] for idx, title in enumerate(result) if title]
    
    return json.dumps({'entity': result})


# Forbidden address not in NTHU(140.114)
#@app.before_request
#def limit_remote_addr():
#    if not request.remote_addr.startswith('127.0.0.1'):
#        abort(403) 

def read_json(post_data):
    data = json.loads(post_data.decode("utf-8"))
    #print("received data:", data)
    text = data["text"]
    spans = [(int(j["start"]), int(j["length"])) for j in data["spans"]]
    return text, spans


if __name__ == "__main__":
        
        
    app.run(host= '0.0.0.0', port=5555)
    
    print("start app server on http://hostname:5555")
