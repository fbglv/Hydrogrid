from flask import Blueprint  
from flask import Flask, abort, request, jsonify
from flask import jsonify
from flask import redirect
import json
from db_manager import DbManager


# print("URL Service")

app = Flask(__name__)
@app.route('/welcome/', methods=['GET'])

# url_service = Blueprint('url_api', __name__) # flask blueprints: https://flask.palletsprojects.com/en/1.1.x/blueprints/

# @url_service.route('/geturl', methods=['GET'])
@app.route('/geturlshrtn/<url_orig>', methods=['GET'])
def getUrlShrtn(url_orig):
    # url_orig = request.args.get('urlorig')
    print("\n\n/geturl/ for: " + str(url_orig))
    dbmgr = DbManager()
    dbmgr.connect_db()
    urls_shrtn = dbmgr.get_url_shrtn(url_orig)
    # urls_shrt_dict = []
    # for i in urls_shrt:
    #    r = {"url_shortened": i[0], "url_original": i[1], "expiration_time": i[2]}  
    #    urls_shrt_dict.append(r)
    return jsonify(urls_shrtn)




@app.route('/geturlorig/<url_shrt>', methods = ['GET'])
def getUrlOrig(url_shrt):
    print("\n\n/geturlorig/ for: " + str(url_shrt))
    dbmgr = DbManager()
    dbmgr.connect_db()
    urls_orig = dbmgr.get_url_orig(url_shrt)
    type(urls_orig)
    print(urls_orig)
    return jsonify(urls_orig)    




@app.route('/teleport/<url_shrt>', methods = ['GET'])
def teleport(url_shrt):
    # return redirect(f"http://www.google.com")
    return redirect(f"http://{url_orig}")
"""
@app.route('/redirect_url_shrt', methods = ['POST', 'GET'])
def redirect_url_shrt():
    if request.method == 'POST':
        url_shrt = request.form['url_shrt']
        return redirect(f"{url_shrt}")
"""



class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)