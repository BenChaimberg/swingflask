import configparser
import re
from flask_wtf import FlaskForm, RecaptchaField
import wtforms
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    RadioField,
    TextAreaField
)


class LocationsForm(FlaskForm):
    postalcode = StringField(
        "Your postal code",
        [wtforms.validators.InputRequired('Please enter your postal code')]
    )
    measure = RadioField(
        'Distance measure',
        choices=[('miles', 'miles'), ('km', 'kilometers')],
        default='km'
    )
    results = RadioField(
        "Show me locations within",
        choices=[('10', '10'), ('25', '25'), ('50', '50')],
        default='25'
    )

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if len(str(self.postalcode.data)) == 5 and int(self.postalcode.data):
            return True
        self.postalcode.data = re.sub(r'\s', r'', self.postalcode.data)
        if not len(str(self.postalcode.data)) == 6:
            self.postalcode.errors.append('Invalid postal code (length)')
            return False
        if not ''.join([
            str(self.postalcode.data)[0],
            str(self.postalcode.data)[2],
            str(self.postalcode.data)[4]
        ]).isalpha():
            self.postalcode.errors.append(
                'Invalid postal code (example: A1A1A1)'
            )
            return False
        if not ''.join([
            str(self.postalcode.data)[1],
            str(self.postalcode.data)[3],
            str(self.postalcode.data)[5]
        ]).isdigit():
            self.postalcode.errors.append(
                'Invalid postal code (example: A1A1A1)'
            )
            return False
        return True


class MessageForm(FlaskForm):
    name = StringField(
        "Name",
        [wtforms.validators.InputRequired('Please enter your name')]
    )
    email = StringField(
        "E-mail",
        [
            wtforms.validators.InputRequired('Please enter your email'),
            wtforms.validators.Email()
        ]
    )
    subject = StringField(
        "Subject",
        [wtforms.validators.InputRequired('Please enter a subject')]
    )
    message = TextAreaField(
        "Message",
        [wtforms.validators.InputRequired('Please enter your message')]
    )
    notifyemail = RadioField(
        'Do you want notification of a response to your message?',
        choices=[('True', 'Yes'), ('False', 'No')]
    )
    recaptcha = RecaptchaField()


class FrenchMessageForm(FlaskForm):
    name = StringField(
        "Nom",
        [wtforms.validators.InputRequired('Veuillez entrez votre nom')]
    )
    email = StringField(
        "Adresse de Couriel",
        [
            wtforms.validators.InputRequired(
                'Veuillez entrez votre adresse de courriel'
            ),
            wtforms.validators.Email()
        ]
    )
    subject = StringField(
        "Sujet",
        [wtforms.validators.InputRequired('Veuillez entrez un sujet')]
    )
    message = TextAreaField(
        "Message",
        [wtforms.validators.InputRequired('Veuillez entrez un message')]
    )
    notifyemail = RadioField(
        'Voulez-vous la notification d&#x0027;un r&#x00E9;ponse &#x00E0; votre\
            message?\
        ',
        choices=[('True', 'Oui'), ('False', 'Non')]
    )
    recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
    username = StringField(
        "Username:",
        [wtforms.validators.InputRequired('Please enter your username')]
    )
    password = PasswordField(
        "Password:",
        [wtforms.validators.InputRequired('Please enter your password')]
    )

    def validate(self):
        rv = FlaskForm.validate(self)
        config = configparser.RawConfigParser()
        config.read('swingflask.conf')
        if (
            self.username.data == config.get('admin', 'username')
            and self.password.data == config.get('admin', 'password')
        ):
            return True
        else:
            self.username.errors.append('Invalid credentials')
            return False


class BrochureForm(FlaskForm):
    name = StringField(
        "Name",
        [wtforms.validators.InputRequired('Please enter your name')]
    )
    email = StringField(
        "E-mail",
        [
            wtforms.validators.InputRequired('Please enter your email'),
            wtforms.validators.Email()
        ]
    )
    address = StringField(
        "Address",
        [wtforms.validators.InputRequired('Please enter your address')]
    )
    city = StringField(
        "City",
        [wtforms.validators.InputRequired('Please enter your city')]
    )
    stateprov = SelectField(
        "State/Prov",
        [wtforms.validators.InputRequired('Please enter your state or province')],
        choices=[
            ('', ''),
            ('Alberta', 'Alberta'),
            ('British Columbia', 'British Columbia'),
            ('Manitoba', 'Manitoba'),
            ('New Brunswick', 'New Brunswick'),
            ('Newfoundland and Labrador', 'Newfoundland and Labrador'),
            ('Northwest Territories', 'Northwest Territories'),
            ('Nova Scotia', 'Nova Scotia'),
            ('Nunavut', 'Nunavut'),
            ('Ontario', 'Ontario'),
            ('Prince Edward Island', 'Prince Edward Island'),
            ('Quebec', 'Quebec'),
            ('Saskatchewan', 'Saskatchewan'),
            ('Yukon Territory', 'Yukon Territory'),
            ('_', ''),
            ('Alabama', 'Alabama'),
            ('Alaska', 'Alaska'),
            ('Arizona', 'Arizona'),
            ('Arkansas', 'Arkansas'),
            ('California', 'California'),
            ('Colorado', 'Colorado'),
            ('Connecticut', 'Connecticut'),
            ('Delaware', 'Delaware'),
            ('Florida', 'Florida'),
            ('Georgia', 'Georgia'),
            ('Hawaii', 'Hawaii'),
            ('Idaho', 'Idaho'),
            ('Illinois', 'Illinois'),
            ('Indiana', 'Indiana'),
            ('Iowa', 'Iowa'),
            ('Kansas', 'Kansas'),
            ('Kentucky', 'Kentucky'),
            ('Louisiana', 'Louisiana'),
            ('Maine', 'Maine'),
            ('Maryland', 'Maryland'),
            ('Massachusetts', 'Massachusetts'),
            ('Michigan', 'Michigan'),
            ('Minnesota', 'Minnesota'),
            ('Mississippi', 'Mississippi'),
            ('Missouri', 'Missouri'),
            ('Montana', 'Montana'),
            ('Nebraska', 'Nebraska'),
            ('Nevada', 'Nevada'),
            ('New Hampshire', 'New Hampshire'),
            ('New Jersey', 'New Jersey'),
            ('New Mexico', 'New Mexico'),
            ('New York', 'New York'),
            ('North Carolina', 'North Carolina'),
            ('North Dakota', 'North Dakota'),
            ('Ohio', 'Ohio'),
            ('Oklahoma', 'Oklahoma'),
            ('Oregon', 'Oregon'),
            ('Pennsylvania', 'Pennsylvania'),
            ('Rhode Island', 'Rhode Island'),
            ('South Carolina', 'South Carolina'),
            ('South Dakota', 'South Dakota'),
            ('Tennessee', 'Tennessee'),
            ('Texas', 'Texas'),
            ('Utah', 'Utah'),
            ('Vermont', 'Vermont'),
            ('Virginia', 'Virginia'),
            ('Washington', 'Washington'),
            ('West Virginia', 'West Virginia'),
            ('Wisconsin', 'Wisconsin'),
            ('Wyoming', 'Wyoming')
        ]
    )
    zipcode = StringField(
        "Zip/Postal Code",
        [wtforms.validators.InputRequired('Please enter your zip or postal code')]
    )
    country = SelectField(
        "Country",
        [wtforms.validators.InputRequired('Please enter your country')],
        choices=[
            ('', ''),
            ('Afghanistan', 'Afghanistan'),
            ('Aland Islands', 'Aland Islands'),
            ('Albania', 'Albania'),
            ('Algeria', 'Algeria'),
            ('American Samoa', 'American Samoa'),
            ('Andorra', 'Andorra'),
            ('Angola', 'Angola'),
            ('Anguilla', 'Anguilla'),
            ('Antarctica', 'Antarctica'),
            ('Antigua And Barbuda', 'Antigua And Barbuda'),
            ('Argentina', 'Argentina'),
            ('Armenia', 'Armenia'),
            ('Aruba', 'Aruba'),
            ('Australia', 'Australia'),
            ('Austria', 'Austria'),
            ('Azerbaijan', 'Azerbaijan'),
            ('Bahamas', 'Bahamas'),
            ('Bahrain', 'Bahrain'),
            ('Bangladesh', 'Bangladesh'),
            ('Barbados', 'Barbados'),
            ('Belarus', 'Belarus'),
            ('Belgium', 'Belgium'),
            ('Belize', 'Belize'),
            ('Benin', 'Benin'),
            ('Bermuda', 'Bermuda'),
            ('Bhutan', 'Bhutan'),
            ('Bolivia', 'Bolivia'),
            ('Bosnia And Herzegovina', 'Bosnia And Herzegovina'),
            ('Botswana', 'Botswana'),
            ('Bouvet Island', 'Bouvet Island'),
            ('Brazil', 'Brazil'),
            (
                'British Indian Ocean Territory',
                'British Indian Ocean Territory'
            ),
            ('Brunei Darussalam', 'Brunei Darussalam'),
            ('Bulgaria', 'Bulgaria'),
            ('Burkina Faso', 'Burkina Faso'),
            ('Burundi', 'Burundi'),
            ('Cambodia', 'Cambodia'),
            ('Cameroon', 'Cameroon'),
            ('Canada', 'Canada'),
            ('Cape Verde', 'Cape Verde'),
            ('Cayman Islands', 'Cayman Islands'),
            ('Central African Republic', 'Central African Republic'),
            ('Chad', 'Chad'),
            ('Chile', 'Chile'),
            ('China', 'China'),
            ('Christmas Island', 'Christmas Island'),
            ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
            ('Colombia', 'Colombia'),
            ('Comoros', 'Comoros'),
            ('Congo', 'Congo'),
            (
                'Congo, The Democratic Republic Of The',
                'Congo, The Democratic Republic Of The'
            ),
            ('Cook Islands', 'Cook Islands'),
            ('Costa Rica', 'Costa Rica'),
            ('Cote D\'ivoire', 'Cote D\'ivoire'),
            ('Croatia', 'Croatia'),
            ('Cuba', 'Cuba'),
            ('Cyprus', 'Cyprus'),
            ('Czech Republic', 'Czech Republic'),
            ('Denmark', 'Denmark'),
            ('Djibouti', 'Djibouti'),
            ('Dominica', 'Dominica'),
            ('Dominican Republic', 'Dominican Republic'),
            ('Ecuador', 'Ecuador'),
            ('Egypt', 'Egypt'),
            ('El Salvador', 'El Salvador'),
            ('Equatorial Guinea', 'Equatorial Guinea'),
            ('Eritrea', 'Eritrea'),
            ('Estonia', 'Estonia'),
            ('Ethiopia', 'Ethiopia'),
            ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
            ('Faroe Islands', 'Faroe Islands'),
            ('Fiji', 'Fiji'),
            ('Finland', 'Finland'),
            ('France', 'France'),
            ('French Guiana', 'French Guiana'),
            ('French Polynesia', 'French Polynesia'),
            ('French Southern Territories', 'French Southern Territories'),
            ('Gabon', 'Gabon'),
            ('Gambia', 'Gambia'),
            ('Georgia', 'Georgia'),
            ('Germany', 'Germany'),
            ('Ghana', 'Ghana'),
            ('Gibraltar', 'Gibraltar'),
            ('Greece', 'Greece'),
            ('Greenland', 'Greenland'),
            ('Grenada', 'Grenada'),
            ('Guadeloupe', 'Guadeloupe'),
            ('Guam', 'Guam'),
            ('Guatemala', 'Guatemala'),
            ('Guernsey', 'Guernsey'),
            ('Guinea', 'Guinea'),
            ('Guinea-bissau', 'Guinea-bissau'),
            ('Guyana', 'Guyana'),
            ('Haiti', 'Haiti'),
            (
                'Heard Island And Mcdonald Islands',
                'Heard Island And Mcdonald Islands'
            ),
            ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
            ('Honduras', 'Honduras'),
            ('Hong Kong', 'Hong Kong'),
            ('Hungary', 'Hungary'),
            ('Iceland', 'Iceland'),
            ('India', 'India'),
            ('Indonesia', 'Indonesia'),
            ('Iran, Islamic Republic Of', 'Iran, Islamic Republic Of'),
            ('Iraq', 'Iraq'),
            ('Ireland', 'Ireland'),
            ('Isle Of Man', 'Isle Of Man'),
            ('Israel', 'Israel'),
            ('Italy', 'Italy'),
            ('Jamaica', 'Jamaica'),
            ('Japan', 'Japan'),
            ('Jersey', 'Jersey'),
            ('Jordan', 'Jordan'),
            ('Kazakhstan', 'Kazakhstan'),
            ('Kenya', 'Kenya'),
            ('Kiribati', 'Kiribati'),
            (
                'Korea, Democratic People\'s Republic Of',
                'Korea, Democratic People\'s Republic Of'
            ),
            ('Korea, Republic Of', 'Korea, Republic Of'),
            ('Kuwait', 'Kuwait'),
            ('Kyrgyzstan', 'Kyrgyzstan'),
            (
                'Lao People\'s Democratic Republic',
                'Lao People\'s Democratic Republic'
            ),
            ('Latvia', 'Latvia'),
            ('Lebanon', 'Lebanon'),
            ('Lesotho', 'Lesotho'),
            ('Liberia', 'Liberia'),
            ('Libyan Arab Jamahiriya', 'Libyan Arab Jamahiriya'),
            ('Liechtenstein', 'Liechtenstein'),
            ('Lithuania', 'Lithuania'),
            ('Luxembourg', 'Luxembourg'),
            ('Macao', 'Macao'),
            (
                'Macedonia, The Former Yugoslav Republic Of',
                'Macedonia, The Former Yugoslav Republic Of'
            ),
            ('Madagascar', 'Madagascar'),
            ('Malawi', 'Malawi'),
            ('Malaysia', 'Malaysia'),
            ('Maldives', 'Maldives'),
            ('Mali', 'Mali'),
            ('Malta', 'Malta'),
            ('Marshall Islands', 'Marshall Islands'),
            ('Martinique', 'Martinique'),
            ('Mauritania', 'Mauritania'),
            ('Mauritius', 'Mauritius'),
            ('Mayotte', 'Mayotte'),
            ('Mexico', 'Mexico'),
            (
                'Micronesia, Federated States Of',
                'Micronesia, Federated States Of'
            ),
            ('Moldova, Republic Of', 'Moldova, Republic Of'),
            ('Monaco', 'Monaco'),
            ('Mongolia', 'Mongolia'),
            ('Montenegro', 'Montenegro'),
            ('Montserrat', 'Montserrat'),
            ('Morocco', 'Morocco'),
            ('Mozambique', 'Mozambique'),
            ('Myanmar', 'Myanmar'),
            ('Namibia', 'Namibia'),
            ('Nauru', 'Nauru'),
            ('Nepal', 'Nepal'),
            ('Netherlands', 'Netherlands'),
            ('Netherlands Antilles', 'Netherlands Antilles'),
            ('New Caledonia', 'New Caledonia'),
            ('New Zealand', 'New Zealand'),
            ('Nicaragua', 'Nicaragua'),
            ('Niger', 'Niger'),
            ('Nigeria', 'Nigeria'),
            ('Niue', 'Niue'),
            ('Norfolk Island', 'Norfolk Island'),
            ('Northern Mariana Islands', 'Northern Mariana Islands'),
            ('Norway', 'Norway'),
            ('Oman', 'Oman'),
            ('Pakistan', 'Pakistan'),
            ('Palau', 'Palau'),
            (
                'Palestinian Territory, Occupied',
                'Palestinian Territory, Occupied'
            ),
            ('Panama', 'Panama'),
            ('Papua New Guinea', 'Papua New Guinea'),
            ('Paraguay', 'Paraguay'),
            ('Peru', 'Peru'),
            ('Philippines', 'Philippines'),
            ('Pitcairn', 'Pitcairn'),
            ('Poland', 'Poland'),
            ('Portugal', 'Portugal'),
            ('Puerto Rico', 'Puerto Rico'),
            ('Qatar', 'Qatar'),
            ('Reunion', 'Reunion'),
            ('Romania', 'Romania'),
            ('Russian Federation', 'Russian Federation'),
            ('Rwanda', 'Rwanda'),
            ('Saint Helena', 'Saint Helena'),
            ('Saint Kitts And Nevis', 'Saint Kitts And Nevis'),
            ('Saint Lucia', 'Saint Lucia'),
            ('Saint Pierre And Miquelon', 'Saint Pierre And Miquelon'),
            (
                'Saint Vincent And The Grenadines',
                'Saint Vincent And The Grenadines'
            ),
            ('Samoa', 'Samoa'),
            ('San Marino', 'San Marino'),
            ('Sao Tome And Principe', 'Sao Tome And Principe'),
            ('Saudi Arabia', 'Saudi Arabia'),
            ('Senegal', 'Senegal'),
            ('Serbia', 'Serbia'),
            ('Seychelles', 'Seychelles'),
            ('Sierra Leone', 'Sierra Leone'),
            ('Singapore', 'Singapore'),
            ('Slovakia', 'Slovakia'),
            ('Slovenia', 'Slovenia'),
            ('Solomon Islands', 'Solomon Islands'),
            ('Somalia', 'Somalia'),
            ('South Africa', 'South Africa'),
            (
                'South Georgia And The South Sandwich Islands',
                'South Georgia And The South Sandwich Islands'
            ),
            ('Spain', 'Spain'),
            ('Sri Lanka', 'Sri Lanka'),
            ('Sudan', 'Sudan'),
            ('Suriname', 'Suriname'),
            ('Svalbard And Jan Mayen', 'Svalbard And Jan Mayen'),
            ('Swaziland', 'Swaziland'),
            ('Sweden', 'Sweden'),
            ('Switzerland', 'Switzerland'),
            ('Syrian Arab Republic', 'Syrian Arab Republic'),
            ('Taiwan, Province Of China', 'Taiwan, Province Of China'),
            ('Tajikistan', 'Tajikistan'),
            ('Tanzania, United Republic Of', 'Tanzania, United Republic Of'),
            ('Thailand', 'Thailand'),
            ('Timor-leste', 'Timor-leste'),
            ('Togo', 'Togo'),
            ('Tokelau', 'Tokelau'),
            ('Tonga', 'Tonga'),
            ('Trinidad And Tobago', 'Trinidad And Tobago'),
            ('Tunisia', 'Tunisia'),
            ('Turkey', 'Turkey'),
            ('Turkmenistan', 'Turkmenistan'),
            ('Turks And Caicos Islands', 'Turks And Caicos Islands'),
            ('Tuvalu', 'Tuvalu'),
            ('Uganda', 'Uganda'),
            ('Ukraine', 'Ukraine'),
            ('United Arab Emirates', 'United Arab Emirates'),
            ('United Kingdom', 'United Kingdom'),
            ('United States', 'United States'),
            (
                'United States Minor Outlying Islands',
                'United States Minor Outlying Islands'
            ),
            ('Uruguay', 'Uruguay'),
            ('Uzbekistan', 'Uzbekistan'),
            ('Vanuatu', 'Vanuatu'),
            ('Venezuela', 'Venezuela'),
            ('Viet Nam', 'Viet Nam'),
            ('Virgin Islands, British', 'Virgin Islands, British'),
            ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
            ('Wallis And Futuna', 'Wallis And Futuna'),
            ('Western Sahara', 'Western Sahara'),
            ('Yemen', 'Yemen'),
            ('Zambia', 'Zambia'),
            ('Zimbabwe', 'Zimbabwe')
        ]
    )


class FrenchBrochureForm(FlaskForm):
    name = StringField(
        "Nom",
        [wtforms.validators.InputRequired('Veuillez entrer votre nom')]
    )
    email = StringField(
        "Couriel",
        [
            wtforms.validators.InputRequired('Veuillez entrer votre couriel'),
            wtforms.validators.Email()
        ]
    )
    address = StringField(
        "Adresse",
        [wtforms.validators.InputRequired('Veuillez entrer votre adresse')]
    )
    city = StringField(
        "Ville",
        [wtforms.validators.InputRequired('Veuillez entrer votre ville')]
    )
    stateprov = SelectField(
        "&#xc9;tat/Province",
        [
            wtforms.validators.InputRequired(
                'Veuillez entrer votre &#xe9;tat ou province'
            )
        ],
        choices=[
            ('', ''),
            ('Alberta', 'Alberta'),
            ('British Columbia', 'British Columbia'),
            ('Manitoba', 'Manitoba'),
            ('New Brunswick', 'New Brunswick'),
            ('Newfoundland and Labrador', 'Newfoundland and Labrador'),
            ('Northwest Territories', 'Northwest Territories'),
            ('Nova Scotia', 'Nova Scotia'),
            ('Nunavut', 'Nunavut'),
            ('Ontario', 'Ontario'),
            ('Prince Edward Island', 'Prince Edward Island'),
            ('Quebec', 'Quebec'),
            ('Saskatchewan', 'Saskatchewan'),
            ('Yukon Territory', 'Yukon Territory'),
            ('_', ''),
            ('Alabama', 'Alabama'),
            ('Alaska', 'Alaska'),
            ('Arizona', 'Arizona'),
            ('Arkansas', 'Arkansas'),
            ('California', 'California'),
            ('Colorado', 'Colorado'),
            ('Connecticut', 'Connecticut'),
            ('Delaware', 'Delaware'),
            ('Florida', 'Florida'),
            ('Georgia', 'Georgia'),
            ('Hawaii', 'Hawaii'),
            ('Idaho', 'Idaho'),
            ('Illinois', 'Illinois'),
            ('Indiana', 'Indiana'),
            ('Iowa', 'Iowa'),
            ('Kansas', 'Kansas'),
            ('Kentucky', 'Kentucky'),
            ('Louisiana', 'Louisiana'),
            ('Maine', 'Maine'),
            ('Maryland', 'Maryland'),
            ('Massachusetts', 'Massachusetts'),
            ('Michigan', 'Michigan'),
            ('Minnesota', 'Minnesota'),
            ('Mississippi', 'Mississippi'),
            ('Missouri', 'Missouri'),
            ('Montana', 'Montana'),
            ('Nebraska', 'Nebraska'),
            ('Nevada', 'Nevada'),
            ('New Hampshire', 'New Hampshire'),
            ('New Jersey', 'New Jersey'),
            ('New Mexico', 'New Mexico'),
            ('New York', 'New York'),
            ('North Carolina', 'North Carolina'),
            ('North Dakota', 'North Dakota'),
            ('Ohio', 'Ohio'),
            ('Oklahoma', 'Oklahoma'),
            ('Oregon', 'Oregon'),
            ('Pennsylvania', 'Pennsylvania'),
            ('Rhode Island', 'Rhode Island'),
            ('South Carolina', 'South Carolina'),
            ('South Dakota', 'South Dakota'),
            ('Tennessee', 'Tennessee'),
            ('Texas', 'Texas'),
            ('Utah', 'Utah'),
            ('Vermont', 'Vermont'),
            ('Virginia', 'Virginia'),
            ('Washington', 'Washington'),
            ('West Virginia', 'West Virginia'),
            ('Wisconsin', 'Wisconsin'),
            ('Wyoming', 'Wyoming')
        ]
    )
    zipcode = StringField(
        "Zip/Code Postal",
        [wtforms.validators.InputRequired('Veuillez entrer votre code postal')]
    )
    country = SelectField(
        "Pays",
        [wtforms.validators.InputRequired('Veuillez entrer votre pays')],
        choices=[
            ('', ''),
            ('Afghanistan', 'Afghanistan'),
            ('Aland Islands', 'Aland Islands'),
            ('Albania', 'Albania'),
            ('Algeria', 'Algeria'),
            ('American Samoa', 'American Samoa'),
            ('Andorra', 'Andorra'),
            ('Angola', 'Angola'),
            ('Anguilla', 'Anguilla'),
            ('Antarctica', 'Antarctica'),
            ('Antigua And Barbuda', 'Antigua And Barbuda'),
            ('Argentina', 'Argentina'),
            ('Armenia', 'Armenia'),
            ('Aruba', 'Aruba'),
            ('Australia', 'Australia'),
            ('Austria', 'Austria'),
            ('Azerbaijan', 'Azerbaijan'),
            ('Bahamas', 'Bahamas'),
            ('Bahrain', 'Bahrain'),
            ('Bangladesh', 'Bangladesh'),
            ('Barbados', 'Barbados'),
            ('Belarus', 'Belarus'),
            ('Belgium', 'Belgium'),
            ('Belize', 'Belize'),
            ('Benin', 'Benin'),
            ('Bermuda', 'Bermuda'),
            ('Bhutan', 'Bhutan'),
            ('Bolivia', 'Bolivia'),
            ('Bosnia And Herzegovina', 'Bosnia And Herzegovina'),
            ('Botswana', 'Botswana'),
            ('Bouvet Island', 'Bouvet Island'),
            ('Brazil', 'Brazil'),
            (
                'British Indian Ocean Territory',
                'British Indian Ocean Territory'
            ),
            ('Brunei Darussalam', 'Brunei Darussalam'),
            ('Bulgaria', 'Bulgaria'),
            ('Burkina Faso', 'Burkina Faso'),
            ('Burundi', 'Burundi'),
            ('Cambodia', 'Cambodia'),
            ('Cameroon', 'Cameroon'),
            ('Canada', 'Canada'),
            ('Cape Verde', 'Cape Verde'),
            ('Cayman Islands', 'Cayman Islands'),
            ('Central African Republic', 'Central African Republic'),
            ('Chad', 'Chad'),
            ('Chile', 'Chile'),
            ('China', 'China'),
            ('Christmas Island', 'Christmas Island'),
            ('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),
            ('Colombia', 'Colombia'),
            ('Comoros', 'Comoros'),
            ('Congo', 'Congo'),
            (
                'Congo, The Democratic Republic Of The',
                'Congo, The Democratic Republic Of The'
            ),
            ('Cook Islands', 'Cook Islands'),
            ('Costa Rica', 'Costa Rica'),
            ('Cote D\'ivoire', 'Cote D\'ivoire'),
            ('Croatia', 'Croatia'),
            ('Cuba', 'Cuba'),
            ('Cyprus', 'Cyprus'),
            ('Czech Republic', 'Czech Republic'),
            ('Denmark', 'Denmark'),
            ('Djibouti', 'Djibouti'),
            ('Dominica', 'Dominica'),
            ('Dominican Republic', 'Dominican Republic'),
            ('Ecuador', 'Ecuador'),
            ('Egypt', 'Egypt'),
            ('El Salvador', 'El Salvador'),
            ('Equatorial Guinea', 'Equatorial Guinea'),
            ('Eritrea', 'Eritrea'),
            ('Estonia', 'Estonia'),
            ('Ethiopia', 'Ethiopia'),
            ('Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas)'),
            ('Faroe Islands', 'Faroe Islands'),
            ('Fiji', 'Fiji'),
            ('Finland', 'Finland'),
            ('France', 'France'),
            ('French Guiana', 'French Guiana'),
            ('French Polynesia', 'French Polynesia'),
            ('French Southern Territories', 'French Southern Territories'),
            ('Gabon', 'Gabon'),
            ('Gambia', 'Gambia'),
            ('Georgia', 'Georgia'),
            ('Germany', 'Germany'),
            ('Ghana', 'Ghana'),
            ('Gibraltar', 'Gibraltar'),
            ('Greece', 'Greece'),
            ('Greenland', 'Greenland'),
            ('Grenada', 'Grenada'),
            ('Guadeloupe', 'Guadeloupe'),
            ('Guam', 'Guam'),
            ('Guatemala', 'Guatemala'),
            ('Guernsey', 'Guernsey'),
            ('Guinea', 'Guinea'),
            ('Guinea-bissau', 'Guinea-bissau'),
            ('Guyana', 'Guyana'),
            ('Haiti', 'Haiti'),
            (
                'Heard Island And Mcdonald Islands',
                'Heard Island And Mcdonald Islands'
            ),
            ('Holy See (Vatican City State)', 'Holy See (Vatican City State)'),
            ('Honduras', 'Honduras'),
            ('Hong Kong', 'Hong Kong'),
            ('Hungary', 'Hungary'),
            ('Iceland', 'Iceland'),
            ('India', 'India'),
            ('Indonesia', 'Indonesia'),
            ('Iran, Islamic Republic Of', 'Iran, Islamic Republic Of'),
            ('Iraq', 'Iraq'),
            ('Ireland', 'Ireland'),
            ('Isle Of Man', 'Isle Of Man'),
            ('Israel', 'Israel'),
            ('Italy', 'Italy'),
            ('Jamaica', 'Jamaica'),
            ('Japan', 'Japan'),
            ('Jersey', 'Jersey'),
            ('Jordan', 'Jordan'),
            ('Kazakhstan', 'Kazakhstan'),
            ('Kenya', 'Kenya'),
            ('Kiribati', 'Kiribati'),
            (
                'Korea, Democratic People\'s Republic Of',
                'Korea, Democratic People\'s Republic Of'
            ),
            ('Korea, Republic Of', 'Korea, Republic Of'),
            ('Kuwait', 'Kuwait'),
            ('Kyrgyzstan', 'Kyrgyzstan'),
            (
                'Lao People\'s Democratic Republic',
                'Lao People\'s Democratic Republic'
            ),
            ('Latvia', 'Latvia'),
            ('Lebanon', 'Lebanon'),
            ('Lesotho', 'Lesotho'),
            ('Liberia', 'Liberia'),
            ('Libyan Arab Jamahiriya', 'Libyan Arab Jamahiriya'),
            ('Liechtenstein', 'Liechtenstein'),
            ('Lithuania', 'Lithuania'),
            ('Luxembourg', 'Luxembourg'),
            ('Macao', 'Macao'),
            (
                'Macedonia, The Former Yugoslav Republic Of',
                'Macedonia, The Former Yugoslav Republic Of'
            ),
            ('Madagascar', 'Madagascar'),
            ('Malawi', 'Malawi'),
            ('Malaysia', 'Malaysia'),
            ('Maldives', 'Maldives'),
            ('Mali', 'Mali'),
            ('Malta', 'Malta'),
            ('Marshall Islands', 'Marshall Islands'),
            ('Martinique', 'Martinique'),
            ('Mauritania', 'Mauritania'),
            ('Mauritius', 'Mauritius'),
            ('Mayotte', 'Mayotte'),
            ('Mexico', 'Mexico'),
            (
                'Micronesia, Federated States Of',
                'Micronesia, Federated States Of'
            ),
            ('Moldova, Republic Of', 'Moldova, Republic Of'),
            ('Monaco', 'Monaco'),
            ('Mongolia', 'Mongolia'),
            ('Montenegro', 'Montenegro'),
            ('Montserrat', 'Montserrat'),
            ('Morocco', 'Morocco'),
            ('Mozambique', 'Mozambique'),
            ('Myanmar', 'Myanmar'),
            ('Namibia', 'Namibia'),
            ('Nauru', 'Nauru'),
            ('Nepal', 'Nepal'),
            ('Netherlands', 'Netherlands'),
            ('Netherlands Antilles', 'Netherlands Antilles'),
            ('New Caledonia', 'New Caledonia'),
            ('New Zealand', 'New Zealand'),
            ('Nicaragua', 'Nicaragua'),
            ('Niger', 'Niger'),
            ('Nigeria', 'Nigeria'),
            ('Niue', 'Niue'),
            ('Norfolk Island', 'Norfolk Island'),
            ('Northern Mariana Islands', 'Northern Mariana Islands'),
            ('Norway', 'Norway'),
            ('Oman', 'Oman'),
            ('Pakistan', 'Pakistan'),
            ('Palau', 'Palau'),
            (
                'Palestinian Territory, Occupied',
                'Palestinian Territory, Occupied'
            ),
            ('Panama', 'Panama'),
            ('Papua New Guinea', 'Papua New Guinea'),
            ('Paraguay', 'Paraguay'),
            ('Peru', 'Peru'),
            ('Philippines', 'Philippines'),
            ('Pitcairn', 'Pitcairn'),
            ('Poland', 'Poland'),
            ('Portugal', 'Portugal'),
            ('Puerto Rico', 'Puerto Rico'),
            ('Qatar', 'Qatar'),
            ('Reunion', 'Reunion'),
            ('Romania', 'Romania'),
            ('Russian Federation', 'Russian Federation'),
            ('Rwanda', 'Rwanda'),
            ('Saint Helena', 'Saint Helena'),
            ('Saint Kitts And Nevis', 'Saint Kitts And Nevis'),
            ('Saint Lucia', 'Saint Lucia'),
            ('Saint Pierre And Miquelon', 'Saint Pierre And Miquelon'),
            (
                'Saint Vincent And The Grenadines',
                'Saint Vincent And The Grenadines'
            ),
            ('Samoa', 'Samoa'),
            ('San Marino', 'San Marino'),
            ('Sao Tome And Principe', 'Sao Tome And Principe'),
            ('Saudi Arabia', 'Saudi Arabia'),
            ('Senegal', 'Senegal'),
            ('Serbia', 'Serbia'),
            ('Seychelles', 'Seychelles'),
            ('Sierra Leone', 'Sierra Leone'),
            ('Singapore', 'Singapore'),
            ('Slovakia', 'Slovakia'),
            ('Slovenia', 'Slovenia'),
            ('Solomon Islands', 'Solomon Islands'),
            ('Somalia', 'Somalia'),
            ('South Africa', 'South Africa'),
            (
                'South Georgia And The South Sandwich Islands',
                'South Georgia And The South Sandwich Islands'
            ),
            ('Spain', 'Spain'),
            ('Sri Lanka', 'Sri Lanka'),
            ('Sudan', 'Sudan'),
            ('Suriname', 'Suriname'),
            ('Svalbard And Jan Mayen', 'Svalbard And Jan Mayen'),
            ('Swaziland', 'Swaziland'),
            ('Sweden', 'Sweden'),
            ('Switzerland', 'Switzerland'),
            ('Syrian Arab Republic', 'Syrian Arab Republic'),
            ('Taiwan, Province Of China', 'Taiwan, Province Of China'),
            ('Tajikistan', 'Tajikistan'),
            ('Tanzania, United Republic Of', 'Tanzania, United Republic Of'),
            ('Thailand', 'Thailand'),
            ('Timor-leste', 'Timor-leste'),
            ('Togo', 'Togo'),
            ('Tokelau', 'Tokelau'),
            ('Tonga', 'Tonga'),
            ('Trinidad And Tobago', 'Trinidad And Tobago'),
            ('Tunisia', 'Tunisia'),
            ('Turkey', 'Turkey'),
            ('Turkmenistan', 'Turkmenistan'),
            ('Turks And Caicos Islands', 'Turks And Caicos Islands'),
            ('Tuvalu', 'Tuvalu'),
            ('Uganda', 'Uganda'),
            ('Ukraine', 'Ukraine'),
            ('United Arab Emirates', 'United Arab Emirates'),
            ('United Kingdom', 'United Kingdom'),
            ('United States', 'United States'),
            (
                'United States Minor Outlying Islands',
                'United States Minor Outlying Islands'
            ),
            ('Uruguay', 'Uruguay'),
            ('Uzbekistan', 'Uzbekistan'),
            ('Vanuatu', 'Vanuatu'),
            ('Venezuela', 'Venezuela'),
            ('Viet Nam', 'Viet Nam'),
            ('Virgin Islands, British', 'Virgin Islands, British'),
            ('Virgin Islands, U.S.', 'Virgin Islands, U.S.'),
            ('Wallis And Futuna', 'Wallis And Futuna'),
            ('Western Sahara', 'Western Sahara'),
            ('Yemen', 'Yemen'),
            ('Zambia', 'Zambia'),
            ('Zimbabwe', 'Zimbabwe')
        ]
    )


class ReferForm(FlaskForm):
    visitorname = StringField(
        "Your name",
        [wtforms.validators.InputRequired('Please enter your name')]
    )
    visitoremail = StringField(
        "Your email",
        [
            wtforms.validators.InputRequired('Please enter your email'),
            wtforms.validators.Email()
        ]
    )
    friendname = StringField(
        "Your friend's name",
        [wtforms.validators.InputRequired('Please enter your friend&apos;s name')]
    )
    friendemail = StringField(
        "Your friend's email",
        [
            wtforms.validators.InputRequired(
                'Please enter your friend&apos;s email'
            ),
            wtforms.validators.Email()
        ]
    )


class FrenchReferForm(FlaskForm):
    visitorname = StringField(
        "Votre nom",
        [wtforms.validators.InputRequired('Veuillez entrer votre nom')]
    )
    visitoremail = StringField(
        "Votre adresse de courriel",
        [
            wtforms.validators.InputRequired(
                'Veuillez entrer votre adresse de courriel'
            ),
            wtforms.validators.Email()
        ]
    )
    friendname = StringField(
        "Le nom de votre amie",
        [wtforms.validators.InputRequired('Veuillez entrer le nom de votre amie')]
    )
    friendemail = StringField(
        "Son adresse de courriel",
        [
            wtforms.validators.InputRequired(
                'Veuillez entrer son adresse de courriel'
            ),
            wtforms.validators.Email()
        ]
    )
