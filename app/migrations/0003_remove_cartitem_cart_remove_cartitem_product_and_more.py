# Generated by Django 4.2.3 on 2023-07-10 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]