from aiogram.dispatcher import FSMContext
from data.config import CHANNELS
from data.config import ADMINS
from keyboards.default import phone_number, location_buttons
from keyboards.inline import yes_or_no
from keyboards.inline.confirum_buttons import phone_callback_data
from states import CompStates
from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery


@dp.message_handler(text="Kompyuter sotish")
async def sell_phone(msg: types.Message, state: FSMContext):
    await msg.answer("Ism familiyangizni kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CompStates.name)


@dp.message_handler(state=CompStates.name)
async def name_send(msg: types.Message, state: FSMContext):
    name = msg.text
    await state.update_data({'name': name, 'mention': msg.from_user.get_mention(as_html=True)})
    await msg.answer("Telefon raqamingizni kiriting yoki kiriting: ", reply_markup=phone_number)
    await CompStates.next()


@dp.message_handler(state=CompStates.number)
async def name_send(msg: types.Message, state: FSMContext):
    number = msg.text
    await state.update_data({'number': number})
    await msg.answer("Joylashuvingizni yuboring yoki manzilingizni kiriting: ", reply_markup=location_buttons)
    await CompStates.next()


@dp.message_handler(content_types=types.ContentType.CONTACT, is_sender_contact=True, state=CompStates.number)
async def phone_send(msg: types.Message, state: FSMContext):
    contact = msg.contact.phone_number
    await state.update_data({'number': contact})
    await msg.answer("Joylashuvingizni yuboring yoki manzilingizni kiriting: ", reply_markup=location_buttons)
    await CompStates.next()


@dp.message_handler(state=CompStates.location)
async def name_send(msg: types.Message, state: FSMContext):
    location = msg.text
    await state.update_data({'location': location})
    await msg.answer("Kompyuteringizni nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await CompStates.next()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=CompStates.location)
async def location_send(msg: types.Message, state: FSMContext):
    location = msg.text
    await state.update_data({'location': location})
    await msg.answer("Kompyuteringizni nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await CompStates.next()


@dp.message_handler(state=CompStates.comp)
async def location_send(msg: types.Message, state: FSMContext):
    comp_name = msg.text
    await state.update_data({'comp': comp_name})
    await msg.answer("Kompyuteringizni protsesorini kiriting: ")
    await CompStates.next()


@dp.message_handler(state=CompStates.processor)
async def location_send(msg: types.Message, state: FSMContext):
    comp_processor = msg.text
    await state.update_data({'comp': comp_processor})
    await msg.answer("Kompyuteringizni hotirasini kiriting: ")
    await CompStates.next()


@dp.message_handler(state=CompStates.memory)
async def location_send(msg: types.Message, state: FSMContext):
    comp_ram = msg.text
    await state.update_data({'memory': comp_ram})
    await msg.answer("Kompyuteringizni operativ xotirasini(ram) kiriting: ")
    await CompStates.next()


@dp.message_handler(state=CompStates.ram)
async def location_send(msg: types.Message, state: FSMContext):
    phone_ram = msg.text
    await state.update_data({'ram': phone_ram})
    await msg.answer("Kompyuteringizni narxini kiriting: ")
    await CompStates.next()


@dp.message_handler(state=CompStates.price)
async def phone_price_send(msg: types.Message, state: FSMContext):
    price = msg.text
    await state.update_data({'price': price})
    post = "Telefon sotiladi"
    async with state.proxy() as data:
        post += f"\n🧔🏿 Sotuvchi: {data.get('name')}"
        post += f"\n📞 Tel nomer: {data.get('number')}"
        post += f"\n📍 Manzil: {data.get('location')}"
        post += f"\n📱 Comp: {data.get('comp')}"
        post += f"\n📱 Comp processor: {data.get('processor')}"
        post += f"\n📝 Comp hotirasi: {data.get('memory')}"
        post += f"\n📝 RAM: {data.get('ram')}"
        post += f"\n💵 Comp narxi: {data.get('price')}"
    await msg.reply(post)
    await msg.answer("Adminga yuborish uchun tasdiqlang: ", reply_markup=yes_or_no)
    await CompStates.next()


@dp.callback_query_handler(phone_callback_data.filter(action='post'), state=CompStates.confirm)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Post adminga yuborildi.")
    await call.message.edit_reply_markup()
    post = "Telefon sotiladi"
    async with state.proxy() as data:
        mention = data.get("mention")
        post += f"\n🧔🏿 Sotuvchi: {data.get('name')}"
        post += f"\n📞 Tel nomer: {data.get('number')}"
        post += f"\n📍 Manzil: {data.get('location')}"
        post += f"\n📱 Comp: {data.get('comp')}"
        post += f"\n📱 Comp processor: {data.get('processor')}"
        post += f"\n📝 Comp hotirasi: {data.get('memory')}"
        post += f"\n📝 RAM: {data.get('ram')}"
        post += f"\n💵 Comp narxi: {data.get('price')}"
        post += f"\n\n#{data.get('comp').split()[0]}, {data.get('memory')}"
        chat = await bot.get_chat(CHANNELS[0])
        invite_link = await chat.export_invite_link()
        post += f"\n\n<a href={invite_link}>E'lon</a> kanalga ulanish"
    await state.finish()
    await bot.send_message(ADMINS[0], f"{mention} bu user kanalga quyidagi elonni chiqarmoqchi")
    await bot.send_message(ADMINS[0], post, reply_markup=yes_or_no)


@dp.callback_query_handler(phone_callback_data.filter(action='cancel'), state=CompStates.confirm)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Post adminga yuborilmadi.")
    await call.message.edit_reply_markup()
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=CompStates.confirm, content_types=types.ContentType.ANY)
async def send_admin(call: CallbackQuery):
    await call.message.answer("Tasdiqlash yoki rad etishni tanlang.")


@dp.callback_query_handler(phone_callback_data.filter(action='post'), chat_id=ADMINS)
async def send_admin(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berildi.", show_alert=True)
    target_channel = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(phone_callback_data.filter(action='cancel'), chat_id=ADMINS)
async def send_admin(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berilmadi.", show_alert=True)
    await call.message.edit_reply_markup()
