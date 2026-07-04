import React from 'react';
import {
  Body,
  Button,
  Container,
  Head,
  Hr,
  Html,
  Link,
  Preview,
  Section,
  Text,
} from 'react-email';
import { EmailHeader } from './components/EmailHeader';
import { EmailFooter } from './components/EmailFooter';
import { getFirstName } from './helpers/getFirstName';

interface WelcomeEmailProps {
  userEmail?: string;
  userName?: string;
}

export const WelcomeEmail = ({ userEmail, userName }: WelcomeEmailProps) => {
  const firstName = getFirstName(userName);
  const subject = firstName !== 'there' ? `💜 Welcome to SoulConnect, ${firstName}` : '💜 Welcome to SoulConnect';

  return (
    <Html lang="en">
      <Head>
        <meta name="color-scheme" content="light dark" />
        <meta name="supported-color-schemes" content="light dark" />
        <style>{`
          @media (prefers-color-scheme: dark) {
            .dark-text { color: #e5e5e5; }
            .dark-secondary { color: #a0a0a0; }
          }
        `}</style>
      </Head>
      <Preview>Thank you for joining the SoulConnect waitlist</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header - Compact */}
          <EmailHeader />

          {/* Welcome Section - Minimal */}
          <Section style={welcomeSection}>
            <Text style={welcomeIcon}>💜</Text>
            <Text style={welcomeTitle}>Welcome to SoulConnect</Text>
            <Text style={greeting}>Hi {firstName}! 👋</Text>
            <Text style={bodyText}>
              Thank you for joining the SoulConnect waitlist.
            </Text>
            <Text style={bodyText}>
              You're now part of a community built on one simple belief.
            </Text>
            <Text style={quote}>
              "You don't have to go through life's challenges alone."
            </Text>
          </Section>

          {/* What You'll Get - Compact List */}
          <Section style={whatSection}>
            <Text style={sectionLabel}>What you'll get</Text>
            <table role="presentation" cellPadding="0" cellSpacing="0" width="100%" style={checklistTable}>
              <tbody>
                <tr>
                  <td style={checklistItemStyle}>
                    <Text style={checkItem}>✔ Connect with people who understand</Text>
                  </td>
                </tr>
                <tr>
                  <td style={checklistItemStyle}>
                    <Text style={checkItem}>✔ Daily wellness support</Text>
                  </td>
                </tr>
                <tr>
                  <td style={checklistItemStyle}>
                    <Text style={checkItem}>✔ Access to trusted professionals</Text>
                  </td>
                </tr>
              </tbody>
            </table>
          </Section>

          {/* CTA - Single Button */}
          <Section style={ctaSection}>
            <Button
              pX={32}
              pY={12}
              style={ctaButton}
              href="https://soulconnect.health"
            >
              Visit SoulConnect
            </Button>
          </Section>

          {/* Closing - Brief */}
          <Section style={closingSection}>
            <Text style={closingText}>
              We'll let you know as soon as early access is available.
            </Text>
            <Text style={closingText}>
              Take care of yourself.
            </Text>
            <Text style={heartIcon}>💜</Text>
            <Text style={teamName}>The SoulConnect Team</Text>
          </Section>
        </Container>

        {/* VML Fallback for Outlook */}
        <div dangerouslySetInnerHTML={{
          __html: `<!--[if mso]>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
              <tr>
                <td style="padding: 24px 0;">
                  <table role="presentation" align="center" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                      <td style="border-radius: 6px; background: #4B2E83; padding: 12px 32px;">
                        <a href="https://soulconnect.health" style="color: white; text-decoration: none; font-weight: 600; display: block; font-size: 15px;">Visit SoulConnect</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          <![endif]-->`
        }} />
      </Body>
    </Html>
  );
};

WelcomeEmail.PreviewProps = {
  userEmail: 'user@example.com',
  userName: 'Amol Londhe',
};

export default WelcomeEmail;

// Optimized Styles
const main = {
  backgroundColor: '#ffffff',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif',
};

const container = {
  maxWidth: '600px',
  margin: '0 auto',
  width: '100%',
};

const welcomeSection = {
  padding: '32px 24px',
  textAlign: 'center' as const,
};

const welcomeIcon = {
  fontSize: '40px',
  lineHeight: '40px',
  margin: '0 0 12px 0',
  display: 'block',
  textAlign: 'center' as const,
};

const welcomeTitle = {
  fontSize: '28px',
  fontWeight: 700,
  color: '#1a1a1a',
  margin: '0 0 8px 0',
  lineHeight: '1.2',
};

const greeting = {
  fontSize: '16px',
  fontWeight: 600,
  color: '#1a1a1a',
  margin: '0 0 16px 0',
  lineHeight: '1.4',
};

const bodyText = {
  fontSize: '15px',
  color: '#4a4a4a',
  margin: '8px 0',
  lineHeight: '1.5',
};

const quote = {
  fontSize: '16px',
  fontStyle: 'italic',
  color: '#4B2E83',
  fontWeight: 600,
  margin: '16px 0 0 0',
  lineHeight: '1.6',
};

const whatSection = {
  padding: '24px 24px 32px 24px',
  backgroundColor: '#ffffff',
  textAlign: 'center' as const,
};

const sectionLabel = {
  fontSize: '14px',
  fontWeight: 600,
  color: '#4B2E83',
  margin: '0 0 12px 0',
  textTransform: 'uppercase',
  letterSpacing: '0.5px',
  lineHeight: '1.4',
};

const checklistTable = {
  margin: '0 auto',
};

const checklistItemStyle = {
  padding: '6px 0',
  textAlign: 'left' as const,
};

const checkItem = {
  fontSize: '14px',
  color: '#1a1a1a',
  margin: '0',
  lineHeight: '1.5',
};

const ctaSection = {
  padding: '24px 24px',
  textAlign: 'center' as const,
};

const ctaButton = {
  backgroundColor: '#4B2E83',
  color: '#ffffff',
  fontSize: '15px',
  fontWeight: 600,
  borderRadius: '6px',
  textDecoration: 'none',
  display: 'inline-block',
  mso: {
    padding: '12px 32px',
  },
};

const closingSection = {
  padding: '24px 24px',
  textAlign: 'center' as const,
};

const closingText = {
  fontSize: '14px',
  color: '#4a4a4a',
  margin: '8px 0',
  lineHeight: '1.5',
};

const heartIcon = {
  fontSize: '24px',
  lineHeight: '24px',
  margin: '12px 0 0 0',
  display: 'block',
  textAlign: 'center' as const,
};

const teamName = {
  fontSize: '14px',
  color: '#4B2E83',
  fontWeight: 600,
  margin: '8px 0 0 0',
  lineHeight: '1.4',
};

// Styles
const main = {
  backgroundColor: '#ffffff',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif',
};

const container = {
  maxWidth: '640px',
  margin: '0 auto',
  width: '100%',
};

const heroSection = {
  padding: '60px 20px',
  textAlign: 'center' as const,
  backgroundColor: '#ffffff',
};

const heroIcon = {
  fontSize: '48px',
  lineHeight: '48px',
  margin: '0 0 24px 0',
  textAlign: 'center' as const,
};

const heading1 = {
  fontSize: '36px',
  fontWeight: 700,
  color: '#1a1a1a',
  margin: '0 0 16px 0',
  lineHeight: '1.2',
};

const greeting = {
  fontSize: '18px',
  fontWeight: 600,
  color: '#1a1a1a',
  margin: '0 0 24px 0',
  lineHeight: '1.4',
};

const heroText = {
  fontSize: '16px',
  color: '#4a4a4a',
  margin: '12px 0',
  lineHeight: '1.6',
};

const quote = {
  fontSize: '18px',
  fontStyle: 'italic',
  color: '#7C3AED',
  fontWeight: 600,
  margin: '32px 0',
  lineHeight: '1.8',
};

const featuresSection = {
  padding: '40px 20px',
  backgroundColor: '#ffffff',
};

const sectionHeading = {
  fontSize: '24px',
  fontWeight: 700,
  color: '#1a1a1a',
  margin: '0 0 32px 0',
  textAlign: 'center' as const,
  lineHeight: '1.3',
};

const cardsRow = {
  width: '100%',
  margin: '0 0 20px 0',
};

const buildingSection = {
  padding: '40px 20px',
  backgroundColor: '#f9f5ff',
};

const checklistContainer = {
  padding: '20px',
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  border: '1px solid #e5e5e5',
};

const checklistItem = {
  margin: '12px 0',
};

const checklistText = {
  fontSize: '15px',
  color: '#1a1a1a',
  fontWeight: 500,
  margin: '0',
  lineHeight: '1.6',
};

const ctaSection = {
  padding: '40px 20px',
  textAlign: 'center' as const,
  backgroundColor: '#ffffff',
};

const ctaButton = {
  backgroundColor: '#7C3AED',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 600,
  borderRadius: '6px',
  textDecoration: 'none',
  display: 'inline-block',
  mso: {
    padding: '16px 40px',
  },
};

const closingSection = {
  padding: '40px 20px',
  textAlign: 'center' as const,
  backgroundColor: '#ffffff',
};

const closingIcon = {
  fontSize: '32px',
  lineHeight: '32px',
  margin: '0 0 16px 0',
  textAlign: 'center' as const,
};

const closingMessage = {
  fontSize: '16px',
  color: '#4a4a4a',
  margin: '12px 0',
  lineHeight: '1.6',
};

const closingSignature = {
  fontSize: '15px',
  color: '#7C3AED',
  fontWeight: 600,
  margin: '24px 0 4px 0',
  lineHeight: '1.4',
};

const closingSignatureTeam = {
  fontSize: '15px',
  color: '#7C3AED',
  fontWeight: 700,
  margin: '0',
  lineHeight: '1.4',
};