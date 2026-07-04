"""Email service using Resend API for transactional emails."""

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger("email_service")


class ResendEmailService:
    """Send emails via Resend API."""

    def __init__(self):
        """Initialize Resend email service."""
        self.api_key = os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "community@soulconnect.health")
        self.admin_email = os.getenv("ADMIN_EMAIL", "community@soulconnect.health")

        if not self.api_key:
            logger.warning("RESEND_API_KEY not configured - emails will not be sent")

    def send_welcome_email(self, user_email: str, user_name: Optional[str] = None) -> bool:
        """
        Send welcome email to new waitlist member with SoulConnect logo header.

        Returns True if successful, False otherwise.
        """
        if not self.api_key:
            logger.warning("Cannot send welcome email: RESEND_API_KEY not set")
            return False

        try:
            import httpx

            display_name = user_name or "Friend"

            email_html = self._get_welcome_email_html(display_name)

            response = httpx.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "from": f"SoulConnect <{self.from_email}>",
                    "to": user_email,
                    "subject": "💜 Welcome to the SoulConnect Waitlist",
                    "html": email_html,
                },
                timeout=10.0,
            )

            if response.status_code in (200, 201):
                logger.info(f"Welcome email sent to {user_email}")
                return True
            else:
                logger.error(
                    f"Failed to send welcome email to {user_email}: "
                    f"Status {response.status_code}: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(f"Exception sending welcome email to {user_email}: {str(e)}")
            return False

    def send_admin_notification(
        self,
        user_email: str,
        user_name: Optional[str] = None,
        struggle: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """
        Send admin notification email when someone joins waitlist.

        Returns True if successful, False otherwise.
        """
        if not self.api_key:
            logger.warning("Cannot send admin notification: RESEND_API_KEY not set")
            return False

        try:
            import httpx

            current_date = datetime.utcnow().strftime("%Y-%m-%d")
            current_time = datetime.utcnow().strftime("%H:%M:%S UTC")

            email_html = self._get_admin_notification_html(
                user_email=user_email,
                user_name=user_name,
                struggle=struggle,
                date=current_date,
                time=current_time,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            response = httpx.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "from": f"SoulConnect <{self.from_email}>",
                    "to": self.admin_email,
                    "subject": "🎉 New Waitlist Signup",
                    "html": email_html,
                },
                timeout=10.0,
            )

            if response.status_code in (200, 201):
                logger.info(f"Admin notification sent for {user_email}")
                return True
            else:
                logger.error(
                    f"Failed to send admin notification for {user_email}: "
                    f"Status {response.status_code}: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(f"Exception sending admin notification for {user_email}: {str(e)}")
            return False

    @staticmethod
    def _get_welcome_email_html(user_name: str) -> str:
        """Generate welcome email HTML with new optimized design."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to SoulConnect</title>
            <style>
                * {{margin: 0; padding: 0; box-sizing: border-box;}}
                body {{font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif; line-height: 1.6; color: #1a1a1a;}}
                .container {{max-width: 600px; margin: 0 auto; background-color: #fff; overflow: hidden;}}
                .header {{padding: 0; margin: 0;}}
                .header img {{width: 100%; height: auto; display: block; margin: 0; padding: 0; line-height: 0; font-size: 0; border: none;}}
                .header-border {{height: 4px; background-color: #D4AF37; display: block; margin: 0; padding: 0;}}
                .content {{padding: 32px 24px; text-align: center;}}
                .welcome-icon {{font-size: 40px; margin-bottom: 12px; line-height: 40px;}}
                h1 {{font-size: 28px; font-weight: 700; color: #1a1a1a; margin: 0 0 8px 0; line-height: 1.2;}}
                .greeting {{font-size: 16px; font-weight: 600; color: #1a1a1a; margin: 0 0 16px 0; line-height: 1.4;}}
                .body-text {{font-size: 15px; color: #4a4a4a; margin: 8px 0; line-height: 1.5;}}
                .quote {{font-size: 16px; font-style: italic; color: #4B2E83; font-weight: 600; margin: 16px 0 0 0; line-height: 1.6;}}
                .what-section {{padding: 24px 24px 32px 24px;}}
                .section-label {{font-size: 14px; font-weight: 600; color: #4B2E83; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.4;}}
                .check-item {{font-size: 14px; color: #1a1a1a; margin: 0; padding: 6px 0; line-height: 1.5; text-align: left;}}
                .cta-section {{padding: 24px 24px; text-align: center;}}
                .cta-button {{background: #4B2E83; color: white; font-size: 15px; font-weight: 600; padding: 12px 32px; border-radius: 6px; text-decoration: none; display: inline-block; border: none; cursor: pointer;}}
                .closing-section {{padding: 24px 24px; text-align: center;}}
                .closing-text {{font-size: 14px; color: #4a4a4a; margin: 8px 0; line-height: 1.5;}}
                .heart-icon {{font-size: 24px; line-height: 24px; margin: 12px 0 0 0; display: block;}}
                .team-name {{font-size: 14px; color: #4B2E83; font-weight: 600; margin: 8px 0 0 0; line-height: 1.4;}}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://raw.githubusercontent.com/Amol3011-zap/soulconnect/main/emails/email.png" alt="SoulConnect" style="width: 100%; height: auto; display: block; margin: 0; padding: 0; line-height: 0; font-size: 0; border: none;">
                    <div class="header-border"></div>
                </div>

                <div class="content">
                    <div class="welcome-icon">💜</div>
                    <h1>Welcome to SoulConnect</h1>
                    <div class="greeting">Hi {user_name}! 👋</div>
                    <div class="body-text">Thank you for joining the SoulConnect waitlist.</div>
                    <div class="body-text">You're now part of a community built on one simple belief.</div>
                    <div class="quote">"You don't have to go through life's challenges alone."</div>
                </div>

                <div class="what-section">
                    <div class="section-label">What you'll get</div>
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin: 0 auto;">
                        <tr><td class="check-item">✔ Connect with people who understand</td></tr>
                        <tr><td class="check-item">✔ Daily wellness support</td></tr>
                        <tr><td class="check-item">✔ Access to trusted professionals</td></tr>
                    </table>
                </div>

                <div class="cta-section">
                    <a href="https://soulconnect.health" class="cta-button">Visit SoulConnect</a>
                </div>

                <div class="closing-section">
                    <div class="closing-text">We'll let you know as soon as early access is available.</div>
                    <div class="closing-text">Take care of yourself.</div>
                    <div class="heart-icon">💜</div>
                    <div class="team-name">The SoulConnect Team</div>
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def _get_admin_notification_html(
        user_email: str,
        user_name: Optional[str],
        struggle: Optional[str],
        date: str,
        time: str,
        ip_address: Optional[str],
        user_agent: Optional[str],
    ) -> str:
        """Generate admin notification email HTML."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Waitlist Signup</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                    line-height: 1.6;
                    color: #1a1a1a;
                    background-color: #f5f5f5;
                }}

                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}

                .header {{
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
                    border-radius: 12px 12px 0 0;
                    color: white;
                }}

                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}

                .content {{
                    padding: 30px;
                }}

                .field {{
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #e5e5e5;
                }}

                .field:last-child {{
                    border-bottom: none;
                }}

                .field-label {{
                    font-weight: 600;
                    color: #7C3AED;
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 5px;
                }}

                .field-value {{
                    font-size: 14px;
                    color: #1a1a1a;
                    word-break: break-word;
                }}

                .footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f9f5ff;
                    border-radius: 0 0 12px 12px;
                    font-size: 12px;
                    color: #4a4a4a;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 New Waitlist Signup</h1>
                </div>

                <div class="content">
                    <div class="field">
                        <div class="field-label">Email</div>
                        <div class="field-value">{user_email}</div>
                    </div>

                    {f'<div class="field"><div class="field-label">Name</div><div class="field-value">{user_name}</div></div>' if user_name else ''}

                    {f'<div class="field"><div class="field-label">Struggle</div><div class="field-value">{struggle}</div></div>' if struggle else ''}

                    <div class="field">
                        <div class="field-label">Date</div>
                        <div class="field-value">{date}</div>
                    </div>

                    <div class="field">
                        <div class="field-label">Time</div>
                        <div class="field-value">{time}</div>
                    </div>

                    {f'<div class="field"><div class="field-label">IP Address</div><div class="field-value">{ip_address}</div></div>' if ip_address else ''}

                    {f'<div class="field"><div class="field-label">User Agent</div><div class="field-value" style="font-size: 12px; word-wrap: break-word;">{user_agent}</div></div>' if user_agent else ''}
                </div>

                <div class="footer">
                    <p>This is an automated notification from SoulConnect.</p>
                </div>
            </div>
        </body>
        </html>
        """


# Singleton instance
_email_service = None


def get_email_service() -> ResendEmailService:
    """Get or create the email service singleton."""
    global _email_service
    if _email_service is None:
        _email_service = ResendEmailService()
    return _email_service
