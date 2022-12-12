import os
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])

BOT_TOKEN = '5334439271:AAFWmpskZqlpS35ezK99bWEeEI8NLV5SEZQ'
admin_list = [1021524873]
admin_tag = '@...'
count_orders_for_one_page = 10
bscScanAPI = ''
payAdress_bep20 = '0xee5b5b923ffce93a870b3104b7ca09c3db80047a'
payAdress_trc20 = ''
USDTcontractAddress_bep20 = '0x55d398326f99059ff775485246999027b3197955'
USDTcontractAddress_trc20 = ''
amount = 100
host_url = 'localhost'
port = 8000
db_path = f'{homeDir}\\DBs\\db.db'
