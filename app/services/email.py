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
        Send welcome email to new waitlist member.

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
        """Generate welcome email HTML."""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to SoulConnect</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                    line-height: 1.6;
                    color: #1a1a1a;
                    background-color: #f5f5f5;
                }}

                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}

                .header {{
                    text-align: center;
                    padding: 30px 20px;
                    background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
                    border-radius: 12px 12px 0 0;
                    color: white;
                }}

                .logo {{
                    font-size: 28px;
                    font-weight: 800;
                    margin-bottom: 10px;
                }}

                .content {{
                    padding: 40px 30px;
                }}

                .greeting {{
                    font-size: 18px;
                    font-weight: 600;
                    color: #1a1a1a;
                    margin-bottom: 20px;
                }}

                .message {{
                    font-size: 14px;
                    color: #4a4a4a;
                    line-height: 1.8;
                    margin-bottom: 20px;
                }}

                .highlight {{
                    font-weight: 600;
                    color: #7C3AED;
                }}

                .benefits {{
                    margin: 30px 0;
                    padding: 20px;
                    background-color: #f9f5ff;
                    border-left: 4px solid #7C3AED;
                    border-radius: 6px;
                }}

                .benefits-title {{
                    font-weight: 600;
                    color: #1a1a1a;
                    margin-bottom: 15px;
                }}

                .benefit-item {{
                    font-size: 14px;
                    color: #4a4a4a;
                    margin-bottom: 10px;
                    padding-left: 25px;
                    position: relative;
                }}

                .benefit-item:before {{
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #10B981;
                    font-weight: bold;
                }}

                .cta-button {{
                    display: inline-block;
                    padding: 14px 32px;
                    background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    margin: 30px 0;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}

                .cta-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 16px rgba(124, 58, 237, 0.3);
                }}

                .closing {{
                    font-size: 14px;
                    color: #4a4a4a;
                    margin: 30px 0 20px;
                    line-height: 1.8;
                }}

                .tagline {{
                    font-size: 13px;
                    color: #7C3AED;
                    font-weight: 600;
                    font-style: italic;
                    margin-top: 15px;
                }}

                .footer {{
                    text-align: center;
                    padding: 30px;
                    background-color: #f9f5ff;
                    border-radius: 0 0 12px 12px;
                    font-size: 12px;
                    color: #4a4a4a;
                }}

                .footer-link {{
                    color: #7C3AED;
                    text-decoration: none;
                }}

                .divider {{
                    height: 1px;
                    background-color: #e5e5e5;
                    margin: 20px 0;
                }}

                .gold-accent {{
                    color: #EAB308;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">💜 SoulConnect</div>
                    <p style="font-size: 14px; opacity: 0.95;">Welcome to our community</p>
                </div>

                <div class="content">
                    <div class="greeting">Hi {user_name},</div>

                    <div class="message">
                        Thank you for joining the <span class="highlight">SoulConnect waitlist</span>.
                    </div>

                    <div class="message">
                        You're now part of a community built on one simple belief:
                    </div>

                    <div class="message" style="text-align: center; font-style: italic; color: #7C3AED; font-weight: 600; margin: 30px 0; font-size: 15px;">
                        "No one should have to go through life's challenges alone."
                    </div>

                    <div class="benefits">
                        <div class="benefits-title">We're building a place where you can:</div>
                        <div class="benefit-item">Connect with others who truly understand</div>
                        <div class="benefit-item">Build small daily wellness habits</div>
                        <div class="benefit-item">Find professional support when you need it</div>
                    </div>

                    <div class="message">
                        We'll notify you as soon as early access is available. In the meantime, take care of yourself.
                    </div>

                    <a href="https://soulconnect.health" class="cta-button">Visit SoulConnect</a>

                    <div class="closing">
                        Until then,<br>
                        Take care of yourself.<br>
                        <span class="gold-accent">💜</span>
                    </div>

                    <div class="closing" style="margin: 20px 0 0; color: #7C3AED; font-weight: 600;">
                        The SoulConnect Team
                    </div>

                    <div class="divider"></div>

                    <div style="text-align: center; color: #7C3AED; font-weight: 600; margin-top: 20px;">
                        https://soulconnect.health
                    </div>
                </div>

                <div class="footer">
                    <p>You're receiving this email because you joined the SoulConnect waitlist.</p>
                    <p style="margin-top: 10px;">
                        <a href="https://soulconnect.health/privacy" class="footer-link">Privacy Policy</a> ·
                        <a href="https://soulconnect.health/terms" class="footer-link">Terms of Service</a>
                    </p>
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
