class User(object):
  def __init__(self, email, data, client):
    self._email = email
    self._data = data
    self._client = client

  @property
  def id(self):
    return self._data["id"]

  @property
  def email(self):
    return self._email

  @property
  def name(self):
    return self._data["name"]
  
  @property   
  def ticks(self):
    # get all the ticks
    return self._client.ticks.get(self.email)
    
  @property
  def todos(self):
    return self._client.routes.get_todos(self.email)
