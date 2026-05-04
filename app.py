import streamlit as st
from youtube_api import get_channel_data, get_videos
from analyzer import calculate_health_score, generate_suggestions
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="YouTube Analyzer", layout="wide")

st.title("📊 YouTube Growth Analyzer")

channel_id = st.text_input("Enter YouTube Channel ID")

if st.button("Analyze"):
    from youtube_api import youtube
    if youtube is None:
        st.error("⚠️ YouTube API Key is missing. Please add it to your `.env` file.")
    else:
        data = get_channel_data(channel_id)
        if data is None:
            st.error("❌ Invalid Channel ID")
        else:
            st.success(f"Channel: {data['title']}")

            # Show stats
            col1, col2, col3 = st.columns(3)

            col1.metric("Subscribers", data['subs'])
            col2.metric("Total Views", data['views'])
            col3.metric("Total Videos", data['videos'])

            # Calculate score
            score = calculate_health_score(
                data['subs'], data['views'], data['videos']
            )

            st.subheader("📈 Channel Health Score")
            st.progress(score)
            st.write(f"Score: {score}/100")

            # Suggestions
            suggestions = generate_suggestions(
               score, data['subs'], data['views'], data['videos']
            )
            
            
            st.markdown("## 📊 Advanced Analytics Dashboard")

            videos = get_videos(channel_id)

            if len(videos) > 0:
                df = pd.DataFrame(videos)

                # ---------------- SAFETY ----------------
                if 'likes' not in df.columns:
                    df['likes'] = 0

                df['engagement'] = df['likes'] / df['views'].replace(0, 1)

                # ---------------- 1. BAR CHART ----------------
                # st.subheader("📊 Views per Video")
                # fig1 = px.bar(df, x="title", y="views", color="views")
                # st.plotly_chart(fig1, use_container_width=True)

                # ---------------- 2. PIE CHART ----------------
                st.subheader("🧩 View Distribution")
                fig2 = px.pie(df, names="title", values="views")
                st.plotly_chart(fig2, use_container_width=True)

                # ---------------- 3. LINE CHART ----------------
                st.subheader("📈 Performance Trend")
                df['index'] = range(1, len(df)+1)
                fig3 = px.line(df, x="index", y="views", markers=True)
                st.plotly_chart(fig3, use_container_width=True)

                # ---------------- 4. BUBBLE CHART ----------------
                st.subheader("🔥 Views vs Likes (Engagement Map)")
                fig4 = px.scatter(
                    df,
                    x="views",
                    y="likes",
                    size="views",
                    color="likes",
                    hover_name="title"
                )
                st.plotly_chart(fig4, use_container_width=True)

                # ---------------- 5. ENGAGEMENT CHART ----------------
                # st.subheader("💬 Engagement per Video")
                # fig5 = px.bar(df, x="title", y="engagement", color="engagement")
                # st.plotly_chart(fig5, use_container_width=True)

                # ---------------- 6. RADAR CHART ----------------
                st.subheader("🧠 Channel Performance Radar")

                metrics = {
                    "Views": data['views'],
                    "Subscribers": data['subs'],
                    "Videos": data['videos'],
                    "Avg Views": df['views'].mean(),
                    "Engagement": df['engagement'].mean()
                }

                fig6 = go.Figure()

                fig6.add_trace(go.Scatterpolar(
                    r=list(metrics.values()),
                    theta=list(metrics.keys()),
                    fill='toself'
                ))

                fig6.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=False
                )

                st.plotly_chart(fig6, use_container_width=True)

                # ---------------- 7. BEST vs WORST ----------------
                st.subheader("⚖️ Best vs Worst Video")

                top_video = df.loc[df['views'].idxmax()]
                low_video = df.loc[df['views'].idxmin()]

                compare_df = pd.DataFrame({
                    "Type": ["Best Video", "Worst Video"],
                    "Views": [top_video['views'], low_video['views']]
                })

                fig7 = px.bar(compare_df, x="Type", y="Views", color="Type")
                st.plotly_chart(fig7, use_container_width=True)

            else:
                st.warning("No video data available")

            st.markdown("## 🚀 AI Growth Strategy")

            for s in suggestions:
                st.markdown(f"""
                <div style="
                  background: rgba(255,255,255,0.05);
                  padding: 12px;
                  border-radius: 10px;
                  margin-bottom: 10px;
                  border-left: 4px solid #ff4b2b;">
                 {s}
                </div>
                """, unsafe_allow_html=True)

            # Video titles
            st.subheader("🎬 Recent Videos")
            videos = get_videos(channel_id)

            for v in videos:
                st.write(f"- {v['title']}")
