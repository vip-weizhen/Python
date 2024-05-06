import requests
import json

# 从网页上获取IP地址
def get_ip():
    response = requests.get('   ')
    ip = response.text.strip()
    return ip

# 添加DNS记录到Cloudflare
def add_dns_record(ip):
    cf_api_key = '  '
    cf_email = '  '
    cf_zone_id = '   '
    cf_record_name = '   '

    # 检查Cloudflare是否已存在该记录
    headers = {
        'X-Auth-Email': cf_email,
        'X-Auth-Key': cf_api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records', headers=headers)
    records = json.loads(response.text)['result']
    for record in records:
        if record['name'] == cf_record_name:
            # 如果已存在则先删除
            response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records/{record["id"]}', headers=headers)
            print('Deleted existing DNS record:', record['name'])
            break

    # 添加新的DNS记录
    data = {
        'type': 'A',
        'name': cf_record_name,
        'content': ip,
        'ttl': 1,
        'proxied': False
    }
    response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records', headers=headers, json=data)
    print('Added DNS record:', cf_record_name)

# 通过电报机器人推送DNS更新记录
def send_telegram_notification(message):
    bot_token = '    '
    chat_id = '    '
    tgapi =    

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    print('Telegram notification sent:', message)

# 执行主程序
def main():
    ip = get_ip()
    add_dns_record(ip)
    send_telegram_notification(f'DNS record updated with IP: {ip}')

if __name__ == '__main__':
    main()
