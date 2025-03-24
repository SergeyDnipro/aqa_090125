from __future__ import unicode_literals
import sys, glob, csv, pytz, shutil
from os import listdir, getcwd, access, W_OK
from os.path import abspath, join, dirname, split, exists, isfile, isdir
sys.path.append("/randominfo/")
from random import randint, choice, sample, randrange
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from math import ceil


__title__ = 'randominfo'
__version__ = '2.0.2'
__author__ = 'Bhuvan Gandhi'
__license__ = 'MIT'

full_path = lambda filename: abspath(join(dirname(__file__), filename))

def load_dataset(file=None):
	if not file:
		file = open(full_path('data.csv'), 'r', newline='')
		csv_file = csv.reader(file)
		# print('Open file in method')
		return csv_file, file
	csv_file = csv.reader(file)
	# print('class instance read file')
	return csv_file, file

def file_postprocessing(*, current_file_obj, passed_file_obj=None):
	current_file_obj.seek(0)
	if not passed_file_obj:
		current_file_obj.close()

def get_id(length = 6, seq_number = None, step = 1, prefix = None, postfix = None):
	generated_id = ""
	if seq_number == None:
		for _ in range(length):
			generated_id += str(randint(0,9))
	else:
		if type(seq_number).__name__ != 'int' or type(step).__name__ != 'int':
			raise TypeError("Sequence number must be an integer.")
		else:
			generated_id = str(seq_number + step)
	if prefix != None:
		prefix += generated_id
		generated_id = prefix
	if postfix != None:
		generated_id += postfix
	return generated_id

def get_first_name(gender=None, passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	gender_list = ["male", "female"]
	if gender is not None and gender not in gender_list:
		raise ValueError("Enter valid gender: 'male' or 'female'.")
	first_name_list = []
	for data in csv_file:
		if gender is None:
			first_name_list.append(data[0]) if data[0] != '' else None
		elif gender.lower() == data[2]:
			first_name_list.append(data[0])

	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return choice(first_name_list)

def get_last_name(passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	last_name_list = []
	for data in csv_file:
		last_name_list.append(data[1]) if data[1] != '' else None
	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return choice(last_name_list)

def get_gender(first_name, passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	gender = "N/A"
	for data in csv_file:
		if data[0] == first_name:
			gender = data[2]
			break
	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return gender

def get_country(first_name = None, passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	country = "N/A"
	if first_name is not None:
		for data in csv_file:
			if data[0] == first_name:
				country = data[9]
				break
		if country == "N/A":
			print("Specified user data is not available. Tip: Generate random country.")
	else:
		countries_set = set()
		for data in csv_file:
			if data[9] != '':
				countries_set.add(data[9])
		country = choice(list(countries_set))
	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return country

def get_full_name(gender = None):
	return get_first_name(gender) + " " + get_last_name()

def get_otp(length = 6, digit = True, alpha = True, lowercase = True, uppercase = True):
	lwrChars = "qwertyuioplkjhgfdsazxcvbnm"
	uprChars = "QWERTYUIOPLKJHGFDSAZXCVBNM"
	digs = "0123456789"
	chars = ""
	otp = ""
	if digit != False or alpha != False:
		if digit == True:
			chars += digs
		if alpha == True:
			if lowercase == True:
				chars += lwrChars
			if uppercase == True:
				chars += uprChars
		for _ in range(length):
			otp += str(chars[randint(0, len(chars) - 1)])
		return otp
	else:
		raise ValueError("From parameters 'digit' and 'alpha' anyone must be True.")

def get_formatted_datetime(outFormat, strDate, strFormat = "%d-%m-%Y %H:%M:%S"):
    return datetime.strptime(strDate, strFormat).strftime(outFormat)

def get_email(person_instance = None):
	domains = ["gmail", "yahoo", "hotmail", "express", "yandex", "nexus", "online", "omega", "institute", "finance", "company", "corporation", "community"]
	extentions = ['com', 'in', 'jp', 'us', 'uk', 'org', 'edu', 'au', 'de', 'co', 'me', 'biz', 'dev', 'ngo', 'site', 'xyz', 'zero', 'tech']

	if person_instance is None:
		person_instance = Person()

	c = randint(0,2)
	dmn = '@' + choice(domains)
	ext = choice(extentions)

	if c == 0:
		email = person_instance.first_name + get_formatted_datetime("%Y", person_instance.birthdate, "%d %b, %Y") + dmn + "." + ext
	elif c == 1:
		email = person_instance.last_name + get_formatted_datetime("%d", person_instance.birthdate, "%d %b, %Y") + dmn + "." + ext
	else:
		email = person_instance.first_name + get_formatted_datetime("%y", person_instance.birthdate, "%d %b, %Y") + dmn + "." + ext
	return email

def random_password(length = 8, special_chars = True, digits = True):
	spec_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
	alpha = "QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq"
	spec_char_len = dig_char_len = 0
	chars = ""
	paswd = ""
	if special_chars == True:
		spec_char_len = randint(1,ceil(length/4))
		for _ in range(spec_char_len):
			chars += choice(spec_chars)
	if digits == True:
		dig_char_len = randint(1,ceil(length/3))
		for _ in range(dig_char_len):
			chars += str(randint(0,9))
	for _ in range(length - (dig_char_len + spec_char_len)):
		chars += choice(alpha[randint(0, len(alpha) - 1)])

	paswd = ''.join(sample(chars, len(chars)))
	return paswd

def get_phone_number(country_code = True):
    phone = ""
    if country_code == True:
        cCodes = [91, 144, 141, 1, 44, 86, 52, 61, 32, 20, 33, 62, 81, 31, 7]
        phone = "+"
        phone += str(choice(cCodes))
        phone += " "
    for i in range(0,10):
        if i == 0:
            phone += str(randint(6,9))
        else:
            phone += str(randint(0,9))
    return phone

def get_alphabetic_profile_img(char, filePath, imgName, charColor = None, bgColor = None):
	chars = "qwertyuioplkjhgfdsazxcvbnmQAZXSWEDCVFRTGBNHYUJMKLIOP0123456789 ,.+=-_()[]{}"
	if all((c in chars) for c in imgName):
		if access(dirname(filePath), W_OK):
			if charColor != None:
				if not charColor.isalpha():
					raise ValueError("Character color must be a name of color.")
			if bgColor != None:
				if not bgColor.isalpha():
					raise ValueError("Background color must be a name of color.")
			char = char[:1].upper()
			if bgColor == None:
				colors = ['red', 'green', 'royalblue', 'violet', 'pink', 'indigo', 'grey', 'yellowgreen', 'teal']
				bgColor = choice(colors)
			if charColor == None:
				charColor = (40, 40, 40)
			img = Image.new('RGB', (512, 512), color = bgColor)
			d = ImageDraw.Draw(img)
			font = ImageFont.truetype("Candara.ttf", 280)
			d.text((170,140), char, fill=charColor, font = font)
			filePath = filePath + "\\" + str(imgName) + ".jpg"
			img.save(filePath)
		else:
			raise OSError("Invalid or insufficient privileges for specified file path.")
	else:
		raise OSError("Invalid image name. Image name must contains characher including digits, alphabets, white space, dot, comma, ( ) [ ] { } _ + - =.")
	return filePath

def get_face_profile_img(filePath, imgName, gender = None):
	dir_name, file_name = split(abspath(__file__))
	chars = "qwertyuioplkjhgfdsazxcvbnmQAZXSWEDCVFRTGBNHYUJMKLIOP0123456789 ,.+=-_()[]{}"
	if all((c in chars) for c in imgName):
		if access(dirname(filePath), W_OK):
			if gender == None:
				orig_file = choice(glob.glob(dir_name + "\\images\\people\\*.jpg"))
			elif gender.lower() == "female":
				orig_file = choice(glob.glob(dir_name + "\\images\\people\\female_*.jpg"))
			elif gender.lower() == "male":
				orig_file = choice(glob.glob(dir_name + "\\images\\people\\male_*.jpg"))
			else:
				return ValueError("Invalid gender. It must be male or female.")
			return shutil.copy(orig_file, filePath + "\\" + str(imgName) + ".jpg")
		else:
			raise OSError("Invalid or insufficient privileges for specified file path.")
	else:
		raise OSError("Invalid image name. Image name must contains characher including digits, alphabets, white space, dot, comma, ( ) [ ] { } _ + - =.")

startRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
endRange = datetime.today()

def get_today(_format = "%d-%m-%Y %H:%M:%S"):
	return datetime.today().strftime(_format)

def get_date(tstamp = None, _format = "%d %b, %Y"):
	if tstamp == None:
		startTs = startRange.timestamp()
		endTs = datetime.timestamp(endRange)
		tstamp = randrange(int(startTs), int(endTs))
	else:
		if type(tstamp).__name__ != 'int':
			raise ValueError("Timestamp must be an integer.")
	return datetime.utcfromtimestamp(tstamp).strftime(_format)

def get_birthdate(startAge = None, endAge = None, _format = "%d %b, %Y"):
	startRange = datetime.today()
	endRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
	if startAge != None:
		if type(startAge).__name__ != 'int':
			raise ValueError("Starting age value must be integer.")
	if endAge != None:
		if type(endAge).__name__ != 'int':
			raise ValueError("Ending age value must be integer.")
	if startAge != None and endAge != None: #If both are given in arg
		if startAge >= endAge:
			raise ValueError("Starting age must be less than ending age.")
		else:
			startRange = datetime(datetime.now().year - startAge, 12, 31, 23, 59, 59, 0, pytz.UTC)
			endRange = datetime(datetime.now().year - endAge, 1, 1, 0, 0, 0, 0, pytz.UTC)
	elif startAge != None or endAge != None: #If anyone is given in arg
		ageYear = startAge if startAge != None else endAge
		startRange = datetime(datetime.now().year - ageYear, 12, 31, 23, 59, 59, 0, pytz.UTC)
		endRange = datetime(datetime.now().year - ageYear, 1, 1, 0, 0, 0, 0, pytz.UTC)
	else:
		pass
	startTs = startRange.timestamp()
	endTs = endRange.timestamp()
	return datetime.fromtimestamp(randrange(int(endTs), int(startTs))).strftime(_format)

def get_address(passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	address_params = ['street', 'landmark', 'area', 'city', 'state', 'country', 'pincode']
	all_addresses_list = []
	for data in csv_file:
		current_address = []
		if data[0] == 'firstname':
			continue
		for i in range(4, 11):

			if data[i] != '':
				current_address.append(data[i])
			else:
				current_address.append(choice(all_addresses_list)[i - 4])
		all_addresses_list.append(current_address)
	chosen_address = choice(all_addresses_list)
	full_address = dict(zip(address_params, chosen_address))
	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return full_address

def get_hobbies(passed_file_obj=None):
	csv_file, current_file_obj = load_dataset(passed_file_obj)
	hobbies_set = set()
	for data in csv_file:
		if data[3] != '':
			hobbies_set.add(data[3])
	hobbies = []
	for _ in range (1, randint(2,6)):
		hobbies.append(choice(list(hobbies_set)))
	file_postprocessing(current_file_obj=current_file_obj, passed_file_obj=passed_file_obj)
	return hobbies

class Person:
	def __init__(self):
		self.data_file = open(full_path('data.csv'), 'r', newline='')
		self.first_name = get_first_name(passed_file_obj=self.data_file)
		self.last_name = get_last_name(passed_file_obj=self.data_file)
		self.full_name = self.first_name + " " + self.last_name
		self.birthdate = get_birthdate()
		self.phone = get_phone_number()
		self.email = get_email(self)
		self.gender = get_gender(self.first_name, passed_file_obj=self.data_file)
		self.country = get_country(self.first_name, passed_file_obj=self.data_file)
		self.paswd = random_password()
		self.hobbies = get_hobbies(passed_file_obj=self.data_file)
		self.address = get_address(passed_file_obj=self.data_file)
		self.customAttr = {}
		self.data_file.close()

	def set_attr(self, attr_name, value = None):
		if attr_name.isalnum():
			if attr_name[0].isalpha():
				self.customAttr[attr_name] = value
				print("Attribute '" + str(attr_name) + "' added.")
			else:
				raise ValueError("First character of attribute must be an alphabet.")
		else:
			raise ValueError("Attribute name only contains alphabets and digits.")

	def get_attr(self, attr_name):
		if attr_name.isalnum():
			if attr_name[0].isalpha():
				if attr_name in self.customAttr.keys():
					return self.customAttr[attr_name]
				else:
					raise AttributeError("Specified attribute is not exists.")
			else:
				raise ValueError("First character of attribute must be an alphabet.")
		else:
			raise ValueError("Attribute name only contains alphabets and digits.")

	def get_details(self):
		return {
			"first_name": self.first_name,
			"last_name": self.last_name,
			"full_name": self.full_name,
			"birthdate": self.birthdate,
			"gender": self.gender,
			"email": self.email,
			"phone": self.phone,
			"paswd": self.paswd,
			"country": self.country,
			"hobbies": self.hobbies,
			"address": self.address,
			"other_attr": self.customAttr
		}

'''
REFERENCE:
http://www.first-names-meanings.com/country-indian-names.html
https://www.familyeducation.com/baby-names/browse-origin/surname/indian
https://thispersondoesnotexist.com/
https://en.wikipedia.org/wiki/List_of_hobbies
'''
