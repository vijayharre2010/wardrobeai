import Link from 'next/link';
import './globals.css';

export default function Home() {
  return (
    <div className="container" style={{ textAlign: 'center' }}>
      <h1>Welcome to WardrobeAI</h1>
      <Link href="/login">Login</Link>
    </div>
  );
}
