def get_api_key():
    with open("openai_api_key.txt", "r") as f:
        return f.read().strip()
    

    