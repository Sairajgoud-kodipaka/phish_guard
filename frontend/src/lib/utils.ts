import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date): string {
  if (!date || isNaN(date.getTime())) {
    return 'Invalid date'
  }
  
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date)
}

export function formatThreatLevel(level: number): {
  label: string
  color: string
  bgColor: string
} {
  if (level >= 80) {
    return {
      label: 'Critical',
      color: 'text-danger-700',
      bgColor: 'bg-danger-100'
    }
  } else if (level >= 60) {
    return {
      label: 'High',
      color: 'text-warning-700',
      bgColor: 'bg-warning-100'
    }
  } else if (level >= 40) {
    return {
      label: 'Medium',
      color: 'text-warning-600',
      bgColor: 'bg-warning-50'
    }
  } else if (level >= 20) {
    return {
      label: 'Low',
      color: 'text-success-600',
      bgColor: 'bg-success-50'
    }
  } else {
    return {
      label: 'Safe',
      color: 'text-success-700',
      bgColor: 'bg-success-100'
    }
  }
} 