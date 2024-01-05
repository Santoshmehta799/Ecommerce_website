# Generated by Django 5.0 on 2024-01-05 06:27

import common.helpers
import common.validators
import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TempPhoneVerified',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('country', models.CharField(choices=[('AF', 'Afghanistan +93'), ('AL', 'Albania +355'), ('DZ', 'Algeria +213'), ('AS', 'American Samoa +1'), ('AD', 'Andorra +376'), ('AO', 'Angola +244'), ('AG', 'Antigua &amp; Barbuda +1'), ('AR', 'Argentina +54'), ('AM', 'Armenia +374'), ('AW', 'Aruba +297'), ('AU', 'Australia +61'), ('AT', 'Austria +43'), ('AZ', 'Azerbaijan +994'), ('BS', 'Bahamas +1'), ('BH', 'Bahrain +973'), ('BD', 'Bangladesh +880'), ('BB', 'Barbados +1'), ('BY', 'Belarus +375'), ('BE', 'Belgium +32'), ('BZ', 'Belize +501'), ('BJ', 'Benin +229'), ('BM', 'Bermuda +1'), ('BT', 'Bhutan +975'), ('BO', 'Bolivia +591'), ('BA', 'Bosnia &amp; Herzegovina +387'), ('BW', 'Botswana +267'), ('BR', 'Brazil +55'), ('VG', 'British Virgin Islands +1'), ('BN', 'Brunei +673'), ('BG', 'Bulgaria +359'), ('BF', 'Burkina Faso +226'), ('BI', 'Burundi +257'), ('KH', 'Cambodia +855'), ('CM', 'Cameroon +237'), ('CA', 'Canada +1'), ('CV', 'Cape Verde +238'), ('BQ', 'Caribbean Netherlands +599'), ('KY', 'Cayman Islands +1'), ('CF', 'Central African Republic +236'), ('TD', 'Chad +235'), ('CL', 'Chile +56'), ('CN', 'China +86'), ('CO', 'Colombia +57'), ('KM', 'Comoros +269'), ('CG', 'Congo - Brazzaville +242'), ('CD', 'Congo - Kinshasa +243'), ('CK', 'Cook Islands +682'), ('CR', 'Costa Rica +506'), ('HR', 'Croatia +385'), ('CU', 'Cuba +53'), ('CW', 'Curaçao +599'), ('CY', 'Cyprus +357'), ('CZ', 'Czech Republic +420'), ("('CI', 'Côte d’Ivoire +225')", 'Ci'), ('DK', 'Denmark +45'), ('DJ', 'Djibouti +253'), ('DM', 'Dominica +1'), ('DO', 'Dominican Republic +1'), ('EC', 'Ecuador +593'), ('EG', 'Egypt +20'), ('SV', 'El Salvador +503'), ('GQ', 'Equatorial Guinea +240'), ('ER', 'Eritrea +291'), ('EE', 'Estonia +372'), ('ET', 'Ethiopia +251'), ('FK', 'Falkland Islands +500'), ('FO', 'Faroe Islands +298'), ('FJ', 'Fiji +679'), ('FI', 'Finland +358'), ('FR', 'France +33'), ('GF', 'French Guiana +594'), ('PF', 'French Polynesia +689'), ('GA', 'Gabon +241'), ('GM', 'Gambia +220'), ('GE', 'Georgia +995'), ('DE', 'Germany +49'), ('GH', 'Ghana +233'), ('GI', 'Gibraltar +350'), ('GR', 'Greece +30'), ('GL', 'Greenland +299'), ('GD', 'Grenada +1'), ('GP', 'Guadeloupe +590'), ('GU', 'Guam +1'), ('GT', 'Guatemala +502'), ('GN', 'Guinea +224'), ('GW', 'Guinea-Bissau +245'), ('GY', 'Guyana +592'), ('HT', 'Haiti +509'), ('HN', 'Honduras +504'), ('HK', 'Hong Kong +852'), ('HU', 'Hungary +36'), ('IS', 'Iceland +354'), ('IN', 'India +91'), ('ID', 'Indonesia +62'), ('IR', 'Iran +98'), ('IQ', 'Iraq +964'), ('IE', 'Ireland +353'), ('IL', 'Israel +972'), ('IT', 'Italy +39'), ('JM', 'Jamaica +1'), ('JP', 'Japan +81'), ('JO', 'Jordan +962'), ('KZ', 'Kazakhstan +7'), ('KE', 'Kenya +254'), ('KI', 'Kiribati +686'), ('XK', 'Kosovo +383'), ('KW', 'Kuwait +965'), ('KG', 'Kyrgyzstan +996'), ('LA', 'Laos +856'), ('LV', 'Latvia +371'), ('LB', 'Lebanon +961'), ('LS', 'Lesotho +266'), ('LR', 'Liberia +231'), ('LY', 'Libya +218'), ('LI', 'Liechtenstein +423'), ('LT', 'Lithuania +370'), ('LU', 'Luxembourg +352'), ('MO', 'Macau +853'), ('MK', 'Macedonia +389'), ('MG', 'Madagascar +261'), ('MW', 'Malawi +265'), ('MY', 'Malaysia +60'), ('MV', 'Maldives +960'), ('ML', 'Mali +223'), ('MT', 'Malta +356'), ('MH', 'Marshall Islands +692'), ('MQ', 'Martinique +596'), ('MR', 'Mauritania +222'), ('MU', 'Mauritius +230'), ('MX', 'Mexico +52'), ('FM', 'Micronesia +691'), ('MD', 'Moldova +373'), ('MC', 'Monaco +377'), ('MN', 'Mongolia +976'), ('ME', 'Montenegro +382'), ('MS', 'Montserrat +1'), ('MA', 'Morocco +212'), ('MZ', 'Mozambique +258'), ('MM', 'Myanmar (Burma), +95'), ('NA', 'Namibia +264'), ('NR', 'Nauru +674'), ('NP', 'Nepal +977'), ('NL', 'Netherlands +31'), ('NC', 'New Caledonia +687'), ('NZ', 'New Zealand +64'), ('NI', 'Nicaragua +505'), ('NE', 'Niger +227'), ('NG', 'Nigeria +234'), ('NU', 'Niue +683'), ('NF', 'Norfolk Island +672'), ('KP', 'North Korea +850'), ('NO', 'Norway +47'), ('OM', 'Oman +968'), ('PK', 'Pakistan +92'), ('PW', 'Palau +680'), ('PS', 'Palestinian Territories +970'), ('PA', 'Panama +507'), ('PG', 'Papua New Guinea +675'), ('PY', 'Paraguay +595'), ('PE', 'Peru +51'), ('PH', 'Philippines +63'), ('PL', 'Poland +48'), ('PT', 'Portugal +351'), ('PR', 'Puerto Rico +1'), ('QA', 'Qatar +974'), ('RO', 'Romania +40'), ('RU', 'Russia +7'), ('RW', 'Rwanda +250'), ('RE', 'Réunion +262'), ('WS', 'Samoa +685'), ('SM', 'San Marino +378'), ('SA', 'Saudi Arabia +966'), ('SN', 'Senegal +221'), ('RS', 'Serbia +381'), ('SC', 'Seychelles +248'), ('SL', 'Sierra Leone +232'), ('SG', 'Singapore +65'), ('SX', 'Sint Maarten +1'), ('SK', 'Slovakia +421'), ('SI', 'Slovenia +386'), ('SB', 'Solomon Islands +677'), ('SO', 'Somalia +252'), ('ZA', 'South Africa +27'), ('KR', 'South Korea +82'), ('SS', 'South Sudan +211'), ('ES', 'Spain +34'), ('LK', 'Sri Lanka +94'), ('KN', 'St. Kitts &amp; Nevis +1'), ('LC', 'St. Lucia +1'), ('PM', 'St. Pierre &amp; Miquelon +508'), ('VC', 'St. Vincent &amp; Grenadines +1'), ('SD', 'Sudan +249'), ('SR', 'Suriname +597'), ('SZ', 'Swaziland +268'), ('SE', 'Sweden +46'), ('CH', 'Switzerland +41'), ('SY', 'Syria +963'), ('ST', 'São Tomé &amp; Príncipe +239'), ('TW', 'Taiwan +886'), ('TJ', 'Tajikistan +992'), ('TZ', 'Tanzania +255'), ('TH', 'Thailand +66'), ('TL', 'Timor-Leste +670'), ('TG', 'Togo +228'), ('TO', 'Tonga +676'), ('TT', 'Trinidad &amp; Tobago +1'), ('TN', 'Tunisia +216'), ('TR', 'Turkey +90'), ('TM', 'Turkmenistan +993'), ('TC', 'Turks &amp; Caicos Islands +1'), ('TV', 'Tuvalu +688'), ('VI', 'U.S. Virgin Islands +1'), ('UG', 'Uganda +256'), ('UA', 'Ukraine +380'), ('AE', 'United Arab Emirates +971'), ('GB', 'United Kingdom +44'), ('US', 'United States +1'), ('UY', 'Uruguay +598'), ('UZ', 'Uzbekistan +998'), ('VU', 'Vanuatu +678'), ('VE', 'Venezuela +58'), ('VN', 'Vietnam +84'), ('YE', 'Yemen +967'), ('ZM', 'Zambia +260'), ('ZW', 'Zimbabwe +263'), ('AX', 'Åland Islands +358')], default='IN', max_length=50, validators=[django.core.validators.RegexValidator(message='Invalid characters in country.', regex='^[A-Z]{2}$')])),
                ('ph_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid phone number.', regex='^[0-9]*$')])),
                ('otp', models.CharField(blank=True, default='', max_length=6)),
                ('otp_send', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Verification - Temp Phone Verification',
                'verbose_name_plural': 'Verification - Temp Phone Verification',
            },
        ),
        migrations.CreateModel(
            name='BankVerification',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_holder', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('ifsc', models.CharField(max_length=11)),
                ('bank', models.CharField(blank=True, max_length=255, null=True)),
                ('branch', models.CharField(blank=True, max_length=225, null=True)),
                ('beneficiary_id', models.CharField(blank=True, max_length=225, null=True)),
                ('mobile', models.CharField(default='', max_length=13)),
                ('utr', models.CharField(blank=True, max_length=50, null=True)),
                ('name_at_bank', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_deposited', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('reject_reason', models.TextField(blank=True, default='', null=True)),
                ('response_json', models.JSONField(blank=True, default=dict, null=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_bank_verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - Bank Detail',
                'verbose_name_plural': 'Verification - Bank Detail',
            },
        ),
        migrations.CreateModel(
            name='CompanyAddressDetail',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('address_line_1', models.CharField(blank=True, max_length=500, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=200, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{6}$')])),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_dashboard.cities')),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_company_address', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_dashboard.states')),
            ],
            options={
                'verbose_name': 'Verification - Company Address Detail',
                'verbose_name_plural': 'Verification - Company Address Detail',
            },
        ),
        migrations.CreateModel(
            name='CompanyBasicDetail',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255, unique=True)),
                ('about_brand', models.CharField(blank=True, max_length=500, null=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_company_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - Company Basic Detail',
                'verbose_name_plural': 'Verification - Company Basic Detail',
            },
        ),
        migrations.CreateModel(
            name='GstDetail',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_gst_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid GST Number.', regex='^[0-9][1-9][A-Z]{3}[PCHABGJLFT][A-Z][0-9]{4}[A-Z][0-9][Z][a-zA-Z0-9]$')])),
                ('legal_name_of_business', models.CharField(blank=True, max_length=225, null=True)),
                ('state_jurisdiction', models.CharField(blank=True, max_length=225, null=True)),
                ('state_jurisdiction_code', models.CharField(blank=True, max_length=225, null=True)),
                ('date_of_registration', models.DateField(blank=True, null=True)),
                ('constitution_of_business', models.CharField(blank=True, max_length=225, null=True)),
                ('taxpayer_type', models.CharField(blank=True, max_length=225, null=True)),
                ('nature_of_business_activity', models.CharField(blank=True, max_length=700, null=True)),
                ('gstn_status', models.CharField(blank=True, max_length=225, null=True)),
                ('last_updated_date', models.CharField(blank=True, max_length=225, null=True)),
                ('trade_name', models.CharField(blank=True, max_length=700, null=True)),
                ('additional_place_of_business_address', models.CharField(blank=True, max_length=225, null=True)),
                ('building_name', models.CharField(blank=True, max_length=225, null=True)),
                ('street', models.CharField(blank=True, max_length=225, null=True)),
                ('location', models.CharField(blank=True, max_length=225, null=True)),
                ('state_name', models.CharField(blank=True, max_length=225, null=True)),
                ('floor_nbr', models.CharField(blank=True, max_length=225, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True)),
                ('pricipal_place_of_business_address', models.CharField(blank=True, max_length=225, null=True)),
                ('state_name_repeat', models.CharField(blank=True, max_length=225, null=True)),
                ('pin_code_repeat', models.CharField(blank=True, max_length=6, null=True)),
                ('response_json', models.JSONField(blank=True, default=dict, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('reject_reason', models.TextField(blank=True, default='', null=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_gst_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - GST Details',
                'verbose_name_plural': 'Verification - GST Details',
            },
        ),
        migrations.CreateModel(
            name='PanCinDetails',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('document_type', models.CharField(blank=True, choices=[('cin', 'CIN'), ('pan', 'PAN')], max_length=5, null=True)),
                ('documnet_id', models.CharField(max_length=255, unique=True)),
                ('response_json', models.JSONField(blank=True, default=dict, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('reject_reason', models.TextField(blank=True, default='', null=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_pan_cin_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - Pan Cin Detail',
                'verbose_name_plural': 'Verification - Pan Cin Detail',
            },
        ),
        migrations.CreateModel(
            name='RepresentativeDetail',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('representative_name', models.CharField(blank=True, max_length=100, null=True)),
                ('representative_image', models.FileField(blank=True, help_text='please Uploaded Documents above.', null=True, upload_to=common.helpers.FileUploadPath('representative_proof'), validators=[common.validators.image_validator])),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_representative_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - Representative Detail',
                'verbose_name_plural': 'Verification - Representative Detail',
            },
        ),
        migrations.CreateModel(
            name='UserPhoneVerified',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('country', models.CharField(choices=[('AF', 'Afghanistan +93'), ('AL', 'Albania +355'), ('DZ', 'Algeria +213'), ('AS', 'American Samoa +1'), ('AD', 'Andorra +376'), ('AO', 'Angola +244'), ('AG', 'Antigua &amp; Barbuda +1'), ('AR', 'Argentina +54'), ('AM', 'Armenia +374'), ('AW', 'Aruba +297'), ('AU', 'Australia +61'), ('AT', 'Austria +43'), ('AZ', 'Azerbaijan +994'), ('BS', 'Bahamas +1'), ('BH', 'Bahrain +973'), ('BD', 'Bangladesh +880'), ('BB', 'Barbados +1'), ('BY', 'Belarus +375'), ('BE', 'Belgium +32'), ('BZ', 'Belize +501'), ('BJ', 'Benin +229'), ('BM', 'Bermuda +1'), ('BT', 'Bhutan +975'), ('BO', 'Bolivia +591'), ('BA', 'Bosnia &amp; Herzegovina +387'), ('BW', 'Botswana +267'), ('BR', 'Brazil +55'), ('VG', 'British Virgin Islands +1'), ('BN', 'Brunei +673'), ('BG', 'Bulgaria +359'), ('BF', 'Burkina Faso +226'), ('BI', 'Burundi +257'), ('KH', 'Cambodia +855'), ('CM', 'Cameroon +237'), ('CA', 'Canada +1'), ('CV', 'Cape Verde +238'), ('BQ', 'Caribbean Netherlands +599'), ('KY', 'Cayman Islands +1'), ('CF', 'Central African Republic +236'), ('TD', 'Chad +235'), ('CL', 'Chile +56'), ('CN', 'China +86'), ('CO', 'Colombia +57'), ('KM', 'Comoros +269'), ('CG', 'Congo - Brazzaville +242'), ('CD', 'Congo - Kinshasa +243'), ('CK', 'Cook Islands +682'), ('CR', 'Costa Rica +506'), ('HR', 'Croatia +385'), ('CU', 'Cuba +53'), ('CW', 'Curaçao +599'), ('CY', 'Cyprus +357'), ('CZ', 'Czech Republic +420'), ("('CI', 'Côte d’Ivoire +225')", 'Ci'), ('DK', 'Denmark +45'), ('DJ', 'Djibouti +253'), ('DM', 'Dominica +1'), ('DO', 'Dominican Republic +1'), ('EC', 'Ecuador +593'), ('EG', 'Egypt +20'), ('SV', 'El Salvador +503'), ('GQ', 'Equatorial Guinea +240'), ('ER', 'Eritrea +291'), ('EE', 'Estonia +372'), ('ET', 'Ethiopia +251'), ('FK', 'Falkland Islands +500'), ('FO', 'Faroe Islands +298'), ('FJ', 'Fiji +679'), ('FI', 'Finland +358'), ('FR', 'France +33'), ('GF', 'French Guiana +594'), ('PF', 'French Polynesia +689'), ('GA', 'Gabon +241'), ('GM', 'Gambia +220'), ('GE', 'Georgia +995'), ('DE', 'Germany +49'), ('GH', 'Ghana +233'), ('GI', 'Gibraltar +350'), ('GR', 'Greece +30'), ('GL', 'Greenland +299'), ('GD', 'Grenada +1'), ('GP', 'Guadeloupe +590'), ('GU', 'Guam +1'), ('GT', 'Guatemala +502'), ('GN', 'Guinea +224'), ('GW', 'Guinea-Bissau +245'), ('GY', 'Guyana +592'), ('HT', 'Haiti +509'), ('HN', 'Honduras +504'), ('HK', 'Hong Kong +852'), ('HU', 'Hungary +36'), ('IS', 'Iceland +354'), ('IN', 'India +91'), ('ID', 'Indonesia +62'), ('IR', 'Iran +98'), ('IQ', 'Iraq +964'), ('IE', 'Ireland +353'), ('IL', 'Israel +972'), ('IT', 'Italy +39'), ('JM', 'Jamaica +1'), ('JP', 'Japan +81'), ('JO', 'Jordan +962'), ('KZ', 'Kazakhstan +7'), ('KE', 'Kenya +254'), ('KI', 'Kiribati +686'), ('XK', 'Kosovo +383'), ('KW', 'Kuwait +965'), ('KG', 'Kyrgyzstan +996'), ('LA', 'Laos +856'), ('LV', 'Latvia +371'), ('LB', 'Lebanon +961'), ('LS', 'Lesotho +266'), ('LR', 'Liberia +231'), ('LY', 'Libya +218'), ('LI', 'Liechtenstein +423'), ('LT', 'Lithuania +370'), ('LU', 'Luxembourg +352'), ('MO', 'Macau +853'), ('MK', 'Macedonia +389'), ('MG', 'Madagascar +261'), ('MW', 'Malawi +265'), ('MY', 'Malaysia +60'), ('MV', 'Maldives +960'), ('ML', 'Mali +223'), ('MT', 'Malta +356'), ('MH', 'Marshall Islands +692'), ('MQ', 'Martinique +596'), ('MR', 'Mauritania +222'), ('MU', 'Mauritius +230'), ('MX', 'Mexico +52'), ('FM', 'Micronesia +691'), ('MD', 'Moldova +373'), ('MC', 'Monaco +377'), ('MN', 'Mongolia +976'), ('ME', 'Montenegro +382'), ('MS', 'Montserrat +1'), ('MA', 'Morocco +212'), ('MZ', 'Mozambique +258'), ('MM', 'Myanmar (Burma), +95'), ('NA', 'Namibia +264'), ('NR', 'Nauru +674'), ('NP', 'Nepal +977'), ('NL', 'Netherlands +31'), ('NC', 'New Caledonia +687'), ('NZ', 'New Zealand +64'), ('NI', 'Nicaragua +505'), ('NE', 'Niger +227'), ('NG', 'Nigeria +234'), ('NU', 'Niue +683'), ('NF', 'Norfolk Island +672'), ('KP', 'North Korea +850'), ('NO', 'Norway +47'), ('OM', 'Oman +968'), ('PK', 'Pakistan +92'), ('PW', 'Palau +680'), ('PS', 'Palestinian Territories +970'), ('PA', 'Panama +507'), ('PG', 'Papua New Guinea +675'), ('PY', 'Paraguay +595'), ('PE', 'Peru +51'), ('PH', 'Philippines +63'), ('PL', 'Poland +48'), ('PT', 'Portugal +351'), ('PR', 'Puerto Rico +1'), ('QA', 'Qatar +974'), ('RO', 'Romania +40'), ('RU', 'Russia +7'), ('RW', 'Rwanda +250'), ('RE', 'Réunion +262'), ('WS', 'Samoa +685'), ('SM', 'San Marino +378'), ('SA', 'Saudi Arabia +966'), ('SN', 'Senegal +221'), ('RS', 'Serbia +381'), ('SC', 'Seychelles +248'), ('SL', 'Sierra Leone +232'), ('SG', 'Singapore +65'), ('SX', 'Sint Maarten +1'), ('SK', 'Slovakia +421'), ('SI', 'Slovenia +386'), ('SB', 'Solomon Islands +677'), ('SO', 'Somalia +252'), ('ZA', 'South Africa +27'), ('KR', 'South Korea +82'), ('SS', 'South Sudan +211'), ('ES', 'Spain +34'), ('LK', 'Sri Lanka +94'), ('KN', 'St. Kitts &amp; Nevis +1'), ('LC', 'St. Lucia +1'), ('PM', 'St. Pierre &amp; Miquelon +508'), ('VC', 'St. Vincent &amp; Grenadines +1'), ('SD', 'Sudan +249'), ('SR', 'Suriname +597'), ('SZ', 'Swaziland +268'), ('SE', 'Sweden +46'), ('CH', 'Switzerland +41'), ('SY', 'Syria +963'), ('ST', 'São Tomé &amp; Príncipe +239'), ('TW', 'Taiwan +886'), ('TJ', 'Tajikistan +992'), ('TZ', 'Tanzania +255'), ('TH', 'Thailand +66'), ('TL', 'Timor-Leste +670'), ('TG', 'Togo +228'), ('TO', 'Tonga +676'), ('TT', 'Trinidad &amp; Tobago +1'), ('TN', 'Tunisia +216'), ('TR', 'Turkey +90'), ('TM', 'Turkmenistan +993'), ('TC', 'Turks &amp; Caicos Islands +1'), ('TV', 'Tuvalu +688'), ('VI', 'U.S. Virgin Islands +1'), ('UG', 'Uganda +256'), ('UA', 'Ukraine +380'), ('AE', 'United Arab Emirates +971'), ('GB', 'United Kingdom +44'), ('US', 'United States +1'), ('UY', 'Uruguay +598'), ('UZ', 'Uzbekistan +998'), ('VU', 'Vanuatu +678'), ('VE', 'Venezuela +58'), ('VN', 'Vietnam +84'), ('YE', 'Yemen +967'), ('ZM', 'Zambia +260'), ('ZW', 'Zimbabwe +263'), ('AX', 'Åland Islands +358')], default='IN', max_length=50, validators=[django.core.validators.RegexValidator(message='Invalid characters in country.', regex='^[A-Z]{2}$')])),
                ('ph_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid phone number.', regex='^[0-9]*$')])),
                ('otp', models.CharField(blank=True, default='', max_length=6)),
                ('otp_send', models.BooleanField(default=False)),
                ('is_verified', models.CharField(choices=[('PENDING', 'PENDING'), ('REVIEWED', 'REVIEWED'), ('REJECTED', 'REJECTED'), ('VERIFIED', 'VERIFIED'), ('EXPIRED', 'EXPIRED')], default='PENDING', max_length=10)),
                ('reset_password_verify', models.BooleanField(default=False)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('reject_reason', models.TextField(blank=True, default='', null=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_phone_number', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification - Phone',
                'verbose_name_plural': 'Verification - Phone',
            },
        ),
    ]
