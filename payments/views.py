from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.contrib.auth.models import Group
import os
from dotenv import load_dotenv
load_dotenv()

def initiate_payment(request):
	if request.method == "POST":
		membership_type = request.POST['membership_type']
		email = request.POST['email']
		
        # For student and retired
		amount = 260
	    # Logic for different payment amounts based on membership type
		if membership_type == "individual":
			amount = 520
		elif membership_type == "corporate_institutional":
			amount = 2370
        
		pk = os.environ.get('PAYSTACK_PUBLIC_KEY')

		payment = Payment.objects.create(amount=amount, email=email, user=request.user)
		payment.save()

		context = {
			'payment': payment,
			'field_values': request.POST,
			'paystack_pub_key': pk,
			'amount_value': payment.amount_value(),
		}
		return render(request, 'payments/make_payment.html', context)

	return render(request, 'payments/payment.html')


def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()
	user = request.user

	if verified:
		# Check if UserWallet exists for the user, create if it doesn't
		user_wallet, created = UserWallet.objects.get_or_create(user=user)
		
		user_wallet.balance += payment.amount
		user_wallet.save()
		
        # Add the user to the members user group
		group = Group.objects.get(name='Members')
		user.groups.add(group)
		user.save()
	
		print(request.user.username, " funded wallet successfully")
		return render(request, "payments/success.html")
	return render(request, "payments/success.html")