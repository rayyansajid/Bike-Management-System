from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
import logging, random, string
from .models import *
from django.db import transaction
from django.contrib import messages
import datetime, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        pswd = request.POST['password']
        user = authenticate(username=username, password=pswd)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)                              #IDHAR AAO
            #fetch dashboard data for dashboard.html
            return redirect('Show Dashboard')
        else:
            # If not, return to login page again
            messages.error(request, "Incorrect username and/or password.")
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("homepage")

@transaction.atomic
def payorder(request):
    context = {}
    context['Logistics'] = Logistics.objects.all()
    context['Products'] = Product.objects.all()
    if request.method == 'POST':
        clientname = request.POST['name']
        contactnum = request.POST['contactnum']
        company = request.POST['company']
        instructions = request.POST['instructions']
        address = request.POST['address']
        city = request.POST['city']
        email = request.POST['email']
        client = Client(Name = clientname,
                        Contact_Num = contactnum,
                        Company = company,
                        Email = email,
                        Address = address)
        package = Package(City = city,
                          Client = client,
                          Instructions = instructions,
                          Status = "Pending",       #send email to client
                          Num_of_Boxes = 0)  
        client.save()
        package.save()
        selected_products = request.POST.getlist('productList')
        print(selected_products)
        for prodID in selected_products:
            product = Product.objects.get(id = prodID)
            print(product)
            associatedproduct = AssociatedProducts(Quantity = request.POST[f'Quantity{prodID}'])
            associatedproduct.save()
            associatedproduct.Product.add(product)
            package.associatedproducts_set.add(associatedproduct)
            print('associatedproduct: ',associatedproduct)
            print(f'package.associatedproducts_set: {package.associatedproducts_set}')
        context['PackID'] = package.id
        subject = "Order Received - Bike Traders"
        english_content = f'''Dear Mr. {clientname}, Your Pay order have received and we started preparing and
                            packing your order. Your Order ID is {package.id}.
                            Please confirm your preferred logistics service to ship your order on our WhatsApp mentioned
                            below.
                            Thank you for your purchase, looking forward to have long term relations with you.'''
        urdu_content= f"محترم جناب {clientname}، آپ کا پے آرڈر موصول ہو گیا ہے اور ہم نے آپ کے آرڈر کی تیاری اور پیکنگ شروع کر دی ہے۔ آپ کی آرڈر آئی ڈی {package.id} ہے۔ براہ کرم ذیل میں بیان کردہ ہمارے واٹس ایپ نمبر پر اپنی ترجیحی لاجسٹک سروس کی تصدیق کریں۔ آپ کی خریداری کے لئے آپ کا شکریہ، آپ کے ساتھ طویل مدتی تعلقات کے منتظر ہیں۔"
        EmailAlertToCustomer(subject, 
                    english_content,
                    urdu_content, 
                    email)
        #TODO: Send notification email to Admin
        #EmailAlertToAdmin(subject, 
                    # english_content,
                    # urdu_content, 
                    # email)
        return render(request, 'success.html', context)
    return render(request, 'payorder.html', context)

def ReceiveIt(request):
    print('IN RECEIVEIT VIEW:')
    if request.method == 'POST':
        PackID = request.POST['packageID']
        NameOfReceiver = request.POST['name']
        print(f'{PackID}, {NameOfReceiver}')
        receiver = request.POST['receiver']
        print(receiver)
        try:
            package = Package.objects.get(id = PackID)
            if receiver == "customer":
                context = {}
                today = datetime.date.today()
                print(today)
                package.DeliveryDate = today
                package.Receivername = NameOfReceiver
                package.Status = 'Delivered'
                package.save()
                subject = f"Order No. {package.id} Delivered - Bike Traders"
                english_content = f'''Dear Mr. {package.Client.Name}, Your Order status is Delivered and received by Mr.
                                    {NameOfReceiver}. Thank you For Your Purchase with Bike Traders.
                                    We hope that you are really satisfied with the products, also looking forward to have more
                                    deals with you.'''
                urdu_content = f'''آپ کا آرڈر مکمل طور پر ڈیلیور ہوگیا ہے اور {NameOfReceiver} نے اسے وصول کر لیا ہے۔ Bike Traders کے ساتھ آپ کی خریداری کا شکریہ۔

ہمیں امید ہے کہ آپ ہماری مصنوعات سے مکمل طور پر مطمئن ہوں گے، اور ہم آئندہ بھی آپ کے ساتھ مزید خریداری کے منتظر ہیں۔'''
                EmailAlertToCustomer(subject,
                                     english_content,
                                     urdu_content,
                                    package.Client.Email)
                #TODO: Send notification email to Bike
                #EmailAlertToAdmin(subject, 
                    # english_content,
                    # urdu_content, 
                    # email)
                return render(request, 'deliverysuccess.html', context)
            package.Status = "On The Way"
            subject = f"Order No. {package.id} Update - Bike Traders"
            english_content = f'''Dear Mr. {package.Client.Name}, Your Order status is On the Way and received by Mr.
                                {NameOfReceiver} from {package.Logistics.Name} with Builty#{request.POST['builtyNumber']}, and Inshallah it will be
                                delivered to you in 3 to 4 working days.
                                Please Scan the QR code on boxes to confirm their receiving, Your Order ID is {package.id}.'''
            urdu_content = f'''محترم جناب  {package.Client.Name} ، آپ کا آرڈر آپکی بتائی گئی لوجسٹکس کمپنی {package.Logistics.Name} سے {NameOfReceiver} نے وصول کر لیا ہے اور آپکی طرف روانہ کر دیا ہے جو آپکو 3 سے 4 کام کے دنوں میں پہنچا دیا جائیگا .
براہ کرم اپنے آرڈر کو وصول کرنے کی تصدیق کے لیے باکسز پر موجود QR کوڈ اسکین کریں۔ آپ کا آرڈر آئی ڈی ہے {package.id} اور آپ کا بلٹی نمبر {request.POST['builtyNumber']} ہے۔ 
ہمارے ساتھ تعاون کرنے کا شکریہ۔'''
            EmailAlertToCustomer(subject,
                                 english_content,
                                 urdu_content,
                                 package.Client.Email)
            
            #TODO: Send notification email to Admin
            #EmailAlertToBike(subject, 
                    # english_content,
                    # urdu_content, 
                    # email)
            package.save()
            context = {"PackID" : package.id}
            return render(request, "success.html", context)
            
        except Package.DoesNotExist:
            context={}
            messages.error(request, f"pkg#{PackID} not found")
            return render(request, 'receiveportal.html', context)
    return render(request, 'receiveportal.html')

def PackageDetails(request, package_id):
    context = {}
    package = Package.objects.get(id = package_id)
    associated_products = package.associatedproducts_set.all()
    print(associated_products)
    products_info = []
    for assprods in associated_products:
        print(f"assprods: {assprods}")
        print(f"assprods.Products.all(): {assprods.Product.all()}")
        for product in assprods.Product.all():
            quantity = assprods.Quantity  # Access the quantity
            print(f"product: {product}")
            # Create a dictionary to store product information
            product_info = {
                "id": product.id,
                "Name": product.Name,
                "Bike_Type": product.Bike_Type,
                "Quantity": quantity  # Include the quantity in the dictionary
            }
            print(product_info)
            products_info.append(product_info)
            print(products_info)
            print()
    context['Package'] = package
    context['AssociatedProducts'] = products_info
    return render(request, 'package_details.html', context)

def AllPackages(request):
    context = {}
    context['Packages'] = Package.objects.all().order_by('-id')
    return render(request, 'Allpackages.html', context)

def AllProducts(request):
    context = {}
    context['Products'] = Product.objects.all().order_by('-id')
    return render(request, 'AllProducts.html', context)

def AllLogistics(request):
    context = {}
    context['Logistics'] = Logistics.objects.all().order_by('-id')
    return render(request, 'AllLogistics.html', context)

def DispatchPack(request, package_id):
    package = Package.objects.get(id = package_id) #into if
    if request.method == 'POST':
        print(request.POST)
        package.Num_of_Boxes = request.POST['NumOfBoxes']
        package.Logistics = Logistics.objects.get(id = request.POST['deliveringlogistic'])
        package.Status = "Dispatched"
        package.save()
        subject = f"Order No {package.id} Dispatched - Bike Traders"
        english_content = f'''Dear Mr.{package.Client.Name}, your Order has been dispatched from our warehouse and handed
over to your desired logistics service {package.Logistics.Name}.
Your Order ID is {package_id}'''
        urdu_content = f'''محترم جناب {package.Client.Name} آپ کا آرڈر ہمارے گودام سے بھیج دیا گیا ہے اور آپ کی بتائی گئی لوجسٹکس کمپنی {package.Logistics.Name} کو دیدیا گیا ہے ، آپکا آرڈر نمبر {package.id} ہے .

مزید معلومات کے لیے آپ نیچے دیئے گئے واٹس ایپ نمبر پہ رابطہ کر سکتے ہیں .
شکریہ'''
        EmailAlertToCustomer(subject,
                     english_content,
                     urdu_content, 
                     package.Client.Email)
        #TODO: Send notification email to Admin
        #EmailAlertToAdmin(subject, 
                    # english_content,
                    # urdu_content, 
                    # email)
        context = {
            'Package' : package,
            'NumOfBoxes' : package.Num_of_Boxes
        }
        return render(request, 'QRcode.html', context)
    context = {'Package':package,
               'Logistics': Logistics.objects.all()}
    return render(request, 'dispatchpack.html', context)
    
    
def AddProduct(request):
    if request.method == 'POST':
        prodname = request.POST['name']
        biketype = request.POST['biketype']
        rate = request.POST['rate']
        product = Product(Name = prodname,
                          Rate = rate,
                          Bike_Type = biketype)
        product.save()
        return redirect('Show Dashboard')
    return render(request, "AddProduct.html")

def AddLogistics(request):
    if request.method == 'POST':
        logname = request.POST['name']
        contactnum = request.POST['contactnum']
        email = request.POST['email']
        address = request.POST['address']
        contact_prsn = request.POST['Contact_prsn']
        logistic = Logistics(Name = logname,
                             Contact_Num = contactnum,
                             Email = email,
                             Contact_prsn = contact_prsn,
                             Address = address)
        logistic.save()
        return redirect('Show Dashboard')
    return render(request, "AddLogistics.html")

def EditProduct(request, product_id):
    product = Product.objects.get(id = product_id)
    if request.method == 'POST':
        prodname = request.POST['name']
        biketype = request.POST['biketype']
        rate = request.POST['rate']
        product.Name = prodname
        product.Bike_Type = biketype
        product.Rate = rate
        product.save()
        return redirect('Show Dashboard')
    return render(request, 'editproduct.html',{'Product' : product})

def EditLogistics(request, logistic_id):
    logistic = Logistics.objects.get(id = logistic_id)
    if request.method == 'POST':
        logname = request.POST['name']
        contactnum = request.POST['contactnum']
        email = request.POST['email']
        address = request.POST['address']
        contact_prsn = request.POST['Contact_prsn']
        logistic.Name = logname
        logistic.Contact_Num = contactnum
        logistic.Email = email
        logistic.Contact_prsn = contact_prsn
        logistic.Address = address
        logistic.save()
        # return redirect('Show Dashboard')
        return redirect('Show Dashboard')
    return render(request, 'editlogistics.html', {'Logistic' : logistic})


##Email start

def EmailAlertToCustomer(subject, english_content, urdu_content, to):
    # Create a MIMEMultipart message
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['to'] = to

    # Sender's email address
    user = "Infuzic.tech@gmail.com"
    msg['from'] = user

    # Password (Note: Use an "App Password" for security instead of the account password)
    password = "ovdn zvzu lhlx xnhv"

    # Set the body of the email as HTML
    body_html = f"""
    <html>
        <head></head>
        <body style="font-family: 'Urdu Typesetting', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">

            <p>{english_content}</p>
            
            <hr style="border: 1px solid #ddd;">

            <p style="text-align: right; direction: rtl;">{urdu_content}</p>
            
            <p>Regards,<br>
            Admin Traders<br>
            For Any Queries,<br>
            WhatsApp: 03202085420<br>
            Email: <a href="mailto:Infuzic.tech@gmail.com">Infuzic.tech@gmail.com</a><br>
            Available Products Catalogue:<a href="https://wa.me/qr/PJQ2AQIEZOB4A1">https://wa.me/qr/PJQ2AQIEZOB4A1</a>
            </p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body_html, 'html'))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.sendmail(user, to, msg.as_string())
    server.quit()


# def EmailAlertToAdmin(subject, english_content, urdu_content, to):
#     msg = MIMEMultipart()
#     msg['subject'] = subject
#     msg['to'] = to

#     #NOTE: Use Admin's Email here
#     user = "Infuzic.tech@gmail.com"
#     msg['from'] = user

#     #NOTE: Use Admin's password here
#     password = "ovdn zvzu lhlx ****"
#     body_html = f"""
#     <html>
#         <head></head>
#         <body style="font-family: 'Urdu Typesetting', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">

#             <p>{english_content}</p>
            
#             <hr style="border: 1px solid #ddd;">

#             <p style="text-align: right; direction: rtl;">{urdu_content}</p>
            
#             <p>Regards,<br>
#             Bike Traders<br>
#             For Any Queries,<br>
#             WhatsApp: 03202085420<br>
#             Email: <a href="mailto:Infuzic.tech@gmail.com">Infuzic.tech@gmail.com</a><br>
#             Available Products Catalogue:<a href="https://wa.me/c/923202085420"> https://wa.me/c/923202085420</a>
#             </p>
#         </body>
#     </html>
#     """
#     msg.attach(MIMEText(body_html, 'html'))
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(user, password)
#     server.sendmail(user, to, msg.as_string())
#     server.quit()

def RenderDashboard(request):
    context = {}
    AllPackages = Package.objects.all().order_by('-id')[:5]
    AllLogistics = Logistics.objects.all()
    context['Packages'] = AllPackages
    context['Logistics'] = AllLogistics
    context['ProductCount'] = Product.objects.count()
    context['PackageCount'] = Package.objects.count()
    context['LogisticCount'] = Logistics.objects.count()
    return render(request, 'dashboard.html', context)

