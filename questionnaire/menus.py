from django.core.urlresolvers import reverse

from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Home",
                               reverse("questionnaire.views.index"),
                               icon="home"))

Menu.add_item("main", MenuItem("Healthy Habits Questionnaire",
                               reverse("questionnaire.views.respond_hh"),
                               icon="assessment"))


Menu.add_item("main", MenuItem("WIC Questionnaire",
                               reverse("questionnaire.views.respond_wic"),
                               icon="assignment"))

Menu.add_item("main", MenuItem("Messages",
                               reverse("questionnaire.views.messages"),
                               icon="mail"))

Menu.add_item("main", MenuItem("History",
                               reverse("questionnaire.views.history"),
                               icon="history"))

Menu.add_item("main", MenuItem("About",
                               reverse("questionnaire.views.about"),
                               icon="info"))

# this item will be shown to users who are not logged in
# Menu.add_item("main", MenuItem("Login",
#                                reverse('django.contrib.auth.views.login'),
#                                check=lambda request: not request.user.is_authenticated()))

# this will only be shown to logged in users and also demonstrates how to use
# a callable for the title to return a customized title for each request
# Menu.add_item("main", MenuItem(profile_title,
#                                reverse('accounts.views.profile'),
#                                check=lambda request: request.user.is_authenticated()))
