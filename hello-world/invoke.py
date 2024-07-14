import requests

def send_request_to_gcp_function(function_url, name):
    """Sends a request to a GCP HTTP Cloud Function.

    Args:
        function_url (str): The URL of the GCP function.
        name (str): The name to be included in the request (default "Maciej").
    """

    try:
        # Prepare the data for the request (as JSON or query parameters)
        # Uncomment the appropriate line depending on how your function expects data
        # data = {"name": name}  # If your function expects JSON payload
        params = {"name": name}  # If your function expects query parameters

        # Send the request
        # response = requests.get(function_url, json=data) 
        response = requests.get(function_url, params=params) 

        # Check if the request was successful
        response.raise_for_status()

        # Handle the response from the function
        print("Response from GCP function:", response.text)

    except requests.exceptions.RequestException as error:
        print(f"Error sending request to GCP function: {error}")


# Replace 'YOUR_FUNCTION_URL' with the actual URL of your deployed GCP function
function_url = 'https://us-central1-aesthetic-fiber-428811-m0.cloudfunctions.net/hello-world'  

# Send the request with the name "Maciej"
send_request_to_gcp_function(function_url, "machofvmaciek")
