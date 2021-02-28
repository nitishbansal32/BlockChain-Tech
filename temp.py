import datetime
import hashlib
import json
from flask import Flask,jsonify


class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.create(proof=1, previous_hash='0')
        
    def create(self, proof, previous_hash):
        block = {'block':len(self.chain)+1,
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'Date_Time':str(datetime.datetime.now())}
        self.chain.append(block)
        return block
    
    def lastBlock(self):
        return self.chain[-1] 
    
    def PoW(self, previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hashh=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hashh[0:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        a=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(a).hexdigest()
    
    
    def chain_v(self,chain):
        Pblock=chain[0]
        index=1
        while index<len(chain):
            block=chain[index]
            if(block['previous_hash']!=self.hash(Pblock)):
                return False
            previous_proof=Pblock['proof']
            proof=block['proof']
            hashh=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hashh[0:4]!='0000':
                return False
            Pblock=block
            index+=1
            return True
        
app=Flask(__name__)
        
obj1=Blockchain()
        
@app.route('/mine',methods=['GET','POST'])

def mine():
     Pblock=obj1.lastBlock()
     previous_proof=Pblock['proof']
     proof=obj1.PoW(previous_proof)
     previous_hash=obj1.hash(Pblock)
     block=obj1.create(proof, previous_hash)
     res={'Block':block['block'],
         'proof of work':block['proof'],
         'previous_hash':block['previous_hash'],
         'Date_Time':block['Date_Time'],}
     return jsonify(res)

@app.route('/chain',methods=['GET','POST'])
def chain():
    res=obj1.chain
    return jsonify(res)


app.run(host='0.0.0.0', port=5000) 
