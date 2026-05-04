def calculate_health_score(subs, views, videos):
    if videos == 0:
        return 0

    avg_views = views / videos

    # Simple scoring logic
    score = 0

    if avg_views > 10000:
        score += 40
    elif avg_views > 1000:
        score += 25
    else:
        score += 10

    if subs > 10000:
        score += 30
    elif subs > 1000:
        score += 20
    else:
        score += 10

    if videos > 50:
        score += 30
    elif videos > 10:
        score += 20
    else:
        score += 10

    return score


def generate_suggestions(score, subs, views, videos):

    suggestions = []

    avg_views = views / videos if videos > 0 else 0

    # ---------------- CONTENT STRATEGY ----------------
    if avg_views < 1000:
        suggestions.append("📉 Low average views → Improve content hook in first 5 seconds")
        suggestions.append("🎯 Use curiosity-driven titles (e.g., 'You won’t believe this…')")
    elif avg_views > 10000:
        suggestions.append("🚀 High-performing content → Create series based on top videos")

    # ---------------- CONSISTENCY ----------------
    if videos < 20:
        suggestions.append("📅 Low upload frequency → Post 3 videos/week for faster growth")
    elif videos > 100:
        suggestions.append("📦 Large content library → Re-optimize old videos for SEO")

    # ---------------- SUBSCRIBER GROWTH ----------------
    if subs < 1000:
        suggestions.append("👥 Low subscribers → Add strong CTA ('Subscribe now') in every video")
    elif subs > 50000:
        suggestions.append("🔥 Strong audience → Launch exclusive content or memberships")

    # ---------------- ENGAGEMENT ----------------
    suggestions.append("💬 Ask questions in videos → Increase comments & engagement")
    suggestions.append("📌 Pin comments to guide audience interaction")

    # ---------------- VIRAL STRATEGY ----------------
    suggestions.append("⚡ Post YouTube Shorts daily → Boost discovery algorithm")
    suggestions.append("🔥 Follow trending topics weekly (use Google Trends)")

    # ---------------- SEO OPTIMIZATION ----------------
    suggestions.append("🔍 Add keywords in title + description + tags for better ranking")
    suggestions.append("📈 Use long-tail keywords (e.g., 'AI tools for students 2026')")

    # ---------------- THUMBNAIL ----------------
    suggestions.append("🎨 Use high contrast colors (yellow/red) in thumbnails")
    suggestions.append("😲 Add facial expressions → increases CTR significantly")

    # ---------------- WATCH TIME ----------------
    suggestions.append("⏱️ Increase watch time → avoid long boring intros")
    suggestions.append("🎬 Use pattern interrupts (cuts, zooms, text) every 5–10 seconds")

    # ---------------- COMPETITOR STRATEGY ----------------
    suggestions.append("🕵️ Analyze top 3 competitors → replicate their viral formats")
    suggestions.append("📊 Identify their best-performing videos → create similar content")

    # ---------------- BRANDING ----------------
    suggestions.append("🏷️ Build a niche identity → focus on one topic (AI, coding, etc.)")
    suggestions.append("🎤 Create a unique intro style → improve brand recall")

    # ---------------- ADVANCED AI INSIGHTS ----------------
    if score < 40:
        suggestions.append("🚨 Early stage channel → prioritize consistency over perfection")
    elif score > 70:
        suggestions.append("🏆 Scaling phase → focus on audience retention & brand deals")

    # ---------------- MONETIZATION ----------------
    suggestions.append("💰 Explore affiliate marketing (tools/products)")
    suggestions.append("📢 Promote your own digital product or course")

    # ---------------- COMMUNITY BUILDING ----------------
    suggestions.append("🤝 Reply to comments within 24 hours → boost engagement")
    suggestions.append("📊 Use polls & community posts to interact with audience")

    return suggestions
