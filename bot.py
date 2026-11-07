import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import urllib.request
import json
from flask import Flask
import threading

TOKEN_BOT = os.environ.get("TOKEN_BOT")
API_GEMINI = os.environ.get("API_GEMINI")

app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot lagi jalan bang!"

def jalanin_web():
    app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo bang! Tanya apa aja, gua jawab kayak AI")

async def ai_bales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = update.message.text
    await update.message.reply_text("Bentar, gua mikir dulu...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_GEMINI}"
        data = {"contents": [{"parts": [{"text": f"Kamu adalah asisten gaul Indonesia, jawab santai, singkat, pake bahasa gaul. Pertanyaan: {pesan}"}]}]}
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as res:
            hasil = json.loads(res.read().decode())
        jawaban = hasil["candidates"][0]["content"]["parts"][0]["text"]
        await update.message.reply_text(jawaban)
    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("Waduh sinyal lagi jelek nih, coba tanya lagi bang")

if __name__ == "__main__":
    threading.Thread(target=jalanin_web).start()
    app = Application.builder().token(TOKEN_BOT).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_bales))
    print("Bot AI jalan...")
    app.run_polling()
