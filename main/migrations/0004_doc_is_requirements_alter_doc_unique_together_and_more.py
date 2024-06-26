# Generated by Django 5.0.4 on 2024-04-14 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_file_doc_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='is_requirements',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='doc',
            unique_together={('user', 'file', 'is_requirements')},
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('results', models.TextField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.doc')),
                ('requirements', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparisons', to='main.doc')),
            ],
            options={
                'unique_together': {('requirements', 'application')},
            },
        ),
    ]
