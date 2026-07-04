import React from 'react';
import { Section, Text, Hr } from 'react-email';

export const EmailHeader = () => {
  return (
    <Section style={headerContainer}>
      <table role="presentation" width="100%" cellPadding="0" cellSpacing="0" style={headerTable}>
        <tbody>
          <tr>
            <td style={headerContent} align="center">
              <Text style={logoIcon}>💜</Text>
              <Text style={logoText}>
                Soul<span style={logoAccent}>Connect</span>
              </Text>
            </td>
          </tr>
        </tbody>
      </table>
      <Hr style={headerDivider} />
    </Section>
  );
};

const headerContainer = {
  backgroundColor: '#4B2E83',
  padding: '20px 20px 16px',
  width: '100%',
};

const headerTable = {
  width: '100%',
  textAlign: 'center' as const,
};

const headerContent = {
  textAlign: 'center' as const,
};

const logoIcon = {
  fontSize: '32px',
  lineHeight: '32px',
  margin: '0 0 6px 0',
  display: 'block',
};

const logoText = {
  fontSize: '26px',
  fontWeight: 800,
  color: '#ffffff',
  margin: '0',
  lineHeight: '1',
  letterSpacing: '-0.3px',
};

const logoAccent = {
  color: '#D4AF37',
};

const headerDivider = {
  borderColor: '#D4AF37',
  borderWidth: '2px',
  borderStyle: 'solid',
  margin: '0',
};