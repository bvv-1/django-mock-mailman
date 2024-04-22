from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmailForm, MailingListForm
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import MailingListMember, Email
from django.urls import reverse
from django.utils.crypto import get_random_string

def home(request):
    return render(request, 'home.html')

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            sender = 'yamada-kentaro246@g.ecc.u-tokyo.ac.jp' # FIXME
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            mailing_list = MailingListMember.objects.all()
            recipient_list = [member.email for member in mailing_list]
            
            send_mail(subject=subject, message=message, from_email=sender, recipient_list=recipient_list) # FIXME: Change to BCC using EmailMessage class

            email = Email.objects.create(subject=subject, sender=sender, body=message)
            email.save()

            return HttpResponse('Email sent')
    else:
        form = EmailForm()
    return render(request, 'email_form.html', {'form': form})

def mailing_list_members(request):
    members = MailingListMember.objects.all()
    return render(request, 'mailing_list_members.html', {'members': members})

def email_list(request):
    emails = Email.objects.all()
    return render(request, 'email_list.html', {'emails': emails})

def email_detail(request, mail_id):
    email = get_object_or_404(Email, pk=mail_id)
    return render(request, 'email_detail.html', {'email': email})

def delete_email(request, mail_id):
    email = get_object_or_404(Email, pk=mail_id)
    email.delete()
    return redirect('mails')

def subscribe(request):
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # マジックリンクの生成
            token = get_random_string(32)
            confirm_url = request.build_absolute_uri(
                reverse('confirm_subscription', args=[token])
            )
            
            # メールの送信
            subject = 'メーリングリスト登録確認'
            message = f'このリンクをクリックして登録を完了してください: {confirm_url}'
            sender = 'noreply@gmail.com'
            send_mail(subject=subject, message=message, from_email=sender, recipient_list=[email])
            
            # 一時的にメールアドレスを保存する
            # (後で本登録時に永続化する)
            request.session['pending_email'] = email
            request.session['subscribe_token'] = token
            
            return HttpResponse('確認メールを送信しました')
    else:
        form = MailingListForm()
    return render(request, 'subscribe_form.html', {'form': form})

def confirm_subscription(request, token):
    email = request.session.get('pending_email')
    saved_token = request.session.get('subscribe_token')

    if email and saved_token and saved_token == token:
        # メールアドレスを永続化する
        mailing_list, is_created = MailingListMember.objects.get_or_create(email=email)
        
        # セッションからデータを削除する
        del request.session['pending_email']
        del request.session['subscribe_token']
        
        return HttpResponse('登録が完了しました')
    else:
        # 無効なリンクの場合
        return HttpResponse('無効なリンクです')

def unsubscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            token = get_random_string(32)
            confirm_url = request.build_absolute_uri(
                reverse('confirm_unsubscription', args=[token])
            )

            subject = 'メーリングリスト解除確認'
            message = f'このリンクをクリックして登録を解除してください: {confirm_url}'
            sender = 'noreply@gmail.com'
            send_mail(subject=subject, message=message, from_email=sender, recipient_list=[email])

            request.session['pending_email'] = email
            request.session['unsubscribe_token'] = token

            return HttpResponse('確認メールを送信しました')
    else:
        form = MailingListForm()
    return render(request, 'unsubscribe_form.html', {'form': form})

def confirm_unsubscription(request, token):
    email = request.session.get('pending_email')
    saved_token = request.session.get('unsubscribe_token')

    if email and saved_token and saved_token == token:
        MailingListMember.objects.filter(email=email).delete()
        
        del request.session['pending_email']
        del request.session['unsubscribe_token']
        
        return HttpResponse('解除が完了しました')
    else:
        return HttpResponse('無効なリンクです')

