from aiogram.dispatcher import FSMContext
from data.config import CHANNELS
from data.config import ADMINS
from keyboards.default import phone_number, location_buttons
from keyboards.inline import yes_or_no
from keyboards.inline.confirum_buttons import phone_callback_data
from states import PhoneStates
from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery


@dp.message_handler(text="Telefon sotish")
async def sell_phone(msg: types.Message, state: FSMContext):
    await msg.answer("Ism familiyangizni kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PhoneStates.name)


@dp.message_handler(state=PhoneStates.name)
async def name_send(msg: types.Message, state: FSMContext):
    name = msg.text
    await state.update_data({'name': name, 'mention': msg.from_user.get_mention(as_html=True)})
    await msg.answer("Telefon raqamingizni kiriting yoki kiriting: ", reply_markup=phone_number)
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.number)
async def name_send(msg: types.Message, state: FSMContext):
    number = msg.text
    await state.update_data({'number': number})
    await msg.answer("Joylashuvingizni yuboring yoki manzilingizni kiriting: ", reply_markup=location_buttons)
    await PhoneStates.next()


@dp.message_handler(content_types=types.ContentType.CONTACT, is_sender_contact=True, state=PhoneStates.number)
async def phone_send(msg: types.Message, state: FSMContext):
    contact = msg.contact.phone_number
    await state.update_data({'number': contact})
    await msg.answer("Joylashuvingizni yuboring yoki manzilingizni kiriting: ", reply_markup=location_buttons)
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.location)
async def name_send(msg: types.Message, state: FSMContext):
    location = msg.text
    await state.update_data({'location': location})
    await msg.answer("Telefoningizni nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await PhoneStates.next()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=PhoneStates.location)
async def location_send(msg: types.Message, state: FSMContext):
    location = msg.text
    await state.update_data({'location': location})
    await msg.answer("Telefoningizni nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.phone)
async def location_send(msg: types.Message, state: FSMContext):
    phone_name = msg.text
    await state.update_data({'phone': phone_name})
    await msg.answer("Telefoningizni hotirasini kiriting: ")
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.memory)
async def location_send(msg: types.Message, state: FSMContext):
    phone_ram = msg.text
    await state.update_data({'memory': phone_ram})
    await msg.answer("Telefoningizni operativ xotirasini(ram) kiriting: ")
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.ram)
async def location_send(msg: types.Message, state: FSMContext):
    phone_ram = msg.text
    await state.update_data({'ram': phone_ram})
    await msg.answer("Telefoningizni narxini kiriting: ")
    await PhoneStates.next()


@dp.message_handler(state=PhoneStates.price)
async def phone_price_send(msg: types.Message, state: FSMContext):
    price = msg.text
    await state.update_data({'price': price})
    post = "Telefon sotiladi"
    async with state.proxy() as data:
        post += f"\n🧔🏿 Sotuvchi: {data.get('name')}"
        post += f"\n📞 Tel nomer: {data.get('number')}"
        post += f"\n📍 Manzil: {data.get('location')}"
        post += f"\n📱 Telefon: {data.get('phone')}"
        post += f"\n📝 Telefon hotirasi: {data.get('memory')}"
        post += f"\n📝 RAM: {data.get('ram')}"
        post += f"\n💵 Telefon narxi: {data.get('price')}"
    await msg.reply(post)
    await msg.answer("Adminga yuborish uchun tasdiqlang: ", reply_markup=yes_or_no)
    await PhoneStates.next()


@dp.callback_query_handler(phone_callback_data.filter(action='post'), state=PhoneStates.confirm)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Post adminga yuborildi.")
    await call.message.edit_reply_markup()
    post = "Telefon sotiladi"
    async with state.proxy() as data:
        mention = data.get("mention")
        post += f"\n🧔🏿 Sotuvchi: {data.get('name')}"
        post += f"\n📞 Tel nomer: {data.get('number')}"
        post += f"\n📍 Manzil: {data.get('location')}"
        post += f"\n📱 Telefon: {data.get('phone')}"
        post += f"\n📝 Telefon hotirasi: {data.get('memory')}"
        post += f"\n📝 RAM: {data.get('ram')}"
        post += f"\n💵 Telefon narxi: {data.get('price')}"
        post += f"\n\n#{data.get('phone').split()[0]}, {data.get('memory')}"
        chat = await bot.get_chat(CHANNELS[0])
        invite_link = await chat.export_invite_link()
        post += f"\n\n<a href={invite_link}>E'lon</a> kanalga ulanish"
    await state.finish()
    await bot.send_message(ADMINS[-1], f"{mention} bu user kanalga quyidagi elonni chiqarmoqchi")
    await bot.send_message(ADMINS[-1], post, reply_markup=yes_or_no)


@dp.callback_query_handler(phone_callback_data.filter(action='cancel'), state=PhoneStates.confirm)
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Post adminga yuborilmadi.")
    await call.message.edit_reply_markup()
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=PhoneStates.confirm, content_types=types.ContentType.ANY)
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
