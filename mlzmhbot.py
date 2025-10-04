from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# 🔐 التوكن الخاص بك
BOT_TOKEN = '8272472614:AAEdNOE22VW2yFoYCzcOHoRHIVp661KbgTs'

# 📚 قائمة المواد
subjects = {
    'data_management': {
        'name': 'إدارة البيانات والمعلومات',
        'professor': 'د. ضياء عبد الستار',
        'file': 'data_management.pdf'
    },
    'object_programming': {
        'name': 'برمجة كيانية', 
        'professor': 'د. آلاء عبد مسلم',
        'file': 'object_programming.pdf'
    },
    'data_structures': {
        'name': 'هياكل بيانات',
        'professor': 'م.م. هالة محمد', 
        'file': 'data_structures.pdf'
    },
    'systems_analysis': {
        'name': 'تحليل وتصميم نظم',
        'professor': 'أ.م. رافد نبيل',
        'file': 'systems_analysis.pdf'
    },
    'cyber_crimes': {
        'name': 'جرائم إلكترونية',
        'professor': 'د. نورس سرحان',
        'file': 'cyber_crimes.pdf'
    },
    'numerical_analysis': {
        'name': 'تحليل عددي',
        'professor': 'أ.م.د. علاء حسين',
        'file': 'numerical_analysis.pdf'
    }
}

# 🏁 أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 إدارة البيانات والمعلومات", callback_data='data_management')],
        [InlineKeyboardButton("💻 برمجة كيانية", callback_data='object_programming')],
        [InlineKeyboardButton("🔗 هياكل بيانات", callback_data='data_structures')],
        [InlineKeyboardButton("📋 تحليل وتصميم نظم", callback_data='systems_analysis')],
        [InlineKeyboardButton("🛡️ جرائم إلكترونية", callback_data='cyber_crimes')],
        [InlineKeyboardButton("📐 تحليل عددي", callback_data='numerical_analysis')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎓 **مرحباً بك في بوت ملازم قسم نظم المعلومات**\n\n"
        "اختر المادة التي تريد تحميل ملزمتها:",
        reply_markup=reply_markup
    )

# 🔘 معالجة الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    subject_id = query.data
    
    if subject_id in subjects:
        subject = subjects[subject_id]
        
        # التحقق من وجود الملف
        if os.path.exists(subject['file']):
            with open(subject['file'], 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=pdf_file,
                    filename=f"{subject['name']}.pdf",
                    caption=f"📚 **{subject['name']}**\n"
                           f"👨‍🏫 **الأستاذ:** {subject['professor']}\n"
                           f"✅ تم التحميل بنجاح!"
                )
        else:
            await query.message.reply_text(
                f"📖 **{subject['name']}**\n"
                f"👨‍🏫 **الأستاذ:** {subject['professor']}\n\n"
                f"⏳ عذراً، الملزمة غير متوفرة حالياً.\n"
                f"سيتم توفيرها قريباً إن شاء الله 📚"
            )

# ℹ️ أمر المساعدة
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 **أوامر البوت:**

/start - بدء استخدام البوت وعرض المواد
/help - عرض هذه الرسالة
/materials - عرض جميع المواد المتاحة

📞 **للتواصل أو الإبلاغ عن مشكلة:**
راسل الإدارة للحصول على المساعدة.
"""
    await update.message.reply_text(help_text)

# 📋 عرض جميع المواد
async def materials_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    materials_text = "📚 **المواد المتاحة:**\n\n"
    
    for subject_id, subject in subjects.items():
        materials_text += f"• {subject['name']}\n"
        materials_text += f"  👨‍🏫 {subject['professor']}\n\n"
    
    materials_text += "🔹 استخدم /start لتحميل الملازم"
    
    await update.message.reply_text(materials_text)

# 🚀 تشغيل البوت
if __name__ == '__main__':
    # إنشاء التطبيق
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # إضافة ال handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("materials", materials_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 بوت الملازم يعمل الآن...")
    print("📍 أرسل /start إلى بوتك في تيليجرام")
    
    # بدء الاستقبال
    app.run_polling()