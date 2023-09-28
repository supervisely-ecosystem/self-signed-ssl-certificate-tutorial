from os.path import expanduser
from dotenv import load_dotenv

# load env files before importing supervisely
load_dotenv("local.env")
load_dotenv(expanduser("~/supervisely.env"))

import supervisely as sly

api = sly.Api.from_env()

# If you've set the environment variables correctly, you should be able to connect to the server
# Your code to interact with Supervisely goes here, send any API request, for example request user info
user = api.user.get_my_info()
print(user.login)
