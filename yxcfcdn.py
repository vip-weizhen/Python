import requests
import re
import json
import os
import telegram
import asyncio

# 获取网页上的所有IP地址
def get_all_ips_from_website(url):
    response = requests.get(url)
    content = response.text
    
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip_matches = re.findall(ip_pattern, content)
    
    return ip_matches

# 添加或更新 Cloudflare 的 DNS 记录
def update_dns_record(ip):
    cf_api_token = '     '
    cf_zone_id = '    '
    cf_record_name = 'yxcfip'

    # 检查是否存在该 DNS 记录
    headers = {
        'Authorization': f'Bearer {cf_api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(
        f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records',
        headers=headers,
        params={'name': cf_record_name}
    )
    data = json.loads(response.text)

    if 'success' in data and data['success']:
        if data['result']:
            # 如果存在，则删除该 DNS 记录
            record_id = data['result'][0]['id']
            response = requests.delete(
                f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records/{record_id}',
                headers=headers
            )
    
    # 添加新的 DNS 记录
    for ip_address in ip:
        data = {
            'type': 'A',
            'name': cf_record_name,
            'content': ip_address,
            'ttl': 1,
            'proxied': False
        }
        response = requests.post(
            f'https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records',
            headers=headers,
            json=data
        )

# 发送更新通知到 Telegram
async def send_telegram_message(message):
    bot_token = '     '
    chat_id = '    '

    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# 主函数
def main():
    # 获取网页上的所有IP地址
    website_url = 'https://ip.164746.xyz/'
    ip_addresses = get_all_ips_from_website(website_url)

    if ip_addresses:
        # 添加或更新 Cloudflare 的 DNS 记录
        update_dns_record(ip_addresses)

        # 发送 DNS 记录的更新通知
        asyncio.run(send_telegram_message(f'DNS记录已更新，新的IP地址为: {", ".join(ip_addresses)}'))
    else:
        print(f"No IP addresses found on {website_url}")

if __name__ == '__main__':
    main()
