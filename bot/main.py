import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder,
    Application,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from app.city_codes.city_codes import get_codes_for_city
from app.generator.generator import generate_national_id
from app.validator.validator import is_national_id_valid


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GET_CITY, GET_QUANTITY, GET_ID = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'سلام {update.message.from_user.first_name}! 👋\n\nبا این ربات می‌تونی این کارها رو انجام بدی:'
        '\n\tساختن کد ملی ← /generate' '\n\tاعتبارسنجی کد ملی ← /validate'
        '\nاگه مشکلی بود به پشتیبانی گزارش بده 🙂'
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'این کد ملی برای چه شهری باشه؟',
        reply_markup=ForceReply(input_field_placeholder='تهران')
    )
    return GET_CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    codes = get_codes_for_city(update.message.text.strip())
    if codes:
        context.user_data['codes'] = tuple(codes)
        await update.message.reply_text(
            'چه تعداد کد ملی میخوای؟ بین ۱ تا ۱۰۰ میتونی انتخاب کنی',
            reply_markup=ForceReply(input_field_placeholder='۱۰ یا 10')
        )
        return GET_QUANTITY

    await update.message.reply_text(
        'متاسفانه این شهر در دیتابیس پیدا نشد، به پشتیبانی پیام بده یا شهر دیگه‌ای رو امتحان کن:',
        reply_markup=ForceReply(input_field_placeholder='تهران')
    )
    return GET_CITY


async def get_quanity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    quanity = convert_num_to_en(update.message.text.strip())
    if quanity and 1 <= quanity <= 100:
        await update.message.reply_text(
            '\n'.join(
                generate_national_id(city_code_prefixes=context.user_data['codes'], quantity=int(quanity))
            ),
        )
        del context.user_data['codes']
        return ConversationHandler.END
    await update.message.reply_text(
        'عدد وارد شده صحیح نیست، بین ۱ تا ۱۰۰ میتونی انتخاب کنی',
        reply_markup=ForceReply(input_field_placeholder='۱۰ یا 10')
    )
    return GET_QUANTITY


async def validate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'یه کد ملی بفرس تا چک کنم:',
        reply_markup=ForceReply(input_field_placeholder='۰۱۲۳۴۵۶۷۸۹')
    )
    return GET_ID


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    national_id = convert_id_to_en(update.message.text.strip())
    if national_id and is_national_id_valid(national_id):
        await update.message.reply_text('این کد ملی معتبره! 🥳')
    else:
        await update.message.reply_text('سرت کلاه رفته! این کد ملی فیکه! 😭')
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return ConversationHandler.END


def convert_num_to_en(num: str) -> int:
    if num.isdigit():
        return int(num.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')))
    return None


def convert_id_to_en(national_id: str) -> str:
    if national_id.isdigit() and len(national_id) == 10:
        return national_id.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    return None


def register_handlers(app: Application) -> None:
    generate_handler = ConversationHandler(
        entry_points=[CommandHandler('generate', generate)],
        states={
            GET_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)
            ],
            GET_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_quanity)
            ]
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)]
    )

    validate_handler = ConversationHandler(
        entry_points=[CommandHandler('validate', validate)],
        states={
            GET_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)
            ]
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)]
    )

    app.add_handler(CommandHandler('start', start), 1)
    app.add_handler(generate_handler, 2)
    app.add_handler(validate_handler, 3)


def main() -> None:
    app: Application = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    app.run_polling()


if __name__ == '__main__':
    main()
