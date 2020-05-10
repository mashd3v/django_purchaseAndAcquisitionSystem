# Generated by Django 2.2 on 2020-02-26 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('userModifier', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(help_text='Category Description', max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Category')),
                ('userCreator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Subcategories',
                'unique_together': {('category', 'description')},
            },
        ),
    ]
