from dotenv import dotenv_values

def get_env_variable(key, default=None):
    env = dotenv_values()
    return env.get(key, default)

