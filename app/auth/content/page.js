'use client';
import { Client, Account } from 'appwrite';
import Link from 'next/link';
import '../../globals.css';

const client = new Client()
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT)
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID);

const account = new Account(client);

export default function Content() {
  const handleLogout = async () => {
    try {
      await account.deleteSession('current');
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout failed:', error);
      alert('Logout failed. Please try again.');
    }
  };

  const todaysWears = [
    { title: 'Home', description: 'Cozy and comfortable outfit for staying in.', img: '/placeholder-home.png' },
    { title: 'Professional', description: 'Sharp look for work and meetings.', img: '/placeholder-professional.png' },
    { title: 'Social', description: 'Trendy style for outings and gatherings.', img: '/placeholder-social.png' },
  ];

  return (
    <div className="content-wrapper">
      {/* Top bar */}
      <div className="top-bar">
        <Link href="/auth/profile" className="top-btn">Edit Profile</Link>
        <button onClick={handleLogout} className="top-btn">Logout</button>
      </div>

      <div className="container content-container">
        <h1>Today’s Wears</h1>
        <p>AI-generated style suggestions tailored to you.</p>

        <div className="card-grid">
          {todaysWears.map((wear, index) => (
            <div key={index} className="card">
              <div className="card-image">
                <img src={wear.img} alt={wear.title} />
              </div>
              <div className="card-content">
                <h3>{wear.title}</h3>
                <p>{wear.description}</p>
              </div>
            </div>
          ))}
        </div>

        <Link href="/">Back to Home</Link>
      </div>
    </div>
  );
}
