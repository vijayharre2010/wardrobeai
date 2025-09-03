import { supabase } from './supabaseClient';

const emailInput = document.getElementById('email-input') as HTMLInputElement;
const loginButton = document.getElementById('login-button') as HTMLButtonElement;
const loginForm = document.getElementById('login-form') as HTMLFormElement;
const popup = document.getElementById('popup') as HTMLDivElement;
const popupMessage = document.getElementById('popup-message') as HTMLParagraphElement;

function showPopup(message: string, isError: boolean = false) {
  popupMessage.textContent = message;
  if (isError) {
    popup.classList.add('error');
  } else {
    popup.classList.remove('error');
  }
  popup.classList.add('show');
  setTimeout(() => {
    popup.classList.remove('show');
  }, 3000); // Popup disappears after 3 seconds
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = emailInput.value;

  if (!email) {
    showPopup('Please enter your email address.', true);
    return;
  }

  loginButton.disabled = true;
  loginButton.textContent = 'Sending Magic Link...';

  const { error } = await supabase.auth.signInWithOtp({ email });

  if (error) {
    console.error('Supabase signInWithOtp error:', error);
    showPopup(`Login failed: ${error.message}`, true);
  } else {
    showPopup('Check your email for the magic link!');
  }

  loginButton.disabled = false;
  loginButton.textContent = 'Login with Magic Link';
});

// Handle session changes (e.g., after magic link click)
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN' && session) {
    console.log('User signed in:', session.user);
    // Redirect to home page or dashboard
    window.location.href = 'home.html'; // Assuming you have a home.html
  } else if (event === 'SIGNED_OUT') {
    console.log('User signed out');
    // Optionally redirect to login page if signed out
    // window.location.href = 'login.html';
  }
});