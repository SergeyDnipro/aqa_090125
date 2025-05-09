def test_user_registration(homepage, open_page, open_registration_form, fill_registration_form,
                           send_registration_form, delete_user):
    """ Test open registration form, fill fields, send form, validate data and delete user at the end. """

    open_page()
    open_registration_form()

    fill_registration_form(
        name='Sergey',
        last_name='Sergey',
        email='serg123@test.com',
        password='Qwerty123',
        repeated_password='Qwerty123',
    )

    send_registration_form()
    delete_user()
