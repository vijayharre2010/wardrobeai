<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WardrobeAI - AI-Powered Wardrobe Assistant</title>
    <meta name="description" content="Professional AI-powered wardrobe management and outfit suggestions">
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>👔</text></svg>">
</head>
<body>
    <div class="app-container">
        <div class="page-container fade-in">
            {% include page %}
        </div>
    </div>

    <nav class="bottom-nav">
        <ul id="nav-tabs"></ul>
    </nav>

    <script src="/static/js/nav.js"></script>
    <script src="/static/js/popup.js"></script>
    <script>
        // Initialize Lucide icons
        lucide.createIcons();

        // Add active class to current page navigation
        document.addEventListener('DOMContentLoaded', function() {
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.bottom-nav a');

            navLinks.forEach(link => {
                if (link.getAttribute('href') === currentPath) {
                    link.classList.add('active');
                }
            });
        });
    </script>
</body>
</html>
