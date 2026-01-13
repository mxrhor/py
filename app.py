from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def zw_request(phonenumber):
    cookies = {'zcauthcookie': 'XdW-ZAvxW2VY84cDrUNdJ3BZtoZI15N8CGlf3Kaeyb2s2-mxcEZ0tA6c7h6t8Jyphn4ROC0CwtvGdG7z668Qabk74FkAN9b23X1-LVmYkFGeQ9DlMJ95STWWKIJXTPUpOVQ2h8RvgdkjsQ3r3huDOpRXXwTuIBqIBc2M28LnJx2Gh2mrHg1ccXQxQtVMA5I3ldV3lr1D0f2ebZrGiB0WBx27a5di2ciqiB2v5M8MradGLzCJrWHSheSjmrhRRA4fV-2heUuuEPJ8ODtxqX9lQ5DDiAPMsHN2ivEAbrSc714cY3DsGzqLHaI94ZPAusEjZVFYZiotigi2Fq4xYcR-jqChA9RSgGyh9j6o-pO_y0g',}
    headers = {'Accept': 'application/json, text/plain, */*','Cache-Control': 'no-cache','Connection': 'keep-alive','Pragma': 'no-cache','Referer': 'https://myzain.kw.zain.com/','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36','accept-language': 'ar','sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"','sec-ch-ua-mobile': '?0',}
    response = requests.get(f'https://myzain.kw.zain.com/api/customers/anonymous/lines/{phonenumber}/info/type',cookies=cookies,headers=headers,)
    contact_id = response.json()['ContractID']
    return requests.get(f'https://myzain.kw.zain.com/api/customers/{contact_id}/lines/{phonenumber}/billing/balance/postpaid',cookies=cookies,headers=headers,)


@app.route('/zw',methods=['POST'])
def process_data():
    if request.method == 'POST':
        phonenumber = request.get_json().get('phonenumber')
        try:
            response = zw_request(phonenumber)
            pastdue = response.json()['result']['PastDue']
        # unbilled = response.json()['result']['Unbilled']
        # totalpastdue = float(pastdue) + float(unbilled)
        # message = {'totalpastdue':totalpastdue,'unbilled':unbilled,'pastdue':pastdue}
            return jsonify({'pastdue':pastdue}),200
        except Exception as e:
            return jsonify({'error':str(e)}),401

        # return jsonify({'totalpastdue': f'{totalpastdue}', 'unbilled':unbilled,'pastdue':pastdue})
    else:
        return "METHOD IS NOT FUCKING ALLOWED",200

