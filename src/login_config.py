import json

def get_credentials(filepath):
    """
    Retrieve login credentials
    """
    with open(filepath, 'r') as f:
        credentials = json.load(f)
    return credentials

def main():
    # Path to your credentials file
    credentials_filepath = 'credentials.json'
    
    # Retreieve credentials
    credentials = get_credentials(credentials_filepath)
    
    # Access your credentials
    username = credentials['username']
    password = credentials['password']

    return username, password

if __name__ == "__main__":
    main()