from enum import Enum
from django.db.models import TextChoices

# app_usser

class UserAuthIdentifierType(TextChoices):
    PH_NUMBER = ('PH_NUMBER', 'PH_NUMBER')
    EMAIL = ('EMAIL', 'EMAIL')
    UnKNOWN = ('UnKNOWN', 'UnKNOWN')


# app_verification
class UserStatusEnums(TextChoices):
    PENDING = ('PENDING', 'PENDING')
    REVIEWED = ('REVIEWED', 'REVIEWED')
    REJECTED = ('REJECTED', 'REJECTED')
    VERIFIED = ('VERIFIED', 'VERIFIED')
    EXPIRED = ('EXPIRED', 'EXPIRED')

class OrderHandlingTimeEnums(TextChoices):
    DAY_1 = ('1-day', '1 Day')
    DAY_2 = ('2-day', '2 Day')
    DAY_3 = ('3-day', '3 Day')
    DAY_4 = ('4-day', '4 Day')
    DAY_5 = ('5-day', '5 Day')
    DAY_6 = ('6-day', '6 Day')
    DAY_7 = ('7-day', '7 Day')
    DAY_8 = ('8-day', '8 Day')
    DAY_9 = ('9-day', '9 Day')
    DAY_10 = ('10-day', '10 Day')
    SAME_DAY = ('same-day', 'Same day')
    MORE_THAN_10_DAY = ('more-than-10-days', 'More Than 10 Days')

class OrderCuttOffTime(TextChoices):
    T_00_00 = ('00.00', '12.00 AM')
    T_00_30 = ('00.30', '12.30 AM')
    T_01_00 = ('01.00', '01.00 AM')
    T_01_30 = ('01.30', '01.30 AM')
    T_02_00 = ('02.00', '02.00 AM')
    T_02_30 = ('02.30', '02.30 AM')
    T_03_00 = ('03.00', '03.00 AM')
    T_03_30 = ('03.30', '03.30 AM')
    T_04_00 = ('04.00', '04.00 AM')
    T_04_30 = ('04.30', '04.30 AM')
    T_05_00 = ('05.00', '05.00 AM')
    T_05_30 = ('05.30', '05.30 AM')
    T_06_00 = ('06.00', '06.00 AM')
    T_06_30 = ('06.30', '06.30 AM')
    T_07_00 = ('07.00', '07.00 AM')
    T_07_30 = ('07.30', '07.30 AM')
    T_08_00 = ('08.00', '08.00 AM')
    T_08_30 = ('08.30', '08.30 AM')
    T_09_00 = ('09.00', '09.00 AM')
    T_09_30 = ('09.30', '09.30 AM')
    T_10_00 = ('10.00', '10.00 AM')
    T_10_30 = ('10.30', '10.30 AM')
    T_11_00 = ('11.00', '11.00 AM')
    T_11_30 = ('11.30', '11.30 AM')
    T_12_00 = ('12.00', '12.00 PM')
    T_12_30 = ('12.30', '12.30 PM')
    T_13_00 = ('13.00', '01.00 PM')
    T_13_30 = ('13.30', '01.30 PM')
    T_14_00 = ('14.00', '02.00 PM')
    T_14_30 = ('14.30', '02.30 PM')
    T_15_00 = ('15.00', '03.00 PM')
    T_15_30 = ('15.30', '03.30 PM')
    T_16_00 = ('16.00', '04.00 PM')
    T_16_30 = ('16.30', '04.30 PM')
    T_17_00 = ('17.00', '05.00 PM')
    T_17_30 = ('17.30', '05.30 PM')
    T_18_00 = ('18.00', '06.00 PM')
    T_18_30 = ('18.30', '06.30 PM')
    T_19_00 = ('19.00', '07.00 PM')
    T_19_30 = ('19.30', '07.30 PM')
    T_20_00 = ('20.00', '08.00 PM')
    T_20_30 = ('20.30', '08.30 PM')
    T_21_00 = ('21.00', '09.00 PM')
    T_21_30 = ('21.30', '09.30 PM')
    T_22_00 = ('22.00', '10.00 PM')
    T_22_30 = ('22.30', '10.30 PM')
    T_23_00 = ('23.00', '11.00 PM')
    T_23_30 = ('23.30', '11.30 PM')    

class PanCinDetailEnums(TextChoices):
    CIN = ('cin', 'CIN')
    PAN = ('pan', 'PAN')

class CountryWithDialCodeEnums(TextChoices):
   AF = ('AF', 'Afghanistan +93')
   AL = ('AL', 'Albania +355')
   DZ = ('DZ', 'Algeria +213')
   AS = ('AS', 'American Samoa +1')
   AD = ('AD', 'Andorra +376')
   AO = ('AO', 'Angola +244')
   AG = ('AG', 'Antigua &amp; Barbuda +1')
   AR = ('AR', 'Argentina +54')
   AM = ('AM', 'Armenia +374')
   AW = ('AW', 'Aruba +297')
   AU = ('AU', 'Australia +61')
   AT = ('AT', 'Austria +43')
   AZ = ('AZ', 'Azerbaijan +994')
   BS = ('BS', 'Bahamas +1')
   BH = ('BH', 'Bahrain +973')
   BD = ('BD', 'Bangladesh +880')
   BB = ('BB', 'Barbados +1')
   BY = ('BY', 'Belarus +375')
   BE = ('BE', 'Belgium +32')
   BZ = ('BZ', 'Belize +501')
   BJ = ('BJ', 'Benin +229')
   BM = ('BM', 'Bermuda +1')
   BT = ('BT', 'Bhutan +975')
   BO = ('BO', 'Bolivia +591')
   BA = ('BA', 'Bosnia &amp; Herzegovina +387')
   BW = ('BW', 'Botswana +267')
   BR = ('BR', 'Brazil +55')
   VG = ('VG', 'British Virgin Islands +1')
   BN = ('BN', 'Brunei +673')
   BG = ('BG', 'Bulgaria +359')
   BF = ('BF', 'Burkina Faso +226')
   BI = ('BI', 'Burundi +257')
   KH = ('KH', 'Cambodia +855')
   CM = ('CM', 'Cameroon +237')
   CA = ('CA', 'Canada +1')
   CV = ('CV', 'Cape Verde +238')
   BQ = ('BQ', 'Caribbean Netherlands +599')
   KY = ('KY', 'Cayman Islands +1')
   CF = ('CF', 'Central African Republic +236')
   TD = ('TD', 'Chad +235')
   CL = ('CL', 'Chile +56')
   CN = ('CN', 'China +86')
   CO = ('CO', 'Colombia +57')
   KM = ('KM', 'Comoros +269')
   CG = ('CG', 'Congo - Brazzaville +242')
   CD = ('CD', 'Congo - Kinshasa +243')
   CK = ('CK', 'Cook Islands +682')
   CR = ('CR', 'Costa Rica +506')
   HR = ('HR', 'Croatia +385')
   CU = ('CU', 'Cuba +53')
   CW = ('CW', 'Curaçao +599')
   CY = ('CY', 'Cyprus +357')
   CZ = ('CZ', 'Czech Republic +420')
   CI = ('CI', "Côte d’Ivoire +225"),
   DK = ('DK', 'Denmark +45')
   DJ = ('DJ', 'Djibouti +253')
   DM = ('DM', 'Dominica +1')
   DO = ('DO', 'Dominican Republic +1')
   EC = ('EC', 'Ecuador +593')
   EG = ('EG', 'Egypt +20')
   SV = ('SV', 'El Salvador +503')
   GQ = ('GQ', 'Equatorial Guinea +240')
   ER = ('ER', 'Eritrea +291')
   EE = ('EE', 'Estonia +372')
   ET = ('ET', 'Ethiopia +251')
   FK = ('FK', 'Falkland Islands +500')
   FO = ('FO', 'Faroe Islands +298')
   FJ = ('FJ', 'Fiji +679')
   FI = ('FI', 'Finland +358')
   FR = ('FR', 'France +33')
   GF = ('GF', 'French Guiana +594')
   PF = ('PF', 'French Polynesia +689')
   GA = ('GA', 'Gabon +241')
   GM = ('GM', 'Gambia +220')
   GE = ('GE', 'Georgia +995')
   DE = ('DE', 'Germany +49')
   GH = ('GH', 'Ghana +233')
   GI = ('GI', 'Gibraltar +350')
   GR = ('GR', 'Greece +30')
   GL = ('GL', 'Greenland +299')
   GD = ('GD', 'Grenada +1')
   GP = ('GP', 'Guadeloupe +590')
   GU = ('GU', 'Guam +1')
   GT = ('GT', 'Guatemala +502')
   GN = ('GN', 'Guinea +224')
   GW = ('GW', 'Guinea-Bissau +245')
   GY = ('GY', 'Guyana +592')
   HT = ('HT', 'Haiti +509')
   HN = ('HN', 'Honduras +504')
   HK = ('HK', 'Hong Kong +852')
   HU = ('HU', 'Hungary +36')
   IS = ('IS', 'Iceland +354')
   IN = ('IN', 'India +91')
   ID = ('ID', 'Indonesia +62')
   IR = ('IR', 'Iran +98')
   IQ = ('IQ', 'Iraq +964')
   IE = ('IE', 'Ireland +353')
   IL = ('IL', 'Israel +972')
   IT = ('IT', 'Italy +39')
   JM = ('JM', 'Jamaica +1')
   JP = ('JP', 'Japan +81')
   JO = ('JO', 'Jordan +962')
   KZ = ('KZ', 'Kazakhstan +7')
   KE = ('KE', 'Kenya +254')
   KI = ('KI', 'Kiribati +686')
   XK = ('XK', 'Kosovo +383')
   KW = ('KW', 'Kuwait +965')
   KG = ('KG', 'Kyrgyzstan +996')
   LA = ('LA', 'Laos +856')
   LV = ('LV', 'Latvia +371')
   LB = ('LB', 'Lebanon +961')
   LS = ('LS', 'Lesotho +266')
   LR = ('LR', 'Liberia +231')
   LY = ('LY', 'Libya +218')
   LI = ('LI', 'Liechtenstein +423')
   LT = ('LT', 'Lithuania +370')
   LU = ('LU', 'Luxembourg +352')
   MO = ('MO', 'Macau +853')
   MK = ('MK', 'Macedonia +389')
   MG = ('MG', 'Madagascar +261')
   MW = ('MW', 'Malawi +265')
   MY = ('MY', 'Malaysia +60')
   MV = ('MV', 'Maldives +960')
   ML = ('ML', 'Mali +223')
   MT = ('MT', 'Malta +356')
   MH = ('MH', 'Marshall Islands +692')
   MQ = ('MQ', 'Martinique +596')
   MR = ('MR', 'Mauritania +222')
   MU = ('MU', 'Mauritius +230')
   MX = ('MX', 'Mexico +52')
   FM = ('FM', 'Micronesia +691')
   MD = ('MD', 'Moldova +373')
   MC = ('MC', 'Monaco +377')
   MN = ('MN', 'Mongolia +976')
   ME = ('ME', 'Montenegro +382')
   MS = ('MS', 'Montserrat +1')
   MA = ('MA', 'Morocco +212')
   MZ = ('MZ', 'Mozambique +258')
   MM = ('MM', 'Myanmar (Burma), +95')
   NA = ('NA', 'Namibia +264')
   NR = ('NR', 'Nauru +674')
   NP = ('NP', 'Nepal +977')
   NL = ('NL', 'Netherlands +31')
   NC = ('NC', 'New Caledonia +687')
   NZ = ('NZ', 'New Zealand +64')
   NI = ('NI', 'Nicaragua +505')
   NE = ('NE', 'Niger +227')
   NG = ('NG', 'Nigeria +234')
   NU = ('NU', 'Niue +683')
   NF = ('NF', 'Norfolk Island +672')
   KP = ('KP', 'North Korea +850')
   NO = ('NO', 'Norway +47')
   OM = ('OM', 'Oman +968')
   PK = ('PK', 'Pakistan +92')
   PW = ('PW', 'Palau +680')
   PS = ('PS', 'Palestinian Territories +970')
   PA = ('PA', 'Panama +507')
   PG = ('PG', 'Papua New Guinea +675')
   PY = ('PY', 'Paraguay +595')
   PE = ('PE', 'Peru +51')
   PH = ('PH', 'Philippines +63')
   PL = ('PL', 'Poland +48')
   PT = ('PT', 'Portugal +351')
   PR = ('PR', 'Puerto Rico +1')
   QA = ('QA', 'Qatar +974')
   RO = ('RO', 'Romania +40')
   RU = ('RU', 'Russia +7')
   RW = ('RW', 'Rwanda +250')
   RE = ('RE', 'Réunion +262')
   WS = ('WS', 'Samoa +685')
   SM = ('SM', 'San Marino +378')
   SA = ('SA', 'Saudi Arabia +966')
   SN = ('SN', 'Senegal +221')
   RS = ('RS', 'Serbia +381')
   SC = ('SC', 'Seychelles +248')
   SL = ('SL', 'Sierra Leone +232')
   SG = ('SG', 'Singapore +65')
   SX = ('SX', 'Sint Maarten +1')
   SK = ('SK', 'Slovakia +421')
   SI = ('SI', 'Slovenia +386')
   SB = ('SB', 'Solomon Islands +677')
   SO = ('SO', 'Somalia +252')
   ZA = ('ZA', 'South Africa +27')
   KR = ('KR', 'South Korea +82')
   SS = ('SS', 'South Sudan +211')
   ES = ('ES', 'Spain +34')
   LK = ('LK', 'Sri Lanka +94')
   KN = ('KN', 'St. Kitts &amp; Nevis +1')
   LC = ('LC', 'St. Lucia +1')
   PM = ('PM', 'St. Pierre &amp; Miquelon +508')
   VC = ('VC', 'St. Vincent &amp; Grenadines +1')
   SD = ('SD', 'Sudan +249')
   SR = ('SR', 'Suriname +597')
   SZ = ('SZ', 'Swaziland +268')
   SE = ('SE', 'Sweden +46')
   CH = ('CH', 'Switzerland +41')
   SY = ('SY', 'Syria +963')
   ST = ('ST', 'São Tomé &amp; Príncipe +239')
   TW = ('TW', 'Taiwan +886')
   TJ = ('TJ', 'Tajikistan +992')
   TZ = ('TZ', 'Tanzania +255')
   TH = ('TH', 'Thailand +66')
   TL = ('TL', 'Timor-Leste +670')
   TG = ('TG', 'Togo +228')
   TO = ('TO', 'Tonga +676')
   TT = ('TT', 'Trinidad &amp; Tobago +1')
   TN = ('TN', 'Tunisia +216')
   TR = ('TR', 'Turkey +90')
   TM = ('TM', 'Turkmenistan +993')
   TC = ('TC', 'Turks &amp; Caicos Islands +1')
   TV = ('TV', 'Tuvalu +688')
   VI = ('VI', 'U.S. Virgin Islands +1')
   UG = ('UG', 'Uganda +256')
   UA = ('UA', 'Ukraine +380')
   AE = ('AE', 'United Arab Emirates +971')
   GB = ('GB', 'United Kingdom +44')
   US = ('US', 'United States +1')
   UY = ('UY', 'Uruguay +598')
   UZ = ('UZ', 'Uzbekistan +998')
   VU = ('VU', 'Vanuatu +678')
   VE = ('VE', 'Venezuela +58')
   VN = ('VN', 'Vietnam +84')
   YE = ('YE', 'Yemen +967')
   ZM = ('ZM', 'Zambia +260')
   ZW = ('ZW', 'Zimbabwe +263')
   AX = ('AX', 'Åland Islands +358')