import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vle_webapp.settings")

application = get_wsgi_application()

from alumnica_model.models import Learner


for user in Learner.objects.all():
    print('{0}'.format(user.auth_user.email))