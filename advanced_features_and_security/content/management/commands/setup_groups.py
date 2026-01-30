from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from content.models import Article, Comment


class Command(BaseCommand):
    help = 'Setup groups and permissions as per ALX assignment requirements'
    
    def handle(self, *args, **options):
        # Get content types for our models
        article_ct = ContentType.objects.get_for_model(Article)
        comment_ct = ContentType.objects.get_for_model(Comment)
        
        # Create groups as per assignment requirements
        groups_data = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit', 'can_delete'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete', 'can_publish'],
        }
        
        for group_name, perm_codenames in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            # Clear existing permissions
            group.permissions.clear()
            
            # Add Article permissions
            for codename in perm_codenames:
                try:
                    perm = Permission.objects.get(content_type=article_ct, codename=codename)
                    group.permissions.add(perm)
                    self.stdout.write(self.style.SUCCESS(
                        f'Added permission {codename} to group {group_name}'
                    ))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Permission {codename} not found for Article model'
                    ))
            
            # Add basic Comment permissions for Editors and Admins
            if group_name in ['Editors', 'Admins']:
                comment_perm_codenames = ['can_view', 'can_create', 'can_delete']
                for codename in comment_perm_codenames:
                    try:
                        perm = Permission.objects.get(content_type=comment_ct, codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(self.style.SUCCESS(
                            f'Added comment permission {codename} to group {group_name}'
                        ))
                    except Permission.DoesNotExist:
                        pass
        
        self.stdout.write(self.style.SUCCESS(
            'Successfully set up groups: Viewers, Editors, and Admins'
        ))
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('GROUP PERMISSIONS SUMMARY:')
        self.stdout.write('='*50)
        
        for group in Group.objects.filter(name__in=['Viewers', 'Editors', 'Admins']):
            self.stdout.write(f'\n{group.name}:')
            perms = group.permissions.all().order_by('content_type__model', 'codename')
            for perm in perms:
                self.stdout.write(f'  - {perm.content_type.app_label}.{perm.codename}')
