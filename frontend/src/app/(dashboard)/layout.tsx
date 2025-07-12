export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto py-8">
        {children}
      </div>
    </div>
  )
} 