'use client';
import Link from 'next/link';
import '../../globals.css';

export default function Profile() {
  return (
    <div className="container profile-container">
      <h1>Edit Profile</h1>
      <form className="profile-form">
        <label>Age</label>
        <input type="number" placeholder="Enter your age" />

        <label>Height (cm)</label>
        <input type="number" placeholder="Enter your height" />

        <label>Skin Tone</label>
        <input type="text" placeholder="e.g. Fair, Medium, Dark" />

        <label>Hair Color</label>
        <input type="text" placeholder="e.g. Black, Brown, Blonde" />

        <label>Location</label>
        <input type="text" placeholder="Enter your location" />

        <button type="submit">Save Changes</button>
      </form>

      <Link href="/auth/content">Back to Dashboard</Link>
    </div>
  );
}
