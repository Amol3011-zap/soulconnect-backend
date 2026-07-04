import React from 'react';
import { Hr } from 'react-email';

interface DividerProps {
  color?: string;
  margin?: string;
}

export const Divider = ({ color = '#e5e5e5', margin = '24px 0' }: DividerProps) => {
  return (
    <Hr
      style={{
        borderColor: color,
        borderWidth: '1px',
        borderStyle: 'solid',
        margin,
      }}
    />
  );
};