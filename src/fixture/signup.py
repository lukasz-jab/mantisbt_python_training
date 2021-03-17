import re

class SignupHelper:
    def __init__(self, app):
        self.app = app

    def new_user(self, username, password, email):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        #wd.find_element_by_css_selector("div.main-content a[href='signup_page.php']").click()
        wd.find_element_by_css_selector("label[for='username'] input#username").send_keys(username)
        wd.find_element_by_css_selector("label[for='email-field'] input#email-field").send_keys(email)
        wd.find_element_by_css_selector("form#signup-form input[type='submit']").click()

        mail = self.app.mail.get_mail(username=username, password=password, subject="[MantisBT] Rejestracja konta")
        url = self.extract_confirmation_url(mail)
        wd.get(url)
        wd.find_element_by_css_selector("input[name='password']").send_keys(password)
        wd.find_element_by_css_selector("input[name='password_confirm']").send_keys(password)
        wd.find_element_by_css_selector("input[value='Update User']").click()

    def extract_confirmation_url(self, mail):
        return re.search("http://.*$", mail, re.MULTILINE).group(0)
