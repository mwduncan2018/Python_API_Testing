import configparser

class ConfigProvider:
    _config = configparser.ConfigParser()
    _config.read("./automation_config.ini")

    _username = _config["AUTOMATION CONFIG"]["Username"] 
    _password = _config["AUTOMATION CONFIG"]["Password"] 
    _g_token = _config["AUTOMATION CONFIG"]["GToken"]
    _host = _config["AUTOMATION CONFIG"]["Host"]

    @classmethod
    def get_username(cls) -> str:
        return cls._username

    @classmethod
    def get_password(cls) -> str:
        return cls._password
    
    @classmethod
    def get_g_token(cls) -> str:
        return cls._g_token

    @classmethod 
    def get_host(cls) -> str:
        return cls._host

    @classmethod
    def print_config(cls):
        print("Username: " + cls._username)
        print("Password: " + cls._password)
        print("GToken: " + cls._g_token)
        print("Host: " + cls._host)