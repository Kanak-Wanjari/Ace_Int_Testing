import requests

def test_successful_login():
    url = "https://www.bootcoding.in/codelab/api/v1/auth/signin"

    data = {
        "email": "wanjarikanak@gmail.com",
        "password": "Kanak@1234"
    }

    response = requests.post(url, json=data)

    assert response.status_code == 201
    # assert "token" in response.json()
    json_data = response.json()
    assert json_data["status"] == "success"