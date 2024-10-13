from django.shortcuts import render, redirect
from .models import Payment, UserWallet
import os
from dotenv import load_dotenv
load_dotenv()

def initiate_payment(request):
	if request.method == "POST":
		amount = request.POST['amount']
		email = request.POST['email']

		pk = os.environ.get('PAYSTACK_PUBLIC_KEY')

		payment = Payment.objects.create(amount=amount, email=email, user=request.user)
		payment.save()

		context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
		return render(request, 'make_payment.html', context)

	return render(request, 'payment.html')


def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
		# Check if UserWallet exists for the user, create if it doesn't
		user_wallet, created = UserWallet.objects.get_or_create(user=request.user)
		
		user_wallet.balance += payment.amount
		user_wallet.save()
		print(request.user.username, " funded wallet successfully")
		return render(request, "success.html")
	return render(request, "success.html")