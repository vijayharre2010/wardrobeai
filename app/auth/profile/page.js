'use client';
import { Client, Account } from 'appwrite';
import Link from 'next/link';
import '../../globals.css';
import { useEffect, useState } from 'react';

const client = new Client()
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT)
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID);

const account = new Account(client);

export default function ProfilePage() {
  const [prefs, setPrefs] = useState({
    age: '',
    height: '',
    skinTone: '',
    hairColor: '',
    location: ''
  });

  useEffect(() => {
    (async () => {
      try {
        const user = await account.get();
        setPrefs(user.prefs || {});
      } catch (err) {
        console.error('Failed to load user:', err);
      }
    })();
  }, []);

  const handleChange = (e) => setPrefs(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await account.updatePrefs(prefs);
      alert('Profile saved.');
    } catch (err) {
      console.error('Save failed:', err);
      alert('Could not save profile.');
    }
  };

  return (
    <div className="content-wrapper">
      <div className="navbar">
        <div className="nav-actions">
          <Link href="/auth/content" className="nav-btn secondary">Back</Link>
        </div>
      </div>

      <main className="content-container" style={{ maxWidth: 600 }}>
        <div className="container profile-container">
          <h1>Edit Profile</h1>
          <form className="profile-form" onSubmit={handleSubmit}>
            <label>Age</label>
            <input name="age" type="number" value={prefs.age || ''} onChange={handleChange} placeholder="Enter age" />

            <label>Height (cm)</label>
            <input name="height" type="number" value={prefs.height || ''} onChange={handleChange} placeholder="Enter height in cm" />

            <label>Skin Tone</label>
            <input name="skinTone" type="text" value={prefs.skinTone || ''} onChange={handleChange} placeholder="e.g. Fair, Medium, Dark" />

            <label>Hair Color</label>
            <input name="hairColor" type="text" value={prefs.hairColor || ''} onChange={handleChange} placeholder="e.g. Black, Brown, Blonde" />

            <label>Location</label>
            <input name="location" type="text" value={prefs.location || ''} onChange={handleChange} placeholder="City, Country" />

            <button type="submit">Save Changes</button>
          </form>
        </div>
      </main>
    </div>
  );
}
