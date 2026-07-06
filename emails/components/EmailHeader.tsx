import React from 'react';
import { Section, Img } from 'react-email';

export const EmailHeader = () => {
  return (
    <Section style={headerContainer}>
      <table role="presentation" width="100%" cellPadding="0" cellSpacing="0" border="0" style={{ borderCollapse: 'collapse' }}>
        <tbody>
          <tr>
            <td style={headerImageCell} width="100%">
              <Img
                src="https://res.cloudinary.com/lh7xcjvh/image/upload/f_auto,q_auto/ChatGPT_Image_Jul_6_2026_03_22_00_AM_qkzxxu.png"
                alt="SoulConnect"
                width="600"
                height="auto"
                style={logoImage}
              />
            </td>
          </tr>
          <tr>
            <td style={headerBorder} height="4" width="100%"></td>
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
  display: 'block',
  border: 'none',
  outline: 'none',
  textDecoration: 'none',
};

const logoImage = {
  width: '100%',
  maxWidth: '600px',
  height: 'auto',
  display: 'block',
  margin: '0',
  padding: '0',
  lineHeight: '0',
  fontSize: '0',
  border: 'none',
  outline: 'none',
  textDecoration: 'none',
};

const headerBorder = {
  backgroundColor: '#D4AF37',
  height: '4px',
  padding: '0',
  margin: '0',
  display: 'block',
  border: 'none',
};