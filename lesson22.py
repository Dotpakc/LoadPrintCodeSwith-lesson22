import logging

from aiogram import Bot, Dispatcher, executor, types

from decouple import config

API_TOKEN = config('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

all_photos = []
with open('photos_ids.txt','r') as file:
    for line in file:
        all_photos.append(line.strip())
        
print(all_photos)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')

@dp.message_handler(commands=['get_photo'])
async def send_welcome(message: types.Message):
    # останні 5 фото відправити групою
    # for photo_id in all_photos[-5:]:
    #     await message.answer_photo(photo_id)
    #отримати параметр з команди
    arg = message.get_args()
    print(arg)
    if not arg:
        arg = 5
    
    # Create media group
    media = types.MediaGroup()
    for photo_id in all_photos[int(arg)*-1:]:
        media.attach_photo(photo_id)
        
    await message.answer_media_group(media=media)
        

# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)

#     await message.answer(message.text)

#отримати фото з повідомлення
@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    await message.answer_photo(message.photo[-1].file_id,caption='Фото з повідомлення')
    all_photos.append(message.photo[-1].file_id)
    with open('photos_ids.txt','a') as file:
        file.write(message.photo[-1].file_id+'\n')
   

    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)