import React from 'react';
import { Text } from 'react-email';

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
}

export const FeatureCard = ({ icon, title, description }: FeatureCardProps) => {
  return (
    <table
      role="presentation"
      cellPadding="0"
      cellSpacing="0"
      width="50%"
      style={cardCell}
      align="left"
    >
      <tbody>
        <tr>
          <td style={cardPadding}>
            <div style={card}>
              <Text style={cardIcon}>{icon}</Text>
              <Text style={cardTitle}>{title}</Text>
              <Text style={cardDescription}>{description}</Text>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  );
};

const cardCell = {
  display: 'inline-block',
  width: '50%',
  paddingRight: '8px',
  paddingBottom: '16px',
  verticalAlign: 'top',
};

const cardPadding = {
  paddingRight: '8px',
};

const card = {
  backgroundColor: '#ffffff',
  border: '1px solid #e5e5e5',
  borderRadius: '12px',
  padding: '24px 16px',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
  textAlign: 'center' as const,
};

const cardIcon = {
  fontSize: '32px',
  lineHeight: '32px',
  margin: '0 0 12px 0',
  display: 'block',
};

const cardTitle = {
  fontSize: '16px',
  fontWeight: 600,
  color: '#1a1a1a',
  margin: '0 0 8px 0',
  lineHeight: '1.3',
};

const cardDescription = {
  fontSize: '14px',
  color: '#4a4a4a',
  margin: '0',
  lineHeight: '1.5',
};