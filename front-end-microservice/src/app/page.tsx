import AppTable from "./_components/app_table"

export default function Home() {
  return (
    <main className="min-h-screen p-6 sm:p-10 bg-background">
      <h1 className="text-2xl font-bold mb-4">📊 App Metrics Dashboard</h1>
      <AppTable />
    </main>
  )
}
