from index import lambda_handler

if __name__ == "__main__":
    event = {}
    context = {}

    lambda_handler(event, context)
