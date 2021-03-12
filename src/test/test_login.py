def test_login(app, user):
    app.session.login(user["username"], user["password"])
    app.session.is_logged_in_as(user["username"])
    app.session.logout()
