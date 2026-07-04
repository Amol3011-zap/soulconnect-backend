import React from 'react';
import { Section, Text, Hr } from 'react-email';

export const EmailHeader = () => {
  return (
    <Section style={headerContainer}>
      <table role="presentation" width="100%" cellPadding="0" cellSpacing="0" style={headerTable}>
        <tbody>
          <tr>
            <td style={headerContent} align="center">
              <Text style={logoContainer}>
                <span style={logoIcon}>💜</span>
              </Text>
              <Text style={logoText}>
                Soul<span style={logoAccent}>Connect</span>
              </Text>
              <Text style={tagline}>HEAL • CONNECT • GROW • TOGETHER.</Text>
            </td>
          </tr>
        </tbody>
      </table>
      <Hr style={headerDivider} />
    </Section>
  );
};

const headerContainer = {
  backgroundColor: '#3e1c52',
  padding: '40px 20px 24px',
  width: '100%',
};

const headerTable = {
  width: '100%',
  textAlign: 'center' as const,
};

const headerContent = {
  textAlign: 'center' as const,
  paddingBottom: '16px',
};

const logoContainer = {
  fontSize: '48px',
  lineHeight: '48px',
  margin: '0 0 12px 0',
  display: 'block',
};

const logoIcon = {
  fontSize: '48px',
};

const logoText = {
  fontSize: '32px',
  fontWeight: 800,
  color: '#ffffff',
  margin: '0 0 8px 0',
  lineHeight: '1',
  letterSpacing: '-0.5px',
};

const logoAccent = {
  color: '#EAB308',
};

const tagline = {
  fontSize: '11px',
  fontWeight: 700,
  color: '#d4af37',
  margin: '0',
  letterSpacing: '1.5px',
  textTransform: 'uppercase',
  lineHeight: '1.2',
};

const headerDivider = {
  borderColor: '#EAB308',
  borderWidth: '2px',
  borderStyle: 'solid',
  margin: '0',
};