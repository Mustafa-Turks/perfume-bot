
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN غير موجود")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

PERFUMES = {
    "men": [
        ("بلو دي شانيل", "25,000 د.ع", "عطر رجالي أنيق ومنعش."),
        ("ديور سوفاج", "30,000 د.ع", "عطر رجالي قوي ومنعش."),
    ],
    "women": [
        ("لانكوم", "30,000 د.ع", "عطر نسائي ناعم وأنيق."),
        ("شانيل", "35,000 د.ع", "عطر نسائي فخم وأنيق."),
    ],
    "unisex": [
        ("مسك", "20,000 د.ع", "رائحة هادئة ومناسبة للجميع."),
    ],
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("👨 عطور رجالية", callback_data="men"),
            InlineKeyboardButton("👩 عطور نسائية", callback_data="women"),
        ],
        [
            InlineKeyboardButton("🌸 عطور للجنسين", callback_data="unisex"),
        ],
        [
            InlineKeyboardButton("📞 التواصل والطلب", callback_data="contact"),
        ],
    ]

    await update.message.reply_text(
        "🌹 أهلاً وسهلاً بك في متجر العطور\n\n"
        "اختار القسم اللي تريد تتصفحه:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "contact":
        await query.edit_message_text(
            "📞 للطلب والاستفسار تواصل معنا.\n\n"
            "سنضيف رقم الهاتف وواتساب لاحقاً."
        )
        return

    if query.data == "home":
        await start_from_button(query)
        return

    perfumes = PERFUMES.get(query.data, [])

    text = "🌹 العطور المتوفرة:\n\n"

    for name, price, description in perfumes:
        text += (
            f"🧴 {name}\n"
            f"💰 السعر: {price}\n"
            f"📝 {description}\n\n"
        )

    keyboard = [
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="home")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def start_from_button(query):
    keyboard = [
        [
            InlineKeyboardButton("👨 عطور رجالية", callback_data="men"),
            InlineKeyboardButton("👩 عطور نسائية", callback_data="women"),
        ],
        [
            InlineKeyboardButton("🌸 عطور للجنسين", callback_data="unisex"),
        ],
        [
            InlineKeyboardButton("📞 التواصل والطلب", callback_data="contact"),
        ],
    ]

    await query.edit_message_text(
        "🌹 القائمة الرئيسية\n\nاختار القسم:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(
            buttons,
            pattern="^(men|women|unisex|contact|home)$"
        )
    )

    print("✅ عطر-بوت يعمل الآن")

    app.run_polling()


if __name__ == "__main__":
    main()
