import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

# This line loads the variables from your .env file into the environment
load_dotenv()

# Create the FastAPI application instance
app = FastAPI()


# --- Configuration ---
# Read the client ID and secret from the environment.
# os.getenv() will return None if the variable is not found.
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# --- !! CRUCIAL DEBUGGING BLOCK !! ---
# This will print the loaded values to your terminal when the server starts.
# It helps you verify if the .env file is being read correctly.
print("--- Checking Loaded Environment Variables ---")
print(f"CLIENT_ID: {GOOGLE_CLIENT_ID}")
print(f"CLIENT_SECRET: {'Loaded' if GOOGLE_CLIENT_SECRET else 'Not Found'}")
print("---------------------------------------------")
# ----------------------------------------


# This redirect URI must EXACTLY match one of the URIs you configured
# in your Google Cloud Console credentials page.
REDIRECT_URI = "http://localhost:8000/auth/callback" 

# Google's OAuth 2.0 endpoints
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


@app.get("/")
def read_root():
    """ A simple endpoint to check if the server is running. """
    return {"message": "Welcome to the Sandbox_AI Backend!"}


@app.get("/login")
def login():
    """
    This endpoint initiates the Google login flow.
    It constructs the authorization URL and redirects the user's browser to Google.
    """
    # Define the parameters for the authorization request.
    # `scope` determines what permissions we are asking for.
    # `openid profile email` are standard scopes for basic user info.
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "access_type": "offline",
    }
    
    # Use httpx to safely build the URL with the query parameters.
    auth_url = httpx.URL(AUTHORIZATION_URL, params=params)
    
    # Redirect the user's browser to the constructed URL.
    return RedirectResponse(str(auth_url))


@app.get("/auth/callback")
async def auth_callback(request: Request):
    """
    This is the endpoint that Google redirects the user back to after they
    have successfully authenticated.
    """
    # The 'code' is a one-time use authorization code from Google.
    code = request.query_params.get("code")

    # Now, we exchange this 'code' for an 'access token'.
    # The access token is what we'll use to make API calls on behalf of the user.
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    # Make a POST request to Google's token endpoint to get the token.
    async with httpx.AsyncClient() as client:
        token_response = await client.post(TOKEN_URL, data=token_data)
    
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # With the access token, we can now fetch the user's profile information.
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(user_info_url, headers=headers)
        
    user_info = user_info_response.json()

    # In a real application, you would create a session for the user here.
    # For this demo, we'll just display their info to confirm it worked.
    return {"user_info": user_info}