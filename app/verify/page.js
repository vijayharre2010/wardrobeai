'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Client, Account } from 'appwrite';
import '../globals.css';

const client = new Client()
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT)
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID);

const account = new Account(client);

export default function Verify() {
  const [message, setMessage] = useState('Verifying...');
  const router = useRouter();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('userId');
    const secret = urlParams.get('secret');

    if (userId && secret) {
      account.updateMagicURLSession(userId, secret)
        .then(() => {
          setMessage('Login successful! Redirecting...');
          
          // Appwrite sets a session cookie automatically for the browser
          // just redirect to dashboard
          window.location.href = '/auth/dashboard';
        })
        .catch((error) => {
          setMessage(`Error: ${error.message}`);
        });
    } else {
      setMessage('Invalid verification link.');
    }
  }, []);

  return (
    <div className="container" style={{ textAlign: 'center' }}>
      <h1>Verification</h1>
      <p>{message}</p>
    </div>
  );
}
