from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .parser import parse_resume
from .scoring import calculate_match_score

SHORTLIST_THRESHOLD = 50  # percent


@shared_task
def process_resume(candidate_id):
    from .models import Candidate

    candidate = Candidate.objects.select_related("job").get(id=candidate_id)
    parsed = parse_resume(candidate.resume.path)
    candidate.name = parsed["name"]
    candidate.email = parsed["email"]
    candidate.skills = parsed["skills"]
    candidate.experience_years = parsed["experience_years"]
    candidate.raw_text = parsed["raw_text"]
    candidate.score = calculate_match_score(
        candidate.skill_list(),
        candidate.job.skill_list(),
        candidate.experience_years,
        candidate.job.minimum_experience,
    )
    candidate.processed_at = timezone.now()

    if candidate.score >= SHORTLIST_THRESHOLD:
        candidate.status = Candidate.Status.SHORTLISTED
        candidate.save()
        send_candidate_status_email.delay(candidate.id)
    else:
        candidate.save()

    return candidate.id


@shared_task
def send_candidate_status_email(candidate_id):
    from .models import Candidate, EmailLog

    candidate = Candidate.objects.select_related("job").get(id=candidate_id)

    if not candidate.email:
        EmailLog.objects.create(
            candidate=candidate,
            status=EmailLog.Status.SKIPPED,
            error_message="Candidate has no email address.",
        )
        return "Candidate has no email address."

    if candidate.status == Candidate.Status.SHORTLISTED:
        subject = f"Congratulations! Shortlisted for {candidate.job.title}"

        # Use custom job message if provided, otherwise use default
        custom_note = candidate.job.shortlist_message.strip()
        if custom_note:
            body_note = custom_note
        else:
            body_note = (
                "You have caught our attention and we are excited about your profile. "
                "We will be in touch soon with further communication regarding the next steps."
            )

        message = (
            f"Dear {candidate.name},\n\n"
            f"Congratulations! You have been shortlisted for the position of {candidate.job.title}.\n\n"
            f"{body_note}\n\n"
            f"Best regards,\n"
            f"The Recruiting Team"
        )
    elif candidate.status == Candidate.Status.REJECTED:
        subject = f"Update on your application for {candidate.job.title}"
        message = (
            f"Dear {candidate.name},\n\n"
            f"Thank you for taking the time to apply for the position of {candidate.job.title}.\n\n"
            f"After careful consideration, we are sorry to inform you that we will not be moving "
            f"forward with your application at this time.\n\n"
            f"We appreciate your interest and wish you the very best in your job search.\n\n"
            f"Best regards,\n"
            f"The Recruiting Team"
        )
    else:
        EmailLog.objects.create(
            candidate=candidate,
            recipient=candidate.email,
            status=EmailLog.Status.SKIPPED,
            error_message="No email is sent when candidate status is Review.",
        )
        return "No email sent for review status."

    try:
        send_mail(subject, message, None, [candidate.email], fail_silently=False)
    except Exception as exc:
        EmailLog.objects.create(
            candidate=candidate,
            recipient=candidate.email,
            subject=subject,
            status=EmailLog.Status.FAILED,
            error_message=str(exc),
        )
        return f"Email failed: {exc}"

    EmailLog.objects.create(
        candidate=candidate,
        recipient=candidate.email,
        subject=subject,
        status=EmailLog.Status.SENT,
    )
    return f"Email sent to {candidate.email}"