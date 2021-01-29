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


@app.route('/geturlshrtn/<url_orig>', methods=['GET'])
def getUrlShrtn(url_orig):
    # url_orig = request.args.get('urlorig')
    print("\n\n/geturlshrtn/ for: " + str(url_orig))
    dbmgr = DbManager()
    dbmgr.connect_db()
    url_shrtn = dbmgr.get_url_shrtn(url_orig)

    return jsonify(url_shrtn)


# DEBUG
@app.route('/geturlshrtntest/<url_orig>/<exp_days>', methods=['GET'])
def getUrlShrtnTest(url_orig, exp_days):
    print("\n\n/geturlshrtntest/ for: " + str(url_orig) + "; expiration_date: " + str(exp_days))
    dbmgr = DbManager()
    dbmgr.connect_db()
    url_shrtn = dbmgr.get_url_shrtn_test(url_orig, exp_days)

    return jsonify(url_shrtn)   




@app.route('/geturlorig/<url_shrt>', methods = ['GET'])
def getUrlOrig(url_shrt):
    dbmgr = DbManager()
    dbmgr.connect_db()
    url_orig = dbmgr.get_url_orig(url_shrt)

    print("\n\n/geturlorig/ for: " + str(url_shrt))
    print(url_orig)
    type("urls_orig_type: " + str(url_orig))
    print("urls_orig: " + str(url_orig))

    return jsonify(url_orig)    




@app.route('/teleport/<url_shrt>', methods = ['GET'])
def teleport(url_shrt):
    print("\n\n/teleport/ for: " + str(url_shrt))

    dbmgr = DbManager()
    dbmgr.connect_db()
    url_orig = dbmgr.get_url_orig(url_shrt)

    print("type of url_orig: "+str(type(url_orig)))
    print(url_orig)
    print("url_orig: "+str(url_orig['url_original']))
    print("jsonifyed url_orig: "+str(jsonify(url_orig)))
    
    return redirect("http://" + url_orig['url_original'])
    # return redirect(f"http://{urls_orig[0]}")




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