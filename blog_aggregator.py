import streamlit as st
import feedparser
from datetime import datetime, timedelta
import pytz
import json

# Configure the app
st.set_page_config(page_title="AWS Blog Aggregator", page_icon="📰", layout="wide")

# AWS Blog Feeds in JSON format
AWS_FEEDS = {
    "Architecture": [
        {"name": "AWS Architecture Blog", "url": "https://aws.amazon.com/blogs/architecture/feed/"}
    ],
    "AWS Cost Management": [
        {"name": "AWS Cost Management Blog", "url": "https://aws.amazon.com/blogs/aws-cost-management/feed/"}
    ],
    "AWS Partner Network": [
        {"name": "APN Blog", "url": "https://aws.amazon.com/blogs/apn/feed/"}
    ],
    "AWS Podcast": [
        {"name": "AWS Podcast", "url": "https://aws.amazon.com/podcasts/aws-podcast/"}
    ],
    "AWS Marketplace": [
        {"name": "AWS Marketplace Blog", "url": "https://aws.amazon.com/blogs/awsmarketplace/feed/"}
    ],
    "AWS News": [
        {"name": "AWS News Blog", "url": "https://aws.amazon.com/blogs/aws/feed/"}
    ],
    "Big Data": [
        {"name": "AWS Big Data Blog", "url": "https://aws.amazon.com/blogs/big-data/feed/"}
    ],
    "Business Productivity": [
        {"name": "Business Productivity Blog", "url": "https://aws.amazon.com/blogs/business-productivity/feed/"}
    ],
    "Compute": [
        {"name": "AWS Compute Blog", "url": "https://aws.amazon.com/blogs/compute/feed/"}
    ],
    "Contact Center": [
        {"name": "Contact Center Blog", "url": "https://aws.amazon.com/blogs/contact-center/feed/"}
    ],
    "Containers": [
        {"name": "AWS Containers Blog", "url": "https://aws.amazon.com/blogs/containers/feed/"}
    ],
    "Database": [
        {"name": "AWS Database Blog", "url": "https://aws.amazon.com/blogs/database/feed/"}
    ],
    "Desktop & Application Streaming": [
        {"name": "Desktop & App Streaming Blog", "url": "https://aws.amazon.com/blogs/desktop-and-application-streaming/feed/"}
    ],
    "Developer": [
        {"name": "AWS Developer Blog", "url": "https://aws.amazon.com/blogs/developer/feed/"}
    ],
    "DevOps": [
        {"name": "AWS DevOps Blog", "url": "https://aws.amazon.com/blogs/devops/feed/"}
    ],
    "Enterprise Strategy": [
        {"name": "Enterprise Strategy Blog", "url": "https://aws.amazon.com/blogs/enterprise-strategy/feed/"}
    ],
    "Front-End Web & Mobile": [
        {"name": "Front-End Web & Mobile Blog", "url": "https://aws.amazon.com/blogs/mobile/feed/"}
    ],
    "Game Tech": [
        {"name": "AWS Game Tech Blog", "url": "https://aws.amazon.com/blogs/gametech/feed/"}
    ],
    "HPC": [
        {"name": "AWS HPC Blog", "url": "https://aws.amazon.com/blogs/hpc/feed/"}
    ],
    "Infrastructure & Automation": [
        {"name": "Infrastructure & Automation Blog", "url": "https://aws.amazon.com/blogs/infrastructure-and-automation/feed/"}
    ],
    "Industries": [
        {"name": "AWS Industries Blog", "url": "https://aws.amazon.com/blogs/industries/feed/"}
    ],
    "Internet of Things": [
        {"name": "AWS IoT Blog", "url": "https://aws.amazon.com/blogs/iot/feed/"}
    ],
    "Machine Learning": [
        {"name": "AWS ML Blog", "url": "https://aws.amazon.com/blogs/machine-learning/feed/"}
    ],
    "Management & Governance": [
        {"name": "AWS Management & Governance Blog", "url": "https://aws.amazon.com/blogs/mt/feed/"}
    ],
    "Media": [
        {"name": "AWS Media Blog", "url": "https://aws.amazon.com/blogs/media/feed/"}
    ],
    "Messaging & Targeting": [
        {"name": "Messaging & Targeting Blog", "url": "https://aws.amazon.com/blogs/messaging-and-targeting/feed/"}
    ],
    "Networking & Content Delivery": [
        {"name": "AWS Networking Blog", "url": "https://aws.amazon.com/blogs/networking-and-content-delivery/feed/"}
    ],
    "Open Source": [
        {"name": "AWS Open Source Blog", "url": "https://aws.amazon.com/blogs/opensource/feed/"}
    ],
    "Public Sector": [
        {"name": "AWS Public Sector Blog", "url": "https://aws.amazon.com/blogs/publicsector/feed/"}
    ],
    "Quantum Computing": [
        {"name": "AWS Quantum Blog", "url": "https://aws.amazon.com/blogs/quantum-computing/feed/"}
    ],
    "Robotics": [
        {"name": "AWS Robotics Blog", "url": "https://aws.amazon.com/blogs/robotics/feed/"}
    ],
    "SAP": [
        {"name": "AWS for SAP Blog", "url": "https://aws.amazon.com/blogs/awsforsap/feed/"}
    ],
    "Security, Identity, & Compliance": [
        {"name": "AWS Security Blog", "url": "https://aws.amazon.com/blogs/security/feed/"}
    ],
    "Startups": [
        {"name": "AWS Startups Blog", "url": "https://aws.amazon.com/blogs/startups/feed/"}
    ],
    "Storage": [
        {"name": "AWS Storage Blog", "url": "https://aws.amazon.com/blogs/storage/feed/"}
    ],
    "Training & Certification": [
        {"name": "AWS Training Blog", "url": "https://aws.amazon.com/blogs/training-and-certification/feed/"}
    ],
    "Windows on AWS": [
        {"name": "Windows on AWS Blog", "url": "https://aws.amazon.com/blogs/modernizing-with-aws/feed/"}
    ]
}

def fetch_recent_posts(feeds, days=7):
    recent_posts = []
    cutoff_date = datetime.now(pytz.utc) - timedelta(days=days)
    
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries:
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc)
                    if published > cutoff_date:
                        recent_posts.append({
                            "title": entry.title,
                            "link": entry.link,
                            "source": feed["name"],
                            "published": published.strftime("%b %d, %Y"),
                            "category": next((k for k, v in AWS_FEEDS.items() if feed in v), "Uncategorized")
                        })
        except Exception as e:
            st.sidebar.warning(f"Error fetching {feed['name']}: {str(e)}")
    
    return sorted(recent_posts, key=lambda x: x["published"], reverse=True)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("AWS Blog Aggregator")
    st.caption("Aggregates posts from all official AWS blogs")
    
    days = st.slider("Show posts from last N days:", 1, 30, 7)
    
    # Initialize session state for posts if not exists
    if 'all_posts' not in st.session_state:
        st.session_state.all_posts = []
    
    if st.button("Fetch All Posts", type="primary"):
        # Fetch all posts when button is clicked
        all_feeds = [feed for category in AWS_FEEDS.values() for feed in category]
        st.session_state.all_posts = fetch_recent_posts(all_feeds, days)
    
    # Display category selector with counts
    if st.session_state.all_posts:
        # Calculate post counts per category
        category_counts = {}
        for post in st.session_state.all_posts:
            category = post["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Create options with counts
        options_with_counts = [
            f"{category} ({count})" 
            for category, count in category_counts.items()
        ]
        
        selected_options = st.multiselect(
            "Filter by category:",
            options=options_with_counts,
            default=None  # None selected by default
        )
        
        # Extract pure category names from selections
        selected_categories = [
            option.split(" (")[0] 
            for option in selected_options
        ]
    else:
        selected_categories = []

# --- Main Content ---
st.title("AWS Blog Aggregator")

if st.session_state.all_posts:
    if not selected_categories:
        # Show all posts if no categories selected
        filtered_posts = st.session_state.all_posts
        st.info("Showing all posts (no categories selected)")
    else:
        # Filter posts by selected categories
        filtered_posts = [
            post for post in st.session_state.all_posts 
            if post["category"] in selected_categories
        ]
    
    if not filtered_posts:
        st.warning("No posts match your filters")
    else:
        st.success(f"Showing {len(filtered_posts)} posts")
        
        # Group posts by category
        posts_by_category = {}
        for post in filtered_posts:
            if post["category"] not in posts_by_category:
                posts_by_category[post["category"]] = []
            posts_by_category[post["category"]].append(post)
        
        # Display posts by category
        for category, posts in posts_by_category.items():
            with st.expander(f"{category} ({len(posts)})", expanded=True):
                for post in posts:
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 20px; padding: 10px; border-radius: 5px; 
                                    border-left: 4px solid #ff9900; background-color: #f9f9f9;">
                            <h4><a href="{post['link']}" target="_blank">{post['title']}</a></h4>
                            <p style="color: #666; font-size: 0.9em; margin-bottom: 0;">
                                <b>{post['source']}</b> • {post['published']}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
else:
    st.info("Click 'Fetch All Posts' to load articles from all AWS blogs")

# Optional: Add footer
st.sidebar.markdown("---")
st.sidebar.caption(f"Total articles loaded: {len(st.session_state.all_posts)}")