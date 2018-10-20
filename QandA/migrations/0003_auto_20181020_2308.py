# Generated by Django 2.0.5 on 2018-10-20 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20181020_2308'),
        ('QandA', '0002_auto_20181020_2209'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AlterField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(related_name='questions', to='account.Topic'),
        ),
    ]
