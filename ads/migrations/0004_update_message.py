"""
Migration 0004: Replace old Message fields with from_user/to_user/content/read.
Deletes existing test messages first (safe for dev).
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def delete_old_messages(apps, schema_editor):
    Message = apps.get_model('ads', 'Message')
    Message.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0003_add_sous_categorie'),
    ]

    operations = [
        # Purge old test messages first so we can drop/add non-null columns
        migrations.RunPython(delete_old_messages, migrations.RunPython.noop),

        # Remove old fields
        migrations.RemoveField(model_name='message', name='expediteur'),
        migrations.RemoveField(model_name='message', name='contact_nom'),
        migrations.RemoveField(model_name='message', name='contact_email'),
        migrations.RemoveField(model_name='message', name='contact_tel'),
        migrations.RemoveField(model_name='message', name='contenu'),
        migrations.RemoveField(model_name='message', name='lu'),

        # Add new fields
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(max_length=1000, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sent_messages',
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='received_messages',
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),

        # Update Meta ordering
        migrations.AlterModelOptions(
            name='message',
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]