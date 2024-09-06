from app.views import *
import os
from core.settings import BASE_DIR
from bot.services.notification_service import send_start_message_notify_job
from bot.bot import application

def get_file(request, path):
    file = open(os.path.join(BASE_DIR, f'files/{path}'), 'rb')
    return FileResponse(file)

@login_required
def telegram_login(request):
    if params := request.GET:
        user_tg_id = params['id']
        user: Manager = request.user
        user.tg_id = user_tg_id
        user.save()
        from bot.control.updater import application
        bot_username = (
            async_to_sync(application.bot.get_me)()
        ).username
        context = {
            "bot_username": bot_username
        }
        # send start message to bot
        application.job_queue.run_once(
            send_start_message_notify_job, 1, data=user_tg_id
        )
        return render(request, 'telegram_login.html', context)
    else:
        return JsonResponse({'Error': True})