#!/usr/bin/env node

/**
 * Render WelcomeEmail to HTML string
 * Usage: node render-email.js [email] [name]
 * Example: node render-email.js user@example.com "Amol Londhe"
 */

import { render } from '@react-email/render';
import React from 'react';
import { WelcomeEmail } from './WelcomeEmail.jsx';

async function renderEmail() {
  try {
    const args = process.argv.slice(2);
    const userEmail = args[0] || 'user@example.com';
    const userName = args[1] || undefined;

    const html = await render(
      React.createElement(WelcomeEmail, {
        userEmail,
        userName,
      })
    );

    // Output HTML to stdout
    process.stdout.write(html);
    process.exit(0);
  } catch (error) {
    console.error('Error rendering email:', error);
    process.exit(1);
  }
}

renderEmail();