import { supabase } from "./supabaseClient";

async function loadApp() {
  const appDiv = document.getElementById("app");
  if (!appDiv) {
    console.error("App div not found!");
    return;
  }

  const { data: { session } } = await supabase.auth.getSession();

  if (session) {
    // User is authenticated, load home.html
    const response = await fetch("/src/home.html");
    const homeHtml = await response.text();
    // Normalize relative asset paths inside injected HTML (css links) and remove embedded TS scripts
    const processedHomeHtml = homeHtml
      .replace(/href="(?!https?:\/\/)([^"]+\.css)"/g, 'href="/src/$1"')
      .replace(/<script[^>]+src="[^"]+\.ts"[^>]*><\/script>/g, "");
    appDiv.innerHTML = processedHomeHtml;

    // Dynamically load home.ts as a module
    const script = document.createElement("script");
    script.type = "module";
    script.src = "/src/home.ts";
    appDiv.appendChild(script);
  } else {
    // User is not authenticated, redirect to login.html
    const response = await fetch("/src/login.html");
    const loginHtml = await response.text();
    // Normalize relative asset paths inside injected HTML (css links) and remove embedded TS scripts
    const processedLoginHtml = loginHtml
      .replace(/href="(?!https?:\/\/)([^"]+\.css)"/g, 'href="/src/$1"')
      .replace(/<script[^>]+src="[^"]+\.ts"[^>]*><\/script>/g, "");
    appDiv.innerHTML = processedLoginHtml;

    // Dynamically load login.ts as a module
    const script = document.createElement("script");
    script.type = "module";
    script.src = "/src/login.ts";
    appDiv.appendChild(script);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  loadApp();
});
