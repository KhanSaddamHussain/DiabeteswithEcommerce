# Generated by Django 3.1.1 on 2020-12-04 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_discription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='state',
            new_name='zip_add',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='zip_added',
        ),
    ]
