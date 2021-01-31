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


#
#   geturlshrtn: returns the shortened url for a given url (internal)
#
@app.route('/geturlshrtn/<url_shrt_code>', methods=['GET'])
def getUrlShrtn(url_shrt_code):
    print("\n\n/geturlshrtn/ for: " + str(url_shrt_code))

    url_shrtn = dbmgr.get_url_shrtn(url_shrt_code)

    return jsonify(url_shrtn)   



#
#   teleport: redirects to the website represented by the shortened URL
#
@app.route('/teleport/<url_shrt_code>', methods = ['GET'])
def teleport(url_shrt_code):
    print("\n\n/teleport/ for: " + str(url_shrt_code))

    res = dbmgr.get_url_shrtn(url_shrt_code)

    print("type of res: "+str(type(res)))
    print(res)
    # print("url_orig: "+str(res['url_original']))
    print("jsonifyed res: "+str(jsonify(res)))
    
    print("STATUS: " + res['status'])
    if res['status'] == "OK":
        return redirect(res['url_original'])
    else:    
        return jsonify(res)



#
#   addurlshrtn: generates a new shortened url for a given url (protocol + domain) and expiration days
#
@app.route('/addurlshrtn/<url_orig_prc>/<url_orig_dom>/<exp_days>', methods=['GET'])
@app.route('/addurlshrtn/<url_orig_prc>/<url_orig_dom>/', methods = ['GET'])
def addurlshrtn(url_orig_prc, url_orig_dom, exp_days="3"):
    print("\n\n/addurlshrtn/ for url prc: " + str(url_orig_prc) + "; urc domain: " + str(url_orig_dom) + "; expiration days: " + str(exp_days))
    
    res = dbmgr.add_url_shrtn(url_orig_prc, url_orig_dom, exp_days)

    return jsonify(res)


#
#   delurlshrtn: removes a shortened url
#
@app.route('/delurlshrtn/<url_shrt_code>', methods = ['GET'])
def delurlshrtn(url_shrt_code):
    print("\n\n/delurlshrtn/: " + str(url_shrt_code))
    
    res = dbmgr.del_url_shrtn(url_shrt_code)

    return jsonify(res)





class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)