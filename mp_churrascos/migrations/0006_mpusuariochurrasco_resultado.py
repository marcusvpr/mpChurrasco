# Generated by Django 4.2.5 on 2023-10-05 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_churrascos', '0005_mpusuariochurrasco_qtdpessoas'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpusuariochurrasco',
            name='resultado',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
    ]
