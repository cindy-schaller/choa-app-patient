from django.core.urlresolvers import reverse

from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Home",
                               reverse("questionnaire.views.index")))

Menu.add_item("main", MenuItem("About",
                               reverse("questionnaire.views.about")))

Menu.add_item("main", MenuItem("Questionnaire",
                               reverse("questionnaire.views.questionnaire")))

# this item will be shown to users who are not logged in
# Menu.add_item("main", MenuItem("Login",
#                                reverse('django.contrib.auth.views.login'),
#                                check=lambda request: not request.user.is_authenticated()))

# this will only be shown to logged in users and also demonstrates how to use
# a callable for the title to return a customized title for each request
# Menu.add_item("main", MenuItem(profile_title,
#                                reverse('accounts.views.profile'),
#                                check=lambda request: request.user.is_authenticated()))
