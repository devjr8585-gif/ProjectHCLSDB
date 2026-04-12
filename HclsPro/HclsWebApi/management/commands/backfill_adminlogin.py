from django.core.management.base import BaseCommand
from HclsWebApi.models import CheckLogin
from HclsApp.repositories.django_admin_repository import DjangoAdminRepository

class Command(BaseCommand):
    help = 'Backfill AdminLogin rows from existing CheckLogin records when missing'

    def handle(self, *args, **options):
        created = 0
        skipped = 0
        repo = DjangoAdminRepository()
        for chk in CheckLogin.objects.all():
            # Check whether a corresponding AdminLogin exists by email
            existing = repo.find_checklogin_by_email(chk.email)
            # find_checklogin_by_email returns CheckLogin — check AdminLogin by email directly
            from HclsWebApi.models import AdminLogin as _AL
            if _AL.objects.filter(Email=chk.email).exists():
                skipped += 1
                continue

            try:
                repo.create_adminlogin_from_check(chk)
                created += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Failed for CheckLogin {chk.pk} ({chk.email}): {e}'))

        self.stdout.write(self.style.SUCCESS(f'Backfill complete — created={created}, skipped={skipped}'))
