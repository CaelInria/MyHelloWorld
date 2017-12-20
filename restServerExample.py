#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
import time
import random
from math import sqrt, exp

from flask import Flask, request, json

################################################################################
class MyToken:

    def __init__(self, aLogin, aPassword):
        self.startTime = int(time.time())
        self.tokenId = "TID_" + str(self.startTime)
        if self.tokenId in myTokens:
            self.tokenId = "TID_" + str(self.startTime + 2)
        self.lifetime = random.randint(1, 300)
        self.currentLifetime = 0
        self.login = aLogin
        self.password = aPassword
        return

    def isValid(self):
        # currentTime
        currentTime = int(time.time())
        self.currentLifetime = currentTime - self.startTime
        return(self.currentLifetime < self.lifetime)


################################################################################
def str2Int(stringValue):
    try: 
        result = int(stringValue)
    except ValueError:
        result = 0
    return(result)


################################################################################
myUsers = {'admin':'admin', 'admin':'root', 'foo':'bar'}
myTokens = {}
myApp = Flask(__name__)

################################################################################
@myApp.route('/welcome', methods = ['POST'])
def myWelcome():
    return "Welcome! :-))))"


################################################################################
@myApp.route('/bye', methods = ['POST'])
def myBye():
    return "That's all Folks! :-))))"


################################################################################
@myApp.route('/login', methods = ['POST'])
def myLogin():
    # print('request = ' + request.method)
    # print('headers : ')
    # print request.headers
    # print('args : ')
    # for key, val in request.args:
        # print key, "=>", val

    aLogin = ""
    aPassword = ""
    theResult = '{"fault":"invalid login and password"}'

    if request.headers['Content-Type'] == 'application/json':
        # jsonContent = json.dumps(request.json)
        # print('json: ' + jsonContent)
        if 'login' in request.json:
            aLogin = request.json['login']
        if 'pass' in request.json:
            aPassword = request.json['pass']
        if aLogin != "" and aPassword != "":
            if aLogin in myUsers:
                if aLogin == aPassword:
                    theResult = '{"fault":"too easy :o) ;-p"}'
                elif myUsers[aLogin] == aPassword:
                    theToken = MyToken(aLogin, aPassword)
                    myTokens[theToken.tokenId] = theToken
                    theResult = '{"token":"' + str(theToken.tokenId) + '"}'
    return(theResult)


################################################################################
@myApp.route('/compute', methods = ['POST'])
def myCompute():
    aToken = ""
    anExpression = ""
    theResult = '{"fault":"invalid expression"}'

    if request.headers['Content-Type'] == 'application/json':
        # jsonContent = json.dumps(request.json)
        # print('json: ' + jsonContent)
        if 'token' in request.json:
            aToken = request.json['token']
        if 'expression' in request.json:
            anExpression = request.json['expression']
        if aToken != "" and anExpression != "":
            if aToken in myTokens:
                tokenLifetime = myTokens[aToken].lifetime
                if myTokens[aToken].isValid():
                    resultValue = eval(anExpression)
                    theResult = '{"result":"' + str(resultValue) + '"}'
                else:
                    theResult = '{"fault":"Zzz Zzz - lived for "' + \
                        str(myTokens[aToken].currentLifetime) + ' seconds"}'
                    del myTokens[aToken]
            else:
                theResult = '{"fault":"invalid token :o) ;-p"}'
    return(theResult)


################################################################################
@myApp.route('/setlifetime', methods = ['POST'])
def setLifetime():
    aToken = ""
    theValue = ""
    theResult = ""

    if request.headers['Content-Type'] == 'application/json':
        # jsonContent = json.dumps(request.json)
        # print('json: ' + jsonContent)
        if 'token' in request.json:
            aToken = request.json['token']
        if 'value' in request.json:
            theValue = request.json['value']
            lifetime = str2Int(theValue)
        if aToken != "":
            if lifetime > 0:
                if aToken in myTokens:
                    if myTokens[aToken].isValid():
                        if lifetime < myTokens[aToken].lifetime:
                            myTokens[aToken].lifetime = lifetime
                            theResult = '{"' + aToken + '.lifetime":"' + str(lifetime) + '"}'
                        else:
                            theResult = '{"fault":"lifetime too large = "' + \
                                str(lifetime) + '"}'
                    else:
                        theResult = '{"fault":"Zzz Zzz - lived for "' + \
                            str(myTokens[aToken].currentLifetime) + ' seconds "}'
                        del myTokens[aToken]
                else:
                    theResult = '{"fault":"invalid token Id: "' + str(aToken) + '"}'
            else:
                theResult = '{"fault":"invalid lifetime = "' + str(lifetime) + '"}'
        else:
            theResult = '{"fault":"invalid tokenId: empty token Id"}'
    return(theResult)


################################################################################
if __name__ == '__main__':
    myApp.run(host = "0.0.0.0", port = "8080")
