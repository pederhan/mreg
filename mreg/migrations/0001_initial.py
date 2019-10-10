# Generated by Django 2.2.6 on 2019-10-10 10:25

import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mreg.fields
import mreg.models
import mreg.utils
import mreg.validators
import netfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwardZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated', models.BooleanField(default=True)),
                ('primary_ns', mreg.fields.DnsNameField(max_length=253, validators=[mreg.validators.validate_hostname])),
                ('email', django.contrib.postgres.fields.citext.CIEmailField(max_length=254)),
                ('serialno', models.BigIntegerField(default=mreg.utils.create_serialno, validators=[mreg.validators.validate_32bit_uint])),
                ('serialno_updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('refresh', models.IntegerField(default=10800)),
                ('retry', models.IntegerField(default=3600)),
                ('expire', models.IntegerField(default=1814400)),
                ('soa_ttl', models.IntegerField(default=43200, validators=[mreg.validators.validate_ttl])),
                ('default_ttl', models.IntegerField(default=43200, validators=[mreg.validators.validate_ttl])),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
            ],
            options={
                'db_table': 'forward_zone',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('contact', django.contrib.postgres.fields.citext.CIEmailField(blank=True, max_length=254)),
                ('ttl', models.IntegerField(blank=True, null=True, validators=[mreg.validators.validate_ttl])),
                ('comment', models.TextField(blank=True)),
                ('zone', models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.ForwardZone')),
            ],
            options={
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='ModelChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=132)),
                ('table_row', models.BigIntegerField()),
                ('data', models.TextField()),
                ('action', models.CharField(max_length=16)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'model_change_log',
            },
        ),
        migrations.CreateModel(
            name='NameServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('ttl', models.IntegerField(blank=True, null=True, validators=[mreg.validators.validate_ttl])),
            ],
            options={
                'db_table': 'ns',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', netfields.fields.CidrAddressField(max_length=43, unique=True)),
                ('description', models.TextField(blank=True)),
                ('vlan', models.IntegerField(blank=True, null=True)),
                ('dns_delegated', models.BooleanField(default=False)),
                ('category', models.TextField(blank=True)),
                ('location', models.TextField(blank=True)),
                ('frozen', models.BooleanField(default=False)),
                ('reserved', models.PositiveIntegerField(default=3)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'network',
                'ordering': ('network',),
            },
        ),
        migrations.CreateModel(
            name='ReverseZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated', models.BooleanField(default=True)),
                ('primary_ns', mreg.fields.DnsNameField(max_length=253, validators=[mreg.validators.validate_hostname])),
                ('email', django.contrib.postgres.fields.citext.CIEmailField(max_length=254)),
                ('serialno', models.BigIntegerField(default=mreg.utils.create_serialno, validators=[mreg.validators.validate_32bit_uint])),
                ('serialno_updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('refresh', models.IntegerField(default=10800)),
                ('retry', models.IntegerField(default=3600)),
                ('expire', models.IntegerField(default=1814400)),
                ('soa_ttl', models.IntegerField(default=43200, validators=[mreg.validators.validate_ttl])),
                ('default_ttl', models.IntegerField(default=43200, validators=[mreg.validators.validate_ttl])),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_reverse_zone_name])),
                ('network', netfields.fields.CidrAddressField(blank=True, max_length=43, unique=True)),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
            ],
            options={
                'db_table': 'reverse_zone',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
        migrations.CreateModel(
            name='Hinfo',
            fields=[
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mreg.Host')),
                ('cpu', models.TextField()),
                ('os', models.TextField()),
            ],
            options={
                'db_table': 'hinfo',
            },
        ),
        migrations.CreateModel(
            name='Loc',
            fields=[
                ('host', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mreg.Host')),
                ('loc', models.TextField(validators=[mreg.validators.validate_loc])),
            ],
            options={
                'db_table': 'loc',
            },
        ),
        migrations.CreateModel(
            name='ReverseZoneDelegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_reverse_zone_name])),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
                ('zone', models.ForeignKey(db_column='zone', on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='mreg.ReverseZone')),
            ],
            options={
                'db_table': 'reverse_zone_delegation',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
        migrations.CreateModel(
            name='PtrOverride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(unique=True)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='ptr_overrides', to='mreg.Host')),
            ],
            options={
                'db_table': 'ptr_override',
            },
        ),
        migrations.CreateModel(
            name='NetGroupRegexPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=80)),
                ('range', netfields.fields.CidrAddressField(max_length=43)),
                ('regex', models.CharField(max_length=250, validators=[mreg.validators.validate_regex])),
            ],
            options={
                'db_table': 'perm_net_group_regex',
                'unique_together': {('group', 'range', 'regex')},
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.LCICharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hosts', models.ManyToManyField(related_name='hostgroups', to='mreg.Host')),
                ('owners', models.ManyToManyField(blank=True, to='auth.Group')),
                ('parent', models.ManyToManyField(blank=True, related_name='groups', to='mreg.HostGroup')),
            ],
            options={
                'db_table': 'hostgroup',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ForwardZoneDelegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
                ('zone', models.ForeignKey(db_column='zone', on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='mreg.ForwardZone')),
            ],
            options={
                'db_table': 'forward_zone_delegation',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
        migrations.AddField(
            model_name='forwardzone',
            name='nameservers',
            field=models.ManyToManyField(db_column='ns', to='mreg.NameServer'),
        ),
        migrations.CreateModel(
            name='Cname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.DnsNameField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('ttl', models.IntegerField(blank=True, null=True, validators=[mreg.validators.validate_ttl])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='cnames', to='mreg.Host')),
                ('zone', models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.ForwardZone')),
            ],
            options={
                'db_table': 'cname',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Txt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.TextField(max_length=255)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='txts', to='mreg.Host')),
            ],
            options={
                'db_table': 'txt',
                'unique_together': {('host', 'txt')},
            },
        ),
        migrations.CreateModel(
            name='Sshfp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttl', models.IntegerField(blank=True, null=True, validators=[mreg.validators.validate_ttl])),
                ('algorithm', models.IntegerField(choices=[(1, 'RSA'), (2, 'DSS'), (3, 'ECDSA'), (4, 'Ed25519')])),
                ('hash_type', models.IntegerField(choices=[(1, 'SHA-1'), (2, 'SHA-256')])),
                ('fingerprint', models.CharField(max_length=64, validators=[mreg.validators.validate_hexadecimal])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, to='mreg.Host')),
            ],
            options={
                'db_table': 'sshfp',
                'unique_together': {('host', 'algorithm', 'hash_type', 'fingerprint')},
            },
        ),
        migrations.CreateModel(
            name='Srv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', mreg.fields.LCICharField(max_length=255, validators=[mreg.validators.validate_srv_service_text])),
                ('priority', models.IntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('weight', models.IntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('port', models.IntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('ttl', models.IntegerField(blank=True, null=True, validators=[mreg.validators.validate_ttl])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='srvs', to='mreg.Host')),
                ('zone', models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.ForwardZone')),
            ],
            options={
                'db_table': 'srv',
                'ordering': ('name', 'priority', 'weight', 'port', 'host'),
                'unique_together': {('name', 'priority', 'weight', 'port', 'host')},
            },
        ),
        migrations.CreateModel(
            name='Naptr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.IntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('order', models.IntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('flag', models.CharField(blank=True, max_length=1, validators=[mreg.validators.validate_naptr_flag])),
                ('service', mreg.fields.LCICharField(blank=True, max_length=128)),
                ('regex', models.CharField(blank=True, max_length=128)),
                ('replacement', mreg.fields.LCICharField(max_length=255)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='naptrs', to='mreg.Host')),
            ],
            options={
                'db_table': 'naptr',
                'ordering': ('preference', 'order', 'flag', 'service', 'regex', 'replacement'),
                'unique_together': {('host', 'preference', 'order', 'flag', 'service', 'regex', 'replacement')},
            },
        ),
        migrations.CreateModel(
            name='Mx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('mx', mreg.fields.DnsNameField(max_length=253, validators=[mreg.validators.validate_hostname])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='mxs', to='mreg.Host')),
            ],
            options={
                'db_table': 'mx',
                'unique_together': {('host', 'priority', 'mx')},
            },
        ),
        migrations.CreateModel(
            name='Ipaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField()),
                ('macaddress', models.CharField(blank=True, max_length=17, validators=[mreg.validators.validate_mac_address])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='ipaddresses', to='mreg.Host')),
            ],
            options={
                'db_table': 'ipaddress',
                'unique_together': {('host', 'ipaddress')},
            },
        ),
    ]
