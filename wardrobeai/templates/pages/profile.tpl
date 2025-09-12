<div class="content-card">
    <h1 class="page-title">
        <i data-lucide="user" class="icon"></i>
        Profile Settings
    </h1>
    <p style="font-size: 1.1rem; color: #cccccc; margin-bottom: 2rem;">
        Manage your personal details and account preferences for better AI recommendations
    </p>

    {% if profile_updated %}
    <div class="status-message status-success">
        <i data-lucide="check-circle" class="icon-small"></i>
        Profile updated successfully! Your AI recommendations will now be personalized.
    </div>
    {% endif %}

    {% if profile_error %}
    <div class="status-message status-error">
        <i data-lucide="alert-circle" class="icon-small"></i>
        Error updating profile: {{ profile_error }}
    </div>
    {% endif %}

    {% if upgrade_error %}
    <div class="status-message status-error">
        <i data-lucide="alert-circle" class="icon-small"></i>
        Error upgrading plan: {{ upgrade_error }}
    </div>
    {% endif %}
</div>

<div class="grid grid-2">
    <div class="content-card">
        <h2 class="section-title">
            <i data-lucide="user-circle" class="icon-small"></i>
            Personal Information
        </h2>

        <div class="form-card">
            <form action="/page/profile" method="post">
                <div class="form-group">
                    <label class="form-label" for="height">
                        <i data-lucide="ruler" class="icon-small"></i>
                        Height (cm)
                    </label>
                    <input type="number" id="height" name="height" class="form-input" placeholder="170" min="120" max="220" value="{{ profile.height if profile else '' }}">
                </div>

                <div class="form-group">
                    <label class="form-label" for="age">
                        <i data-lucide="calendar" class="icon-small"></i>
                        Age
                    </label>
                    <input type="number" id="age" name="age" class="form-input" placeholder="25" min="13" max="100" value="{{ profile.age if profile else '' }}">
                </div>

                <div class="form-group">
                    <label class="form-label" for="weight">
                        <i data-lucide="scale" class="icon-small"></i>
                        Weight (kg)
                    </label>
                    <input type="number" id="weight" name="weight" class="form-input" placeholder="65" min="30" max="200" value="{{ profile.weight if profile else '' }}">
                </div>

                <div class="form-group">
                    <label class="form-label" for="gender">
                        <i data-lucide="users" class="icon-small"></i>
                        Gender
                    </label>
                    <select id="gender" name="gender" class="form-input">
                        <option value="">Select gender</option>
                        <option value="male" {% if profile and profile.gender == 'male' %}selected{% endif %}>Male</option>
                        <option value="female" {% if profile and profile.gender == 'female' %}selected{% endif %}>Female</option>
                        <option value="non-binary" {% if profile and profile.gender == 'non-binary' %}selected{% endif %}>Non-binary</option>
                        <option value="prefer-not-to-say" {% if profile and profile.gender == 'prefer-not-to-say' %}selected{% endif %}>Prefer not to say</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="ethnicity">
                        <i data-lucide="globe" class="icon-small"></i>
                        Ethnicity/Skin Tone
                    </label>
                    <select id="ethnicity" name="ethnicity" class="form-input">
                        <option value="">Select ethnicity</option>
                        <option value="light" {% if profile and profile.ethnicity == 'light' %}selected{% endif %}>Light/Fair</option>
                        <option value="medium" {% if profile and profile.ethnicity == 'medium' %}selected{% endif %}>Medium</option>
                        <option value="olive" {% if profile and profile.ethnicity == 'olive' %}selected{% endif %}>Olive/Mediterranean</option>
                        <option value="tan" {% if profile and profile.ethnicity == 'tan' %}selected{% endif %}>Tan</option>
                        <option value="dark" {% if profile and profile.ethnicity == 'dark' %}selected{% endif %}>Dark</option>
                        <option value="ebony" {% if profile and profile.ethnicity == 'ebony' %}selected{% endif %}>Ebony</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="style_preference">
                        <i data-lucide="palette" class="icon-small"></i>
                        Style Preference
                    </label>
                    <select id="style_preference" name="style_preference" class="form-input">
                        <option value="casual" {% if profile and profile.style_preference == 'casual' %}selected{% endif %}>Casual</option>
                        <option value="professional" {% if profile and profile.style_preference == 'professional' %}selected{% endif %}>Professional</option>
                        <option value="elegant" {% if profile and profile.style_preference == 'elegant' %}selected{% endif %}>Elegant</option>
                        <option value="trendy" {% if profile and profile.style_preference == 'trendy' %}selected{% endif %}>Trendy</option>
                        <option value="minimalist" {% if profile and profile.style_preference == 'minimalist' %}selected{% endif %}>Minimalist</option>
                        <option value="bohemian" {% if profile and profile.style_preference == 'bohemian' %}selected{% endif %}>Bohemian</option>
                        <option value="streetwear" {% if profile and profile.style_preference == 'streetwear' %}selected{% endif %}>Streetwear</option>
                        <option value="vintage" {% if profile and profile.style_preference == 'vintage' %}selected{% endif %}>Vintage</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="extra_info">
                        <i data-lucide="file-text" class="icon-small"></i>
                        Additional Information
                    </label>
                    <textarea id="extra_info" name="extra_info" class="form-input" rows="4" placeholder="Any additional preferences, allergies, or style notes...">{{ profile.extra_info if profile else '' }}</textarea>
                </div>

                <button type="submit" class="btn-primary">
                    <i data-lucide="save" class="icon-small"></i>
                    Save Profile
                </button>
            </form>
        </div>
    </div>

    <div class="content-card">
        <h2 class="section-title">
            <i data-lucide="settings" class="icon-small"></i>
            Account & Preferences
        </h2>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="mail" class="icon-small" style="color: #B19CD9;"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Email</div>
                    <div style="font-size: 0.9rem; color: #888;">user@example.com</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="calendar" class="icon-small" style="color: #4ecdc4;"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Member Since</div>
                    <div style="font-size: 0.9rem; color: #888;">January 2024</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                <i data-lucide="shield" class="icon-small" style="color: {% if is_premium %}#4ecdc4{% else %}#ff6b6b{% endif %}"></i>
                <div>
                    <div style="font-weight: 600; color: #ffffff;">Account Status</div>
                    <div style="font-size: 0.9rem; color: #888;">
                        {% if is_premium %}
                        Premium Member
                        {% else %}
                        Free Account
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <div style="margin-top: 2rem;">
            <h3 style="color: #ffffff; margin-bottom: 1rem; font-size: 1rem;">Quick Settings</h3>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                    <i data-lucide="moon" class="icon-small" style="color: #B19CD9;"></i>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #ffffff;">Theme</div>
                        <div style="font-size: 0.9rem; color: #888;">Dark Mode</div>
                    </div>
                    <button class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                        <i data-lucide="edit" class="icon-small"></i>
                        Edit
                    </button>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); border-radius: 8px;">
                    <i data-lucide="bell" class="icon-small" style="color: #4ecdc4;"></i>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #ffffff;">Notifications</div>
                        <div style="font-size: 0.9rem; color: #888;">Email notifications enabled</div>
                    </div>
                    <button class="btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                        <i data-lucide="edit" class="icon-small"></i>
                        Edit
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

{% if not is_premium %}
<div class="content-card" style="border: 2px solid #B19CD9; box-shadow: 0 0 30px rgba(177, 156, 217, 0.3);">
     <div style="background: linear-gradient(145deg, rgba(177, 156, 217, 0.1) 0%, rgba(177, 156, 217, 0.05) 100%); padding: 1rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(177, 156, 217, 0.3);">
         <div style="display: flex; align-items: center; gap: 1rem;">
             <div style="background: #B19CD9; color: #121212; padding: 0.5rem; border-radius: 50%; font-weight: bold; font-size: 1.2rem;">★</div>
             <div>
                 <h3 style="color: #B19CD9; margin: 0; font-size: 1.2rem;">Limited Time Offer!</h3>
                 <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">{{ app_config.messages.limited_offer }} - {{ app_config.messages.offer_ends|format(hours=app_config.pricing.countdown_hours) }}</p>
             </div>
             <div style="margin-left: auto; background: #ff6b6b; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">⏰ 24:00:00</div>
         </div>
     </div>

     <h2 class="section-title">
         <i data-lucide="crown" class="icon-small"></i>
         Premium Plans
     </h2>
{% else %}
<div class="content-card" style="border: 2px solid #4ecdc4; box-shadow: 0 0 30px rgba(78, 205, 196, 0.3);">
     <div style="background: linear-gradient(145deg, rgba(78, 205, 196, 0.1) 0%, rgba(78, 205, 196, 0.05) 100%); padding: 1rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid rgba(78, 205, 196, 0.3);">
         <div style="display: flex; align-items: center; gap: 1rem;">
             <div style="background: #4ecdc4; color: #121212; padding: 0.5rem; border-radius: 50%; font-weight: bold; font-size: 1.2rem;">✓</div>
             <div>
                 <h3 style="color: #4ecdc4; margin: 0; font-size: 1.2rem;">Premium Member</h3>
                 <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">Thank you for being a premium member! Enjoy unlimited access to all features.</p>
             </div>
         </div>
     </div>

     <h2 class="section-title">
         <i data-lucide="crown" class="icon-small"></i>
         Your Premium Benefits
     </h2>
{% endif %}

    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
        <i data-lucide="users" class="icon-small" style="color: #4ecdc4;"></i>
        <span style="color: #4ecdc4; font-weight: 600;">Over {{ app_config.social_proof.user_count }} users upgraded last month!</span>
        <div style="display: flex; gap: 0.25rem;">
            {% for i in range(app_config.social_proof.rating_stars) %}
            <span style="color: #ff6b6b;">★</span>
            {% endfor %}
            <span style="color: #cccccc; font-size: 0.9rem;">{{ app_config.social_proof.rating }}/5 rating</span>
        </div>
    </div>

    {% if not is_premium %}
    <div class="grid grid-3">
        {% for plan_key, plan in app_config.pricing.plans.items() %}
        <div class="content-card" style="border: 2px solid {% if plan.popular %}#ff6b6b{% elif plan.best_value %}#4ecdc4{% else %}#555555{% endif %}; position: relative; {% if plan.popular %}transform: scale(1.05);{% endif %}">
            {% if plan.popular %}
            <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #ff6b6b; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                🔥 MOST POPULAR
            </div>
            {% elif plan.best_value %}
            <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #4ecdc4; color: #121212; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                🏆 BEST VALUE
            </div>
            {% endif %}

            <div style="text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #ffffff; font-size: 1.4rem;">{{ plan.name }}</h3>
                <div style="font-size: 2.5rem; font-weight: 800; color: #B19CD9; margin: 1rem 0;">
                    ${{ "%.2f"|format(plan.price) }}
                </div>
                {% if plan.original_price %}
                <div style="text-decoration: line-through; color: #888; font-size: 1.1rem;">${{ "%.2f"|format(plan.original_price) }}</div>
                <div style="background: #ff6b6b; color: white; padding: 0.25rem 0.5rem; border-radius: 8px; font-size: 0.9rem; font-weight: bold; display: inline-block; margin-top: 0.5rem;">
                    Save ${{ "%.2f"|format(plan.savings) }}!
                </div>
                {% endif %}
                <p style="color: #cccccc; font-size: 0.9rem;">per {{ plan.period }}</p>
            </div>

            <div style="margin: 1rem 0;">
                {% for feature in plan.features %}
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <i data-lucide="check" class="icon-small" style="color: #4ecdc4;"></i>
                    <span style="color: #cccccc; font-size: 0.9rem;">{{ feature }}</span>
                </div>
                {% endfor %}
            </div>

            <button class="{% if plan.best_value %}btn-primary{% else %}btn-secondary{% endif %}" style="width: 100%; {% if plan.best_value %}background: linear-gradient(145deg, #4ecdc4 0%, #45b7aa 100%);{% endif %}" onclick="selectPlan('{{ plan_key }}')">
                Choose Plan
            </button>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div style="text-align: center; padding: 2rem;">
        <i data-lucide="crown" style="font-size: 3rem; color: #4ecdc4; margin-bottom: 1rem;"></i>
        <h3 style="color: #ffffff; margin-bottom: 1rem;">Premium Features Unlocked!</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;">
            <div style="background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid #4ecdc4;">
                <i data-lucide="infinity" class="icon-small" style="color: #4ecdc4; margin-bottom: 0.5rem;"></i>
                <h4 style="color: #ffffff; margin: 0 0 0.5rem 0;">Unlimited Generations</h4>
                <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Generate as many outfits as you want</p>
            </div>
            <div style="background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid #4ecdc4;">
                <i data-lucide="zap" class="icon-small" style="color: #4ecdc4; margin-bottom: 0.5rem;"></i>
                <h4 style="color: #ffffff; margin: 0 0 0.5rem 0;">Priority Processing</h4>
                <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Faster AI processing times</p>
            </div>
            <div style="background: linear-gradient(145deg, #2a2a2a 0%, #1f1f1f 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid #4ecdc4;">
                <i data-lucide="star" class="icon-small" style="color: #4ecdc4; margin-bottom: 0.5rem;"></i>
                <h4 style="color: #ffffff; margin: 0 0 0.5rem 0;">Premium Styles</h4>
                <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Access to exclusive style options</p>
            </div>
        </div>
    </div>
    {% endif %}

    {% if not is_premium %}
    <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(145deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 107, 107, 0.05) 100%); border-radius: 12px; border: 1px solid rgba(255, 107, 107, 0.3);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <i data-lucide="alert-triangle" class="icon-small" style="color: #ff6b6b;"></i>
            <div>
                <h4 style="color: #ff6b6b; margin: 0; font-size: 1rem;">Don't Miss Out!</h4>
                <p style="color: #cccccc; margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                    {{ app_config.messages.loss_aversion }}
                </p>
            </div>
        </div>
    </div>
    {% endif %}
</div>

<div class="content-card">
    <h2 class="section-title">
        <i data-lucide="log-out" class="icon-small"></i>
        Account Actions
    </h2>

    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <form action="/logout" method="post" style="display: inline;">
            <button type="submit" class="btn-secondary">
                <i data-lucide="log-out" class="icon-small"></i>
                Logout
            </button>
        </form>

        <button class="btn-secondary">
            <i data-lucide="download" class="icon-small"></i>
            Export Data
        </button>

        <button class="btn-secondary" style="background: linear-gradient(145deg, #2a1a1a 0%, #3a1a1a 100%); border-color: #ff6b6b;">
            <i data-lucide="trash-2" class="icon-small"></i>
            Delete Account
        </button>
    </div>
</div>

<script>
function selectPlan(planType) {
    // Redirect to payment processing (Stripe or similar)
    window.location.href = `/upgrade?plan=${planType}`;
}

let countdownTime = {{ app_config.pricing.countdown_hours }} * 60 * 60; // {{ app_config.pricing.countdown_hours }} hours in seconds
const countdownElement = document.querySelector('.countdown-timer');

function updateCountdown() {
    const hours = Math.floor(countdownTime / 3600);
    const minutes = Math.floor((countdownTime % 3600) / 60);
    const seconds = countdownTime % 60;

    if (countdownElement) {
        countdownElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    if (countdownTime > 0) {
        countdownTime--;
        setTimeout(updateCountdown, 1000);
    } else {
        // Offer expired
        document.querySelector('.limited-offer').style.display = 'none';
    }
}

updateCountdown();
</script>
