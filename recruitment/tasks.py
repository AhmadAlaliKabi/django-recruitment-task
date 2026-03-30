from celery import shared_task


@shared_task
def test_resume_processing():
    return "Resume processing task executed successfully."
#Later, this could be replaced with real logic like: resume parsing AI skill extraction sending notifications