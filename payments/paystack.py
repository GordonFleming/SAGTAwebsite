import requests
import os
from dotenv import load_dotenv
load_dotenv()

class Paystack:
	PAYSTACK_SK = os.environ.get('PAYSTACK_SECRET_KEY')
	base_url = "https://api.paystack.co/"
	print(PAYSTACK_SK)

	def verify_payment(self, ref, *args, **kwargs):
		path = f'transaction/verify/{ref}'
		headers = {
			"Authorization": f"Bearer {self.PAYSTACK_SK}",
			"Content-Type": "application/json",
		}
		url = self.base_url + path
		response = requests.get(url, headers=headers)

		print(
			f"\n\nTransaction with ref: {ref} has a response {response} and status_code of {response.status_code}\n\n")

		if response.status_code == 200:
			response_data = response.json()
			return response_data['status'], response_data['data']

		response_data = response.json()

		return response_data['status'], response_data['message']