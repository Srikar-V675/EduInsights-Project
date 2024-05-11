import base64

import requests


def solve_captcha(USN, imagePath):
    with open(imagePath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("ascii")
        url = "https://api.apitruecaptcha.org/one/gettext"

        data = {
            "userid": "srikarvuchiha@gmail.com",
            "apikey": "m6J3qWMwyflnyPsbvyKZ",
            "data": encoded_string,
            "tag": USN,
            "mode": "auto",
            "len_str": "6",
        }
        response = requests.post(url=url, json=data, timeout=5)
        data = response.json()
        return data["result"]
