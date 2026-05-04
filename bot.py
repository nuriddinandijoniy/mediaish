import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from PIL import Image, ImageDraw, ImageFont

API_TOKEN = "7286699930:AAGNDcBXbq_6QJmQcz0NcuW6W5_tcrCwIgE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

data_user = {}

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Rasm yaratish")]],
    resize_keyboard=True
)

again_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔁 Yana")]],
    resize_keyboard=True
)

def fit_text_box(draw, text, font_path, box, max_size=160, min_size=40):
    x1, y1, x2, y2 = box
    box_w = x2 - x1
    box_h = y2 - y1

    for size in range(max_size, min_size, -2):
        font = ImageFont.truetype(font_path, size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        w = bbox[2]
        h = bbox[3]

        if w <= box_w and h <= box_h:
            return font, w, h

    return ImageFont.truetype(font_path, min_size), w, h

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("Boshlash 👇", reply_markup=kb)

@dp.message(F.text.in_(["🚀 Rasm yaratish", "🔁 Yana"]))
async def start_form(msg: Message):
    data_user[msg.from_user.id] = {}
    await msg.answer("Lavozim:")

@dp.message()
async def form(msg: Message):
    uid = msg.from_user.id
    d = data_user.get(uid, {})

    if "lavozim" not in d:
        d["lavozim"] = msg.text
        await msg.answer("Manzil:")
    elif "manzil" not in d:
        d["manzil"] = msg.text
        await msg.answer("Soha:")
    elif "soha" not in d:
        d["soha"] = msg.text
        await msg.answer("Maosh:")
    elif "maosh" not in d:
        d["maosh"] = msg.text
        await msg.answer("Ish tartibi:")
    elif "ish" not in d:
        d["ish"] = msg.text

        img = Image.open("template.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        font_path = "Montserrat-Bold.ttf"

        box = (140, 350, 900, 700)

        words = d["lavozim"].upper().split(" ")
        text = words[0] + ("\n" + " ".join(words[1:]) if len(words) > 1 else "")

        font, w, h = fit_text_box(draw, text, font_path, box)

        x = box[0] + (box[2] - box[0] - w) // 2
        y = box[1] + (box[3] - box[1] - h) // 2

        draw.multiline_text((x, y), text, font=font, fill="white", align="center")

        font_val = ImageFont.truetype(font_path, 52)

        draw.text((1196, 291), d["manzil"], font=font_val, fill="white")
        draw.text((1196, 456), d["soha"], font=font_val, fill="white")
        draw.text((1196, 621), d["maosh"], font=font_val, fill="white")
        draw.text((1196, 785), d["ish"], font=font_val, fill="white")

        file = f"{uid}.png"
        img.save(file)

        # 🔥 ENG MUHIM TUZATISH
        photo = FSInputFile(file)

        await msg.answer_photo(photo, caption="🔥 Tayyor", reply_markup=again_kb)

        data_user[uid] = {}

    data_user[uid] = d

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
