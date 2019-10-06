from config import data_file


def get_data():
    data = []
    with open(data_file, 'r', encoding='utf-8') as file:
        for line in file.read().split('\n'):
            if line.startswith('#') or not line:
                continue
            else:
                from_channel = clear_url(line.split(':::')[0])
                to_channel = clear_url(line.split(':::')[1])
                data.append({'from': from_channel, 'to': to_channel})
        else:
            return data


def clear_url(url: str):
    if url.startswith('https://t.me/joinchat/'):
        return url
    elif url.startswith('https://t.me/'):
        return url.replace('https://t.me/', '')
    elif url.startswith('t.me/'):
        return url.replace('t.me/', '')
