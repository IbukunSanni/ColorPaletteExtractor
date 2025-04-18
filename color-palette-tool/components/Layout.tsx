export default function Layout({ children }: { children: React.ReactNode }) {
    return (
      <main className="min-h-screen bg-white text-gray-800 p-4 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">🎨 Color Palette Generator</h1>
        {children}
      </main>
    );
  }
  