# Generated by Django 2.2.5 on 2020-02-20 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=20)),
                ('event_name', models.CharField(max_length=20)),
                ('event_create_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.RemoveField(
            model_name='database',
            name='event_name',
        ),
        migrations.AddField(
            model_name='database',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.event'),
        ),
    ]
