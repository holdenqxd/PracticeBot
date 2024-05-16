import telebot
TOKEN = '6484373536:AAGPav4PUEMKxNqpTyR-tUI3fERI6DhNMQc'

bot = telebot.TeleBot(TOKEN)

expense_tracker = {}
budget_tracker = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для отслеживания расходов. Используй команду /help, чтобы узнать доступные команды.")


@bot.message_handler(commands=['help'])
def help(message):
    help_text = "Доступные команды:\n" \
                "/add_expense <сумма> <категория> <описание> - добавить расход\n" \
                "/add_income <сумма> <описание> - добавить доход\n" \
                "/delete_transaction <индекс> - удалить транзакцию\n" \
                "/set_budget <сумма> - установить бюджет\n" \
                "/view_balance - просмотреть текущий баланс\n" \
                "/view_transactions - просмотреть транзакции\n" \
                "/view_budget - просмотреть бюджет"
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['add_expense'])
def add_expense(message):
    try:
        amount, category, description = message.text.split()[1:]
        amount = float(amount)
        user_id = message.from_user.id

        if user_id not in expense_tracker:
            expense_tracker[user_id] = {"balance": 0, "transactions": []}

        expense_tracker[user_id]["balance"] -= amount
        expense_tracker[user_id]["transactions"].append({"amount": -amount, "category": category, "description": description})

        bot.send_message(message.chat.id, f"Расход в размере {amount} добавлен успешно!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неправильный формат команды! Используй: /add_expense <сумма> <категория> <описание>")

@bot.message_handler(commands=['add_income'])
def add_income(message):
    try:
        amount, description = message.text.split()[1:]
        amount = float(amount)
        user_id = message.from_user.id

        if user_id not in expense_tracker:
            expense_tracker[user_id] = {"balance": 0, "transactions": []}

        expense_tracker[user_id]["balance"] += amount
        expense_tracker[user_id]["transactions"].append({"amount": amount, "category": "Доход", "description": description})

        bot.send_message(message.chat.id, f"Доход в размере {amount} добавлен успешно!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неправильный формат команды! Используй: /add_income <сумма> <описание>")

@bot.message_handler(commands=['delete_transaction'])
def delete_transaction(message):
    try:
        index = int(message.text.split()[1]) - 1
        user_id = message.from_user.id

        if user_id in expense_tracker and 0 <= index < len(expense_tracker[user_id]["transactions"]):
            transaction = expense_tracker[user_id]["transactions"].pop(index)
            expense_tracker[user_id]["balance"] += transaction["amount"]
            bot.send_message(message.chat.id, "Транзакция удалена успешно!")
        else:
            bot.send_message(message.chat.id, "Неправильный индекс транзакции!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неправильный формат команды! Используй: /delete_transaction <индекс>")

@bot.message_handler(commands=['set_budget'])
def set_budget(message):
    try:
        amount = float(message.text.split()[1])
        user_id = message.from_user.id
        budget_tracker[user_id] = amount
        bot.send_message(message.chat.id, f"Бюджет в размере {amount} установлен успешно!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неправильный формат команды! Используй: /set_budget <сумма>")

@bot.message_handler(commands=['view_budget'])
def view_budget(message):
    user_id = message.from_user.id
    if user_id in budget_tracker:
        budget = budget_tracker[user_id]
        bot.send_message(message.chat.id, f"Твой текущий бюджет: {budget}")
    else:
        bot.send_message(message.chat.id, "Бюджет не установлен!")

@bot.message_handler(commands=['view_balance'])
def view_balance(message):
    user_id = message.from_user.id
    if user_id in expense_tracker:
        balance = expense_tracker[user_id]["balance"]
        bot.send_message(message.chat.id, f"Твой текущий баланс: {balance}")
    else:
        bot.send_message(message.chat.id, "Нет данных! Начни с добавления транзакций.")

@bot.message_handler(commands=['view_transactions'])
def view_transactions(message):
    user_id = message.from_user.id
    if user_id in expense_tracker:
        transactions = expense_tracker[user_id]["transactions"]
        if transactions:
            message_text = "Твои транзакции:\n"
            for i, transaction in enumerate(transactions, 1):
                message_text += f"{i}. {transaction['category']}: {transaction['amount']} - {transaction['description']}\n"
            bot.send_message(message.chat.id, message_text)
        else:
            bot.send_message(message.chat.id, "Нет транзакций!")
    else:
        bot.send_message(message.chat.id, "Нет данных! Начни с добавления транзакций.")

bot.polling()