# Generated by Django 4.2 on 2023-05-04 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_comment_blog_commen_created_0e6ed4_idx'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='emial',
            new_name='email',
        ),
    ]