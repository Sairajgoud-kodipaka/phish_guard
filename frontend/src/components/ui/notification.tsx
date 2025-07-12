'use client'

import { Fragment, useState, useEffect } from 'react'
import { Transition } from '@headlessui/react'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { cn } from '@/lib/utils'

export interface NotificationProps {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
  onClose?: (id: string) => void
}

const notificationStyles = {
  success: {
    bg: 'bg-success-50',
    border: 'border-success-200',
    icon: CheckCircleIcon,
    iconColor: 'text-success-400',
    titleColor: 'text-success-800',
    messageColor: 'text-success-700',
  },
  error: {
    bg: 'bg-danger-50',
    border: 'border-danger-200',
    icon: XCircleIcon,
    iconColor: 'text-danger-400',
    titleColor: 'text-danger-800',
    messageColor: 'text-danger-700',
  },
  warning: {
    bg: 'bg-warning-50',
    border: 'border-warning-200',
    icon: ExclamationTriangleIcon,
    iconColor: 'text-warning-400',
    titleColor: 'text-warning-800',
    messageColor: 'text-warning-700',
  },
  info: {
    bg: 'bg-primary-50',
    border: 'border-primary-200',
    icon: InformationCircleIcon,
    iconColor: 'text-primary-400',
    titleColor: 'text-primary-800',
    messageColor: 'text-primary-700',
  },
}

export function Notification({
  id,
  type,
  title,
  message,
  duration = 5000,
  onClose,
}: NotificationProps) {
  const [show, setShow] = useState(true)
  const styles = notificationStyles[type]
  const Icon = styles.icon

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setShow(false)
        setTimeout(() => onClose?.(id), 300) // Wait for animation
      }, duration)

      return () => clearTimeout(timer)
    }
  }, [duration, id, onClose])

  const handleClose = () => {
    setShow(false)
    setTimeout(() => onClose?.(id), 300)
  }

  return (
    <Transition
      show={show}
      as={Fragment}
      enter="transform ease-out duration-300 transition"
      enterFrom="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enterTo="translate-y-0 opacity-100 sm:translate-x-0"
      leave="transition ease-in duration-100"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      <div
        className={cn(
          'max-w-sm w-full shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden',
          styles.bg,
          styles.border
        )}
      >
        <div className="p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <Icon className={cn('h-6 w-6', styles.iconColor)} aria-hidden="true" />
            </div>
            <div className="ml-3 w-0 flex-1 pt-0.5">
              <p className={cn('text-sm font-medium', styles.titleColor)}>
                {title}
              </p>
              <p className={cn('mt-1 text-sm', styles.messageColor)}>
                {message}
              </p>
            </div>
            <div className="ml-4 flex-shrink-0 flex">
              <button
                className={cn(
                  'rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                )}
                onClick={handleClose}
              >
                <span className="sr-only">Close</span>
                <XMarkIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  )
}

// Notification Container Component
export function NotificationContainer({
  notifications,
  onClose,
}: {
  notifications: NotificationProps[]
  onClose: (id: string) => void
}) {
  return (
    <div
      aria-live="assertive"
      className="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start z-50"
    >
      <div className="w-full flex flex-col items-center space-y-4 sm:items-end">
        {notifications.map((notification) => (
          <Notification
            key={notification.id}
            {...notification}
            onClose={onClose}
          />
        ))}
      </div>
    </div>
  )
} 