from environs import Env

ENV = Env()
ENV.read_env()

# KAFKA CONFIGURATION
KAFKA_BOOTSTRAP_SERVERS = ENV.list("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_GROUP_ID = ENV("KAFKA_GROUP_ID", default="notificaitons")
KAFKA_TOPIC_USER_REGISTERED = ENV("KAFKA_TOPIC_USER_REGISTERED", default="user-registered")

# USERS CONFIGURATION
USERS_URL = ENV("USERS_URL")