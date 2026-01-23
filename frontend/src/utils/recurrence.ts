/**
 * Utility functions for handling RFC 5545 recurrence rules
 */

export interface RecurrenceRule {
  freq: 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY';
  interval?: number;
  count?: number;
  until?: string; // ISO date string
  byDay?: string[]; // e.g., ['MO', 'TU', 'WE']
  byMonth?: number[]; // e.g., [1, 2, 3] for months
  byMonthDay?: number[]; // e.g., [1, 15] for days of month
}

/**
 * Parse an RFC 5545 recurrence rule string into a structured object
 */
export function parseRRule(rrule: string): RecurrenceRule {
  const parts = rrule.split(';');
  const rule: Partial<RecurrenceRule> = {};

  for (const part of parts) {
    const [key, value] = part.split('=');

    switch (key) {
      case 'FREQ':
        rule.freq = value as RecurrenceRule['freq'];
        break;
      case 'INTERVAL':
        rule.interval = parseInt(value, 10);
        break;
      case 'COUNT':
        rule.count = parseInt(value, 10);
        break;
      case 'UNTIL':
        rule.until = value;
        break;
      case 'BYDAY':
        rule.byDay = value.split(',');
        break;
      case 'BYMONTH':
        rule.byMonth = value.split(',').map(v => parseInt(v, 10));
        break;
      case 'BYMONTHDAY':
        rule.byMonthDay = value.split(',').map(v => parseInt(v, 10));
        break;
    }
  }

  return rule as RecurrenceRule;
}

/**
 * Format a structured recurrence rule object into an RFC 5545 string
 */
export function formatRRule(rule: RecurrenceRule): string {
  const parts: string[] = [`FREQ=${rule.freq}`];

  if (rule.interval !== undefined && rule.interval !== 1) {
    parts.push(`INTERVAL=${rule.interval}`);
  }

  if (rule.count !== undefined) {
    parts.push(`COUNT=${rule.count}`);
  }

  if (rule.until !== undefined) {
    parts.push(`UNTIL=${rule.until}`);
  }

  if (rule.byDay !== undefined && rule.byDay.length > 0) {
    parts.push(`BYDAY=${rule.byDay.join(',')}`);
  }

  if (rule.byMonth !== undefined && rule.byMonth.length > 0) {
    parts.push(`BYMONTH=${rule.byMonth.join(',')}`);
  }

  if (rule.byMonthDay !== undefined && rule.byMonthDay.length > 0) {
    parts.push(`BYMONTHDAY=${rule.byMonthDay.join(',')}`);
  }

  return parts.join(';');
}

/**
 * Generate a simple recurrence rule based on frequency and interval
 */
export function generateSimpleRRule(freq: RecurrenceRule['freq'], interval: number = 1): string {
  return formatRRule({ freq, interval });
}

/**
 * Get human-readable description of a recurrence rule
 */
export function getRecurrenceDescription(rrule: string): string {
  if (!rrule) return 'No recurrence';

  try {
    const rule = parseRRule(rrule);
    let description = '';

    switch (rule.freq) {
      case 'DAILY':
        if (rule.interval === 1) {
          description = 'Daily';
        } else {
          description = `Every ${rule.interval} days`;
        }
        break;
      case 'WEEKLY':
        if (rule.interval === 1) {
          description = 'Weekly';
        } else if (rule.interval === 2) {
          description = 'Bi-weekly';
        } else {
          description = `Every ${rule.interval} weeks`;
        }
        break;
      case 'MONTHLY':
        if (rule.interval === 1) {
          description = 'Monthly';
        } else {
          description = `Every ${rule.interval} months`;
        }
        break;
      case 'YEARLY':
        if (rule.interval === 1) {
          description = 'Yearly';
        } else {
          description = `Every ${rule.interval} years`;
        }
        break;
      default:
        description = 'Custom recurrence';
    }

    return description;
  } catch (error) {
    return 'Invalid recurrence rule';
  }
}