# main.py
from dotenv import load_dotenv
load_dotenv()  # Loads variables from your local .env file

from telegram import BotCommand, BotCommandScopeChat, BotCommandScopeDefault, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    MessageReactionHandler,
    filters,
)
from config import (
    BOT_TOKEN,
    ADMIN_ID,
    READ_TIMEOUT,
    WRITE_TIMEOUT,
    CONNECT_TIMEOUT,
    POOL_TIMEOUT,
    log,
)
from database import init_db
from batch_handlers import (
    start,
    get_link,
    link_stats,
    broadcast_cmd,
    on_rotate_button,
    on_delete_button,
    on_button,
    cleanup_deliveries_job,
)
from chat_handlers import handle_incoming_message, on_message_reaction

async def post_init(app: Application):
    # Hide the command menu globally for regular users
    await app.bot.set_my_commands([], scope=BotCommandScopeDefault())
    
    # Only show the command menu for the admin chat if ADMIN_ID is set
    if ADMIN_ID:
        try:
            await app.bot.set_my_commands(
                [
                    BotCommand("start", "Start / redeem a code"),
                    BotCommand("get_link", "Create a new media batch link"),
                    BotCommand("link_stats", "View, rotate, or delete your links"),
                    BotCommand("broadcast", "Interactive multi-media broadcast to all users"),
                ],
                scope=BotCommandScopeChat(chat_id=ADMIN_ID),
            )
        except Exception as e:
            log.warning(f"Could not set admin commands yet (chat not found): {e}")

def main():
    if not BOT_TOKEN:
        log.error("BOT_TOKEN is missing! Please set it in your environment or .env file.")
        return

    init_db()
    
    # Build application with custom network timeouts for large video transfers
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(READ_TIMEOUT)
        .write_timeout(WRITE_TIMEOUT)
        .connect_timeout(CONNECT_TIMEOUT)
        .pool_timeout(POOL_TIMEOUT)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_link", get_link))
    app.add_handler(CommandHandler("link_stats", link_stats))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))

    app.add_handler(MessageHandler(~filters.COMMAND, handle_incoming_message))
    app.add_handler(MessageReactionHandler(on_message_reaction))

    app.add_handler(CallbackQueryHandler(on_rotate_button, pattern=r"^rotate_"))
    app.add_handler(CallbackQueryHandler(on_delete_button, pattern=r"^del_"))
    app.add_handler(CallbackQueryHandler(on_button))

    app.job_queue.run_repeating(cleanup_deliveries_job, interval=30, first=10)

    log.info("Bot starting with video stability enhancements & higher timeouts...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()