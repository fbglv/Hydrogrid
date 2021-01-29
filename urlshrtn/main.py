from flask import Blueprint  
from flask import Flask, abort, request, jsonify
from flask import jsonify
from flask import redirect
import json
import logging
from db_manager import DbManager


# print("URL Service")

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

dbmgr = DbManager()
dbmgr.connect_db()


# url_service = Blueprint('url_api', __name__) # flask blueprints: https://flask.palletsprojects.com/en/1.1.x/blueprints/



@app.route('/geturlshrtn/<url_orig>', methods=['GET'])
def getUrlShrtn(url_orig):
    print("\n\n/geturlshrtn/ for: " + str(url_orig))
    # dbmgr = DbManager()
    # dbmgr.connect_db()
    url_shrtn = dbmgr.get_url_shrtn(url_orig)

    return jsonify(url_shrtn)   






@app.route('/geturlorig/<url_shrt>', methods = ['GET'])
def getUrlOrig(url_shrt):
    # dbmgr = DbManager()
    # dbmgr.connect_db()
    url_orig = dbmgr.get_url_orig(url_shrt)

    print("\n\n/geturlorig/ for: " + str(url_shrt))
    print(url_orig)
    type("urls_orig_type: " + str(url_orig))
    print("urls_orig: " + str(url_orig))

    return jsonify(url_orig)    




@app.route('/teleport/<url_shrt_code>', methods = ['GET'])
def teleport(url_shrt_code):
    print("\n\n/teleport/ for: " + str(url_shrt_code))

    res = dbmgr.get_url_orig(url_shrt_code)

    print("type of res: "+str(type(res)))
    print(res)
    # print("url_orig: "+str(res['url_original']))
    print("jsonifyed res: "+str(jsonify(res)))
    
    print("STATUS: " + res['status'])
    if res['status'] == "OK":
        return redirect(res['url_original'])
    else:    
        return jsonify(res)

    # return redirect("http://" + url_orig['url_original'])
    # return redirect(f"http://{urls_orig[0]}")




@app.route('/addurlshrtn/<url_orig_prc>/<url_orig_dom>/<exp_days>', methods=['GET'])
def addurlshrtn(url_orig_prc, url_orig_dom, exp_days):
    print("\n\n/addurlshrtn/ for url prc: " + str(url_orig_prc) + "; urc domain: " + str(url_orig_dom) + "; expiration days: " + str(exp_days))
    
    res = dbmgr.add_url_shrtn(url_orig_prc, url_orig_dom, exp_days)

    return jsonify(res)




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