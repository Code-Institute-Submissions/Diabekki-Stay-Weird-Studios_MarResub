# Generated by Django 3.2 on 2022-01-13 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0001_initial'),
        ('cart_checkout', '0003_alter_purchase_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to='user_profiles.userprofile'),
        ),
    ]
