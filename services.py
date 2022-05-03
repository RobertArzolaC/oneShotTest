import requests


class OneShot:
    url = "https://one-shot.developers.uanataca.com/api/v1/request"
    def __init__(self):
        self.payload = {
            'env' :  'test' ,
            'pin' :  'belorado74' ,
            'profile': 'PFnubeNC',
            'username' :  '5131463',
            'password' :  'Fk#3#N,8',
            'id_document_type': 'IDC',
            'id_document_country': 'ES',
            'serial_number': '12345678A',
            'email': 'jimy171@gmail.com',
            'registration_authority': '759',
            'billing_password' :  'YWlkZWFydHVyMDE=',
            'billing_username' :  'jimysanchez@bit4id.pe'
        }
        self.headers = {
          'Content-Type': 'application/json'
        }

    def build_payload(self, name, surname_1, surname_2, email, phone):
        self.payload['given_name'] = name
        self.payload['surname_1'] = surname_1
        self.payload['surname_2'] = surname_2
        self.payload['email'] = email
        self.payload['mobile_phone_number'] = f"+51{phone}"
        return self.payload
        
    def send_data(self):
        return requests.post(
            self.url, json=self.payload, headers=self.headers
        ).text
