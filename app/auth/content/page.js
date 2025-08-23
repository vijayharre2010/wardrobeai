'use client';
import { Client, Account } from 'appwrite';
import Link from 'next/link';
import '../../globals.css';
import { useEffect, useState } from 'react';

const client = new Client()
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT)
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID);

const account = new Account(client);

export default function ContentPage() {
  const [todaysWears, setTodaysWears] = useState([
    { title: 'Home', description: 'Cozy and comfortable outfit for staying in.', img: '/placeholder-home-1024.jpg' },
    { title: 'Professional', description: 'Sharp look for work and meetings.', img: '/placeholder-professional-1024.jpg' },
    { title: 'Social', description: 'Trendy style for outings and gatherings.', img: '/placeholder-social-1024.jpg' },
  ]);

  // Optional: Load prefs / user and adapt cards later
  useEffect(() => {
    // placeholder for potential dynamic data
  }, []);

  const handleLogout = async () => {
    try {
      await account.deleteSession('current');
      window.location.href = '/login';
    } catch (err) {
      console.error('Logout failed', err);
      alert('Logout failed. Try again.');
    }
  };

  return (
    <div className="content-wrapper">
      {/* Top navbar */}
      <div className="navbar">
        <div className="nav-actions">
          <Link href="/auth/profile" className="nav-btn secondary">Edit Profile</Link>
          <button onClick={handleLogout} className="nav-btn">Logout</button>
        </div>
      </div>

      <main className="content-container">
        <h1>Today’s Wears</h1>
        <p>Personalized outfit suggestions, tailored for you.</p>

        <section className="card-row" aria-label="Today's outfit suggestions">
          {todaysWears.map((item, i) => (
            <article key={i} className="card" role="article">
              <div className="card-image">
                {/* images sized to large square source; CSS scales to fit 1024x1024 */}
                <img src={item.img} alt={item.title} loading="lazy" />
              </div>
              <div className="card-content">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
            </article>
          ))}
        </section>
      </main>
    </div>
  );
}
