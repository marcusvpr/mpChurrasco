# Generated by Django 4.2.5 on 2023-10-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_churrascos', '0004_mpusuariochurrasco'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpusuariochurrasco',
            name='qtdPessoas',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]
