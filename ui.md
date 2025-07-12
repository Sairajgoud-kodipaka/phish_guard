# PhishGuard UI/UX Design System

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Visual Identity](#visual-identity)
3. [Design System](#design-system)
4. [Component Library](#component-library)
5. [Layout & Grid System](#layout--grid-system)
6. [User Experience](#user-experience)
7. [Information Architecture](#information-architecture)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)
10. [Interaction Design](#interaction-design)
11. [Data Visualization](#data-visualization)
12. [Design Tokens](#design-tokens)

## Design Philosophy

### Core Principles

#### 1. **Security First**
- Visual hierarchy emphasizes critical security information
- Clear distinction between safe, warning, and danger states
- Immediate recognition of threat levels through color and iconography

#### 2. **Clarity & Simplicity**
- Clean, uncluttered interfaces that reduce cognitive load
- Progressive disclosure of complex information
- Intuitive navigation that matches user mental models

#### 3. **Trust & Reliability**
- Professional appearance that instills confidence
- Consistent behavior across all interactions
- Transparent communication of system status and actions

#### 4. **Efficiency**
- Streamlined workflows for common tasks
- Keyboard shortcuts and power-user features
- Quick access to critical functions

## Visual Identity

### Brand Colors

```css
/* Primary Palette */
:root {
  /* Primary Brand Colors */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-500: #3b82f6;  /* Main brand blue */
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  --primary-900: #1e3a8a;

  /* Security Status Colors */
  --success-50: #f0fdf4;
  --success-500: #22c55e;   /* Safe/Clean */
  --success-600: #16a34a;
  
  --warning-50: #fffbeb;
  --warning-500: #f59e0b;   /* Medium Risk */
  --warning-600: #d97706;
  
  --danger-50: #fef2f2;
  --danger-500: #ef4444;    /* High Risk/Blocked */
  --danger-600: #dc2626;
  
  --critical-50: #fdf2f8;
  --critical-500: #ec4899;  /* Critical Threats */
  --critical-600: #db2777;

  /* Neutral Palette */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
}
```

### Typography

```css
/* Font System */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
}
```

### Iconography

```tsx
// Icon system using Lucide React
import {
  Shield,           // Protection/Security
  AlertTriangle,    // Warning/Medium Risk
  XCircle,         // Danger/High Risk
  CheckCircle,     // Safe/Success
  Eye,             // Monitoring
  Mail,            // Email
  Filter,          // Filtering
  Settings,        // Configuration
  User,            // User Management
  BarChart3,       // Analytics
  Clock,           // Time/History
  Search,          // Search
  ChevronDown,     // Dropdown
  ChevronRight,    // Navigation
  Plus,            // Add
  X,               // Close
  Download,        // Export
  Upload,          // Import
  Refresh,         // Refresh
} from 'lucide-react'

// Security Status Icons
const securityIcons = {
  safe: CheckCircle,
  warning: AlertTriangle,
  danger: XCircle,
  blocked: Shield,
  unknown: HelpCircle,
}
```

## Design System

### Spacing Scale

```css
:root {
  /* Spacing System (4px base) */
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
}
```

### Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem;    /* 2px */
  --radius-base: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;    /* 6px */
  --radius-lg: 0.5rem;      /* 8px */
  --radius-xl: 0.75rem;     /* 12px */
  --radius-2xl: 1rem;       /* 16px */
  --radius-full: 9999px;    /* Circle */
}
```

### Shadows

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
```

## Component Library

### Button Components

```tsx
// Primary Button Variants
const buttonVariants = {
  // Security Actions
  primary: "bg-primary-600 hover:bg-primary-700 text-white",
  safe: "bg-success-600 hover:bg-success-700 text-white",
  warning: "bg-warning-600 hover:bg-warning-700 text-white", 
  danger: "bg-danger-600 hover:bg-danger-700 text-white",
  
  // Secondary Actions
  secondary: "bg-gray-100 hover:bg-gray-200 text-gray-900",
  outline: "border border-gray-300 hover:bg-gray-50 text-gray-700",
  ghost: "hover:bg-gray-100 text-gray-700",
  
  // Sizes
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base", 
  lg: "px-6 py-3 text-lg",
}

// Usage Examples
<Button variant="danger" size="md">Block Email</Button>
<Button variant="safe" size="sm">Mark as Safe</Button>
<Button variant="outline" size="lg">View Details</Button>
```

### Status Indicators

```tsx
// Risk Level Badges
const RiskBadge = ({ level, score }: { level: string, score: number }) => {
  const variants = {
    safe: "bg-success-100 text-success-800 border-success-200",
    low: "bg-blue-100 text-blue-800 border-blue-200", 
    medium: "bg-warning-100 text-warning-800 border-warning-200",
    high: "bg-danger-100 text-danger-800 border-danger-200",
    critical: "bg-critical-100 text-critical-800 border-critical-200",
  }
  
  return (
    <span className={`
      inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border
      ${variants[level]}
    `}>
      <securityIcons[level] className="w-3 h-3 mr-1" />
      {level.toUpperCase()} ({Math.round(score * 100)}%)
    </span>
  )
}
```

### Data Tables

```tsx
// Email List Table
const EmailTable = ({ emails, onEmailClick }: EmailTableProps) => {
  return (
    <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
      <table className="min-w-full divide-y divide-gray-300">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Sender
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Subject
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Risk Level
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Detected
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {emails.map((email) => (
            <EmailRow key={email.id} email={email} onClick={onEmailClick} />
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

### Cards & Panels

```tsx
// Stats Card Component
const StatsCard = ({ title, value, change, icon: Icon, trend }: StatsCardProps) => {
  const trendColors = {
    up: "text-success-600",
    down: "text-danger-600", 
    neutral: "text-gray-500"
  }
  
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className="h-6 w-6 text-gray-400" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">
                {title}
              </dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {value}
                </div>
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${trendColors[trend]}`}>
                  {change}
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Layout & Grid System

### Main Layout Structure

```tsx
// Application Layout
const AppLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Navigation content */}
        </div>
      </nav>
      
      {/* Main Content */}
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {children}
        </div>
      </div>
    </div>
  )
}
```

### Dashboard Grid Layout

```tsx
// Dashboard Layout System
const DashboardGrid = () => {
  return (
    <div className="space-y-6">
      {/* Stats Row */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard {...statsData[0]} />
        <StatsCard {...statsData[1]} />
        <StatsCard {...statsData[2]} />
        <StatsCard {...statsData[3]} />
      </div>
      
      {/* Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card className="lg:col-span-1">
          <ThreatTimeline />
        </Card>
        <Card className="lg:col-span-1">
          <RiskDistribution />
        </Card>
      </div>
      
      {/* Data Table */}
      <div className="grid grid-cols-1">
        <Card>
          <EmailTable emails={emailData} />
        </Card>
      </div>
    </div>
  )
}
```

## User Experience

### User Journey Maps

#### 1. **Security Analyst Workflow**
```
1. Login → 2. Dashboard Overview → 3. Review Alerts → 4. Investigate Email → 5. Take Action
```

#### 2. **Administrator Workflow**  
```
1. Login → 2. System Status → 3. Configuration → 4. User Management → 5. Reports
```

#### 3. **End User Workflow**
```
1. Login → 2. Personal Dashboard → 3. View Emails → 4. Report Issues → 5. Settings
```

### Information Hierarchy

#### Dashboard Priority Levels
1. **Critical Alerts** (Red) - Immediate attention required
2. **Active Threats** (Orange) - Review needed
3. **System Status** (Blue) - Operational awareness
4. **Historical Data** (Gray) - Context information

### User Personas

#### Primary Persona: Security Analyst (Sarah)
- **Role**: Email Security Analyst
- **Goals**: Quickly identify and respond to threats
- **Pain Points**: Information overload, false positives
- **Needs**: Clear threat prioritization, detailed analysis tools

#### Secondary Persona: IT Administrator (Mike)
- **Role**: IT Security Manager  
- **Goals**: Configure security policies, manage users
- **Pain Points**: Complex configuration, system monitoring
- **Needs**: Intuitive admin panels, comprehensive reporting

#### Tertiary Persona: End User (Lisa)
- **Role**: Marketing Manager
- **Goals**: Check email safety, understand threats
- **Pain Points**: Technical complexity, unclear warnings
- **Needs**: Simple interface, clear explanations

## Information Architecture

### Navigation Structure

```
PhishGuard Application
├── Dashboard
│   ├── Overview
│   ├── Real-time Monitoring
│   └── Quick Actions
├── Email Analysis
│   ├── Inbox Review
│   ├── Threat Detection
│   ├── Quarantine
│   └── Safe List
├── Threat Intelligence
│   ├── Active Threats
│   ├── Threat Patterns
│   ├── IOCs (Indicators)
│   └── Threat Feeds
├── Reports & Analytics
│   ├── Security Reports
│   ├── Performance Metrics
│   ├── Trend Analysis
│   └── Export Data
├── Configuration
│   ├── Detection Rules
│   ├── Email Policies
│   ├── Integration Settings
│   └── API Management
└── Administration
    ├── User Management
    ├── Role Permissions
    ├── System Settings
    └── Audit Logs
```

### Content Strategy

#### Page Templates

**Dashboard Page Template**
- Hero stats (4 key metrics)
- Primary chart (threat timeline)
- Secondary charts (risk distribution)
- Recent activity table
- Quick action buttons

**Email Detail Template**
- Email header information
- Risk assessment panel
- Threat analysis details
- URL/attachment analysis
- Action history
- Related emails

**Settings Page Template**
- Navigation sidebar
- Form sections
- Save/cancel actions
- Help tooltips
- Validation messages

## Responsive Design

### Breakpoint System

```css
/* Mobile First Approach */
:root {
  --breakpoint-sm: 640px;    /* Small devices */
  --breakpoint-md: 768px;    /* Medium devices */
  --breakpoint-lg: 1024px;   /* Large devices */
  --breakpoint-xl: 1280px;   /* Extra large devices */
  --breakpoint-2xl: 1536px;  /* 2X Extra large devices */
}
```

### Responsive Components

```tsx
// Responsive Dashboard Grid
const ResponsiveDashboard = () => {
  return (
    <div className="space-y-6">
      {/* Stats - Stack on mobile, grid on larger screens */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {statsData.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>
      
      {/* Charts - Stack on mobile/tablet, side-by-side on desktop */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <ThreatChart className="xl:col-span-1" />
        <RiskChart className="xl:col-span-1" />
      </div>
      
      {/* Table - Horizontal scroll on mobile */}
      <div className="overflow-x-auto">
        <EmailTable />
      </div>
    </div>
  )
}
```

### Mobile-First Components

```tsx
// Mobile Navigation
const MobileNav = () => {
  const [isOpen, setIsOpen] = useState(false)
  
  return (
    <div className="md:hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-md text-gray-600 hover:text-gray-900"
      >
        <Menu className="h-6 w-6" />
      </button>
      
      {isOpen && (
        <div className="absolute top-16 left-0 right-0 bg-white shadow-lg border-t">
          <nav className="px-4 py-6 space-y-4">
            {navigationItems.map((item) => (
              <Link key={item.href} href={item.href} className="block text-gray-900">
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </div>
  )
}
```

## Accessibility

### WCAG 2.1 AA Compliance

#### Color Contrast
```css
/* Minimum contrast ratios */
:root {
  /* Text on backgrounds - 4.5:1 minimum */
  --text-primary: #111827;    /* 16.2:1 on white */
  --text-secondary: #4b5563;  /* 7.2:1 on white */
  --text-tertiary: #6b7280;   /* 5.9:1 on white */
  
  /* Interactive elements - 3:1 minimum */
  --link-color: #2563eb;      /* 5.7:1 on white */
  --button-primary: #1d4ed8;  /* 6.8:1 on white */
}
```

#### Keyboard Navigation
```tsx
// Accessible Button Component
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, disabled, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base styles
          "inline-flex items-center justify-center rounded-md font-medium",
          "focus:outline-none focus:ring-2 focus:ring-offset-2",
          "disabled:opacity-50 disabled:pointer-events-none",
          // Variant styles
          buttonVariants({ variant, size, className })
        )}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    )
  }
)
```

#### Screen Reader Support
```tsx
// Accessible Data Table
const AccessibleTable = ({ data, columns }: TableProps) => {
  return (
    <table role="table" aria-label="Email security analysis results">
      <thead>
        <tr>
          {columns.map((column) => (
            <th 
              key={column.key}
              scope="col"
              aria-sort={column.sortable ? "none" : undefined}
            >
              {column.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={row.id} aria-rowindex={index + 2}>
            {columns.map((column) => (
              <td key={`${row.id}-${column.key}`}>
                {column.render ? column.render(row[column.key], row) : row[column.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

#### ARIA Labels and Descriptions
```tsx
// Accessible Risk Indicator
const RiskIndicator = ({ level, score }: RiskIndicatorProps) => {
  const ariaLabel = `Risk level: ${level}, Score: ${Math.round(score * 100)} percent`
  
  return (
    <div 
      role="status"
      aria-label={ariaLabel}
      className={`risk-indicator risk-indicator--${level}`}
    >
      <span aria-hidden="true" className="risk-icon">
        {getRiskIcon(level)}
      </span>
      <span className="risk-text">
        {level} ({Math.round(score * 100)}%)
      </span>
    </div>
  )
}
```

## Interaction Design

### Micro-interactions

#### Loading States
```tsx
// Skeleton Loading Components
const EmailSkeleton = () => (
  <div className="animate-pulse">
    <div className="space-y-3">
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
    </div>
  </div>
)

// Progressive Loading
const EmailTable = () => {
  const { data, isLoading, error } = useEmails()
  
  if (isLoading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <EmailSkeleton key={i} />
        ))}
      </div>
    )
  }
  
  return <Table data={data} />
}
```

#### Hover Effects
```css
/* Subtle hover interactions */
.email-row {
  @apply transition-colors duration-150 ease-in-out;
}

.email-row:hover {
  @apply bg-gray-50;
}

.button {
  @apply transition-all duration-150 ease-in-out;
  @apply transform hover:scale-105 active:scale-95;
}

.card {
  @apply transition-shadow duration-200 ease-in-out;
}

.card:hover {
  @apply shadow-lg;
}
```

#### Status Transitions
```tsx
// Animated Status Changes
const StatusBadge = ({ status, isChanging }: StatusBadgeProps) => {
  return (
    <span 
      className={cn(
        "inline-flex items-center px-2 py-1 rounded-full text-xs font-medium",
        "transition-all duration-300 ease-in-out",
        statusVariants[status],
        isChanging && "animate-pulse"
      )}
    >
      {isChanging ? (
        <Loader2 className="w-3 h-3 mr-1 animate-spin" />
      ) : (
        <statusIcons[status] className="w-3 h-3 mr-1" />
      )}
      {status}
    </span>
  )
}
```

### Toast Notifications

```tsx
// Toast Notification System
const useToast = () => {
  const showToast = (message: string, type: 'success' | 'error' | 'warning' | 'info') => {
    toast.custom((t) => (
      <div className={cn(
        "max-w-md w-full bg-white shadow-lg rounded-lg pointer-events-auto",
        "flex ring-1 ring-black ring-opacity-5",
        t.visible ? "animate-enter" : "animate-leave"
      )}>
        <div className="flex-1 w-0 p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {type === 'success' && <CheckCircle className="h-6 w-6 text-green-400" />}
              {type === 'error' && <XCircle className="h-6 w-6 text-red-400" />}
              {type === 'warning' && <AlertTriangle className="h-6 w-6 text-yellow-400" />}
              {type === 'info' && <Info className="h-6 w-6 text-blue-400" />}
            </div>
            <div className="ml-3 flex-1">
              <p className="text-sm font-medium text-gray-900">
                {message}
              </p>
            </div>
          </div>
        </div>
        <div className="flex border-l border-gray-200">
          <button
            onClick={() => toast.dismiss(t.id)}
            className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            Close
          </button>
        </div>
      </div>
    ))
  }
  
  return { showToast }
}
```

## Data Visualization

### Chart Color Scheme

```tsx
// Consistent chart colors
const chartColors = {
  safe: '#22c55e',      // Green
  low: '#3b82f6',       // Blue  
  medium: '#f59e0b',    // Orange
  high: '#ef4444',      // Red
  critical: '#ec4899',  // Pink
  
  // Gradients for areas
  safeGradient: 'linear-gradient(180deg, #22c55e33 0%, #22c55e00 100%)',
  dangerGradient: 'linear-gradient(180deg, #ef444433 0%, #ef444400 100%)',
}
```

### Chart Components

```tsx
// Threat Timeline Chart
const ThreatTimeline = ({ data }: { data: ThreatData[] }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis 
          dataKey="timestamp" 
          stroke="#6b7280"
          fontSize={12}
          tickFormatter={(value) => format(new Date(value), 'HH:mm')}
        />
        <YAxis stroke="#6b7280" fontSize={12} />
        <Tooltip 
          contentStyle={{
            backgroundColor: '#f9fafb',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            fontSize: '14px'
          }}
        />
        <Area
          type="monotone"
          dataKey="threats"
          stroke={chartColors.high}
          fill={chartColors.dangerGradient}
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

// Risk Distribution Pie Chart
const RiskDistribution = ({ data }: { data: RiskData[] }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={2}
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={chartColors[entry.risk as keyof typeof chartColors]} 
            />
          ))}
        </Pie>
        <Tooltip />
        <Legend 
          verticalAlign="bottom" 
          height={36}
          iconType="circle"
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
```

## Design Tokens

### Token Structure

```typescript
// Design tokens definition
export const tokens = {
  // Colors
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe', 
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      900: '#1e3a8a',
    },
    semantic: {
      success: '#22c55e',
      warning: '#f59e0b', 
      danger: '#ef4444',
      info: '#3b82f6',
    },
  },
  
  // Typography
  typography: {
    fontFamily: {
      primary: ['Inter', 'sans-serif'],
      mono: ['SF Mono', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  
  // Spacing
  spacing: {
    0: '0',
    1: '0.25rem',
    2: '0.5rem', 
    3: '0.75rem',
    4: '1rem',
    6: '1.5rem',
    8: '2rem',
    12: '3rem',
    16: '4rem',
    20: '5rem',
  },
  
  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
  },
  
  // Border radius
  borderRadius: {
    none: '0',
    sm: '0.125rem',
    base: '0.25rem', 
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    full: '9999px',
  },
}
```

### Implementation with Tailwind

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: tokens.colors.primary,
        success: tokens.colors.semantic.success,
        warning: tokens.colors.semantic.warning,
        danger: tokens.colors.semantic.danger,
      },
      fontFamily: {
        sans: tokens.typography.fontFamily.primary,
        mono: tokens.typography.fontFamily.mono,
      },
      fontSize: tokens.typography.fontSize,
      fontWeight: tokens.typography.fontWeight,
      spacing: tokens.spacing,
      boxShadow: tokens.shadows,
      borderRadius: tokens.borderRadius,
    },
  },
}
```

This comprehensive UI/UX design system provides PhishGuard with a cohesive, accessible, and professional interface that prioritizes security information while maintaining excellent usability across all device types.