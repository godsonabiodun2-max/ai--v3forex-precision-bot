import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

MARKETS = [
    "XAUUSD",
    "GBPJPY",
    "BTCUSD",
    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "USDCHF",
    "USDCAD",
    "AUDUSD",
    "NZDUSD",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔎 SCAN MARKETS", callback_data="scan")],
        [InlineKeyboardButton("📊 MY MARKETS", callback_data="markets")],
        [InlineKeyboardButton("ℹ️ HELP", callback_data="help")],
    ]

    await update.message.reply_text(
        "🤖 PILOTBOT AI V3\n"
        "FOREX SIGNAL ASSISTANT\n\n"
        "Welcome!\n\n"
        "Markets: Gold, Forex and Bitcoin.\n"
        "Mode: Signals only. Manual execution on MT5.\n\n"
        "Choose an option below.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🔎 PILOTBOT AI V3 — MARKET SCANNER\n\n"
        "Markets configured: 10\n\n"
        "🥇 XAU/USD — Gold\n"
        "💷 GBP/JPY\n"
        "₿ BTC/USD\n"
        "💵 GBP/USD\n"
        "EUR/USD\n"
        "USD/JPY\n"
        "USD/CHF\n"
        "USD/CAD\n"
        "AUD/USD\n"
        "NZD/USD\n\n"
        "⚠️ LIVE MARKET DATA IS NOT CONNECTED YET.\n\n"
        "No live trading signal has been generated.\n"
        "The next setup is to connect and validate a market-data provider."
    )

    await update.effective_message.reply_text(message)


async def markets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📊 YOUR WATCHLIST\n\n"
        + "\n".join(f"• {market}" for market in MARKETS)
        + "\n\nBroker symbol names may differ."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🤖 PILOTBOT AI V3 — HELP\n\n"
        "/start - Open the main menu\n"
        "/scan - View scanner status\n"
        "/markets - View your watchlist\n"
        "/help - Show help\n\n"
        "This initial version does not generate trading signals "
        "or execute trades. Live market data and a tested strategy "
        "must be added first."
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "scan":
        await scan(update, context)

    elif query.data == "markets":
        await markets(update, context)

    elif query.data == "help":
        await help_command(update, context)


def main():
    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN environment variable is missing."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("markets", markets))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("PILOTBOT AI V3 is starting...")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
