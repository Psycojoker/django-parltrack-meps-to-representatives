import sys
from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify
from parltrack_meps.models import MEP, CommitteeRole, DelegationRole, GroupMEP, OrganizationMEP, CountryMEP
from representatives.models import Mandate, Representative

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

            Mandate.objects.all().delete()

            total = CommitteeRole.objects.count()
            for number, committee in enumerate(CommitteeRole.objects.all(), 1):
                sys.stdout.write("committees %s/%s\r" % (number, total))
                sys.stdout.flush()
                Mandate.objects.create(
                    name=committee.committee.name,
                    kind="committee",
                    constituency="European Parliament",
                    role=committee.role,
                    begin_date=committee.begin,
                    end_date=committee.end,
                    active=True,
                    short_id=committee.committee.abbreviation,
                    representative=Representative.objects.get(remote_id=committee.mep.ep_id),
                )
            sys.stdout.write("\n")

            total = DelegationRole.objects.count()
            for number, delegation in enumerate(DelegationRole.objects.all(), 1):
                sys.stdout.write("delegations %s/%s\r" % (number, total))
                sys.stdout.flush()
                Mandate.objects.create(
                    name=delegation.delegation.name,
                    kind="delegation",
                    constituency="European Parliament",
                    role=delegation.role,
                    begin_date=delegation.begin,
                    end_date=delegation.end,
                    active=True,
                    representative=Representative.objects.get(remote_id=delegation.mep.ep_id),
                )
            sys.stdout.write("\n")

            total = GroupMEP.objects.count()
            for number, group in enumerate(GroupMEP.objects.all(), 1):
                sys.stdout.write("groups %s/%s\r" % (number, total))
                sys.stdout.flush()
                Mandate.objects.create(
                    name=group.group.name,
                    kind="group",
                    constituency="European Parliament",
                    role=group.role,
                    begin_date=group.begin,
                    end_date=group.end,
                    active=True,
                    short_id=group.group.abbreviation,
                    representative=Representative.objects.get(remote_id=group.mep.ep_id),
                )
            sys.stdout.write("\n")

            total = OrganizationMEP.objects.count()
            for number, organization in enumerate(OrganizationMEP.objects.all(), 1):
                sys.stdout.write("organizations %s/%s\r" % (number, total))
                sys.stdout.flush()
                Mandate.objects.create(
                    name=organization.organization.name,
                    kind="organization",
                    constituency="European Parliament",
                    role=organization.role,
                    begin_date=organization.begin,
                    end_date=organization.end,
                    active=True,
                    representative=Representative.objects.get(remote_id=organization.mep.ep_id),
                )
            sys.stdout.write("\n")

            total = CountryMEP.objects.count()
            for number, country in enumerate(CountryMEP.objects.all(), 1):
                sys.stdout.write("countries %s/%s\r" % (number, total))
                sys.stdout.flush()
                Mandate.objects.create(
                    name=country.country.name,
                    kind="country",
                    constituency=country.party.name,
                    begin_date=country.begin,
                    end_date=country.end,
                    active=True,
                    short_id=country.country.code,
                    representative=Representative.objects.get(remote_id=country.mep.ep_id),
                )
            sys.stdout.write("\n")
