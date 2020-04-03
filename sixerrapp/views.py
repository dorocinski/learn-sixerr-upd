from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Gig, Profile
from.forms import GigForm

import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="p7zg8s2rz6kfh7s8",
        public_key="y86dw42kgw86rzd5",
        private_key="6f3ec31cf1688cf8da66f58e0558effc"
    )
)

# Create your views here.
def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, 'home.html', {"gigs": gigs})



def gig_detail(request, id):
    #generate all other required data that you may need on the #checkout page and add them to context.
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    # Configure Braintree
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id="p7zg8s2rz6kfh7s8",
            public_key="y86dw42kgw86rzd5",
            private_key="6f3ec31cf1688cf8da66f58e0558effc"
        )
    )
    try:
        client_token = gateway.client_token.generate({"customer_id": request.user.id})
    except:
        client_token = gateway.client_token.generate({})

    context = {'client_token': client_token,"gig": gig}
    return render(request, 'gig_detail.html', context)

@login_required(login_url='/')
def create_gig(request):
    error = ''
    if request.method =='POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
            error = gig_form.errors

    gig_form = GigForm()
    return render(request, 'create_gig.html', {"error": error})


@login_required(login_url='/')
def edit_gig(request, id):
    try:
        gig = Gig.objects.get(id=id, user=request.user)
        error = ''
        if request.method =='POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error = gig_form.errors
        return render(request, 'edit_gig.html', {"gig":gig, "error": error})
    except Gig.DoesNotExist:
        return redirect('/')

@login_required(login_url='/')
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})

@login_required(login_url='/')
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return redirect('/')

    gigs = Gig.objects.filter(user=profile.user, status=True)
    return render(request, 'profile.html', {"profile": profile, "gigs": gigs})

@login_required(login_url='/')
def create_purchase(request):
    if request.method =='POST':
        try:
            gig = Gig.objects.get(id=request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('/')


        nonce = request.POST["payment_method_nonce"]

        result = gateway.transaction.sale({
            "amount": gig.price,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            print("success!: " + result.transaction.id)
        elif result.transaction:
            print("Error processing transaction:")
            print("  code: " + result.transaction.processor_response_code)
            print("  text: " + result.transaction.processor_response_text)
            return redirect('/')
        else:
            for error in result.errors.deep_errors:
                print("attribute: " + error.attribute)
                print("  code: " + error.code)
                print("  message: " + error.message)
                return redirect('/')

        if result.is_success:
            print("success!: " + result.transaction.id)
        else:
            print("Buy Gig Failed")
            return redirect('/')
