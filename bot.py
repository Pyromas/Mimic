import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import pandas as pd


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


transactions = pd.DataFrame(columns=["type", "amount", "category"])

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение, когда бот запускается."""
    update.message.reply_text(
        "Привет! Я бот для отслеживания бюджета. Используй /add_income для добавления дохода, "
        "/add_expense для добавления расхода и /summary для получения итогов."
    )

def add_income(update: Update, context: CallbackContext) -> None:
    """Добавляет доход."""
    try:
        amount = float(context.args[0])
        category = context.args[1]
        global transactions
        transactions = pd.concat([transactions, pd.DataFrame({"type": ["income"], "amount": [amount], "category": [category]})], ignore_index=True)
        update.message.reply_text(f"Доход в размере {amount} руб. добавлен в категорию {category}.")
    except (IndexError, ValueError):
        update.message.reply_text("Используй команду так: /add_income <сумма> <категория>")

def add_expense(update: Update, context: CallbackContext) -> None:
    """Добавляет расход."""
    try:
        amount = float(context.args[0])
        category = context.args[1]
        global transactions
        transactions = pd.concat([transactions, pd.DataFrame({"type": ["expense"], "amount": [amount], "category": [category]})], ignore_index=True)
        update.message.reply_text(f"Расход в размере {amount} руб. добавлен в категорию {category}.")
    except (IndexError, ValueError):
        update.message.reply_text("Используй команду так: /add_expense <сумма> <категория>")

def summary(update: Update, context: CallbackContext) -> None:
    """Отправляет итоговые данные о бюджете."""
    global transactions
    income_total = transactions[transactions["type"] == "income"]["amount"].sum()
    expense_total = transactions[transactions["type"] == "expense"]["amount"].sum()
    balance = income_total - expense_total

    summary_message = (
        f"Общий доход: {income_total} руб.\n"
        f"Общие расходы: {expense_total} руб.\n"
        f"Текущий баланс: {balance} руб."
    )
    update.message.reply_text(summary_message)

def main() -> None:
    """Запускает бота."""
    TOKEN = ''  
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_income", add_income))
    application.add_handler(CommandHandler("add_expense", add_expense))
    application.add_handler(CommandHandler("summary", summary))

    
    application.run_polling()

if __name__ == '__main__':
    main()
