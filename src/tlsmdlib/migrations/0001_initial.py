# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-21 03:52
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TLSMDJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_num', models.IntegerField(blank=True, null=True)),
                ('job_id', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('state', models.CharField(blank=True, choices=[(b'PROVIDER_HOME', b'PROVIDER_HOME'), (b'VISIT', b'VISIT')], db_index=True, max_length=36, null=True)),
                ('structure_id', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('header_id', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('submit_time', models.DateTimeField(blank=True, null=True)),
                ('run_time_begin', models.DateTimeField(blank=True, null=True)),
                ('run_time_end', models.DateTimeField(blank=True, null=True)),
                ('chain_sizes', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('submit_date', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('ip_address', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('email', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('user_name', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('user_comment', models.TextField(blank=True, db_index=True, max_length=2048, null=True)),
                ('private_job', models.BooleanField(default=False)),
                ('via_pdb', models.BooleanField(default=False)),
                ('pid', models.IntegerField(blank=True, null=True)),
                ('tls_model', models.CharField(blank=True, choices=[(b'ISOT', b'Isotropic'), (b'ANISO', b'Anisotropic')], db_index=True, max_length=36, null=True)),
                ('weight', models.CharField(blank=True, choices=[(b'NONE', b'NONE'), (b'IUISO', b'IUISO')], db_index=True, max_length=36, null=True)),
                ('include_atoms', models.CharField(blank=True, choices=[(b'ALL', b'ALL'), (b'MAINCHAIN', b'MAINCHAIN')], db_index=True, max_length=36, null=True)),
                ('plot_format', models.CharField(blank=True, choices=[(b'PNG', b'PNG'), (b'SVG', b'SVG')], db_index=True, max_length=36, null=True)),
                ('generate_jmol_view', models.BooleanField(default=False)),
                ('generate_jmol_animate', models.BooleanField(default=False)),
                ('generate_histogram', models.BooleanField(default=False)),
                ('cross_chain_analysis', models.BooleanField(default=False)),
                ('nparts', models.IntegerField(blank=True, null=True)),
                ('resolution', models.FloatField(blank=True, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'tlsmd_job',
            },
        ),
    ]
