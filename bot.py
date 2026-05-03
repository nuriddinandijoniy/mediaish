from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from PIL import Image, ImageDraw, ImageFont

API_TOKEN = "token"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

data_user = {}

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("🚀 Rasm yaratish"))

again_kb = ReplyKeyboardMarkup(resize_keyboard=True)
again_kb.add(KeyboardButton("🔁 Yana"))

# 🔥 TEXT BOX FIT
def fit_text_box(draw, text, font_path, box, max_size=160, min_size=40):
    x1, y1, x2, y2 = box
    box_w = x2 - x1
    box_h = y2 - y1

    for size in range(max_size, min_size, -2):
        font = ImageFont.truetype(font_path, size)
        bbox = draw.multiline_textbbox((0,0), text, font=font, align="center")
        w = bbox[2]
        h = bbox[3]

        if w <= box_w and h <= box_h:
            return font, w, h

    return ImageFont.truetype(font_path, min_size), w, h

# 🔥 GRADIENT TEXT (ikkinchi qatorda)
def gradient_text(draw, x, y, text, font):
    for i, char in enumerate(text):
        color = (
            int(255 - i*10),
            int(80 + i*5),
            255
        )
        draw.text((x + i*font.size*0.6, y), char, font=font, fill=color)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("Boshlash 👇", reply_markup=kb)

@dp.message_handler(lambda m: m.text in ["🚀 Rasm yaratish","🔁 Yana"])
async def start_form(msg: types.Message):
    data_user[msg.from_user.id] = {}
    await msg.answer("Lavozim:")

@dp.message_handler()
async def form(msg: types.Message):
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

        bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

        # 🔥 CHAP TOMON (LAVOZIM)
        box = (140, 350, 900, 700)

        words = d["lavozim"].upper().split(" ")
        line1 = words[0]
        line2 = " ".join(words[1:]) if len(words) > 1 else ""

        # 2 qator qilib beramiz
        text = line1 + ("\n" + line2 if line2 else "")

        font, w, h = fit_text_box(draw, text, bold, box)

        x = box[0] + (box[2] - box[0] - w) // 2
        y = box[1] + (box[3] - box[1] - h) // 2

        # birinchi qator oddiy
        draw.multiline_text((x, y), text, font=font, fill="white", align="center")

        # 🔥 O‘NG TOMON (SENIKI — O‘ZGARMADI)
        font_val = ImageFont.truetype(bold, 52)

        draw.text((1196, 291), d["manzil"], font=font_val, fill="white")
        draw.text((1196, 456), d["soha"], font=font_val, fill="white")
        draw.text((1196, 621), d["maosh"], font=font_val, fill="white")
        draw.text((1196, 785), d["ish"], font=font_val, fill="white")

        file = f"{uid}.png"
        img.save(file)

        await msg.answer_photo(open(file, "rb"), caption="🔥 Tayyor", reply_markup=again_kb)

        data_user[uid] = {}

    data_user[uid] = d

if __name__ == "__main__":
    executor.start_polling(dp)

