import React from 'react';
import { Section, Text } from 'react-email';

export const MomentOfCalm = () => {
  return (
    <Section style={container}>
      <table
        role="presentation"
        cellPadding="0"
        cellSpacing="0"
        width="100%"
        style={calmCard}
      >
        <tbody>
          <tr>
            <td style={calmPadding}>
              <Text style={calmHeading}>🌿 Today's Moment of Calm</Text>
              <Text style={calmText}>Take one slow breath.</Text>
              <Text style={calmText}>Inhale for 4 seconds.</Text>
              <Text style={calmText}>Hold for 4 seconds.</Text>
              <Text style={calmText}>Exhale for 6 seconds.</Text>
              <Text style={calmText}>Repeat three times.</Text>
              <Text style={calmReminder}>
                Remember... You don't have to go through it alone.
              </Text>
            </td>
          </tr>
        </tbody>
      </table>
    </Section>
  );
};

const container = {
  padding: '40px 20px',
  backgroundColor: '#ffffff',
};

const calmCard = {
  border: '1px solid #e5e5e5',
  borderRadius: '12px',
  backgroundColor: '#fafaf9',
};

const calmPadding = {
  padding: '32px 24px',
  textAlign: 'center' as const,
};

const calmHeading = {
  fontSize: '18px',
  fontWeight: 600,
  color: '#1a1a1a',
  margin: '0 0 20px 0',
  lineHeight: '1.4',
};

const calmText = {
  fontSize: '15px',
  color: '#4a4a4a',
  margin: '8px 0',
  lineHeight: '1.6',
};

const calmReminder = {
  fontSize: '15px',
  color: '#7C3AED',
  fontWeight: 600,
  margin: '20px 0 0 0',
  lineHeight: '1.6',
};