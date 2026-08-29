import requests

def get_facebook_page_info() -> str:
    from configs import Config

    url = f"https://graph.facebook.com/v19.0/me?access_token={Config.FACEBOOK_PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data.get("id", "")