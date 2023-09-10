import configparser

from mongoengine import connect

config = configparser.ConfigParser()
configFilePath = "RabbitMQ\config.ini"
config.read(configFilePath)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

# connect to cluster on AtlasDB with connection string
URI = f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"""

connect(host=URI, ssl=True)
