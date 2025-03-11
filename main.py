import streamlit as st
import yaml
import copy
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Aporia - Discover What You Don't Know Yet",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for more natural, friendly styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main .block-container {padding-top: 1rem; max-width: 1000px; margin: 0 auto;}
    .stTabs [data-baseweb="tab-list"] {gap: 2rem; margin-bottom: 1rem;}
    .stTabs [data-baseweb="tab"] {height: 3rem;}
    
    /* Natural button styles */
    .stButton button {
        background-color: #7C83FD !important; 
        color: white !important; 
        border-radius: 25px !important;
        padding: 0.25rem 1.5rem !important;
        box-shadow: 0 3px 5px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease !important;
        border: none !important;
        font-weight: 500 !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 8px rgba(0,0,0,0.15) !important;
    }
    .delete-button button {background-color: #FF6B6B !important;}
    
    /* Topic cards */
    .topic-card {
        background-color: #fff;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #7C83FD;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .topic-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Subtopic cards */
    .subtopic-card {
        background-color: #fafafa;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid #96BAFF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
    }
    .subtopic-card:hover {
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
    }
    
    /* Pleasant text formatting */
    h1 {
        color: #424874;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #7C83FD;
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #7C83FD;
        font-weight: 500;
        margin-top: 1rem;
    }
    h4 {
        color: #424874;
        font-weight: 500;
    }
    p {
        color: #333;
        line-height: 1.6;
    }
    
    /* Pleasant breadcrumbs */
    .breadcrumb {
        background-color: #F5F5F5;
        padding: 0.5rem 1rem;
        border-radius: 30px;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        display: inline-block;
    }
    .breadcrumb-item {
        color: #7C83FD;
        margin: 0 0.25rem;
    }
    
    /* Beautiful welcome box */
    .welcome-box {
        background: linear-gradient(135deg, #96BAFF 0%, #7C83FD 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(124, 131, 253, 0.2);
    }
    .welcome-box h1 {
        color: white;
        margin-bottom: 0.5rem;
    }
    .welcome-box p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 0.5rem 1rem;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 0.5rem 1rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #424874;
        font-weight: 500;
    }
    
    /* Action panels */
    .action-panel {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px dashed #96BAFF;
    }
    
    /* Tree view */
    .tree-view {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 15px;
        max-height: 500px;
        overflow-y: auto;
    }
    .tree-item {
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    .tree-item:hover {
        transform: translateX(5px);
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #999;
    }
    .empty-state img {
        width: 150px;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load YAML data from file with graceful error handling"""
    try:
        with open("learn.yaml", "r") as file:
            data = yaml.safe_load(file)
            original_data = copy.deepcopy(data)
        return data, original_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}, {}

def save_data(data):
    """Save YAML data to file with graceful error handling"""
    try:
        with open("learn.yaml", "w") as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def format_key_display(key):
    """Convert keys like 'Snake_Case' to 'Snake Case' for natural reading"""
    return key.replace('_', ' ')

def display_breadcrumb(path):
    """Display a friendly breadcrumb navigation"""
    if not path:
        return
    
    breadcrumb_html = '<div class="breadcrumb">🏠 '
    for i, item in enumerate(path):
        breadcrumb_html += f'<span class="breadcrumb-item">{format_key_display(item)}</span>'
        if i < len(path) - 1:
            breadcrumb_html += ' > '
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def browse_topics(data):
    """Natural knowledge browsing experience"""
    current_data = data
    path = []
    
    # Navigation
    with st.sidebar:
        st.markdown("### 🧭 Explore Knowledge")
        st.markdown("Navigate through topics that interest you.")
        
        # Create a natural topic navigation
        while isinstance(current_data, dict) and current_data:
            keys = list(current_data.keys())
            
            # Determine the navigation prompt based on the depth
            if not path:
                prompt = "What would you like to explore?"
            elif len(path) == 1:
                prompt = f"Topics within {format_key_display(path[0])}"
            else:
                prompt = "Explore deeper"
            
            selected_key = st.selectbox(
                prompt, 
                keys, 
                key=f"browse_{len(path)}",
                format_func=format_key_display
            )
            
            path.append(selected_key)
            current_data = current_data[selected_key]
    
    # Content display
    display_breadcrumb(path)
    
    # Show content based on type
    if isinstance(current_data, str):
        # Text content
        st.markdown(f"""
        <div class="topic-card">
            <h2>{format_key_display(path[-1])}</h2>
            <p>{current_data}</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif isinstance(current_data, list):
        # List content
        st.markdown(f"""
        <div class="topic-card">
            <h2>{format_key_display(path[-1])}</h2>
        """, unsafe_allow_html=True)
        
        for item in current_data:
            st.markdown(f"• {item}")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif isinstance(current_data, dict):
        # Display subtopics in a friendly way
        st.markdown(f"## Discover {format_key_display(path[-1])}")
        
        # Create subtopic cards in a grid
        cols = st.columns(2)
        
        if not current_data:
            st.markdown("""
            <div class="empty-state">
                <p>No topics found. Let's add some!</p>
            </div>
            """, unsafe_allow_html=True)
        
        for i, (key, value) in enumerate(current_data.items()):
            col_idx = i % 2
            
            with cols[col_idx]:
                # Prepare a preview
                if isinstance(value, str):
                    preview = value[:100] + "..." if len(value) > 100 else value
                    icon = "📝"
                elif isinstance(value, list):
                    preview = f"{len(value)} items to explore"
                    icon = "📋"
                elif isinstance(value, dict):
                    items_count = len(value)
                    preview = f"{items_count} subtopics to discover"
                    icon = "📚" if items_count > 0 else "📁"
                
                # Display card with appropriate styling
                st.markdown(f"""
                <div class="subtopic-card">
                    <h3>{icon} {format_key_display(key)}</h3>
                    <p>{preview}</p>
                </div>
                """, unsafe_allow_html=True)

def build_knowledge_tree(data, parent_stack=None, add_direct_item=False):
    """Interactive knowledge tree builder"""
    # Initialize parent stack if not provided
    if parent_stack is None:
        parent_stack = []
    
    # Start with empty path
    path_crumbs = []
    
    # If we have parents in the stack, build path
    for parent_info in parent_stack:
        _, key = parent_info
        path_crumbs.append(key)
    
    # Show navigation breadcrumbs if we're not at the root
    if path_crumbs:
        display_breadcrumb(path_crumbs)
    
    # Current data reference
    if parent_stack:
        current_data = parent_stack[-1][0][parent_stack[-1][1]]
    else:
        current_data = data
    
    # If we want to add a direct item without selecting a node first
    if add_direct_item:
        return add_new_item(current_data, parent_stack, path_crumbs)
    
    # Interactive node selection
    if isinstance(current_data, dict) and current_data:
        st.markdown("### Where would you like to make changes?")
        
        # Show available nodes as attractive cards
        cols = st.columns(3)
        keys = list(current_data.keys())
        
        # Add "Add new topic here" option
        keys.append("➕ Add new topic here")
        
        for i, key in enumerate(keys):
            col_idx = i % 3
            
            with cols[col_idx]:
                if key == "➕ Add new topic here":
                    # Special card for adding new topic
                    if st.button(key, key=f"add_btn_{len(path_crumbs)}", use_container_width=True):
                        return add_new_item(current_data, parent_stack, path_crumbs)
                else:
                    # Regular node selection
                    if st.button(format_key_display(key), key=f"select_{key}", use_container_width=True):
                        # Navigate to selected node
                        new_stack = parent_stack.copy()
                        new_stack.append((current_data, key))
                        return build_knowledge_tree(data, new_stack)
    
    # If we've reached a leaf node or an empty dictionary, show editing options
    return edit_current_node(current_data, parent_stack, path_crumbs)

def add_new_item(current_data, parent_stack, path_crumbs):
    """UI for adding a new knowledge item"""
    if not isinstance(current_data, dict):
        st.error("Can only add items to a category. Please select a category first.")
        return current_data, parent_stack
    
    st.markdown("""
    <div class="action-panel">
        <h2>✨ Add New Knowledge</h2>
        <p>Let's expand your knowledge map with something new!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get topic name
    topic_name = st.text_input("What would you like to call this topic?", 
                              placeholder="e.g. Machine Learning, History of Rome, Guitar Chords...")
    
    if topic_name:
        # Clean the name for the key
        clean_key = topic_name.replace(' ', '_')
        
        # Choose content type
        content_type = st.radio(
            "What type of content is this?",
            ["Concept or Description", "Category for Subtopics", "List of Items"],
            captions=["Text explaining a concept", "A container for more topics", "A collection of related items"],
            horizontal=True
        )
        
        if content_type == "Concept or Description":
            # Text content
            content = st.text_area(
                "Describe this concept or topic",
                placeholder="Add your description here. What is this topic about? Why is it important?",
                height=150
            )
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.info("This will add a text description to your knowledge map.")
                
            with col2:
                if st.button("Add to Knowledge Map", use_container_width=True):
                    if clean_key not in current_data:
                        current_data[clean_key] = content
                        st.success(f"Added '{topic_name}' to your knowledge map!")
                        st.balloons()
                        # Return to parent view
                        if len(parent_stack) > 0:
                            return current_data, parent_stack[:-1]
                        else:
                            return current_data, []
                    else:
                        st.error(f"'{topic_name}' already exists!")
        
        elif content_type == "Category for Subtopics":
            # Category with optional initial subtopics
            include_subtopics = st.checkbox("Add initial subtopics?")
            
            if include_subtopics:
                subtopics = st.text_area(
                    "List subtopics (one per line)",
                    placeholder="Subtopic 1\nSubtopic 2\nSubtopic 3",
                    height=150
                )
                subtopic_list = [s.strip() for s in subtopics.split("\n") if s.strip()]
            
            if st.button("Create Category", use_container_width=True):
                if clean_key not in current_data:
                    if include_subtopics and 'subtopic_list' in locals() and subtopic_list:
                        # Create with subtopics
                        subtopic_dict = {}
                        for subtopic in subtopic_list:
                            clean_subtopic = subtopic.replace(' ', '_')
                            subtopic_dict[clean_subtopic] = ""
                        current_data[clean_key] = subtopic_dict
                    else:
                        # Empty category
                        current_data[clean_key] = {}
                    
                    st.success(f"Created '{topic_name}' category!")
                    st.balloons()
                    
                    # Navigate to the new category
                    new_stack = parent_stack.copy()
                    new_stack.append((current_data, clean_key))
                    return current_data, new_stack
                else:
                    st.error(f"'{topic_name}' already exists!")
        
        elif content_type == "List of Items":
            # List content
            items = st.text_area(
                "Add items (one per line)",
                placeholder="Item 1\nItem 2\nItem 3",
                height=150
            )
            item_list = [s.strip() for s in items.split("\n") if s.strip()]
            
            if st.button("Create List", use_container_width=True):
                if clean_key not in current_data:
                    current_data[clean_key] = item_list
                    st.success(f"Created '{topic_name}' list!")
                    st.balloons()
                    # Return to parent view
                    if len(parent_stack) > 0:
                        return current_data, parent_stack[:-1]
                    else:
                        return current_data, []
                else:
                    st.error(f"'{topic_name}' already exists!")
    
    # Cancel button
    if st.button("← Go Back"):
        if len(parent_stack) > 0:
            return current_data, parent_stack[:-1]
        else:
            return current_data, []
    
    return current_data, parent_stack

def edit_current_node(current_data, parent_stack, path_crumbs):
    """UI for editing the currently selected node"""
    if not path_crumbs:
        # Root level - nothing to edit
        st.markdown("""
        <div class="welcome-box">
            <h1>Welcome to your Knowledge Map!</h1>
            <p>Select a topic to explore or add new knowledge to your map.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Option to add a top-level topic
        if st.button("➕ Add New Top-Level Topic", use_container_width=True):
            return add_new_item(current_data, parent_stack, path_crumbs)
        
        return current_data, parent_stack
    
    # We have a selected node - show editing options
    st.markdown(f"""
    <div class="action-panel">
        <h2>✏️ Edit: {format_key_display(path_crumbs[-1])}</h2>
        <p>What would you like to change about this knowledge?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Different editing options based on data type
    if isinstance(current_data, str):
        # Edit text content
        new_content = st.text_area("Content", current_data, height=200)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Save Changes", use_container_width=True):
                if new_content != current_data:
                    parent, key = parent_stack[-1]
                    parent[key] = new_content
                    st.success("Saved your changes!")
                    # Stay on the same node
                    return current_data, parent_stack
        
        with col2:
            if st.button("← Go Back", use_container_width=True):
                # Navigate up one level
                if len(parent_stack) > 0:
                    return current_data, parent_stack[:-1]
        
        with col3:
            if st.button("🗑️ Delete", use_container_width=True, help="Delete this item"):
                if len(parent_stack) > 0:
                    parent, key = parent_stack[-1]
                    if st.checkbox(f"Confirm deletion of '{format_key_display(key)}'"):
                        del parent[key]
                        st.success(f"Deleted '{format_key_display(key)}'")
                        # Navigate up one level
                        return current_data, parent_stack[:-1]
    
    elif isinstance(current_data, list):
        # Edit list content
        st.markdown("### Edit List Items")
        
        # Use a dataframe for more natural list editing
        if current_data:
            df = pd.DataFrame({"Items": current_data})
            edited_df = st.data_editor(
                df, 
                num_rows="dynamic", 
                key="list_editor",
                use_container_width=True,
                hide_index=True
            )
            new_list = edited_df["Items"].tolist()
            
            # Remove empty items
            new_list = [item for item in new_list if str(item).strip()]
        else:
            st.info("This list is currently empty. Add your first item below.")
            new_item = st.text_input("New item")
            new_list = [new_item] if new_item else []
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Save Changes", use_container_width=True):
                if new_list != current_data:
                    parent, key = parent_stack[-1]
                    parent[key] = new_list
                    st.success("List updated successfully!")
                    # Stay on the same node
                    return current_data, parent_stack
        
        with col2:
            if st.button("← Go Back", use_container_width=True):
                # Navigate up one level
                if len(parent_stack) > 0:
                    return current_data, parent_stack[:-1]
        
        with col3:
            if st.button("🗑️ Delete", use_container_width=True, help="Delete this list"):
                if len(parent_stack) > 0:
                    parent, key = parent_stack[-1]
                    if st.checkbox(f"Confirm deletion of '{format_key_display(key)}'"):
                        del parent[key]
                        st.success(f"Deleted '{format_key_display(key)}'")
                        # Navigate up one level
                        return current_data, parent_stack[:-1]
    
    elif isinstance(current_data, dict):
        # Edit dictionary/category
        st.markdown("### Manage This Category")
        
        # Show current subtopics
        if current_data:
            st.markdown(f"#### Current items in {format_key_display(path_crumbs[-1])}")
            
            for key, value in current_data.items():
                content_type = "📝 Text" if isinstance(value, str) else "📋 List" if isinstance(value, list) else "📁 Category"
                st.markdown(f"- {content_type}: **{format_key_display(key)}**")
        else:
            st.info(f"This category is empty. Add some knowledge to {format_key_display(path_crumbs[-1])}!")
        
        # Buttons for actions
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("➕ Add New Item", use_container_width=True):
                # Navigate to add item view
                return add_new_item(current_data, parent_stack, path_crumbs)
        
        with col2:
            if st.button("← Go Back", use_container_width=True):
                # Navigate up one level
                if len(parent_stack) > 0:
                    return current_data, parent_stack[:-1]
        
        with col3:
            if st.button("🗑️ Delete", use_container_width=True, help="Delete this category"):
                if len(parent_stack) > 0:
                    parent, key = parent_stack[-1]
                    st.warning(f"This will delete '{format_key_display(key)}' and ALL its contents!")
                    if st.checkbox(f"Yes, permanently delete '{format_key_display(key)}'"):
                        del parent[key]
                        st.success(f"Deleted '{format_key_display(key)}'")
                        # Navigate up one level
                        return current_data, parent_stack[:-1]
    
    return current_data, parent_stack

def main():
    # Load data
    data, original_data = load_data()
    
    # Header
    st.markdown("""
    <div class="welcome-box">
        <h1>🧠 Aporia</h1>
        <p>Discover what you don't know yet. Map your knowledge, identify gaps, and guide your learning journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation tabs
    tab1, tab2 = st.tabs(["📚 Explore Knowledge", "✏️ Build Your Knowledge Map"])
    
    with tab1:
        browse_topics(data)
    
    with tab2:
        # Interactive knowledge building
        current_data, parent_stack = build_knowledge_tree(data)
        
        # Save changes button (only show if changes were made)
        if current_data != original_data:
            st.markdown("---")
            
            # Center the save button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("💾 Save All Changes", use_container_width=True):
                    # Save changes to file
                    if save_data(current_data):
                        st.success("Your knowledge map has been updated!")
                        st.balloons()
                    else:
                        st.error("There was a problem saving your changes.")

if __name__ == "__main__":
    main()