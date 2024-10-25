from create_bot import all_media_dir
from aiogram.types import FSInputFile
from datetime import date
import os
from create_bot import text_model



def generate_prediction():
    text = []
    for i in range(5):
        text.append(text_model.make_sentence())
    return "".join(text)
def make_horoscope(data):
    now = date.today()
    prediction = generate_prediction()
    sign_name = data["sign"]
    text = (f'Гороскоп для {sign_name} на <b>{now}</b>\n' + prediction)
    photo_file = FSInputFile(path=os.path.join(all_media_dir, f"{sign_name}.png"))
    return text, photo_file