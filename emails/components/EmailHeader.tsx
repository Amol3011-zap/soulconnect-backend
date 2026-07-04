import React from 'react';
import { Section, Text, Hr, Img } from 'react-email';

export const EmailHeader = () => {
  return (
    <Section style={headerContainer}>
      <table role="presentation" width="100%" cellPadding="0" cellSpacing="0" style={headerTable}>
        <tbody>
          <tr>
            <td style={headerContent} align="center">
              <Img
                src="https://raw.githubusercontent.com/Amol3011-zap/soulconnect-backend/main/emails/email.png"
                alt="SoulConnect"
                style={logoImage}
              />
            </td>
          </tr>
        </tbody>
      </table>
      <Hr style={headerDivider} />
    </Section>
  );
};

const headerContainer = {
  backgroundColor: '#1a1a3e',
  padding: '24px 20px 16px',
  width: '100%',
};

const headerTable = {
  width: '100%',
  textAlign: 'center' as const,
};

const headerContent = {
  textAlign: 'center' as const,
};

const logoImage = {
  maxWidth: '100%',
  height: 'auto',
  width: '280px',
  display: 'block',
  margin: '0 auto',
};

const headerDivider = {
  borderColor: '#D4AF37',
  borderWidth: '3px',
  borderStyle: 'solid',
  margin: '0',
};