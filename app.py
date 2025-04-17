import streamlit as st
from database import DatabaseManager
from steganography import DatabaseSteganography
from io import BytesIO
import pandas as pd
import plotly.express as px

def create_styled_container():
    st.markdown("""
        <style>
        .styledContainer {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background-color: #1E1E1E;
        }
        .header {
            color: #4CAF50;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .label {
            color: #00BCD4;
            font-weight: bold;
            margin-right: 10px;
        }
        .value {
            color: #FFFFFF;
        }
        .success {
            color: #4CAF50;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .warning {
            color: #FFC107;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Database Steganography Demo",
        page_icon="🔒",
        layout="wide"
    )
    
    create_styled_container()
    
    st.title("🔒 Database Steganography Demo")
    
    db = DatabaseManager()
    stego = DatabaseSteganography()

    # Sidebar với style
    with st.sidebar:
        st.markdown("### 📌 Navigation")
        page = st.selectbox(
            "Select Page",
            ["💫 Hide Message", "🔍 Extract Message", "📊 View Data"],
            label_visibility="collapsed"
        )

    if "💫 Hide Message" in page:
        st.header("💫 Hide Message")
        
        # Chia layout thành 2 cột
        col1, col2 = st.columns(2)
        
        with col1:
            with st.form("hide_message_form"):
                st.markdown("#### 📝 Employee Information")
                name = st.text_input("👤 Employee Name")
                email = st.text_input("📧 Email Address")
                position = st.text_input("💼 Position")
                
                st.markdown("#### 🔐 Message Information")
                cover_text = st.text_input("📄 Cover Text", "ILOVEYOU")
                secret_message = st.text_input("🔑 Secret Message")
                
                submit = st.form_submit_button("🔒 Hide Message")
                
                if submit and secret_message and cover_text:
                    try:
                        modified_text = stego.hide_message_in_text(cover_text, secret_message)
                        new_id = db.insert_employee(name, email, position, modified_text)
                        
                        with col2:
                            st.markdown("#### ✅ Result")
                            st.success(f"Message successfully hidden!")
                            st.info("📋 Details:")
                            st.json({
                                "Record ID": new_id,
                                "Employee": name,
                                "Original Text": cover_text,
                                "Modified Text": modified_text,
                                "Hidden Message": secret_message
                            })
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    elif "🔍 Extract Message" in page:
        st.header("🔍 Extract Hidden Message")
        
        employees = db.get_all_employees()
        
        if not employees:
            st.warning("📭 No records found in database")
        else:
            st.info(f"📊 Found {len(employees)} records")
            
            for emp in employees:
                with st.expander(f"🔍 Record #{emp[0]} - {emp[1]}"):
                    cols = st.columns(2)
                    with cols[0]:
                        st.markdown("#### 📋 Record Details")
                        st.markdown(f"""
                        - 👤 **Name:** {emp[1]}
                        - 📧 **Email:** {emp[2]}
                        - 💼 **Position:** {emp[3]}
                        """)
                    
                    with cols[1]:
                        st.markdown("#### 📄 Stored Text")
                        st.code(emp[4])
                        
                        if st.button(f"🔓 Extract Message", key=f"extract_{emp[0]}"):
                            try:
                                message = stego.extract_message_from_text(emp[4])
                                st.success(f"🔑 Hidden message: {message}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")

    else:  # View Data
        st.header("📊 Database Analytics & Visualization")
        
        employees = db.get_all_employees()
        
        if not employees:
            st.warning("📭 No records found in database")
        else:
            # 1. Dashboard Overview
            st.markdown("### 📈 Dashboard Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(employees), "Active")
            with col2:
                unique_employees = len(set(emp[1] for emp in employees))
                st.metric("Unique Employees", unique_employees)
            with col3:
                positions = len(set(emp[3] for emp in employees))
                st.metric("Different Positions", positions)
            with col4:
                avg_msg_length = sum(len(emp[4]) for emp in employees) / len(employees)
                st.metric("Avg Message Length", f"{avg_msg_length:.1f}")

            # 2. Quick Filters
            st.markdown("### 🔍 Quick Filters")
            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input("🔎 Search by Name")
            with col2:
                position_filter = st.multiselect(
                    "Filter by Position",
                    options=list(set(emp[3] for emp in employees))
                )

            # 3. Data Table with Sorting
            st.markdown("### 📋 Data Table")
            
            # Filter data based on search and filters
            filtered_data = employees
            if search_name:
                filtered_data = [emp for emp in filtered_data 
                               if search_name.lower() in emp[1].lower()]
            if position_filter:
                filtered_data = [emp for emp in filtered_data 
                               if emp[3] in position_filter]

            # Convert to DataFrame for better display
            import pandas as pd
            df = pd.DataFrame(filtered_data, 
                            columns=['ID', 'Name', 'Email', 'Position', 'Stored Text'])
            
            # Add custom styling
            st.dataframe(
                df,
                column_config={
                    "ID": st.column_config.NumberColumn("🔑 ID"),
                    "Name": st.column_config.TextColumn("👤 Name"),
                    "Email": st.column_config.TextColumn("📧 Email"),
                    "Position": st.column_config.TextColumn("💼 Position"),
                    "Stored Text": st.column_config.TextColumn("📝 Stored Text")
                },
                hide_index=True
            )

            # 4. Detailed Records View
            st.markdown("### 📑 Detailed Records")
            
            # Tab view for different display modes
            tab1, tab2 = st.tabs(["Card View", "List View"])
            
            with tab1:
                # Card View
                for i in range(0, len(filtered_data), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(filtered_data):
                            emp = filtered_data[i + j]
                            with cols[j]:
                                st.markdown(f"""
                                <div style='
                                    padding: 20px;
                                    border-radius: 10px;
                                    background-color: #1E1E1E;
                                    border: 1px solid #4CAF50;
                                    margin: 10px 0;
                                '>
                                    <h4>🎫 Record #{emp[0]}</h4>
                                    <p><strong>👤 Name:</strong> {emp[1]}</p>
                                    <p><strong>📧 Email:</strong> {emp[2]}</p>
                                    <p><strong>💼 Position:</strong> {emp[3]}</p>
                                </div>
                                """, unsafe_allow_html=True)
            
            with tab2:
                # List View with Expandable Details
                for emp in filtered_data:
                    with st.expander(f"🔍 Record #{emp[0]} - {emp[1]}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 👤 Employee Information")
                            st.markdown(f"""
                            - **ID:** {emp[0]}
                            - **Name:** {emp[1]}
                            - **Email:** {emp[2]}
                            - **Position:** {emp[3]}
                            """)
                        
                        with col2:
                            st.markdown("#### 📝 Stored Text Analysis")
                            text_length = len(emp[4])
                            words = len(emp[4].split())
                            st.markdown(f"""
                            - **Text Length:** {text_length} characters
                            - **Word Count:** {words} words
                            - **Text Preview:**
                            """)
                            st.code(emp[4][:100] + "..." if len(emp[4]) > 100 else emp[4])

            # 5. Statistics and Analytics
            st.markdown("### 📊 Statistics and Analytics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Position Distribution")
                position_counts = pd.DataFrame(filtered_data).groupby(3).size()
                st.bar_chart(position_counts)
            
            with col2:
                st.markdown("#### 📊 Message Length Distribution")
                message_lengths = [len(emp[4]) for emp in filtered_data]
                
                # Tạo DataFrame với cột rõ ràng
                df_lengths = pd.DataFrame({
                    'Length': message_lengths
                })
                
                # Tạo histogram đơn giản
                fig = px.histogram(
                    df_lengths, 
                    x='Length',
                    nbins=20,
                    title='Distribution of Message Lengths',
                    labels={'Length': 'Message Length (characters)', 'count': 'Frequency'},
                    color_discrete_sequence=['#4CAF50']  # Màu xanh lá cho thanh histogram
                )
                
                # Cập nhật layout
                fig.update_layout(
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',  # Nền trong suốt
                    paper_bgcolor='rgba(0,0,0,0)',  # Nền ngoài trong suốt
                    margin=dict(t=30, b=0, l=0, r=0),  # Điều chỉnh margin
                    xaxis=dict(
                        gridcolor='rgba(128,128,128,0.2)',  # Màu lưới nhạt
                        zerolinecolor='rgba(128,128,128,0.2)'
                    ),
                    yaxis=dict(
                        gridcolor='rgba(128,128,128,0.2)',
                        zerolinecolor='rgba(128,128,128,0.2)'
                    )
                )
                
                # Hiển thị biểu đồ
                st.plotly_chart(fig, use_container_width=True)

            # 6. Export Options
            st.markdown("### 💾 Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Export to CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="database_records.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📊 Export to Excel"):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Records', index=False)
                    st.download_button(
                        label="Download Excel",
                        data=output.getvalue(),
                        file_name="database_records.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

if __name__ == "__main__":
    main()