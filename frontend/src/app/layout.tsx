import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Navigation from '../components/Navigation';
import Footer from '../components/Footer';
import { AuthProvider } from '../context/auth-context';
import { ThemeProvider } from '../context/ThemeContext';
import { NotificationProvider } from '../context/NotificationContext';
import '../styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A secure, multi-user todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          <ThemeProvider>
            <NotificationProvider>
              <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
                <Navigation />
                {/* Main content */}
                <main className="py-6 flex-grow">
                  <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                    {children}
                  </div>
                </main>
                <Footer />
              </div>
            </NotificationProvider>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}