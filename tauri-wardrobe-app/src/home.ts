import { supabase } from "./supabaseClient";

async function checkAuthentication() {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session) {
    // If no session, redirect to login.html
    window.location.href = "/src/login.html";
  }
}

async function loadPage(pageName: string) {
  const appContentDiv = document.getElementById("app-content");
  if (!appContentDiv) {
    console.error("App content div not found!");
    return;
  }

  try {
    const response = await fetch(`/src/${pageName}.html`);
    if (!response.ok) {
      throw new Error(`Failed to load ${pageName}.html: ${response.statusText}`);
    }
    const rawHtml = await response.text();
    const processedHtml = rawHtml
      .replace(/href="(?!https?:\/\/)([^"]+\.css)"/g, 'href="/src/$1"')
      .replace(/<script[^>]+src="[^"]+\.ts"[^>]*><\/script>/g, "");
    appContentDiv.innerHTML = processedHtml;

    // Dynamically load the corresponding TypeScript module if it exists
    const scriptPath = `/src/${pageName}.ts`;
    // Check if script already exists to prevent multiple loads
    if (!document.querySelector(`script[src="${scriptPath}"]`)) {
      const script = document.createElement("script");
      script.type = "module";
      script.src = scriptPath;
      appContentDiv.appendChild(script);
    }
  } catch (error) {
    console.error(`Error loading page ${pageName}:`, error);
    appContentDiv.innerHTML = `<p>Error loading page: ${pageName}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await checkAuthentication(); // Perform authentication check on load

  // Load the default "daily" page
  loadPage("daily");
  (document.getElementById("nav-daily") as HTMLElement | null)?.classList.add("active");

  // Add event listeners to taskbar items
  const taskbarItems = document.querySelectorAll(".taskbar-item");
  taskbarItems.forEach(item => {
    item.addEventListener("click", (event) => {
      event.preventDefault();
      const target = event.currentTarget as HTMLElement;
      const pageName = target.dataset.page || target.id?.replace(/^nav-/, "");
      if (pageName) {
        taskbarItems.forEach(i => (i as HTMLElement).classList.remove("active"));
        target.classList.add("active");
        loadPage(pageName);
      }
    });
  });
});