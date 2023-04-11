from flask import Flask;
from flask_pymongo import PyMongo;
from bson.json_util import dumps;
from bson.objectid import ObjectId;
from flask import jsonify,request;
from werkzeug.security import generate_password_hash,check_password_hash;

app=Flask(__name__)
app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb://localhost:27017/hotelmgmtDB"

mongo=PyMongo(app)

@app.route('/ownerAdd',methods=['POST'])
def ownerAdd():
    _ownerDetails=request.json
    _name=_ownerDetails['name']
    _contact=_ownerDetails['contact']

    if _name and _contact and request.method=='POST':
        ownerID=mongo.db.owner.insert_one({'name':_name,'contact':_contact})
        resp=jsonify("Owner details added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/ownerView')
def ownerView():
    owners=mongo.db.owner.find()
    resp=dumps(owners)
    return resp

@app.route('/ownerView/<name>')
def ownerByID(name):
    hh=[]
    owner=mongo.db.owner.find_one({'name':name}   )
    ownerhh=mongo.db.hhMapping.find({'ownerId':ObjectId(owner['_id'])})
    for i in ownerhh:
        hh.append(mongo.db.hh.find_one({'_id':ObjectId(i['hhId'])}))
    resp=dumps(hh)
    return resp

@app.route('/ownerDelete/<id>',methods=['DELETE'])
def ownerDelete(id):
    mongo.db.owner.delete_one({'_id':ObjectId(id)})
    resp=jsonify("Owner deleted successfully!")
    resp.status_code=200
    return resp

@app.route('/ownerUpdate/<id>',methods=['PUT'])
def ownerUpdate(id):
    _id=id
    _ownerDetails=request.json
    _name=_ownerDetails['name']
    _contact=_ownerDetails['contact']

    if _name and _contact and _id and request.method=='PUT':
        mongo.db.owner.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'contact':_contact}})
        resp=jsonify("Owner updated successfully!")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/hhAdd',methods=['POST'])
def hhAdd():
    _hhDetails=request.json
    _name=_hhDetails['name']
    _address=_hhDetails['address']
    _city=_hhDetails['city']
    _state=_hhDetails['state']

    if _name and _address and _city and _state and request.method=='POST':
        hhId=mongo.db.hh.insert_one({'name':_name,'address':_address,'city':_city,'state':_state})

        resp=jsonify(("Holiday Home listed successfully!"))
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/hhView')
def hhView():
    hhDetails=mongo.db.hh.find()
    resp=dumps(hhDetails)
    return resp

@app.route('/hhView/<name>')
def hhRoom(name):
    room1=[]
    hh=mongo.db.hh.find_one({'name':name}   )
    hhRooms=mongo.db.roomMapping.find({'hhId':ObjectId(hh['_id'])})
    for i in hhRooms:
        room1.append(mongo.db.room.find_one({'_id':ObjectId(i['roomId'])}))
    resp=dumps(room1)
    return resp

@app.route('/hhDelete/<id>',methods=['DELETE'])
def hhDelete(id):
    mongo.db.hh.delete_one({'_id':ObjectId(id)})
    resp=jsonify("Holiday home deleted successfully!")
    resp.status_code=200
    return resp

@app.route('/hhUpdate/<id>',methods=['PUT'])
def hhUpdate(id):
    _id=id
    _hhDetails=request.json
    _name=_hhDetails['name']
    _address=_hhDetails['address']
    _city=_hhDetails['city']
    _state=_hhDetails['state']

    if _name and _address and _id and _city and _state and request.method=='PUT':
        mongo.db.hh.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'address':_address,'city':_city,'state':_state}})
        resp=jsonify("Holiday home updated successfully!")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/roomAdd',methods=['POST'])
def roomAdd():
    _roomDetails=request.json
    _name=_roomDetails['name']
    _price=_roomDetails['price']
    _checkIn=_roomDetails['checkIn']
    _checkOut=_roomDetails['checkOut']
    _availability=_roomDetails['availability']
    _rules=_roomDetails['rules']

    if _name and _price and  _checkIn and _checkOut and _availability and _rules and request.method=='POST':
        roomID=mongo.db.room.insert_one({'name':_name,'price':_price,'checkIn':_checkIn,'checkOut':_checkOut,'availability':_availability,'rules':_rules})
        resp=jsonify("Room details added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/roomView')
def roomView():
    roomDetails=mongo.db.room.find()
    resp=dumps(roomDetails)
    return resp

@app.route('/roomView/<id>')
def roomByID(id):
    roomByID=mongo.db.room.find_one({'_id':ObjectId(id)})
    resp=dumps(roomByID)
    return resp

@app.route('/roomDelete/<id>',methods=['DELETE'])
def roomDelete(id):
    mongo.db.room.delete_one({'_id':ObjectId(id)})
    resp=jsonify("Room deleted successfully!")
    resp.status_code=200
    return resp

@app.route('/roomUpdate/<id>',methods=['PUT'])
def roomUpdate(id):
    _id=id
    _roomDetails=request.json
    _name=_roomDetails['name']
    _price=_roomDetails['price']
    _checkIn=_roomDetails['checkIn']
    _checkOut=_roomDetails['checkOut']
    _availability=_roomDetails['availability']
    _rules=_roomDetails['rules']

    if _name and _price and _id and _checkIn and _checkOut and _availability and _rules and request.method=='PUT':
        mongo.db.room.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'price':_price,'checkIn':_checkIn,'checkOut':_checkOut,'availability':_availability,'rules':_rules}})
        resp=jsonify("Room updated successfully!")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not found'+request.url
    }
    resp = jsonify((message))
    resp.status_code=404
    return resp

if __name__=="__main__":
    app.run(debug=True)
