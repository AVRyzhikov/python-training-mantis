def test_login(app):
    app.session.loginm("administrator","root")
    assert(app.session.is_logged_in_as("administrator"))
    #assert app.session.is_logged_in_as("administrator")