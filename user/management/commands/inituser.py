from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--username", type=str)
        parser.add_argument("--password", type=str)
        parser.add_argument("--action", type=str)

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        action = options["action"]

        if not (username and password and action):
            self.stdout.write(self.style.ERROR("Invalid args"))
            exit(1)

        if action == "create_super_admin":
            if User.objects.filter(is_superuser=True).exists():
                self.stdout.write(self.style.SUCCESS(f"User {username} exists, operation ignored"))
                exit()

            user = User.objects.create_superuser(username=username, password=password)
            user.save()

            self.stdout.write(self.style.SUCCESS("User created"))
        elif action == "reset":
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Password is rested"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User {username} doesnot exist, operation ignored"))
                exit(1)
        else:
            raise ValueError("Invalid action")
