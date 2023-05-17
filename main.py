from pyrogram import Client, filters

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Функція для перевірки, чи є обліковий запис підозрілим
def is_fake_account(member):
    if member.status == member.status.ADMINISTRATOR or member.status == member.status.OWNER:
        return False

    # Якщо обліковий запис є ботом, має обмеження або не був активним за останній місяць,
    # вважаємо його підозрілим
    return member.user.is_bot or member.user.is_restricted or not member.user.status.LAST_MONTH


@app.on_message(filters.command("start"))
async def start_command(client, message):
    # Обробник команди /start
    await message.reply_text("Привіт! Я Telegram-бот, який може очистити чат від фейкових облікових записів та ботів.")


@app.on_message(filters.command("cleanup"))
async def cleanup_command(client, message):
    # Обробник команди /cleanup
    chat_id = message.chat.id
    members = []

    # Отримуємо список учасників чату
    async for member in app.get_chat_members(chat_id, limit=200):
        members.append(member)

    # Перевіряємо кожного учасника і виключаємо підозрілі облікові записи
    for member in members:
        # Перевіряємо, чи є обліковий запис підозрілим і чи не є він самим ботом
        if is_fake_account(member):
            # Виключаємо підозрілий обліковий запис з чату
            await app.ban_chat_member(chat_id, member.user.id)

    await message.reply_text("Чат очищено від неактивних користувачів.")


app.run()
