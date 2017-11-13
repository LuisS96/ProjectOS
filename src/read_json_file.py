import json
import os

def read_order(file):
    # Assures that the file exists and is located in the same directory
    if os.path.isfile(file) == False:
        print('The file "{0}" is not located in the same directory or does not exist.'.format(file))
        return
    else:
        # Creates file title into lowercase string and checks file extension if json
        if file.lower().endswith('.json'):
            # Trys to open the json file, an exception is raised if file can not be read properly
            try:
                with open(file) as jsfl:
                    data = json.load(jsfl)
                return data
            except:
                print("Make sure your json file is correctly written")
        else:
            print('File type is not .json and cannot be readen')