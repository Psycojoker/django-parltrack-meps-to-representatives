import sys
from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify
from parltrack_meps.models import MEP
from representatives.models import Representative

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        with transaction.commit_on_success():
            Representative.objects.all().delete()

            gender_convertion_dict = {
                u"F": 1,
                u"M": 2
            }
            total = MEP.objects.count()
            for number, mep in enumerate(MEP.objects.all(), 1):
                sys.stdout.write("representatives %s/%s\r" % (number, total))
                sys.stdout.flush()
                Representative.objects.create(
                    full_name=mep.full_name,
                    first_name=mep.first_name,
                    last_name=mep.last_name,
                    gender=gender_convertion_dict.get(mep.gender, 0),
                    birth_date=mep.birth_date,
                    birth_place=mep.birth_place,
                    cv="\n".join([x.title for x in mep.cv_set.all()]),
                    remote_id=mep.ep_id,
                    slug=slugify(mep.full_name if mep.full_name else mep.first_name + " " + mep.last_name),
                )

            sys.stdout.write("\n") 
