// app/page.tsx
import Hero from './components/Hero'
import Header from './components/Header'
import Footer from './components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <Footer />
    </main>
  )
}