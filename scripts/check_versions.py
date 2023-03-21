import os

env_list = os.environ

print(env_list.get('SSL_CERT_DIR'))
print(env_list.get('SSL_CERT_FILE'))
print(env_list.get('LDFLAGS'))
print(env_list.get('CPPFLAGS'))
print(env_list.get('PKG_CONFIG_PATH'))
print(env_list.get('PATH'))

print("all evn list:")

# print all
for key in env_list:
    print(key + ' : ' + env_list[key])