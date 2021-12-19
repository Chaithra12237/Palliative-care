from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template import RequestContext
import time
import datetime

from .models import *
from .functions import *
from .forms import *
# Create your views here.

class IndexView(View):
    def get(self, request):
        try:
            user = request.user
            account = Users.objects.get(user=user)
            context={'user': user,'account': account}
        except:
            context = {}
        return render(request, 'common/index.html',context)

class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('home')
            # return HttpResponse("Logged In")
        else:
            msg=""
            return render(request,'common/login.html',{'msg':msg})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            account = Users.objects.get(user=user)
            if account.type=='service_provider'and account.approval == '2':
                msg = "Your profile is awaiting admin approval."
                return render(request,'common/login.html',{'msg':msg})
            elif account.type=='service_provider'and account.approval == '3':
                msg = "Your profile has been rejected.Sorry!"
                return render(request,'common/login.html',{'msg':msg})
            else:
                login(request, user)
                return redirect('home')
                # return HttpResponse("Logged In")
        else:
            msg = "Invalid login credentials"
            return render(request,'common/login.html',{'msg':msg})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class PasswordChangeView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated: 
            form = PasswordChangeForm(user=user)
            account = Users.objects.get(user=user)
            context = {'form': form, 'account': account}
            return render(request,'common/password_change.html',context)
        else:
            return redirect('home')  

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                msg="Password Updated successfully"
                account = Users.objects.get(user=user)
                context = {'form': form,'account': account,'msg': msg}
                return render(request,'common/password_change.html',context)
            else:
                account = Users.objects.get(user=user)
                context = {'form': form,'account': account}
                return render(request,'common/password_change.html',context)
        else:
            return redirect('home')

                
class Home(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                u = Users.objects.get(user=user)
                if u.type == 'admin':
                    return redirect('admin_dashboard')
                    # return HttpResponse("Admin Dashboard")
                elif u.type == 'service_provider':
                    # return HttpResponse("Service Provider")
                    return redirect('provider_dashboard')
                elif u.type == 'public':
                    # return HttpResponse("Public")
                    return redirect('user_dashboard')
                else:
                    return redirect('logout')
            except:
                return redirect('logout')
        else:
            return redirect('logout')


class AdminDashboard(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            providers = Users.objects.filter(type='service_provider').count()
            public = Users.objects.filter(type='public').count()
            services = Service.objects.all().count()
            review = Review.objects.all().count()
            form = AdminMessageForm()
            context = {'account': account,'providers': providers,'public': public,'services': services,'review': review,'form': form}
            return render(request, 'admin/dashboard.html', context)
        else:
            return redirect('home')

    def post(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            form = AdminMessageForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.datetime = datetime.datetime.now()
                f.save()
                sp = Users.objects.filter(type='service_provider')
                for i in sp:
                    ams = AdminMessageStatus(message=f,user=i)
                    ams.save()
                return redirect('home')
            else:
                return redirect('home')
        else:
            return redirect('home')



class AllServices(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = Service.objects.all()
            form = AddServiceForm()
            context = {'account':account,'services':services,'form':form}
            return render(request, 'admin/services.html', context)
        else:
            return redirect('home')

    def post(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = Service.objects.all()
            form = AddServiceForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.providers = 0
                f.users = 0
                f.save()
                return redirect('admin_services')
            else:
                alert="Adding service failed."
                context = {'account':account,'services':services,'form':form}
                return render(request, 'admin/services.html', context)
        else:
            return redirect('home')


class UpdateService(View):
    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            update_service_name = request.POST.get('update_service_name')
            service = Service.objects.get(id=id)
            service.category = update_service_name
            service.save()
            return redirect('admin_services')
        else:
            return redirect('home')

class DeleteService(View):
    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            service = Service.objects.get(id=id)
            service.delete()
            return redirect('admin_services')
        else:
            return redirect('home')

class UserSignup(View):
    def get(self, request):
        form = PublicUserCreationForm()
        dataform = UserSignUpForm()
        context = {'form': form,'dataform': dataform}
        return render(request,'user/signup.html',context)
    
    def post(self, request):
        form = PublicUserCreationForm(request.POST)
        dataform = UserSignUpForm(request.POST)
        if form.is_valid() and dataform.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.save()
            profile = dataform.save(commit=False)
            profile.user = user
            profile.email = user.username
            profile.type='public'
            profile.approval = '1'
            try:
                profile.save()
            except:
                user.delete()
            return redirect('login')
        else:
            context = {'form': form,'dataform': dataform}
            return render(request,'user/signup.html',context)


class ProviderSignUp(View):
    def get(self, request):
        form = PublicUserCreationForm()
        dataform = ProviderSignUpForm()
        context = {'form': form,'dataform': dataform}
        return render(request,'provider/signup.html',context)

    def post(self, request):
        form = PublicUserCreationForm(request.POST)
        dataform = ProviderSignUpForm(request.POST,request.FILES)
        if form.is_valid() and dataform.is_valid():
            user = form.save(commit=False)
            user.email = user.username
            user.save()
            profile = dataform.save(commit=False)
            profile.user = user
            profile.email = user.username
            profile.type='service_provider'
            profile.approval = '2'
            try:
                profile.save()
            except:
                user.delete()
            return redirect('login')
        else:
            context = {'form': form,'dataform': dataform}
            return render(request,'provider/signup.html',context)


class ProviderDashboard(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            review = Review.objects.filter(Q(service__user=account)| Q(product__service__user=account)).count()
            booking = Booking.objects.filter(Q(service__user=account)| Q(product__service__user=account)).count()
            service = ProviderService.objects.filter(user=account).count()
            product = SubProduct.objects.filter(service__user=account).count()
            message = AdminMessageStatus.objects.filter(user=account,status=False).count()
            context = {'account': account,'review': review,'booking': booking,'service': service,'product': product,'message': message}
            return render(request,'provider/dashboard.html',context)
        else:
            return redirect('home')

class UserDashboard(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fav = UserFavorite.objects.filter(user=account).count()
            review = Review.objects.filter(user=account).count()
            booking = Booking.objects.filter(user=account).count()
            context = {'account': account,'fav': fav,'review': review,'booking': booking}
            return render(request,'user/dashboard.html',context)
        else:
            return redirect('home')

class AvailableServices(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            name = []
            provider_service = ProviderService.objects.filter(user=account)
            for i in provider_service:
                name.append(i.service)
            services = Service.objects.exclude(category__in=name)
            print(services)       
            context = {'account': account, 'services': services}
            return render(request,'provider/available_services.html',context)
        else:
            return redirect('home')

class AddToMyService(View):
    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = Service.objects.get(id=id)
            count = request.POST.get('count')
            if count:
                pass
            else:
                count = 1
            cost = request.POST.get('cost')
            ps = ProviderService(user=account,service=service,count=count,cost=cost)
            ps.save()
            return redirect('available_services')
        else:
            return redirect('home')

class MyServices(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.filter(user=account)
            #sp = SubProduct.objects.filter(service__user=account)
            context = {'account': account,'ps': ps}
            return render(request,'provider/my_services.html',context)
        else:
            return redirect('home')

class MyProducts(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            #ps = ProviderService.objects.filter(user=account)
            sp = SubProduct.objects.filter(service__user=account)
            print (sp)
            context = {'account': account,'sp':sp}
            return render(request,'provider/my_products.html',context)
        else:
            return redirect('home')
class Product(View):
    def get(self,request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            sp = SubProduct.objects.filter(service__user=account,service=ps)
            form =  AddSubProductForm()
            context = {'account': account,'ps': ps,'sp':sp,'form': form}
            return render(request,'provider/product.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            sp = SubProduct.objects.filter(service__user=account,service=ps)
            form =  AddSubProductForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.service = ps
                if f.count:
                    pass
                else:
                    f.count = 1
                f.save()
                return redirect('product',id=id)
            else:
                context = {'account': account,'ps': ps,'sp':sp,'form': form}
                return render(request,'provider/product.html',context)
        else:
            return redirect('home')

class RemoveService(View):
    def post(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id=id)
            ps.delete()
            return redirect('my_services')
        else:
            return redirect('home')

class RemoveProduct(View):
     def get(self, request,id):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            product = SubProduct.objects.get(id=id)
            service = product.service
            product.delete()
            return redirect('product',id= service.id)
        else:
            return redirect('home')

class PublicService(View):
    def get(self, request):
        x= UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            services = ProviderService.objects.all()
            products = SubProduct.objects.all()
            context = {'account': account,'services': services,'products':products}
            return render(request, 'user/services.html',context)
        else:
            return redirect('home')


class AddToFavouriteService(View):
    def get(self, request,id):
        x= UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = ProviderService.objects.get(id=id)
            try:
                fav = UserFavorite.objects.filter(user=account,service=service)
                if fav:
                    fav.delete()
                    return redirect('user_services')
                else:
                    fav = UserFavorite(user=account,service=service)
                    fav.save()
                    return redirect('user_services')
            except:
                fav = UserFavorite(user=account,service=service)
                fav.save()
                return redirect('user_services')
        else:
            return redirect('home')

class MyFavorite(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fs = UserFavorite.objects.filter(user=account)
            context = {'account': account,'fs': fs}
            return render(request,'user/favourite.html',context)
        else:
            return redirect('home')

class WriteReview(View):
    def get(self, request,id):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fav = ProviderService.objects.get(id=id)
            form = AddReviewForm()
            context ={'account': account,'form': form}
            return render(request,'user/write_review.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            fav = ProviderService.objects.get(id=id)
            form = AddReviewForm(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.user = account
                f.service = fav
                f.datetime = datetime.datetime.now()
                f.save()
                return redirect('user_services')
        else:
            return redirect('home')

class MyReviews(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            review = Review.objects.filter(user=account)
            print(review)
            context ={'account': account,'review': review}
            return render(request,'user/myreview.html',context)
        
        
class ServiceReviews(View):
    def get(self,request,id):
        user = request.user
        if user.is_authenticated:
            account = Users.objects.get(user=user)
            ps = ProviderService.objects.get(id = id)
            review = Review.objects.filter(service = ps)
            context ={'account': account,'review' : review,'ps':ps}
            return render(request,'common/service_reviews.html',context)
        else:
            return redirect('home')

class PendingApproval(View):
    def get(self,request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            requests = Users.objects.filter(type='service_provider',approval='2')
            context = {'account': account,'requests': requests}
            return render(request,'admin/verify.html', context)
        else:
            return redirect('home')

class ApproveAccount(View):
    def post(self,request,id):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            pa = Users.objects.get(id=id)
            pa.approval = '1'
            pa.save()
            subject = "Account Approved"
            message = "Hi there!\n\nYour account with paliative care has been approved.Please proceed to login in the portal"
            to=pa.email
            MailSend(request,subject,message,to)
            return redirect('service_providers') 
        else:
            return redirect('home')  


class RejectAccount(View):
    def post(self,request,id):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            pa = Users.objects.get(id=id)
            pa.approval = '3'
            pa.save()
            subject = "Account Rejected"
            message = "Hi there!\n\nYour account with paliative care has been rejected."
            to=pa.email
            MailSend(request,subject,message,to)
            return redirect('service_providers') 
        else:
            return redirect('home')  


class ViewServiceProviders(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            sp = Users.objects.filter(type='service_provider',approval='1')
            context = {'account': account,'sp': sp}
            return render(request,'admin/service_providers.html',context)


class ViewUsers(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            sp = Users.objects.filter(type='public')
            context = {'account': account,'sp': sp}
            return render(request,'admin/public_users.html',context)
        else:
            return redirect('home')


class MyProductReview(View):
    def get(self,request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            r = Review.objects.filter(service__user = account)
            context = {'account': account,'r' : r}
            return render(request,'provider/product_review.html',context)
        else:
            return redirect('home')
            

class MyProfile(View):
    def get(self,request):
        user = request.user
        if user.is_authenticated:
            account = Users.objects.get(user=user)
            if account.type == 'admin':
                form = AdminProfileEditForm(instance=account)
            elif account.type == 'service_provider':
                form = ServiceProviderProfileEditForm(instance=account)
            else:
                form = PublicProfileEditForm(instance=account)
            picform = UpdatePic()
            context = {'form': form, 'account': account,'picform': picform}
            return render(request,'common/edit_profile.html',context)
        else:
            return redirect('logout')

    def post(self,request):
        user = request.user
        if user.is_authenticated:
            account = Users.objects.get(user=user)
            if account.type == 'admin':
                form = AdminProfileEditForm(request.POST,instance=account)
            elif account.type == 'service_provider':
                form = ServiceProviderProfileEditForm(request.POST,instance=account)
            else:
                form = PublicProfileEditForm(request.POST,instance=account)
            if form.is_valid:
                form.save()
                return redirect('home')
            else:
                context = {'form': form, 'account': account}
                return render(request,'common/edit_profile.html',context)
        else:
            return redirect('logout')

class UpdateProfilePic(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            account = Users.objects.get(user=user)
            form = UpdatePic(request.POST,request.FILES,instance=account)
            if form.is_valid:
                form.save()
                return redirect('profile')
            else:
                return redirect('profile')
        else:
            return redirect('home')

class MakeServiceBooking(View):
    def get(self, request,id):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = ProviderService.objects.get(id=id)
            context = {'account': account,'service': service}
            return render(request,'user/make_booking.html',context)
        else:
            return redirect('home')

class ApproveBooking(View):
    def get(self, request,id,tid):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            service = ProviderService.objects.get(id=id)
            dt = datetime.datetime.now()
            amt = service.cost
            booking = Booking(user=account,service=service,booking_id=tid,datetime=dt,amount_transferred=amt)
            booking.save()
            context = {'account': account, 'booking': booking,'service': service}
            return render(request,'user/booking_success.html',context)
        else:
            return redirect('home')

class MyBookings(View):
    def get(self, request):
        x = UserCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            booking = Booking.objects.filter(user=account).order_by('-datetime')
            context = {'account': account,'booking': booking}
            return render(request,'user/my_bookings.html',context)
        else:
            return redirect('home')

class Bookings(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            booking = Booking.objects.filter(Q(service__user=account)| Q(product__service__user=account)).order_by('-datetime')
            context = {'account': account,'booking': booking}
            return render(request,'provider/bookings.html',context)
        else:
            return redirect('home')


class Messages(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            message = AdminMessage.objects.all().order_by('-datetime')
            context = {'account': account,'message': message}
            return render(request,'admin/message.html', context)
        else:
            return redirect('home')

class MyMessage(View):
    def get(self, request):
        x = ProviderCheck(request)
        if x == True:
            user = request.user
            account = Users.objects.get(user=user)
            message = AdminMessageStatus.objects.filter(user=account).order_by('-message__datetime')
            for i in message:
                i.status = True
                i.save()
            context = {'account': account,'message': message}
            return render(request,'provider/message.html',context)
        else:
            return redirect('home')





            


            
            
    

           


                
            













            













                




        


        

    

