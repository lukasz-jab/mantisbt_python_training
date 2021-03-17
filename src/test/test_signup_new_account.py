

def test_signup_new_account(app):
    username = 'user1'
    password = 'password'
    app.james.ensure_user_exist(username, password)