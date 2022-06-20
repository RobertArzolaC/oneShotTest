import requests


class OneShot:
    url = "https://one-shot.developers.uanataca.com/api/v1/request"
    url_otp = "https://one-shot.developers.uanataca.com/api/v1/otp/"
    url_sign_otp = "https://one-shot.developers.uanataca.com/api/v1/sign/"
    url_otp_file = "https://one-shot.developers.uanataca.com/api/v1/document/"
    url_otp_download = (
        "https://one-shot.developers.uanataca.com/api/v1/document/%s/signed/%s"
    )

    def __init__(self):
        self.payload = {
            "env": "test",
            "profile": "PFnubeNC",
            "id_document_type": "IDC",
            "id_document_country": "ES",
            "serial_number": "12345678A",
            "registration_authority": "759",
            "billing_password": "YWlkZWFydHVyMDE=",
            "billing_username": "jimysanchez@bit4id.pe",
        }
        self.headers = {"Content-Type": "application/json"}
        self.default_response = {}
        self.payload_otp = dict(options={})

    def build_payload(
        self,
        name,
        surname_1,
        surname_2,
        email,
        phone,
        username,
        password,
        code,
    ):
        self.payload["given_name"] = name
        self.payload["surname_1"] = surname_1
        self.payload["surname_2"] = surname_2
        self.payload["email"] = email
        self.payload["mobile_phone_number"] = f"+51{phone}"
        self.payload["username"] = username
        self.payload["password"] = password
        self.payload["pin"] = code

    def build_payload_otp(self, otp, document_id):
        self.payload_otp["secret"] = otp
        self.payload_otp["options"][document_id] = {
            "image": "212ace32-e411-492f-bfe7-cff296075b54",
            "position": "300, 100, 500, 150",
            "page": 0,
        }
        return self.payload_otp

    def upload_file(self, code, upload_data):
        url = f"{self.url_otp_file}{code}"
        files = {"file": upload_data.stream._file}
        response = requests.post(url, files=files)
        return response.json()

    def get_otp(self, code):
        url = f"{self.url_otp}{code}"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def send_data(self):
        response = requests.post(
            self.url, headers=self.headers, json=self.payload
        )
        if response.ok:
            return response.json()
        return self.default_response

    def send_otp(self, otp):
        url = f"{self.url_sign_otp}{otp}"
        response = requests.post(
            url, headers=self.headers, json=self.payload_otp
        )
        if response.ok:
            return response.json()
        return self.default_response

    def get_download_file_url(self, code, document_id):
        return self.url_otp_download % (code, document_id)
