import click
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from firebase_config import signup, login, fetch_users, save_meeting, fetch_meetings, cancel_meeting

# Google Calendar Setup
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("calendar", "v3", credentials=creds)

def validate_meeting_time(meeting_time):
    day = meeting_time.weekday()
    hour = meeting_time.hour
    return day < 5 and 7 <= hour < 17

def create_event(summary, start_time, end_time, attendees):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "start": {"dateTime": start_time.isoformat()},
        "end": {"dateTime": end_time.isoformat()},
        "attendees": [{"email": email} for email in attendees]
    }
    service.events().insert(calendarId="primary", body=event).execute()

# CLI Commands
@click.group()
def cli():
    """SkillSync CLI - Manage your workshops and meetings."""
    pass

@click.command()
@click.argument("email")
@click.argument("password")
@click.argument("name")
@click.argument("role")
@click.option("--expertise", default=None, help="Optional expertise for mentors.")
def signup_cli(email, password, name, role, expertise):
    """Signup a new user."""
    click.echo(signup(email, password, name, role, expertise))

@click.command()
@click.argument("email")
@click.argument("password")
def login_cli(email, password):
    """Login an existing user."""
    token, uid = login(email, password)
    if token:
        click.echo("Login successful!")
    else:
        click.echo("Login failed!")

@click.command()
def view_workshops():
    """View available workshops and mentors."""
    mentors = fetch_users("mentor")
    for mentor in mentors.each():
        mentor_data = mentor.val()
        click.echo(f"{mentor.key}: {mentor_data['name']} ({mentor_data.get('expertise', 'N/A')})")

@click.command()
@click.argument("mentor_id")
@click.argument("peer_id")
@click.argument("meeting_time", type=click.DateTime())
def request_meeting(mentor_id, peer_id, meeting_time):
    """Request a meeting with a mentor or peer."""
    if validate_meeting_time(meeting_time):
        save_meeting(mentor_id, peer_id, meeting_time)
        click.echo("Meeting booked successfully!")
    else:
        click.echo("Meetings must be scheduled on weekdays between 07:00 and 17:00.")

@click.command()
def view_bookings():
    """View all confirmed bookings."""
    meetings = fetch_meetings()
    for meeting in meetings.each():
        meeting_data = meeting.val()
        click.echo(f"{meeting.key}: Mentor: {meeting_data['mentor_id']}, Peer: {meeting_data['peer_id']}, Time: {meeting_data['time']}")

@click.command()
@click.argument("booking_id")
def cancel_booking_cli(booking_id):
    """Cancel an existing booking."""
    cancel_meeting(booking_id)
    click.echo("Booking canceled!")

# Add CLI Commands
cli.add_command(signup_cli, "signup")
cli.add_command(login_cli, "login")
cli.add_command(view_workshops, "view-workshops")
cli.add_command(request_meeting, "request-meeting")
cli.add_command(view_bookings, "view-bookings")
cli.add_command(cancel_booking_cli, "cancel-booking")

if __name__ == "__main__":
    cli()
