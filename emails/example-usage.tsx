// Example: How to use WelcomeEmail with Resend
// This is a Next.js API route example

import { NextRequest, NextResponse } from 'next/server';
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/WelcomeEmail';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  try {
    const { userEmail, userName } = await request.json();

    const data = await resend.emails.send({
      from: 'SoulConnect <community@soulconnect.health>',
      to: userEmail,
      subject: userName
        ? `💜 Welcome to SoulConnect, ${userName.split(' ')[0]}`
        : '💜 Welcome to SoulConnect',
      react: <WelcomeEmail userEmail={userEmail} userName={userName} />,
    });

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error }, { status: 500 });
  }
}

// =====================================================
// Alternative: React Email CLI for testing locally
// =====================================================
// npx react-email preview emails/WelcomeEmail.tsx

// =====================================================
// To render as HTML string (for use in other backends):
// =====================================================
import { render } from '@react-email/render';

export async function renderWelcomeEmail(userEmail: string, userName?: string) {
  return render(<WelcomeEmail userEmail={userEmail} userName={userName} />, {
    pretty: true,
  });
}