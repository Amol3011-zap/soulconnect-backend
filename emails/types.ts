/**
 * Type definitions for SoulConnect Email System
 */

/**
 * Welcome Email Props
 * @interface WelcomeEmailProps
 */
export interface WelcomeEmailProps {
  /**
   * User's email address
   */
  userEmail?: string;

  /**
   * User's full name for personalization
   * @example "Amol Londhe"
   */
  userName?: string;
}

/**
 * Feature Card Props
 * @interface FeatureCardProps
 */
export interface FeatureCardProps {
  /**
   * Icon emoji or text
   * @example "🤝"
   */
  icon: string;

  /**
   * Feature title
   * @example "Connect"
   */
  title: string;

  /**
   * Feature description
   * @example "Find people who truly understand what you're going through."
   */
  description: string;
}

/**
 * Divider Props
 * @interface DividerProps
 */
export interface DividerProps {
  /**
   * Divider color
   * @default "#e5e5e5"
   */
  color?: string;

  /**
   * Divider margin
   * @default "24px 0"
   */
  margin?: string;
}

/**
 * Email Footer Props
 * @interface EmailFooterProps
 */
export interface EmailFooterProps {
  /**
   * User's email address for display in footer
   */
  userEmail?: string;
}

/**
 * Email Render Result
 * @interface EmailRenderResult
 */
export interface EmailRenderResult {
  /**
   * Rendered HTML string
   */
  html: string;

  /**
   * Email subject line
   */
  subject: string;

  /**
   * Preheader text for email clients
   */
  preheader: string;

  /**
   * Plain text version
   */
  text?: string;
}

/**
 * Resend Email Response
 * @interface ResendEmailResponse
 */
export interface ResendEmailResponse {
  /**
   * Email ID
   */
  id: string;

  /**
   * Recipient email
   */
  to: string;

  /**
   * Sender email
   */
  from: string;

  /**
   * Email subject
   */
  subject: string;

  /**
   * Created timestamp
   */
  created_at: string;

  /**
   * Send status
   */
  status?: 'success' | 'failed' | 'queued';

  /**
   * Error message if failed
   */
  error?: string;
}

/**
 * Email Service Config
 * @interface EmailServiceConfig
 */
export interface EmailServiceConfig {
  /**
   * Resend API Key
   */
  apiKey: string;

  /**
   * From email address
   */
  from: string;

  /**
   * Reply-to email address
   */
  replyTo?: string;

  /**
   * CC addresses
   */
  cc?: string[];

  /**
   * BCC addresses
   */
  bcc?: string[];

  /**
   * Track opens
   */
  trackOpens?: boolean;

  /**
   * Track clicks
   */
  trackClicks?: boolean;
}

/**
 * Send Email Options
 * @interface SendEmailOptions
 */
export interface SendEmailOptions {
  /**
   * Recipient email
   */
  to: string;

  /**
   * Sender email (uses default if not provided)
   */
  from?: string;

  /**
   * Email subject
   */
  subject: string;

  /**
   * HTML content
   */
  html: string;

  /**
   * Plain text content
   */
  text?: string;

  /**
   * Reply-to email
   */
  replyTo?: string;

  /**
   * CC recipients
   */
  cc?: string[];

  /**
   * BCC recipients
   */
  bcc?: string[];

  /**
   * Track opens
   */
  trackOpens?: boolean;

  /**
   * Track clicks
   */
  trackClicks?: boolean;

  /**
   * Custom headers
   */
  headers?: Record<string, string>;

  /**
   * Schedule send time (ISO 8601)
   */
  scheduledAt?: string;

  /**
   * Template variables
   */
  templateVariables?: Record<string, string>;
}

/**
 * Email Template Name
 * @type EmailTemplateName
 */
export type EmailTemplateName = 'welcome' | 'admin-notification' | 'password-reset' | 'verification';

/**
 * Email Status
 * @type EmailStatus
 */
export type EmailStatus = 'sent' | 'failed' | 'bounced' | 'complained' | 'delivered' | 'opened' | 'clicked';

/**
 * First Name Helper Result
 * @type GetFirstNameResult
 */
export type GetFirstNameResult = string;

/**
 * Decode Email Response
 * @interface DecodeEmailResponse
 */
export interface DecodeEmailResponse {
  /**
   * Email bounced
   */
  bounced: boolean;

  /**
   * Bounce type
   */
  bounceType?: 'permanent' | 'temporary' | 'undetermined';

  /**
   * Email suppressed
   */
  suppressed: boolean;

  /**
   * Suppression type
   */
  suppressionType?: 'complaint' | 'bounce' | 'manual';

  /**
   * Last event
   */
  lastEvent?: EmailStatus;

  /**
   * Last event timestamp
   */
  lastEventTimestamp?: string;
}