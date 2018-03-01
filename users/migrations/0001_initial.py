# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-27 15:18
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userbianhao', models.IntegerField(default=0, verbose_name='\u7528\u6237\u7f16\u53f7')),
                ('nick_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u6635\u79f0')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('yue', models.DecimalField(decimal_places=4, default=0, max_digits=20, verbose_name='\u4f59\u989d')),
                ('djyue', models.DecimalField(decimal_places=4, default=0, max_digits=20, verbose_name='\u51bb\u7ed3\u4f59\u989d')),
                ('qianbao', models.CharField(blank=True, max_length=42, null=True, verbose_name='\u94b1\u5305\u5730\u5740')),
                ('jihuo', models.BooleanField(default=False, verbose_name='\u6fc0\u6d3b\u72b6\u6001')),
                ('jingyuan', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='\u7cbe\u5143')),
                ('juejin', models.DecimalField(decimal_places=4, default=0, max_digits=20, verbose_name='\u6398\u91d1\u548c')),
                ('count', models.IntegerField(default=0, verbose_name='\u72d7\u72d7\u6570\u91cf')),
                ('yaoqingrenshu', models.IntegerField(default=0, verbose_name='\u9080\u8bf7\u4eba\u6570')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ChouJiang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choujiang_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u62bd\u5956\u65f6\u95f4')),
                ('choujiang_haoma', models.IntegerField(default=0, verbose_name='\u62bd\u5956\u53f7\u7801')),
                ('choujiang_jiangpin', models.CharField(max_length=25, verbose_name='\u62bd\u5956\u5956\u54c1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='JiaoYiJiLu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jiaoyi_dog', models.IntegerField(default=0, verbose_name='\u4ea4\u6613\u4ea7\u751f\u7684\u72d7')),
                ('jiaoyi_type', models.CharField(choices=[('choujiang', '\u62bd\u5956'), ('weishi', '\u5582\u98df'), ('juejin', '\u6398\u91d1'), ('maide', '\u5356\u5f97'), ('maihua', '\u4e70\u82b1'), ('shengde', '\u751f\u5f97'), ('shenghua', '\u751f\u82b1')], max_length=25, verbose_name='\u4ea4\u6613\u7c7b\u578b')),
                ('jiaoyi_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u4ea4\u6613\u65f6\u95f4')),
                ('jiaoyi_jine', models.DecimalField(decimal_places=4, max_digits=20, verbose_name='\u4ea4\u6613\u91d1\u989d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smscode', models.CharField(max_length=6, verbose_name='\u9a8c\u8bc1\u7801')),
                ('mobile', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u9001\u65f6\u95f4')),
                ('send_type', models.CharField(choices=[('register', '\u6ce8\u518c'), ('forget', '\u5fd8\u8bb0\u5bc6\u7801')], default='register', max_length=50, verbose_name='\u53d1\u9001\u7c7b\u578b')),
            ],
            options={
                'verbose_name': '\u6ce8\u518c\u9a8c\u8bc1\u7801',
                'verbose_name_plural': '\u6ce8\u518c\u9a8c\u8bc1\u7801',
            },
        ),
        migrations.CreateModel(
            name='YaoQing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yaoqing_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u9080\u8bf7\u65f6\u95f4')),
                ('yaoqingdaouser', models.IntegerField(default=0, verbose_name='\u88ab\u9080\u8bf7\u4eba')),
                ('shifoushengxiao', models.BooleanField(default=False, verbose_name='\u662f\u5426\u751f\u6548')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='YueChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_to', models.CharField(max_length=42, verbose_name='\u6536\u6b3e\u65b9')),
                ('change_type', models.CharField(choices=[('tixian', '\u63d0\u73b0'), ('chongzhi', '\u5145\u503c'), ('zhuche', '\u6ce8\u518c')], max_length=50, verbose_name='\u4ea4\u6613\u7c7b\u578b')),
                ('change_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u4ea4\u6613\u65f6\u95f4')),
                ('change_jine', models.DecimalField(decimal_places=4, max_digits=20, verbose_name='\u4ea4\u6613\u91d1\u989d')),
                ('shifouchenggong', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6210\u529f')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u4ea4\u6613',
                'verbose_name_plural': '\u4ea4\u6613',
            },
        ),
    ]
