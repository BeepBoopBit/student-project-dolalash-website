import json
import pymongo

class PyMo:
    def __init__(self, path):
        """
        Description: Sets up mongoDB\n
        `path: string` - path to your credentials.json
        """
        f = open(path)
        data = json.load(f)

        self.credentials = data
        f.close()

        # Check if credentials.json has the keys "user" and "pass"
        self.__validate_credentials();

        # Try to connect to mongoDB
        self.mongoClient = pymongo.MongoClient(f"mongodb+srv://{self.credentials['user']}:{self.credentials['password']}@{self.credentials['clusterAddress']}/?retryWrites=true&w=majority")
        pass

    # Private Methods
    def __validate_credentials(self):
        """
        Description: Validates user mongoDB credentials by checking if JSON has the required keys (user, password, clusterAddress)
        """
        keys_list = []
        if not 'user' in self.credentials:
            keys_list.append("user")
        if not 'password' in self.credentials:
            keys_list.append("password")
        if not 'clusterAddress'in self.credentials:
            keys_list.append("clusterAddress")

        keys_str = ", ".join(keys_list)

        if len(keys_list) != 0:
            raise Exception(f"Invalid credentials missing key/s: {keys_str}")
