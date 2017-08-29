#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "1.0.2"
import sys
import os
import re
import telebot
import requests
import time
from random import choice
from suds.client import Client
from telebot import util,types
reload(sys)  
sys.setdefaultencoding("utf-8")
#		|Config 	#
import redis as Redis
redis = Redis.StrictRedis(host='localhost', port=6379, db=0)
channel_id = -1001085877059	# id channel shoma
admins = [256312423,308158149]	# id admin (ha)
onlines = []
merchent = ''	# az tariq zarinpal eqdam be daryaft merchentid konid va inja qarar bedid
token = '308350587:AAGaqDeSs8oFtSTcan8QG-Cb__AlEp7VDIM'	#token
debug_mode = False
debug_user = 256312423	# id man hast , baraye daryaft error
#		Config|		#
bot = telebot.TeleBot(token)
botid = bot.get_me().id
botuser = bot.get_me().username
botname = bot.get_me().first_name
#------------- Strings ----
firststart = '''سلام [{}] 😉
➖➖➖➖➖

🔖به ربات گپ ناشناس خوش اومدی😍

🔹به وسیله این ربات میتونید با افراد دیگه  اونم به صورت ناشناس صحبت کنید😁

🔸باهم دیگه گپ بزنید و گفت گو کنید بدون این که طرف مقابلت رو بشناسی😆
➖➖➖➖
🔻ابتدا جنسیت خودت رو مشخص کن😃

⚠️یادت باشه جنسیت درست رو انتخاب کنی چون این اقدام دیگه قابل برگشت نیست✔️'''
starttext = '''به بخش دوم خوش اومدی❤️
➖➖➖➖➖
🔹این بخش اصلی رباته تو میتونی به وسیله این بخش با افراد دیگه به صورت ناشناس صحبت کنید🎉

🔸برای شروع کافیه از دکمه شروع چت استفاده کنید تا من شما رو به یکی وصل کنم☺️
➖➖➖➖➖➖
🔖دقت داشته باش اگه میخوای جنسیت طرف مقابلت رو انتخاب کنی باید ربات رو برای خودت ویژه کنید'''
forcejoin = '''🔖برای حمایت از ما و حمایت از اسپانسر ربات کافیه در کانال زیر عضو شوید✔️

🔸ایدی کانال @pouyazamani 🔹

✨سپس به ربات برگشته عبارت :
🔹 /start 🔸

را ارسال کنید تا از امکانات فوق العاده ربات گپ ناشناس بهر مند شوید😉😍'''

buy_vip = '''✨امکانات ویژه کردن ربات :

🚦امکان انتخاب کردن جنسیت طرف مقابل برای شروع گفت گو

💭امکان ارسال انواع رسانه ماننده عکس و فیلم در گفت گو ها
و..

🔻برای ویژه کردن ربات برای خود از دکمه های زیر استفاده کن'''

share = '''
حوصلت سر رفته؟🤔

🔴 با این ربات زیر می‌تونی هر لحظه خواستی تصادفی به یک نفر(دختر یا پسر) وصل بشی و ناشناس باهاش گپ بزنی!😍

برای شروع کلیک کنید👇🏻

https://telegram.me/{}?start={}'''

alreadystarted = '''شما در حال حاضر در ربات عضو هستید!'''
#--------------Defines-----
#	Pay :
def checks(c):
	try:
		client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
		result = client.service.PaymentVerification(merchent,
                                                    c,
                                                    5000)
		if result.Status == 100 or result.Status == 101:
			return True
		else:
			return False
	except Exception as e:
		debug(e)
def buy(amount):
	try:
		client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
		result = client.service.PaymentRequest(merchent,
                                           amount,
                                           u'وضیح تراکنش',
                                           'یه ایمیل بده',
                                           'یه شماره بده',
                                           'https://t.me/'+botuser+'?start=check')
		if result.Status == 100:
			return result.Authority
	except Exception as e:
		debug(e)
#	#	#
def joined(user_id):
	try:
		print 'joined func started'
		userinfo = bot.get_chat_member(channel_id,user_id).status
		if (userinfo != 'left') or user_id in admins:
			return True
		else:
			bot.send_message(user_id)
		print 'joined func Finished'
	except Exception as e:
		debug(e)
		
def online_chat_request(user_id):
	try:
		user1_id = user_id
		user1_gen = redis.hget('secretchat:usergen',user_id)
		print 'user 1 id and gen : ' + str(user1_id) + str(user1_gen)
		print onlines
		if len(onlines) > 1:
			print 'len > 1'
			gen = redis.hget('secretchat:selectedgen',user_id)
			print 'looking gen : ' + str(gen)
			random = choice(onlines)
			print random
			user2_id = random.split(':')[0]
			user2_gen = redis.hget('secretchat:usergen',user2_id)
			print 'user 2 id and gen : ' + str(user2_id) + str(user2_gen)
			if int(user2_id) == int(user1_id):
				return online_chat_request(user_id)
			else:
				if gen == 'any':
					user1 = str(user1_id)+':'+str(user1_gen)
					print 'user 1 : '+ user1
					onlines.remove(user1)
					user2 = str(user2_id)+':'+str(user2_gen)
					print 'user 2 : ' + user2
					onlines.remove(user2)
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					endchat = types.KeyboardButton('🔚 پایان چت 🔚')
					markup.add(endchat)
					bot.send_message(int(user1_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜',reply_markup=markup)
					bot.send_message(int(user2_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜',reply_markup=markup)
					redis.incr('secretchat:maxtry:user-'+str(user1_id))
					redis.incr('secretchat:maxtry:user-'+str(user2_id))
					redis.hset('secretchat:inchat',int(user1_id),int(user2_id))
					redis.hset('secretchat:inchat',int(user2_id),int(user1_id))
					redis.hdel('secretchat:cancelchatfix',int(user1_id))
					redis.hdel('secretchat:cancelchatfix',int(user2_id))
					print 'online chat request func Done'
					pass
				if gen == 'male':
					if user2_gen == gen:
						user1 = str(user1_id)+':'+str(user1_gen)
						print user1
						onlines.remove(user1)
						user2 = str(user2_id)+':'+str(user2_gen)
						onlines.remove(user2)
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						endchat = types.KeyboardButton('🔚 پایان چت 🔚')
						markup.add(endchat)
						bot.send_message(int(user1_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜',reply_markup=markup)
						bot.send_message(int(user2_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜'+str(user1_id),reply_markup=markup)
						redis.incr('secretchat:maxtry:user-'+str(user1_id))
						redis.incr('secretchat:maxtry:user-'+str(user2_id))
						redis.hset('secretchat:inchat',int(user1_id),int(user2_id))
						redis.hset('secretchat:inchat',int(user2_id),int(user1_id))
						redis.hdel('secretchat:cancelchatfix',int(user1_id))
						redis.hdel('secretchat:cancelchatfix',int(user2_id))
						print 'online chat request func Done'
						pass
					else:
						time.sleep(2)
						return online_chat_request(user1_id)
				if gen == 'female':
					if user2_gen == gen:
						user1 = str(user1_id)+':'+str(user1_gen)
						print user1
						onlines.remove(user1)
						user2 = str(user2_id)+':'+str(user2_gen)
						onlines.remove(user2)
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						endchat = types.KeyboardButton('🔚 پایان چت 🔚')
						markup.add(endchat)
						bot.send_message(int(user1_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜',reply_markup=markup)
						bot.send_message(int(user2_id),'شما با موفقیت متصل شدید😃\nشروع به گپ زدن کنید با رعایت ادب☺️\nبه مخاطب ناشناس سلام کن😜',reply_markup=markup)
						redis.incr('secretchat:maxtry:user-'+str(user1_id))
						redis.incr('secretchat:maxtry:user-'+str(user2_id))
						redis.hset('secretchat:inchat',int(user1_id),int(user2_id))
						redis.hset('secretchat:inchat',int(user2_id),int(user1_id))
						redis.hdel('secretchat:cancelchatfix',int(user1_id))
						redis.hdel('secretchat:cancelchatfix',int(user2_id))
						print 'online chat request func Done'
						pass
					else:
						time.sleep(2)
						return online_chat_request(user1_id)
		else:
			bot.send_message(user_id,'شما در لیست انتظار قرار گرفتید✔️\nلطفا کمی صبر کنید به زودی شما رو به یک نفر وصل میکنم😊')
	except Exception as e:
		debug(e)
		
def vip(user_id):
	try:
		print 'vip func started'
		vip_user = redis.sismember('secretchat:vip',user_id)
		print 'vip '+str(vip_user)
		if vip_user or user_id in admins:
			return True
		else:
			return False
		print 'online chat request func finished'
		
	except Exception as e:
		debug(e)
		

def can_use(user_id):
	try:
		print 'can_use func started'
		max = redis.get('secretchat:maxtry:user-'+str(user_id))
		print 'can_use '+str(max)
		if max is not None and int(max) > 5:
			return False
		else:
			return True
		print 'can_use func finished'
	except Exception as e:
		debug(e)
	
def user_invited(user_id):
	try:
		print 'user_invited func started'
		users = redis.scard('secretchat:invited:user'+str(user_id))
		print 'user_invited '+str(users)
		if int(users) > 4:
			return True
			print True
		else:
			return False
			print False
	except Exception as e:
		debug(e)
		
def debug(input):
	if debug_mode is None:
		print 'YOU MUST ENTER debug_mode TO True OR False First!'
	elif debug_mode == True:
		try:
			bot.send_message(debug_user,input)
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#bot.send_message(LOGCHAT, "Something wrong!\nType : "+str(exc_type)+"\nLine : "+str(exc_tb.tb_lineno)+"\nError : "+str(e))
		except:
			print 'PLEASE ENTER CORRECT USER_ID IN debug_user!'
#--------------------------
#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#
@bot.message_handler(content_types=['audio', 'video', 'document', 'text', 'contact', 'sticker', 'photo', 'voice'])

def start(m):
	try:
		print 'main func started'
		inchatid = redis.hget('secretchat:inchat',m.from_user.id)
		if inchatid:
			print 'main func in chat'
			askforend = redis.hget('secretchat:askforend',m.from_user.id)
			if askforend:
				pass
			else:
				print 'main func not in chat'
				if m.text:
					if m.text == '🔚 پایان چت 🔚':
						print 'main func stop chat'
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						yes = types.KeyboardButton('بله ✅')
						no = types.KeyboardButton('نه ❌')
						markup.add(yes)
						markup.add(no)
						redis.hset('secretchat:askforend',m.from_user.id,True)
						user1 = redis.hget('secretchat:inchat',m.from_user.id)
						redis.hset('secretchat:askforend',user1,True)
						msg = bot.send_message(m.from_user.id,'🔹ایا مطمعن هستید میخواهید که گفت گو رو با این شخص اتمام دهید؟',reply_markup=markup)
						bot.register_next_step_handler(msg,stopchat)
					else:
						print 'main func send to other chat partner'
						bot.send_message(inchatid,m.text)
				if m.audio:
					print 'main func send audio'
					if vip(m.from_user.id):
						bot.send_audio(inchatid,m.audio.file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
				if m.voice:
					print 'main func send voice'
					if vip(m.from_user.id):
						bot.send_voice(inchatid,m.voice.file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
				if m.video:
					print 'main func send video'
					if vip(m.from_user.id):
						bot.send_video(inchatid,m.video.file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
				if m.document:
					print 'main func send doc'
					if vip(m.from_user.id):
						bot.send_document(inchatid,m.document.file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
				if m.sticker:
					print 'main func send sticker'
					if vip(m.from_user.id):
						bot.send_sticker(inchatid,m.sticker.file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
				if m.photo:
					print 'main func send photo'
					if vip(m.from_user.id):
						bot.send_audio(inchatid,m.photo[0].file_id)
					else:
						bot.send_message(m.chat.id,'امکان ارسال رسانه در نسخه رایگان در ربات وجود ندارد❌\n➖➖➖\n🔹جهت فعال کردن نسخه ویژه و ارسال انواع رسانه ماننده عکس , فیلم و فایل ... پس از اتمام گفت گو به بخش ویژه کردن ربات مراجعه گنید')
		else:
			if m.text:
				if m.text == '/panel':
					if m.from_user.id in admins:
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						stats = types.KeyboardButton('آمار ربات')
						bcall = types.KeyboardButton('ارسال پیام همگانی')
						fwdall = types.KeyboardButton('فوروارد پیام همگانی')
						addvip = types.KeyboardButton('افزودن وی آی پی')
						back = types.KeyboardButton('بازگشت به منوی اصلی')
						markup.add(stats)
						markup.add(bcall)
						markup.add(fwdall)
						markup.add(addvip)
						markup.add(back)
						msg = bot.send_message(m.chat.id,'خوش آمدید ادمین عزیز!\nلطفا انتخاب فرمایید:',reply_markup=markup)
						bot.register_next_step_handler(msg,adminpanel)
				#	Stats	|>>
				elif m.text == '/stats':
					stats = redis.scard('secretchat:users')
					vipusers = redis.scard('secretchat:vip')
					bot.send_message(m.from_user.id,'کاربران ربات تا کنون : {}\nکاربران آنلاین : {}\nکاربران وی آی پی : {}'.format(str(stats),str(len(onlines)),str(vipusers)))
				#	Stats 	<<|
				#	Start Message |>>
				elif m.text.startswith('/start'):
					print 'text is start'
					if len(m.text) == 6:
						print 'len is 6'
						redis.sadd('secretchat:users',m.from_user.id)
						print 'main func start command start'
						usergen = redis.hget('secretchat:usergen',m.from_user.id)
						if usergen:
							print 'main func user selected gen'
							if joined(m.from_user.id):
								markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
								startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
								buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
								about = types.KeyboardButton('🔹 درباره ما')
								sup = types.KeyboardButton('🔸 پشتیبانی')
								markup.add(startchat)
								markup.add(buyvipkey)
								markup.add(about,sup)
								bot.send_message(m.chat.id,starttext.format(m.from_user.first_name),reply_markup=markup)
							else:
								markup = types.InlineKeyboardMarkup()
								joinlink = types.InlineKeyboardButton("🚩 عضویت در کانال", url="https://telegram.me/pouyazamani")
								markup.add(joinlink)
								bot.send_message(m.chat.id,forcejoin,reply_markup=markup)
						else:
							print 'main func not selected gen'
							markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
							boy = types.KeyboardButton('👨‍💼 پسر')
							girl = types.KeyboardButton('👩‍💼 دختر')
							markup.add(boy,girl)
							msg = bot.send_message(m.chat.id,firststart.format(m.from_user.first_name),reply_markup=markup)
							bot.register_next_step_handler(msg,save_boy_girl)
					elif len(m.text) > 6:
						text2 = m.text.split()[1]
						print 'len is not 6'
						if not text2.isdigit():
							if checks(redis.hget('secretchat:links',m.from_user.id)):
								bot.send_message(m.chat.id,'پرداخت موفقیت آمیز بود!\nحساب شما وی آی پی شد!')
								redis.sadd('secretchat:vip',m.from_user.id)
							else:
								bot.send_message(m.chat.id,'پرداخت انجان نشده است!')
						
						else:
							user = m.text.replace('/start ','')
							now = m.from_user.id
							db = redis.sismember('secretchat:users',now)
							if db:
								print 'is in db'
								markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
								startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
								buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
								about = types.KeyboardButton('🔹 درباره ما')
								sup = types.KeyboardButton('🔸 پشتیبانی')
								markup.add(startchat)
								markup.add(buyvipkey)
								markup.add(about,sup)
								bot.send_message(m.chat.id,alreadystarted,reply_markup=markup)
							else:
								print 'is not in db'
								usergen = redis.hget('secretchat:usergen',m.from_user.id)
								if usergen:
									print 'main func user selected gen'
									markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
									startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
									buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
									about = types.KeyboardButton('🔹 درباره ما')
									sup = types.KeyboardButton('🔸 پشتیبانی')
									markup.add(startchat)
									markup.add(buyvipkey)
									markup.add(about,sup)
									bot.send_message(m.chat.id,starttext.format(m.from_user.first_name),reply_markup=markup)
								else:
									print 'main func not selected gen'
									markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
									boy = types.KeyboardButton('👨‍💼 پسر')
									girl = types.KeyboardButton('👩‍💼 دختر')
									markup.add(boy,girl)
									invitedbyotheruser = int(redis.scard('secretchat:invited:user'+str(user)))
									if invitedbyotheruser < 5:
										countdown = int(4 - invitedbyotheruser)
										bot.send_message(user,'تبریک !\nیک کاربر با استفاده از لینک شما در ربات عضو شد!\n\nبرای رفع محدودیت باید {} کاربر دیگر را به ربات دعوت کنید !'.format(countdown))
									if invitedbyotheruser == 4:
										bot.send_message(user,'تبریک !\n۵ نفر با استفاده از لینک شما عضو ربات شدند !\nهم اکنون میتوانید چت کردن را شروع کنید !\nلذت ببرید ')
									msg = bot.send_message(m.chat.id,firststart.format(m.from_user.first_name),reply_markup=markup)
									bot.register_next_step_handler(msg,save_boy_girl)
									redis.sadd('secretchat:users',m.from_user.id)
									redis.sadd('secretchat:invited:user'+(user),m.from_user.id)
				#	Start Message <<|
				#	 Start Chat |>>
				elif m.text == '💁 شروع چت 💁‍♂':
								#	gen = redis.hget('secretchat:selectedgen',user_id)
					if joined(m.from_user.id):
						if vip(m.from_user.id):
							markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
							girl = types.KeyboardButton('👩 دختر')
							boy = types.KeyboardButton('👱 پسر')
							any = types.KeyboardButton('👤 فرقی نداره')
							back = types.KeyboardButton('🔚 برگشت')
							markup.add(girl,boy)
							markup.add(any,back)
						else:
							markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
							girl = types.KeyboardButton('👩 دختر')
							boy = types.KeyboardButton('👱 پسر')
							any = types.KeyboardButton('👤 فرقی نداره')
							back = types.KeyboardButton('🔚 برگشت')
							markup.add(girl,boy)
							markup.add(any,back)
						msg = bot.send_message(m.from_user.id,'به بخش شروع چت خوش امدید🌹\n➖➖➖➖➖\n🔖لطفا جنسیت طرف مقابل که میخوای باهاش چت کنی رو انتخاب کن😉',reply_markup=markup)
						bot.register_next_step_handler(msg,selectboygirl)
						
				#	Start Chat <<|
				elif m.text == '🔙 لغو جستجو':
					print 'main func stop finding'
					allow = redis.hget('secretchat:cancelchatfix',m.from_user.id)
					if allow:
						return cancelfind(m)
				#	Buy VIP |>>
				elif m.text == '🛍 خرید نسخه کامل ربات':
					print 'main func buy vip'
					if joined(m.from_user.id):
						print 'buyvip func buy'
						a = buy(5000)
						link = 'https://www.payping.ir/virus32/5000?utm_source=bot&utm_medium=preamount'+str(a)
						links = 'https://www.payping.ir/virus32/5000?utm_source=bot&utm_medium=preamount'
						redis.hset('secretchat:links',m.from_user.id,a)
						kb = types.InlineKeyboardMarkup()
						b = types.InlineKeyboardButton("🎯 پرداخت",url=link)
						c = types.InlineKeyboardButton("✔️ تایید",callback_data='check')
						d = types.InlineKeyboardButton("🔅 پرداخت دستی",url=links)
						kb.add(b,c)
						kb.add(d)
						bot.send_message(m.chat.id,'به بخش ویژه کردن حساب خودت خوش اومدی😦❤️\n➖➖➖➖\n🔹از طریق این بخش میتونی ربات رو به صورت نامحدود ویژه کنید😍\n\n✨امکانات ویژه کردن ربات :\n\n🚦امکان انتخاب کردن جنسیت طرف مقابل برای شروع گفت گو\n\n💭امکان ارسال انواع رسانه ماننده عکس و فیلم در گفت گو ها\n\n💥حذف تبلیغات و مقدار استفاده از چت و رفع محدودیت دعوت دیگران\n➖➖➖\n🔖شما میتوانید تنها با پرداخت 3800 هزار تومان برای همیشه ربات را برای خود ویژه کنید و از امکانات ان لذت ببرید😃\n➖➖\n⚠️توجه کنید که ویژه کردن ربات برای شما کاملا خودکاره و پس از پرداخت ربات شما ویژه خواهد شد درصورت ویژه نشدن میتوانید ان را به صورت دستی و با دکمه تایید فعال کنید درصورت بروز هر نوع مشکل کافیست از دکمه پشتیبانی استفاده کنید☺️',reply_markup=kb)
						print 'buyvip func end buy'
						pass
				#	Buy VIP <<|
				#	About Us |>>
				elif m.text == '🔹 درباره ما':
					print 'main func about us'
					link = 't.me/pouyazamani'
					me = types.InlineKeyboardMarkup()
					b = types.InlineKeyboardButton("🎉 ورود به کانال",url=link)
					me.add(b)
					bot.send_message(m.from_user.id,'🔖ساخت شده توسط :\n\n🔸 @virus32 🔹',reply_markup=me)
				elif m.text == '🔸 پشتیبانی':
					print 'main func about us'
					link = 'https://telegram.me/virus32'
					me = types.InlineKeyboardMarkup()
					b = types.InlineKeyboardButton("💥 ارسال پیام",url=link)
					me.add(b)
					bot.send_message(m.from_user.id,'به بخش پشتیبانی خوش امدید😃\n➖➖➖➖\n\n🔹پیشنهادات انتقادات و مشکلات خود را برای ما ارسال کنید تا ما اون هارو برسی کنیم☺️\n\n🔸از ارسال پیام بیهوده و سلام علیک خود داری کن دوست من😉',reply_markup=me)	
				elif m.text == '🔚 برگشت':
					print 'main func about us'
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
					buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
					about = types.KeyboardButton('🔹 درباره ما')
					sup = types.KeyboardButton('🔸 پشتیبانی')
					markup.add(startchat)
					markup.add(buyvipkey)
					markup.add(about,sup)
					bot.send_message(m.from_user.id,'شما به منوی اصلی بازگشتید✔️\n➖➖➖➖\nاز دکمه های زیر استفاده کنید🔻',reply_markup=markup)
				#	About Us <<|
		print 'main func finished'
	except Exception as e:
		debug(e)
		
def selectboygirl(m):
	try:
		if m.text:
			if m.text == '👩 دختر':
				if vip(m.from_user.id):
					usergen = redis.hget('secretchat:usergen',m.from_user.id)
					if usergen:
						print 'main func lets start chat'
						if joined(m.from_user.id):
							if can_use(m.from_user.id) or user_invited(m.from_user.id) or vip(m.from_user.id):
								onlines.append(str(m.from_user.id)+':'+str(usergen))
								markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
								cancelfindkey = types.KeyboardButton('🔙 لغو جستجو')
								markup.add(cancelfindkey)
								bot.send_message(m.from_user.id,'✨در حال اتصال به کاربر...',reply_markup=markup)
								redis.hset('secretchat:cancelchatfix',m.from_user.id,True)
								redis.hset('secretchat:selectedgen',m.from_user.id,'female')
								return online_chat_request(m.from_user.id)
							else:
								bot.send_message(m.chat.id,'🔖شما از تمام فرصت های چت خود استفاده کرده اید\n➖➖➖➖\n🔹جهت رفع این محدودیت کافیست پست زیر را برای 5 نفر ارسال کنید تا محدودیت شما به صورت کامل رفع گردد\n\n🔸پس از ورود هر فرد یک پیام از طرف ربات برای شما ارسال میشود')
								bot.send_photo(m.chat.id,photo=open('img.jpg','rb'),caption=share.format(botuser,m.from_user.id))
						else:
							markup = types.InlineKeyboardMarkup()
							joinlink = types.InlineKeyboardButton("🚩 عضویت در کانال", url="https://telegram.me/pouyazamani")
							markup.add(joinlink)
							bot.send_message(m.chat.id,forcejoin,reply_markup=markup)
					else:
						print 'main func not selected gen'
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						boy = types.KeyboardButton('👨‍💼 پسر')
						girl = types.KeyboardButton('👩‍💼 دختر')
						markup.add(boy,girl)
						msg = bot.send_message(m.chat.id,firststart.format(m.from_user.first_name),reply_markup=markup)
						bot.register_next_step_handler(msg,save_boy_girl)
				else:
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
					buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
					about = types.KeyboardButton('🔹 درباره ما')
					sup = types.KeyboardButton('🔸 پشتیبانی')
					markup.add(startchat)
					markup.add(buyvipkey)
					markup.add(about,sup)
					bot.send_message(m.chat.id,'ربات برای شما ویژه نمیباشد⚠️\n➖➖➖➖\n🔹ربات در حال حاضر برای شما ویژه نمبیاشد و شما نمیتوانید جنسیت طرف مقابل را تایین کنید\n\n🔸در حال حاضر تنها میتوانید با استفاده از کلید فرقی ندارد به گفت گو بپردازید\n➖➖➖\n🔖برای ویژه کردن ربات خودت کافیه با استفاده از دکمه خرید نسخه اصلی ربات اقدام به ویژه کردن ربات برای خودتون بکنید😉😦',reply_markup=markup)
					pass
			if m.text == '👱 پسر':
				if vip(m.from_user.id):
					usergen = redis.hget('secretchat:usergen',m.from_user.id)
					if usergen:
						print 'main func lets start chat'
						if joined(m.from_user.id):
							if can_use(m.from_user.id) or user_invited(m.from_user.id) or vip(m.from_user.id):
								onlines.append(str(m.from_user.id)+':'+str(usergen))
								markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
								cancelfindkey = types.KeyboardButton('🔙 لغو جستجو')
								markup.add(cancelfindkey)
								bot.send_message(m.from_user.id,'✨در حال اتصال به کاربر...',reply_markup=markup)
								redis.hset('secretchat:selectedgen',m.from_user.id,'male')
								redis.hset('secretchat:cancelchatfix',m.from_user.id,True)
								return online_chat_request(m.from_user.id)
							else:
								bot.send_message(m.chat.id,'🔖شما از تمام فرصت های چت خود استفاده کرده اید\n➖➖➖➖\n🔹جهت رفع این محدودیت کافیست پست زیر را برای 5 نفر ارسال کنید تا محدودیت شما به صورت کامل رفع گردد\n\n🔸پس از ورود هر فرد یک پیام از طرف ربات برای شما ارسال میشود')
								bot.send_photo(m.chat.id,photo=open('img.jpg','rb'),caption=share.format(botuser,m.from_user.id))
						else:
							markup = types.InlineKeyboardMarkup()
							joinlink = types.InlineKeyboardButton("🚩 عضویت در کانال", url="https://telegram.me/pouyazamani")
							markup.add(joinlink)
							bot.send_message(m.chat.id,forcejoin,reply_markup=markup)
					else:
						print 'main func not selected gen'
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						boy = types.KeyboardButton('👨‍💼 پسر')
						girl = types.KeyboardButton('👩‍💼 دختر')
						markup.add(boy,girl)
						msg = bot.send_message(m.chat.id,firststart.format(m.from_user.first_name),reply_markup=markup)
						bot.register_next_step_handler(msg,save_boy_girl)
				else:
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
					buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
					about = types.KeyboardButton('🔹 درباره ما')
					sup = types.KeyboardButton('🔸 پشتیبانی')
					markup.add(startchat)
					markup.add(buyvipkey)
					markup.add(about,sup)
					bot.send_message(m.chat.id,'ربات برای شما ویژه نمیباشد⚠️\n➖➖➖➖\n🔹ربات در حال حاضر برای شما ویژه نمبیاشد و شما نمیتوانید جنسیت طرف مقابل را تایین کنید\n\n🔸در حال حاضر تنها میتوانید با استفاده از کلید فرقی ندارد به گفت گو بپردازید\n➖➖➖\n🔖برای ویژه کردن ربات خودت کافیه با استفاده از دکمه خرید نسخه اصلی ربات اقدام به ویژه کردن ربات برای خودتون بکنید😉😦',reply_markup=markup)
					pass
			if m.text == '👤 فرقی نداره':
					usergen = redis.hget('secretchat:usergen',m.from_user.id)
					if usergen:
						print 'main func lets start chat'
						if joined(m.from_user.id):
							if can_use(m.from_user.id) or user_invited(m.from_user.id) or vip(m.from_user.id):
								onlines.append(str(m.from_user.id)+':'+str(usergen))
								markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
								cancelfindkey = types.KeyboardButton('🔙 لغو جستجو')
								markup.add(cancelfindkey)
								bot.send_message(m.from_user.id,'✨در حال اتصال به کاربر...',reply_markup=markup)
								redis.hset('secretchat:selectedgen',m.from_user.id,'any')
								redis.hset('secretchat:cancelchatfix',m.from_user.id,True)
								return online_chat_request(m.from_user.id)
							else:
								bot.send_message(m.chat.id,'🔖شما از تمام فرصت های چت خود استفاده کرده اید\n➖➖➖➖\n🔹جهت رفع این محدودیت کافیست پست زیر را برای 5 نفر ارسال کنید تا محدودیت شما به صورت کامل رفع گردد\n\n🔸پس از ورود هر فرد یک پیام از طرف ربات برای شما ارسال میشود')
								bot.send_photo(m.chat.id,photo=open('img.jpg','rb'),caption=share.format(botuser,m.from_user.id))
						else:
							markup = types.InlineKeyboardMarkup()
							joinlink = types.InlineKeyboardButton("🚩 عضویت در کانال", url="https://telegram.me/pouyazamani")
							markup.add(joinlink)
							bot.send_message(m.chat.id,forcejoin,reply_markup=markup)
					else:
						print 'main func not selected gen'
						markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
						boy = types.KeyboardButton('👨‍💼 پسر')
						girl = types.KeyboardButton('👩‍💼 دختر')
						markup.add(boy,girl)
						msg = bot.send_message(m.chat.id,firststart.format(m.from_user.first_name),reply_markup=markup)
						bot.register_next_step_handler(msg,save_boy_girl)
						
						#bot.forward_message(m.chat.id, channel, m.message_id)
	except Exception as e:
		debug(e)
def adminpanel(m):
	try:
		if m.text:
			dontdo = types.ReplyKeyboardMarkup(resize_keyboard=True)
			cancel = types.KeyboardButton('بیخیال')
			dontdo.add(cancel)
			if m.text == 'آمار ربات':
				stats = redis.scard('secretchat:users')
				vipusers = redis.scard('secretchat:vip')
				bot.send_message(m.from_user.id,'کاربران ربات تا کنون : {}\nکاربران آنلاین : {}\nکاربران وی آی پی : {}'.format(str(stats),str(len(onlines)),str(vipusers)))
				bot.register_next_step_handler(msg,adminpanel)
			elif m.text == 'ارسال پیام همگانی':
				msg = bot.send_message(m.chat.id,'لطفا پیام مورد نظر را ارسال کنید:',reply_markup=dontdo)
				bot.register_next_step_handler(msg,sendmessage)
			elif m.text == 'فوروارد پیام همگانی':
				msg = bot.send_message(m.chat.id,'لطفا پیام مورد نظر را ارسال کنید:',reply_markup=dontdo)
				bot.register_next_step_handler(msg,fwdmessage)
			elif m.text == 'افزودن وی آی پی':
				msg = bot.send_message(m.chat.id,'لطفا یک پیام از شخص را فوروارد کنید:',reply_markup=dontdo)
				bot.register_next_step_handler(msg,addvip)
			elif m.text == 'بازگشت به منوی اصلی':
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
				buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
				about = types.KeyboardButton('🔹 درباره ما')
				sup = types.KeyboardButton('🔸 پشتیبانی')
				markup.add(startchat)
				markup.add(buyvipkey)
				markup.add(about,sup)
				bot.send_message(m.chat.id,'به منوی اصلی ربات بازگشتید!',reply_markup=markup)
			else:
				msg = bot.send_message(m.chat.id,'لطفا از کیبورد انتخاب کنید')
				bot.register_next_step_handler(msg,adminpanel)
				
		else:
			msg = bot.send_message(m.chat.id,'لطفا از کیبورد انتخاب کنید')
			bot.register_next_step_handler(msg,adminpanel)
	except Exception as e:
		debug(e)

def addvip(m):
	try:
		if m.forward_from:
			user_id = m.forward_from.id
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			stats = types.KeyboardButton('آمار ربات')
			bcall = types.KeyboardButton('ارسال پیام همگانی')
			fwdall = types.KeyboardButton('فوروارد پیام همگانی')
			addvip = types.KeyboardButton('افزودن وی آی پی')
			back = types.KeyboardButton('بازگشت به منوی اصلی')
			markup.add(stats)
			markup.add(bcall)
			markup.add(fwdall)
			markup.add(addvip)
			markup.add(back)
			msg = bot.send_message(m.chat.id,'کاربر {} به لیست کاربران وی آی پی افزوده شد!'.format(user_id),reply_markup=markup)
			bot.register_next_step_handler(msg,adminpanel)
			redis.sadd('secretchat:vip',user_id)
		else:
			if m.text:
				if m.text == 'بیخیال':
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					stats = types.KeyboardButton('آمار ربات')
					bcall = types.KeyboardButton('ارسال پیام همگانی')
					fwdall = types.KeyboardButton('فوروارد پیام همگانی')
					addvip = types.KeyboardButton('افزودن وی آی پی')
					back = types.KeyboardButton('بازگشت به منوی اصلی')
					markup.add(stats)
					markup.add(bcall)
					markup.add(fwdall)
					markup.add(addvip)
					markup.add(back)
					msg = bot.send_message(m.chat.id,'هرطور مایلید!',reply_markup=markup)
					bot.register_next_step_handler(msg,adminpanel)
				elif m.text.isdigit():
					msg = bot.send_message(m.chat.id,'کاربر {} به لیست کاربران وی آی پی افزوده شد!'.format(m.text),reply_markup=markup)
					bot.register_next_step_handler(msg,adminpanel)
					redis.sadd('secretchat:vip',int(m.text))
				else:
					msg = bot.send_message(m.chat.id,'ورودی صحیح نیست!\nمجددا تلاش کنید:')
					bot.register_next_step_handler(msg,addvip_2)
			else:
				msg = bot.send_message(m.chat.id,'ورودی صحیح نیست!\nمجددا تلاش کنید:')
				bot.register_next_step_handler(msg,addvip_2)
	except Exception as e:
		debug(e)
				
def fwdmessage(m):
	try:
		if m.forward_from:
			global fwdmessage_text
			fwdmessage_text = m.message_id
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			yes = types.KeyboardButton('بله')
			no = types.KeyboardButton('خیر')
			markup.add(yes,no)
			msg = bot.reply_to(m,'آیا از ارسال پیام بالا مطمعن هستید ؟',reply_markup=markup)
			bot.register_next_step_handler(msg,confirm_fwdmessage)
		elif m.forward_from_message_id:
			fwdmessage_text = m.message_id
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			yes = types.KeyboardButton('بله')
			no = types.KeyboardButton('خیر')
			markup.add(yes,no)
			msg = bot.reply_to(m,'آیا از ارسال پیام بالا مطمعن هستید ؟',reply_markup=markup)
			bot.register_next_step_handler(msg,confirm_fwdmessage)
		else:
			if m.text:
				if m.text == 'بیخیال':
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					stats = types.KeyboardButton('آمار ربات')
					bcall = types.KeyboardButton('ارسال پیام همگانی')
					fwdall = types.KeyboardButton('فوروارد پیام همگانی')
					addvip = types.KeyboardButton('افزودن وی آی پی')
					back = types.KeyboardButton('بازگشت به منوی اصلی')
					markup.add(stats)
					markup.add(bcall)
					markup.add(fwdall)
					markup.add(addvip)
					markup.add(back)
					msg = bot.send_message(m.chat.id,'هرطور مایلید!',reply_markup=markup)
					bot.register_next_step_handler(msg,adminpanel)
				else:
					fwdmessage_text = m.message_id
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					yes = types.KeyboardButton('بله')
					no = types.KeyboardButton('خیر')
					markup.add(yes,no)
					msg = bot.reply_to(m,'آیا از ارسال پیام بالا مطمعن هستید ؟',reply_markup=markup)
					bot.register_next_step_handler(msg,confirm_fwdmessage)
			else:
				msg = bot.send_message(m.chat.id,'در حالت ارسال پیام ، فقط متن پشتیبانی میشود !\nبرای ارسال این نوع پیام میتوانید از فوروارد همگانی استفاده کنید')
				bot.register_next_step_handler(msg,fwdmessage)
	except Exception as e:
		debug(e)
		
def confirm_fwdmessage(m):
	try:
		if m.text:
			if m.text == 'بله':
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				stats = types.KeyboardButton('آمار ربات')
				bcall = types.KeyboardButton('ارسال پیام همگانی')
				fwdall = types.KeyboardButton('فوروارد پیام همگانی')
				addvip = types.KeyboardButton('افزودن وی آی پی')
				back = types.KeyboardButton('بازگشت به منوی اصلی')
				markup.add(stats)
				markup.add(bcall)
				markup.add(fwdall)
	except Exception as e:
		debug(e)
#	#	#	#	#	#		
def sendmessage(m):
	try:
		if m.text:
			if m.text == 'بیخیال':
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				stats = types.KeyboardButton('آمار ربات')
				bcall = types.KeyboardButton('ارسال پیام همگانی')
				fwdall = types.KeyboardButton('فوروارد پیام همگانی')
				addvip = types.KeyboardButton('افزودن وی آی پی')
				back = types.KeyboardButton('بازگشت به منوی اصلی')
				markup.add(stats)
				markup.add(bcall)
				markup.add(fwdall)
				markup.add(addvip)
				markup.add(back)
				msg = bot.send_message(m.chat.id,'هرطور مایلید!',reply_markup=markup)
				bot.register_next_step_handler(msg,adminpanel)
			else:
				global sendmessage_text
				sendmessage_text = m.text
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				yes = types.KeyboardButton('بله')
				no = types.KeyboardButton('خیر')
				markup.add(yes,no)
				msg = bot.reply_to(m,m.text,parse_mode='markdown')
				msg2 = bot.reply_to(msg,'آیا از ارسال پیام بالا مطمعن هستید ؟',reply_markup=markup)
				bot.register_next_step_handler(msg2,confirm_sendmessage)
		else:
			msg = bot.send_message(m.chat.id,'در حالت ارسال پیام ، فقط متن پشتیبانی میشود !\nبرای ارسال این نوع پیام میتوانید از فوروارد همگانی استفاده کنید')
			bot.register_next_step_handler(msg,sendmessage)
	except Exception as e:
		debug(e)
		
def confirm_sendmessage(m):
	try:
		if m.text:
			if m.text == 'بله':
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				stats = types.KeyboardButton('آمار ربات')
				bcall = types.KeyboardButton('ارسال پیام همگانی')
				fwdall = types.KeyboardButton('فوروارد پیام همگانی')
				addvip = types.KeyboardButton('افزودن وی آی پی')
				back = types.KeyboardButton('بازگشت به منوی اصلی')
				markup.add(stats)
				markup.add(bcall)
				markup.add(fwdall)
				markup.add(addvip)
				markup.add(back)
				msg = bot.send_message(m.chat.id,'در حال ارسال پیام همگانی ...',reply_markup=markup)
				bot.register_next_step_handler(msg,adminpanel)
				users = redis.smembers('secretchat:users')
				sent = 0
				notsent = 0
				for i in users:
					try:
						bot.send_message(i,sendmessage_text,parse_mode='markdown')
						sent += 1
					except:
						redis.srem('secretchat:users',i)
						notsent += 1
				msg = bot.send_message(m.chat.id,'پیام همگانی ارسال شد!\nتعداد پیام های ارسال شده : {}\nتعداد پیام های نا موفق : {}'.format(sent,notsent))
				bot.register_next_step_handler(msg,adminpanel)
			elif m.text == 'خیر':
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				stats = types.KeyboardButton('آمار ربات')
				bcall = types.KeyboardButton('ارسال پیام همگانی')
				fwdall = types.KeyboardButton('فوروارد پیام همگانی')
				addvip = types.KeyboardButton('افزودن وی آی پی')
				back = types.KeyboardButton('بازگشت به منوی اصلی')
				markup.add(stats)
				markup.add(bcall)
				markup.add(fwdall)
				markup.add(addvip)
				markup.add(back)
				msg = bot.send_message(m.chat.id,'کنسل شد!\nاز منوی زیر انتخاب کنید:',reply_markup=markup)
				bot.register_next_step_handler(msg,adminpanel)
			else:
				msg = bot.send_message(m.chat.id,'از منوی زیر انتخاب کنید لطفا !')
				bot.register_next_step_handler(msg,confirm_sendmessage)
		else:
			msg = bot.send_message(m.chat.id,'از منوی زیر انتخاب کنید لطفا !')
			bot.register_next_step_handler(msg,confirm_sendmessage)
	except Exception as e:
		debug(e)
		
def stopchat(m):
	try:
		print 'stopchat func started'
		if m.text == 'بله ✅':
			print 'stopchat func yes started'
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
			buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
			about = types.KeyboardButton('🔹 درباره ما')
			sup = types.KeyboardButton('🔸 پشتیبانی')
			markup.add(startchat)
			markup.add(buyvipkey)
			markup.add(about,sup)
			user1 = redis.hget('secretchat:inchat',m.from_user.id)
			redis.hdel('secretchat:inchat',m.from_user.id)
			redis.hdel('secretchat:inchat',user1)
			redis.hdel('secretchat:askforend',m.from_user.id)
			redis.hdel('secretchat:askforend',user1)
			redis.hdel('secretchat:selectedgen',m.from_user.id)
			msg1 = bot.send_message(m.from_user.id,'گفت گو با موفقیت بسته شد✔️\n➖➖➖➖\nاز دکمه های زیر استفاده کنید🔻',reply_markup=markup)
			if not vip(m.from_user.id):
				bot.send_photo(m.chat.id,photo=open('vip.jpg','rb'),caption='''✨امکانات ویژه کردن ربات :

🚦امکان انتخاب کردن جنسیت طرف مقابل برای شروع گفت گو

💭امکان ارسال انواع رسانه ماننده عکس و فیلم در گفت گو ها
و..

🔻برای ویژه کردن ربات برای خود از دکمه های زیر استفاده کن''')
			msg2 = bot.send_message(user1,'گفتگو از طرف فرد مقابل بسته شد☹️😦',reply_markup=markup)
			if not vip(user1):
				bot.send_photo(user1,photo=open('vip.jpg','rb'),caption='''✨امکانات ویژه کردن ربات :

🚦امکان انتخاب کردن جنسیت طرف مقابل برای شروع گفت گو

💭امکان ارسال انواع رسانه ماننده عکس و فیلم در گفت گو ها
و..

🔻برای ویژه کردن ربات برای خود از دکمه های زیر استفاده کن''')
			print 'stopchat func yes done'
			pass
		elif m.text == 'نه ❌':
			print 'stopchat func no started'
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			endchat = types.KeyboardButton('🔚 پایان چت 🔚')
			markup.add(endchat)
			msg = bot.send_message(m.from_user.id,'بسیار خوب😉\nبه گفت گو ادامه بده😃',reply_markup=markup)
			redis.hdel('secretchat:askforend',m.from_user.id)
			user1 = redis.hget('secretchat:inchat',m.from_user.id)
			redis.hdel('secretchat:askforend',user1)
			print 'stopchat func no done'
			pass
		#	bot.register_next_step_handler(msg,start)
		else:
			print 'stopchat func else'
			msg = bot.send_message(m.from_user.id,'متوجه نشدم!\nچت رو ببندم ؟😦')
			bot.register_next_step_handler(msg,stopchat)
	except Exception as e:
		debug(e)
		
def cancelfind(m):
	try:
		print 'cancelfind func start'
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
		buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
		about = types.KeyboardButton('🔹 درباره ما')
		sup = types.KeyboardButton('🔸 پشتیبانی')
		markup.add(startchat)
		markup.add(buyvipkey)
		markup.add(about,sup)
		redis.hdel('secretchat:cancelchatfix',m.from_user.id)
		msg = bot.send_message(m.from_user.id,'جستجو لغو شد✔️',reply_markup=markup)
		list = onlines
		usr = str(m.from_user.id)+':'+redis.hget('secretchat:usergen',m.from_user.id)
		list.remove(usr)
		print 'cancelfind func finished'
		pass
	#	bot.register_next_step_handler(msg,start)
	except Exception as e:
		debug(e)
#def buyvip(m):
#	try:
#		print 'buyvip func start'
#		if m.text:
#			if m.text == 'بزن بریم خرید':
#				print 'buyvip func buy'
#				a = buy(5000)
#				link = 'https://www.payping.ir/virus32/5000?utm_source=bot&utm_medium=preamount'+str(a)
#				redis.hset('secretchat:links',m.from_user.id,a)
#				kb = types.InlineKeyboardMarkup()
#				b = types.InlineKeyboardButton("پرداخت",url=link)
#				c = types.InlineKeyboardButton("تایید",callback_data='check')
#				kb.add(b,c)
#				bot.send_message(m.chat.id,'برای پرداخت از طریق کیبرد زیر اقدام کنید\nنکته: شما بعد از پرداخت دوباره به ربات بازگشت داده می شوید و تایید خودکار انجام میگیرد چناچه مشکلی پیش امد برای تایید دستی بر روی دکمه تایید کلیک نمایید',reply_markup=kb)
#				print 'buyvip func end buy'
#				pass
#	#			bot.register_next_step_handler(msg,start)
#			elif m.text == 'بیخیال':
#				print 'buyvip func back'
#				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#				startchat = types.KeyboardButton(💁 شروع چت 💁‍♂')
#				buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
#				about = types.KeyboardButton('درباره ما')
#				markup.add(startchat)
#				#markup.add(buyvipkey)
#				markup.add(about)
#				msg = bot.send_message(m.chat.id,'باشه\nهر وقت خواستی بهم بگو ^_^',reply_markup=markup)
#				print 'buyvip func back done'
#				pass
#	#			bot.register_next_step_handler(msg,start)
#			else:
#				print 'buyvip func else 1'
#				msg = bot.send_message(m.chat.id,'میخوای وی آی پی بخری ؟')
#				bot.register_next_step_handler(msg,buyvip)
#		else:
#			print 'buyvip func else 2'
#			msg = bot.send_message(m.chat.id,'چی ؟\nمن که نمیفهمم چی میگی من فقط یه رباتم!')
#			bot.register_next_step_handler(msg,buyvip)
#	except Exception as e:
#		debug(e)
				
def save_boy_girl(m):
	try:
		print 'save_boy_girl func start'
		if m.text:
			if m.text == '👨‍💼 پسر' or m.text == '👩‍💼 دختر':
				print 'save_boy_girl func text matched'
				if joined(m.from_user.id):
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
					buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
					about = types.KeyboardButton('🔹 درباره ما')
					sup = types.KeyboardButton('🔸 پشتیبانی')
					markup.add(startchat)
					markup.add(buyvipkey)
					markup.add(about,sup)
					bot.send_message(m.chat.id,starttext.format(m.from_user.first_name),reply_markup=markup)
					if m.text == '👨‍💼 پسر':
						gen = 'male'
					elif m.text == '👩‍💼 دختر':
						gen = 'female'
					redis.hset('secretchat:usergen',m.from_user.id,gen)
				else:
					markup = types.InlineKeyboardMarkup()
					joinlink = types.InlineKeyboardButton("🚩 عضویت در کانال", url="https://telegram.me/pouyazamani")
					markup.add(joinlink)
					msg = bot.send_message(m.chat.id,forcejoin,reply_markup=markup)
					bot.register_next_step_handler(msg,save_boy_girl)
				print 'save_boy_girl func done'
			else:
				msg = bot.send_message(m.chat.id,'')
				bot.register_next_step_handler(msg,save_boy_girl)
				print 'save_boy_girl func else 1'
		else:
			msg = bot.send_message(m.chat.id,'لطفا از کیبورد پایین استفاده کنید🔻')
			bot.register_next_step_handler(msg,save_boy_girl)
			print 'save_boy_girl func else 2'
	except Exception as e:
		debug(e)
		
@bot.callback_query_handler(func=lambda call: True)
def che(call):
	try:
		if checks(redis.hget('secretchat:links',call.from_user.id)):
			redis.set('vip',call.from_user.id)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			startchat = types.KeyboardButton('💁 شروع چت 💁‍♂')
			buyvipkey = types.KeyboardButton('🛍 خرید نسخه کامل ربات')
			about = types.KeyboardButton('🔹 درباره ما')
			sup = types.KeyboardButton('🔸 پشتیبانی')
			markup.add(startchat)
			markup.add(buyvipkey)
			markup.add(about,sup)
			bot.send_message(call.message.chat.id,'پرداخت تایید شد و حساب شما ویژه شد.',reply_markup=markup)
			bot.delete_message(call.message.chat.id,call.message.message_id)
		else:
			bot.send_message(call.message.chat.id,'شما هنوز پرداخت نکرده اید.')
	except Exception as e:
		debug(e)

bot.polling(True)