from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from artworks.models import Artwork
from accounts.models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from artworks.forms import ArtworkForm
from django.contrib.auth import update_session_auth_hash
from .utils import validate_signup
from orders.models import Order
from django.utils import timezone
from .forms import ArtworkReviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from artworks.models import ArtworkMessage
from django.db.models import Max
from django.db.models import Q



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()  #strip method ensures " eren " and "eren" are treated the same.
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'customer').lower()

        # validate form data using util function
        errors = validate_signup(username, email, password1, password2)
        if errors:
            messages.error(request, errors)
            return render(request, "signup.html",{
                "username": username,
                "email": email,
                "role": role
            }) 

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Create profile instance
        Profile.objects.create(user=user, role=role)

        messages.success(request, "Account Created Successfully")
        return redirect("accounts:login")

    return render(request, "signup.html")

from django.contrib.auth.models import User

def login_view(request): 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # checks if username or password is empty
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "login.html")

        # First check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username doesn't exist.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            role = user.profile.role
            
            if role == 'admin':
                return redirect('accounts:admin_dashboard')
            elif role == 'designer':
                return redirect('accounts:designer_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Username and password do not match.')

    context = {} 
    return render(request, "login.html", context)
        
def logout_view(request):
    logout(request)

    return redirect('accounts:login')


@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        messages.error(request, "Access Denied: Admin privileges required")
        return redirect('home')
    artworks = Artwork.objects.filter(status='approved')[:4]
    designers = Profile.objects.filter(role='designer').select_related('user')
    return render(request, 'accounts/admin/dashboard.html', {'artworks': artworks,'designers': designers})

@login_required
def designer_dashboard(request):
    if request.user.profile.role != 'designer':
        messages.error(request, "Access Denied: Designer privileges required")
        return redirect('home')
    artworks = Artwork.objects.filter(status='approved')[:4]
    designers = Profile.objects.filter(role='designer').select_related('user')[:6]
    return render(request, 'accounts/designer/dashboard.html', {'artworks': artworks,'designers': designers})



@login_required
def user_profile(request):
    role = request.user.profile.role
    current_time = timezone.now()
    
    # Base context
    context = {
        'user': request.user,
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'current_user': request.user.username,
    }

    if role == 'designer':
        # Designer specific data
        artworks = Artwork.objects.filter(designer=request.user).order_by('-created_at')
        received_orders = Order.objects.filter(artwork__designer=request.user).order_by('-created_at')
        
        conversations = ArtworkMessage.objects.filter(
            artwork__designer=request.user
        ).values(
            'artwork', 'sender'
        ).annotate(
            latest_message=Max('created_at')
        ).order_by('-latest_message')

        for conv in conversations:
            conv['artwork'] = Artwork.objects.get(id=conv['artwork'])
            conv['sender'] = User.objects.get(id=conv['sender'])
            conv['latest_message'] = ArtworkMessage.objects.filter(
                artwork=conv['artwork'],
                sender=conv['sender']
            ).latest('created_at')
        
        context.update({
            'artworks': artworks,
            'received_orders': received_orders,
            'conversations': conversations,
            'is_designer': True
        })
        template = 'accounts/designer/profile.html'

    elif role == 'customer':
        # Get customer's orders
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        # Get conversations where customer is either sender or receiver
        conversations = ArtworkMessage.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).values(
            'artwork', 'sender'
        ).annotate(
            latest_message=Max('created_at')
        ).order_by('-latest_message')

        # Fetch related data
        for conv in conversations:
            conv['artwork'] = Artwork.objects.get(id=conv['artwork'])
            conv['sender'] = User.objects.get(id=conv['sender'])
            # Get the latest message in the conversation regardless of sender/receiver
            conv['latest_message'] = ArtworkMessage.objects.filter(
                artwork=conv['artwork']
            ).latest('created_at')

        context.update({
            'orders': orders,
            'conversations': conversations,
            'is_customer': True
        })
        template = 'accounts/customer/profile.html'

    else:
        messages.error(request, "Access Denied: Invalid role")
        return redirect('home')

    return render(request, template, context)


@login_required
def admin_artwork_approval(request):
    user = Profile.objects.get(user=request.user)
    if user.role != 'admin':
        return redirect('home')

    pending_artworks = Artwork.objects.filter(status='pending').order_by('-created_at')
    
    approved_count = Artwork.objects.filter(status='approved').count()
    rejected_count = Artwork.objects.filter(status='rejected').count()

    context = {
        'pending_artworks': pending_artworks,
        'approved_count': approved_count,
        'rejected_count': rejected_count
    }

    return render(request, 'accounts/admin/artwork_approval.html', context)


@login_required
def manage_artists(request):
    #using annotate we fetching count of artwork of the particular user by passing the relationship
    artists = Profile.objects.filter(role='designer').select_related('user').annotate(artwork_count = Count('user__artwork'))
    return render(request, 'accounts/admin/manage_artists.html',{'artists': artists})

@login_required
def remove_artist(request, artist_id):
    artist = get_object_or_404(Profile, user_id=artist_id)
    artist.user.delete()
    messages.error(request, f"Artist '{artist.user.username}' has been removed")
    return redirect('accounts:manage_artists')

@login_required
def manage_artworks(request):
    artworks = Artwork.objects.filter(status='approved')
    return render(request,'accounts/admin/manage_artworks.html',{'artworks':artworks})

@login_required
def remove_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()
    messages.error(request, f"Artwork '{artwork.title}' has been removed")
    return redirect('accounts:manage_artworks')

@login_required
def manage_customers(request):
    customers = Profile.objects.filter(role='customer').select_related('user')
    return render(request,'accounts/admin/manage_customers.html',{'customers':customers})

@login_required
def remove_customer(request, customer_id):
    customer = get_object_or_404(Profile,user_id=customer_id)
    customer.delete()
    messages.error(request, f"Customer '{customer.user.username}' has been removed")
    return redirect('accounts:manage_customers')

@login_required
def update_artwork(request, artwork_id):
    if request.method == 'POST':
        artwork = get_object_or_404(Artwork, id=artwork_id)
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            messages.success(request, "Artwork Updated Successfully")
            return redirect('accounts:user_profile')
    else:  # display the form with the existing artwork details
        artwork = get_object_or_404(Artwork, id=artwork_id)
        form = ArtworkForm(instance=artwork)
    return render(request, 'accounts/designer/update_artwork.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    role = user.profile.role
    if request.method == 'POST':
        user = request.user
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if username:
            user.username = username
        if email:
            user.email = email

        if password and confirm_password:
            if password == confirm_password:
                user.set_password(password) #setpassword method automatically logs out the user so,
                update_session_auth_hash(request, user)  #we keep the user logged in
            else:
                messages.error(request, "Passwords do not match!")
                return redirect('accounts:update_profile')

        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('accounts:user_profile') 
 
 
    context = {
        'username': request.user.username,
        'email': request.user.email,
    }
    if role=='designer':
        template = 'accounts/designer/update_profile.html'
    else:
        template = 'accounts/customer/update_profile.html'

    return render(request, template , context)


@login_required
def approve_artwork(request, artwork_id):
    user = Profile.objects.get(user=request.user)
    if user.role != 'admin':
        return redirect('home')
    
    artwork = get_object_or_404(Artwork, id=artwork_id)
    designer_email = artwork.designer.email  # Corrected from artist to designer
    
    if request.method == 'POST':
        form = ArtworkReviewForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            # Update artwork status
            artwork.status = 'approved'
            artwork.is_approved = True
            artwork.reviewed_at = timezone.now()
            artwork.save()
            
            # Send email
            subject = f"Your artwork '{artwork.title}' has been approved"
            message = f"Congratulations! Your artwork '{artwork.title}' has been approved.\n\nReason: {reason}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [designer_email], fail_silently=False)
            
            messages.success(request, f"Artwork '{artwork.title}' has been approved and email sent")
            return redirect('accounts:admin_artwork_approval')
    else:
        form = ArtworkReviewForm()
    
    return render(request, 'accounts/review_artwork.html', {
        'form': form,
        'artwork': artwork,
        'action': 'approve'
    })

@login_required
def reject_artwork(request, artwork_id):
    user = Profile.objects.get(user=request.user)
    if user.role != 'admin':
        return redirect('home')
    
    artwork = get_object_or_404(Artwork, id=artwork_id)
    designer_email = artwork.designer.email  # Corrected from artist to designer
    
    if request.method == 'POST':
        form = ArtworkReviewForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            # Update artwork status
            artwork.status = 'rejected'
            artwork.is_approved = False
            artwork.reviewed_at = timezone.now()
            artwork.rejection_reason = reason
            artwork.save()
            
            # Send email
            subject = f"Your artwork '{artwork.title}' has been rejected"
            message = f"We regret to inform you that your artwork '{artwork.title}' has been rejected.\n\nReason: {reason}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [designer_email], fail_silently=False)
            
            messages.error(request, f"Artwork '{artwork.title}' has been rejected and email sent")
            return redirect('accounts:admin_artwork_approval')
    else:
        form = ArtworkReviewForm()
    
    return render(request, 'accounts/review_artwork.html', {
        'form': form,
        'artwork': artwork,
        'action': 'reject'
    })

@login_required
@require_POST
def approve_artwork_ajax(request):
    user = Profile.objects.get(user=request.user)
    if user.role != 'admin':
        messages.error(request, 'Unauthorized action.')
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    artwork_id = request.POST.get('artwork_id')
    reason = request.POST.get('reason')
    
    try:
        artwork = get_object_or_404(Artwork, id=artwork_id)
        designer_email = artwork.designer.email
        
        # Update artwork status
        artwork.status = 'approved'
        artwork.is_approved = True
        artwork.reviewed_at = timezone.now()
        artwork.save()
        
        # Send email
        subject = f"Your artwork '{artwork.title}' has been approved"
        message = f"Congratulations! Your artwork '{artwork.title}' has been approved.\n\nReason: {reason}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [designer_email], fail_silently=False)
        
        # Add Django message
        messages.success(request, f"Artwork '{artwork.title}' has been approved and email sent.")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Error approving artwork: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def reject_artwork_ajax(request):
    user = Profile.objects.get(user=request.user)
    if user.role != 'admin':
        messages.error(request, 'Unauthorized action.')
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    artwork_id = request.POST.get('artwork_id')
    reason = request.POST.get('reason')
    
    try:
        artwork = Artwork.objects.get(id=artwork_id)
        designer_email = artwork.designer.email
        artwork.status = 'rejected'
        artwork.rejection_reason = reason
        artwork.reviewed_at = timezone.now()
        artwork.save()

        
        # Send email
        subject = f"Your artwork '{artwork.title}' has been rejected"
        message = f"We regret to inform you that your artwork '{artwork.title}' has been rejected.\n\nReason: {reason}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [designer_email], fail_silently=False)
        
        # Add Django message
        messages.error(request, f"Artwork '{artwork.title}' has been rejected and email sent.")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Error rejecting artwork: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    
