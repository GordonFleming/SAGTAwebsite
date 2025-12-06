import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from member.models import Member

from .models import Payment, UserWallet

load_dotenv()


@login_required
def initiate_payment(request):
    if request.method == "POST":
        membership_type = request.POST["membership_type"]
        email = request.POST["email"]

        # For student and retired
        amount = 300
        # Logic for different payment amounts based on membership type
        if membership_type == "individual":
            amount = 600
        elif membership_type == "corporate_institutional":
            amount = 2560

        pk = os.environ.get("PAYSTACK_PUBLIC_KEY")

        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            "payment": payment,
            "field_values": request.POST,
            "paystack_pub_key": pk,
            "amount_value": payment.amount_value(),
            "membership_type": membership_type,
        }
        return render(request, "payments/make_payment.html", context)

    return render(request, "payments/payment.html")


@login_required
def verify_payment(request, ref, membership_type):
    print(request)
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()
    user = request.user
    if not membership_type:
        return HttpResponseBadRequest("Membership type is missing.")

    if verified:
        # Check if UserWallet exists for the user, create if it doesn't
        user_wallet, created = UserWallet.objects.get_or_create(user=user)

        total_amount = (
            Payment.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )
        if user_wallet.balance < total_amount:
            user_wallet.balance += payment.amount

        user_wallet.save()
        member, created = Member.objects.get_or_create(user=user)
        member.membership_type = membership_type
        member.save()

        # Add the user to the members user group
        group = Group.objects.get(name="Members")
        user.groups.add(group)
        user.save()

        print(request.user.username, " funded wallet successfully")
        return render(request, "payments/success.html")
    return render(request, "payments/success.html")
