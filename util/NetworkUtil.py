import asyncio

class NetworkUtil:  
  def checkResponse(self, response):
    response = self.checkNetwork(response)
    if response == False:
      return False
    json = self.getResponseData(response)
    if json == False:
      return False
    return json

  def checkNetwork(self, response):
    if ( response.status_code != 200 | response.status_code != 201 ):
      return False
    else:
      return response

  def getResponseData(self, response):
    json = response.json()
    if json['code'] != 200:
      return False
    return json
  
