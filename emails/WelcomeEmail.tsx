import React from 'react';
import {
  Body,
  Button,
  Container,
  Head,
  Hr,
  Html,
  Img,
  Link,
  Preview,
  Row,
  Section,
  Text,
} from 'react-email';
import { EmailHeader } from './components/EmailHeader';
import { FeatureCard } from './components/FeatureCard';
import { MomentOfCalm } from './components/MomentOfCalm';
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
          .dark {
            color-scheme: dark;
          }
          @media (prefers-color-scheme: dark) {
            .dark-mode-text { color: #e5e5e5; }
            .dark-mode-secondary { color: #a0a0a0; }
            .dark-mode-bg { background-color: #1a1a1a; }
            .dark-mode-card { background-color: #262626; }
            .dark-mode-border { border-color: #404040; }
          }
        `}</style>
      </Head>
      <Preview>{`Thank you for joining our community. We're glad you're here.`}</Preview>
      <Body style={main}>
        <Container style={container}>
          {/* Header */}
          <EmailHeader />

          {/* Hero Section */}
          <Section style={heroSection}>
            <Text style={heroIcon}>💜</Text>
            <Text style={heading1}>Welcome to SoulConnect!</Text>
            <Text style={greeting}>Hi {firstName}! 👋</Text>
            <Text style={heroText}>
              Thank you for joining our waitlist.
            </Text>
            <Text style={heroText}>
              You're now part of a community built on one simple belief.
            </Text>
            <Text style={quote}>
              "You don't have to go through life's challenges alone."
            </Text>
          </Section>

          {/* Features Section */}
          <Section style={featuresSection}>
            <Text style={sectionHeading}>Here's what you'll discover</Text>

            <Row style={cardsRow}>
              <FeatureCard
                icon="🤝"
                title="Connect"
                description="Find people who truly understand what you're going through."
              />
              <FeatureCard
                icon="🌱"
                title="Heal"
                description="Daily wellness tools and guided healing journeys."
              />
            </Row>

            <Row style={cardsRow}>
              <FeatureCard
                icon="🧠"
                title="Professional Support"
                description="Connect with trusted therapists and wellness professionals."
              />
              <FeatureCard
                icon="💜"
                title="Grow"
                description="Build healthier habits and become your best self."
              />
            </Row>
          </Section>

          {/* Building Section */}
          <Section style={buildingSection}>
            <Text style={sectionHeading}>We're building SoulConnect for you</Text>

            <div style={checklistContainer}>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Anonymous peer matching</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Guided healing journeys</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Verified professionals</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Safe supportive community</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Mood tracking</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Daily check-ins</Text>
              </div>
              <div style={checklistItem}>
                <Text style={checklistText}>✔ Breathing exercises</Text>
              </div>
            </div>
          </Section>

          {/* CTA Section */}
          <Section style={ctaSection}>
            <Button
              pX={40}
              pY={16}
              style={ctaButton}
              href="https://soulconnect.health"
            >
              Visit SoulConnect
            </Button>
          </Section>

          {/* Moment of Calm */}
          <MomentOfCalm />

          {/* Closing */}
          <Section style={closingSection}>
            <Text style={closingIcon}>💜</Text>
            <Text style={closingMessage}>
              One genuine conversation can change someone's day.
            </Text>
            <Text style={closingMessage}>
              Thank you for believing in ours.
            </Text>
            <Text style={closingSignature}>With care,</Text>
            <Text style={closingSignatureTeam}>The SoulConnect Team</Text>
          </Section>

          {/* Footer */}
          <EmailFooter userEmail={userEmail} />
        </Container>

        {/* VML Fallback for Outlook Button */}
        <div dangerouslySetInnerHTML={{
          __html: `<!--[if mso]>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
              <tr>
                <td style="padding: 40px 0;">
                  <table role="presentation" align="center" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                      <td style="border-radius: 6px; background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%); padding: 16px 40px;">
                        <a href="https://soulconnect.health" style="color: white; text-decoration: none; font-weight: 600; display: block; font-size: 16px;">Visit SoulConnect</a>
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