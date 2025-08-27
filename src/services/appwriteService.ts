import { Client, Account } from 'appwrite';
import { Preferences } from '@capacitor/preferences';

// Initialize Appwrite client
const client = new Client();
client
  .setEndpoint('https://syd.cloud.appwrite.io/v1') // Replace with your Appwrite endpoint
  .setProject('68a849440035a24e5a92'); // Replace with your project ID

// Initialize Appwrite services
const account = new Account(client);

// Optional session storage key (only if you want to cache locally)
const SESSION_KEY = 'appwrite_session';

// Create context for Appwrite
export const useAppwrite = () => {
  // Function to create anonymous session
  const createAnonymousSession = async () => {
    try {
      const session = await account.createAnonymousSession();

      // (Optional) Store session in Preferences
      await Preferences.set({
        key: SESSION_KEY,
        value: JSON.stringify(session),
      });

      return session;
    } catch (error) {
      console.error('Error creating anonymous session:', error);
      throw error;
    }
  };

  // Function to get current session (from Appwrite)
  const getCurrentSession = async () => {
    try {
      const session = await account.get();
      return session;
    } catch (error) {
      console.error('Error getting current session:', error);
      return null;
    }
  };

  // Function to check if user is authenticated
  const isAuthenticated = async () => {
    try {
      const user = await account.get();
      return !!user;
    } catch {
      return false;
    }
  };

  // Function to logout
  const logout = async () => {
    try {
      await account.deleteSession('current');
      await Preferences.remove({ key: SESSION_KEY });
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return {
    account,
    createAnonymousSession,
    getCurrentSession,
    isAuthenticated,
    logout,
  };
};
