from resources.resource import Resource
import models.user

class Users(Resource):
  def get(self, email):
    return models.user.User(
      email,
      self.client.get("get-user", {
        "email": email
      }),
      self.client
    )
