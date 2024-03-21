# Generated by Django 5.0.1 on 2024-03-15 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_orderitems_status_order_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tag_objects',
            field=models.ManyToManyField(null=True, to='store.tags'),
        ),
    ]
