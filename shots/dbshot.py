import django
import sys

import os

sys.path.insert(0,'/Users/zhikuncheng/PycharmProjects/crawler_admin_site')

os.environ["DJANGO_SETTINGS_MODULE"]= "crawler_admin_site.settings"
django.setup()
from crawler import models

set_inf=models.TargetMP.objects.all()
for info in set_inf:
    print(info.__str__())
    print(info.name)

print(set_inf)
