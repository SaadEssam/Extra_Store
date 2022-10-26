import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
  def __init__(self):
    self.client_id = "AQolwgt5n0SY30Qg9HZAX6rPuapjo2-6KowllsOXuEuLgUgb2Wd1bU9XmJFJK-1202H5vjNIG5lH6KWA"
    self.client_secret = "EOU9I4tXJnkW4_R8bb1jwx3Fhn6C34g-1TyWxFDALhixeTFSLBDH7neWzGPxHFPL16xn_8hhTg6DKgz4"
    self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
    self.client = PayPalHttpClient(self.environment)