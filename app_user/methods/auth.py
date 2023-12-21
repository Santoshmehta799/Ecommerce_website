


def admin_register_methods(request,form):
    pass
    # # fatch form and clean
    # password = form.cleaned_data.get('password')
    # email = form.cleaned_data.get('email').lower()
    # account_type = 1

    # # creating user
    # user = User.objects.create_user(
    #     username=email,
    #     email=email,
    #     password=password,
    #     is_active = False
    # )
    # print('1. user created')

    # # user credentials
    # user_credentails = models.auth.UserCredentails(
    #         user = user,
    #         account_type = account_type
    #     )
    # user_credentails.save()

 
    # #Send Registration mail configrations
    # mail_subject = 'Activate your account.'
    # mail_subject1 = 'Initial registration of ' + user.first_name + ' ' + user.last_name + f' done on {settings.STORE_NAME}.'
    # current_site = get_current_site(request)
    # template_path = f'{settings.FOLDER_PATH}/mail/initial-admin-registration.html'
    # admin_template_path = f'{settings.FOLDER_PATH}/mail/user-registration-details.html'
    # user = user
    # account_type = user_credentails.account_type
    # account_type = enums.AccountType(account_type).name
    # mail_favicon_img = MAIL_FAVICON_ICON, 
    # mail_company_img = MAIL_COMPANY_ICON,
    # print('3. before sending the user mail')
    # methods.auth.send_registration_mail(
    #     mail_subject,mail_subject1,
    #     current_site,
    #     template_path,admin_template_path,
    #     user,account_type,
    #     mail_favicon_img,mail_company_img
    # )