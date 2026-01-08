import requests
from flask import current_app

PAYSTACK_API_BASE_URL = "https://api.paystack.co"

def verify_paystack_transaction(reference):
    """
    Verifies a Paystack transaction using the Secret Key.
    
    Args:
        reference (str): The transaction reference ID.
        
    Returns:
        tuple: (bool success, dict response_data)
    """
    secret_key = current_app.config.get('PAYSTACK_SECRET_KEY')
    
    if not secret_key:
        print("ERROR: PAYSTACK_SECRET_KEY is missing from configuration.")
        return False, {"message": "Server configuration error."}

    url = f"{PAYSTACK_API_BASE_URL}/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        # Paystack specific success check
        if data.get('status') and data.get('data', {}).get('status') == 'success':
            return True, data['data']
        else:
            return False, data.get('data', {})

    except requests.exceptions.RequestException as e:
        print(f"Paystack verification request failed: {e}")
        return False, {"message": f"Network error during verification: {str(e)}"}
    except Exception as e:
        print(f"An unexpected error occurred during Paystack verification: {e}")
        return False, {"message": f"Unexpected verification error: {str(e)}"}