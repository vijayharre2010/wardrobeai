<div class="content-card">
    <h1 class="page-title">
        <i data-lucide="image" class="icon"></i>
        AI Outfit Generator
    </h1>
    <p style="font-size: 1.1rem; color: #cccccc; margin-bottom: 2rem;">
        Describe your ideal outfit and let AI generate visual suggestions for you
    </p>

    {% if not is_premium %}
    <div style="background: linear-gradient(145deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 107, 107, 0.05) 100%); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <i data-lucide="lock" class="icon-small" style="color: #ff6b6b;"></i>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #ff6b6b;">Free Plan Limitation</div>
                <div style="color: #cccccc; font-size: 0.9rem;">{{ app_config.messages.generation_limit_description|format(limit=app_config.usage_limits.ai_generations) }}</div>
            </div>
            <a href="/page/profile#premium" style="text-decoration: none;">
                <button class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    Upgrade Now
                </button>
            </a>
        </div>
    </div>
    {% endif %}
</div>

{% if limit_exceeded %}
<div class="content-card" style="grid-column: span 2;">
    <div style="text-align: center; padding: 3rem;">
        <i data-lucide="lock" class="icon" style="color: #ff6b6b; margin-bottom: 1rem;"></i>
        <h2 style="color: #ff6b6b; margin-bottom: 1rem;">Generation Limit Reached</h2>
        <p style="color: #cccccc; font-size: 1.1rem; margin-bottom: 2rem;">
            {{ app_config.messages.generation_limit_description|format(limit=app_config.usage_limits.ai_generations) }}
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <a href="/page/profile#premium" style="text-decoration: none;">
                <button class="btn-primary">
                    <i data-lucide="crown" class="icon-small"></i>
                    Upgrade to Premium
                </button>
            </a>
            <a href="/page/dashboard" style="text-decoration: none;">
                <button class="btn-secondary">
                    <i data-lucide="home" class="icon-small"></i>
                    Back to Dashboard
                </button>
            </a>
        </div>
    </div>
</div>
{% else %}
<div class="grid grid-2">
    <div class="content-card">
        <h2 class="section-title">
            <i data-lucide="edit" class="icon-small"></i>
            Describe Your Outfit
        </h2>

        <div class="form-card">
            <form action="/page/generate" method="post">
                <div class="form-group">
                    <label class="form-label" for="prompt">
                        <i data-lucide="type" class="icon-small"></i>
                        Outfit Description
                    </label>
                    <textarea id="prompt" name="prompt" class="form-input" rows="6" placeholder="Describe your perfect outfit... e.g., 'A professional business suit for a corporate meeting' or 'Casual summer dress for a beach party'" required></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label" for="style">
                        <i data-lucide="palette" class="icon-small"></i>
                        Style Preference
                    </label>
                    <select id="style" name="style" class="form-input">
                        <option value="professional">Professional</option>
                        <option value="casual">Casual</option>
                        <option value="elegant">Elegant</option>
                        <option value="trendy">Trendy</option>
                        <option value="bohemian">Bohemian</option>
                        <option value="minimalist">Minimalist</option>
                    </select>
                </div>

                <button type="submit" class="btn-primary">
                    <i data-lucide="sparkles" class="icon-small"></i>
                    Generate Outfits
                </button>
            </form>
        </div>
    </div>
{% endif %}

    <div class="content-card">
        <h2 class="section-title">
            <i data-lucide="lightbulb" class="icon-small"></i>
            Generation Tips
        </h2>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div style="display: flex; align-items: flex-start; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="target" class="icon-small" style="color: #B19CD9; margin-top: 0.2rem;"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Be Specific</div>
                    <div style="font-size: 0.8rem; color: #888;">Include details like occasion, colors, and style preferences</div>
                </div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="zap" class="icon-small" style="color: #4ecdc4; margin-top: 0.2rem;"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Get Creative</div>
                    <div style="font-size: 0.8rem; color: #888;">Mix styles, colors, and accessories for unique combinations</div>
                </div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="clock" class="icon-small" style="color: #ff6b6b; margin-top: 0.2rem;"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Quick Results</div>
                    <div style="font-size: 0.8rem; color: #888;">Get 3 AI-generated outfit images in seconds</div>
                </div>
            </div>
        </div>
    </div>
</div>

{% if generated_images %}
<div class="content-card">
    <h2 class="section-title">
        <i data-lucide="images" class="icon-small"></i>
        Generated Outfits
    </h2>

    <div class="grid grid-3">
        {% for image in generated_images %}
        <div style="background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 12px; padding: 1rem; text-align: center;">
            <div style="width: 100%; height: 200px; background: linear-gradient(145deg, #333333 0%, #444444 100%); border-radius: 8px; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center;">
                <i data-lucide="image" class="icon" style="color: #666;"></i>
            </div>
            <h4 style="color: #ffffff; margin-bottom: 0.5rem;">Outfit {{ loop.index }}</h4>
            <div style="display: flex; gap: 0.5rem; justify-content: center;">
                <button class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                    <i data-lucide="heart" class="icon-small"></i>
                    Save
                </button>
                <button class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                    <i data-lucide="download" class="icon-small"></i>
                    Download
                </button>
            </div>
        </div>
        {% endfor %}
    </div>

    <div style="text-align: center; margin-top: 2rem;">
        <button class="btn-primary">
            <i data-lucide="refresh-cw" class="icon-small"></i>
            Generate More
        </button>
    </div>
</div>
{% endif %}