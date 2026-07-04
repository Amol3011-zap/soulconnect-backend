import React from 'react';
import { Section, Img } from 'react-email';

export const EmailHeader = () => {
  return (
    <Section style={headerContainer}>
      <table role="presentation" width="100%" cellPadding="0" cellSpacing="0" border="0">
        <tbody>
          <tr>
            <td style={headerImageCell}>
              <Img
                src="https://raw.githubusercontent.com/Amol3011-zap/soulconnect-backend/main/emails/email.png"
                alt="SoulConnect"
                style={logoImage}
              />
            </td>
          </tr>
          <tr>
            <td style={headerBorder} height="4"></td>
          </tr>
        </tbody>
      </table>
    </Section>
  );
};

const headerContainer = {
  padding: '0',
  width: '100%',
  backgroundColor: '#ffffff',
  margin: '0',
};

const headerImageCell = {
  padding: '0',
  margin: '0',
  lineHeight: '0',
  fontSize: '0',
  textAlign: 'center' as const,
};

const logoImage = {
  width: '100%',
  height: 'auto',
  display: 'block',
  margin: '0',
  padding: '0',
  lineHeight: '0',
  fontSize: '0',
  border: 'none',
};

const headerBorder = {
  backgroundColor: '#D4AF37',
  height: '4px',
  padding: '0',
  margin: '0',
  display: 'block',
};