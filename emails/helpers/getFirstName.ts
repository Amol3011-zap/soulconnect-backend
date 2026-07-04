export function getFirstName(name?: string): string {
  if (!name) {
    return 'there';
  }

  const trimmed = name.trim();

  if (!trimmed) {
    return 'there';
  }

  const words = trimmed.split(/\s+/);
  const firstName = words[0];

  return firstName || 'there';
}