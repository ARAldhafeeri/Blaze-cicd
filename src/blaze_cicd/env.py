import os
def replace_env_variables(config):
    if isinstance(config, dict):
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("%") and value.endswith("%"):
                env_var = value[1:-1]  # Remove the % symbols
                config[key] = os.getenv(env_var, f"Environment variable '{env_var}' not found")
            elif isinstance(value, (dict, list)):
                replace_env_variables(value)
    elif isinstance(config, list):
        for item in config:
            replace_env_variables(item)
    return config