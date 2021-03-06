# Generated by Django 3.2 on 2022-01-23 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0003_merch_has_sizes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='merchandise.merch')),
            ],
            options={
                'ordering': ['added_on'],
            },
        ),
    ]
