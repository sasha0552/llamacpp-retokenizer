from flask import Flask, Response, jsonify, request
from json import dumps, load
from os import environ
from requests import get, post
from transformers import AutoTokenizer

# Load configuration
try:
  with open(environ.get("CONFIG_PATH", "config.json"), "r") as file:
    config = load(file)
except:
  raise RuntimeException("Failed to load the configuration file")

# Define Flask app
app = Flask(__name__)

# Initialize tokenizer from pretrained model
tokenizer = AutoTokenizer.from_pretrained(config["tokenizer_path"])

def proxy_response(object):
  """
    Construct a Flask Response object from a requests response object.

    Args:
    - object: A requests object containing response data.

    Returns:
    - Response: A Flask response object.
  """

  # List of headers to be excluded from the response
  excluded_headers = [
    "connection",
    "content-encoding",
    "content-length",
    "transfer-encoding",
  ]

  # Filter headers from the requests object, excluding those in excluded_headers
  headers = [
    (key, value) for (key, value) in object.raw.headers.items() if key.lower() not in excluded_headers
  ]

  # Return the response with filtered headers
  return Response(object.content, object.status_code, headers)

@app.route("/completion", methods=["POST"])
@app.route("/completions", methods=["POST"])
@app.route("/v1/completions", methods=["POST"])
def completions():
  """
    Handle requests for text completion.
  """

  # Extract data from the request
  data = request.get_data()

  # If data is JSON
  if request.is_json:
    # Extract JSON data from the request
    data = request.json

    # Check if "prompt" key exists in data and encode if it's a string
    if "prompt" in data:
      if isinstance(data["prompt"], str):
        data["prompt"] = tokenizer.encode(data["prompt"])

    # Save JSON as string
    data = dumps(data)

  # Send a POST request to the specified endpoint with data and return the response
  return proxy_response(
    post(f"{config['endpoint']}/v1/completions", data=data)
  )

@app.route("/tokenize", methods=["POST"])
def tokenize():
  """
    Handle requests for tokenization of input text.
  """

  # Extract JSON data from the request
  data = request.json

  # Tokenize the content and return the tokens as JSON
  return jsonify({
    "tokens": tokenizer.encode(data.get("content", ""))
  })

@app.route("/<path:path>", methods=["GET", "POST"])
def proxy(path):
  """
    Simply resend the remaining requests to the upstream server.
  """

  if request.method == "GET":
    # Send a GET request to the endpoint and return the response
    return proxy_response(
      get(f"{config['endpoint']}/{path}")
    )
  elif request.method == "POST":
    # Send a POST request to the endpoint with data and return the response
    return proxy_response(
      post(f"{config['endpoint']}/{path}", data=request.get_data())
    )

def main():
  app.run(debug=True, host=config["host"], port=config["port"])

if __name__ == "__main__":
  main()
