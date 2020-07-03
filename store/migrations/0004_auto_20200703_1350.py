# Generated by Django 3.0.7 on 2020-07-03 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200703_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='custom_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quality',
            name='additional_info',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='recordingcompany',
            name='recording_company_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='size_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.SizeName'),
        ),
        migrations.AlterField(
            model_name='vynilaudiotype',
            name='audio_type_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
