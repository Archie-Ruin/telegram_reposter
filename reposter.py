import os
import time

from pyrogram import Client, Message, Filters, InputMediaPhoto
from pyrogram.errors import FloodWait

from channels import get_data

from config import api_id, api_hash

app = Client(session_name='rep', api_id=api_id, api_hash=api_hash)
last_media_group_ids = []


app.start()
while True:
    try:
        print('Started')
        from_ids = [app.get_chat(i['from']).id for i in get_data()]
        from_to_ids = []
        for data in get_data():
            from_id = app.get_chat(data['from']).id
            to_id = app.get_chat(data['to']).id
            from_to_ids.append({
                'from_id': from_id,
                'to_id': to_id
            })
            print(f'Check   from: {data["from"]} [{from_id}]    to: {data["to"]} [{to_id}]')
        print('Check is done.\n\nBot has been STARTED')
        break
    except FloodWait as e:
        print("Sleeping for {}s".format(e.x))
        time.sleep(e.x)
app.stop()


from_filter = Filters.create(lambda _, m: m.chat.id in from_ids)


@app.on_message(Filters.media_group & from_filter)
def media_group_worker(cli: Client, msg: Message):
    chat_id = msg.chat.id
    media_group_id = msg.media_group_id
    if media_group_id not in last_media_group_ids:
        last_media_group_ids.append(media_group_id)
        print('Catch media_group')
        for ids in from_to_ids:
            from_id = ids['from_id']
            to_id = ids['to_id']
            if from_id == chat_id:
                photos = []
                for message in app.get_history(chat_id, limit=10):
                    if message.media_group_id == msg.media_group_id:
                        caption = message.caption if message.caption else ''
                        photos.append(InputMediaPhoto(message.photo.file_id, message.photo.file_ref, caption))
                photos.reverse()
                app.send_media_group(to_id, photos)


@app.on_message(Filters.photo & from_filter)
def photo_worker(cli: Client, msg: Message):
    chat_id = msg.chat.id
    for ids in from_to_ids:
        print('Catch photo')
        from_id = ids['from_id']
        to_id = ids['to_id']
        if from_id == chat_id:
            caption = msg.caption if msg.caption else ''
            app.send_photo(to_id, msg.photo.file_id, msg.photo.file_ref, caption=caption)


@app.on_message(Filters.text & from_filter)
def text_worker(cli: Client, msg: Message):
    chat_id = msg.chat.id
    for ids in from_to_ids:
        print('Catch text')
        from_id = ids['from_id']
        to_id = ids['to_id']
        if from_id == chat_id:
            app.send_message(to_id, msg.text)


@app.on_message(Filters.video & from_filter)
def video_worker(cli: Client, msg: Message):
    chat_id = msg.chat.id
    for ids in from_to_ids:
        print('Catch video')
        from_id = ids['from_id']
        to_id = ids['to_id']
        if from_id == chat_id:
            caption = msg.caption if msg.caption else ''
            app.send_video(to_id, msg.video.file_id, msg.video.file_ref, caption=caption)


@app.on_message(from_filter)
def documents_worker(cli: Client, msg: Message):
    chat_id = msg.chat.id
    for ids in from_to_ids:
        print('Catch document')
        from_id = ids['from_id']
        to_id = ids['to_id']
        if from_id == chat_id:
            caption = msg.caption if msg.caption else ''
            app.send_document(to_id, msg.document.file_id, msg.document.file_ref, caption=caption)


if __name__ == '__main__':
    app.run()
