import React from 'react';
import { Section, Text, Link, Hr } from 'react-email';

interface EmailFooterProps {
  userEmail?: string;
}

export const EmailFooter = ({ userEmail }: EmailFooterProps) => {
  return (
    <>
      <Hr style={footerDivider} />
      <Section style={footerContainer}>
        <Text style={footerEmail}>
          <Link href="mailto:community@soulconnect.health" style={footerLink}>
            community@soulconnect.health
          </Link>
        </Text>
        <Text style={footerWebsite}>
          <Link href="https://soulconnect.health" style={footerLink}>
            soulconnect.health
          </Link>
        </Text>
        <Text style={footerLinks}>
          <Link href="https://soulconnect.health/privacy" style={footerLink}>
            Privacy Policy
          </Link>
          {' '} · {' '}
          <Link href="https://soulconnect.health/terms" style={footerLink}>
            Terms of Service
          </Link>
        </Text>
        <Text style={footerDisclaimer}>
          You're receiving this email because you joined the SoulConnect waitlist.
        </Text>
      </Section>
    </>
  );
};

const footerDivider = {
  borderColor: '#e5e5e5',
  borderWidth: '1px',
  borderStyle: 'solid',
  margin: '0',
};

const footerContainer = {
  padding: '16px 20px',
  backgroundColor: '#ffffff',
  textAlign: 'center' as const,
};

const footerEmail = {
  fontSize: '12px',
  color: '#4a4a4a',
  margin: '0 0 4px 0',
  lineHeight: '1.3',
};

const footerWebsite = {
  fontSize: '12px',
  color: '#4a4a4a',
  margin: '0 0 8px 0',
  lineHeight: '1.3',
};

const footerLinks = {
  fontSize: '11px',
  color: '#4a4a4a',
  margin: '0 0 8px 0',
  lineHeight: '1.3',
};

const footerLink = {
  color: '#4B2E83',
  textDecoration: 'none',
  fontWeight: 500,
};

const footerDisclaimer = {
  fontSize: '11px',
  color: '#999999',
  margin: '0',
  lineHeight: '1.4',
};