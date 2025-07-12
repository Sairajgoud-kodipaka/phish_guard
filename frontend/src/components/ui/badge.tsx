import * as React from 'react'
import { cn } from '@/lib/utils'

const badgeVariants = {
  variant: {
    default: 'bg-primary-100 text-primary-800',
    secondary: 'bg-gray-100 text-gray-800',
    destructive: 'bg-danger-100 text-danger-800',
    success: 'bg-success-100 text-success-800',
    warning: 'bg-warning-100 text-warning-800',
    outline: 'border border-gray-300 text-gray-700',
  },
}

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: keyof typeof badgeVariants.variant
}

function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  const baseClasses = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2'
  const variantClasses = badgeVariants.variant[variant]
  
  return (
    <div className={cn(baseClasses, variantClasses, className)} {...props} />
  )
}

export { Badge, badgeVariants } 