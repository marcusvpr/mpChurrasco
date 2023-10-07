# Generated by Django 4.2.5 on 2023-10-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_churrascos', '0003_alter_mptopic_options_mptopic_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpUsuarioChurrasco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14)),
                ('cep', models.CharField(max_length=9)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]