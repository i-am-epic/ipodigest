// app/page.tsx
import { Metadata } from 'next'
import IPOTable from '../components/IPOTable'
import { ThemeProvider } from '../components/theme-provider'
import { ModeToggle } from '../components/mode-toggle'

export const metadata: Metadata = {
  title: 'IPO Investment Platform | Explore Current IPOs',
  description: 'Discover and invest in the latest Initial Public Offerings (IPOs). Get real-time data, expert analysis, and seamless investment options.',
  keywords: 'IPO, investment, stocks, public offering, financial markets',
}

export default function Home() {
  
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <div className="min-h-screen bg-background text-foreground">
        <header className="p-4 border-b">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">IPO Investment Platform</h1>
            <ModeToggle />
          </div>
        </header>

        <main className="container mx-auto py-8">
          <section className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">Welcome to IPO Insights</h2>
            <p className="text-lg mb-4">
              Explore the latest Initial Public Offerings and make informed investment decisions.
              Our platform provides real-time data, expert analysis, and seamless investment options.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">Current IPOs</h2>
            <IPOTable />
          </section>
        </main>

        <footer className="border-t p-4 mt-12">
          <div className="container mx-auto text-center">
            <p>&copy; 2024 IPO Investment Platform. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  )
}