import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta
from config import API_BASE_URL

def show():
    if "user" not in st.session_state:
        st.error("Please log in to view detailed reports.")
        return

    user_id = st.session_state["user"]["id"]

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Analysis Filters")
    date_input = st.sidebar.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=60), datetime.now()),
        key="report_date_filter"
    )

    try:
        # Fetch Data
        exp_res = requests.get(f"{API_BASE_URL}/reports/expenses/{user_id}")
        bud_res = requests.get(f"{API_BASE_URL}/budgets/{user_id}")
        
        if exp_res.status_code == 200:
            exp_data = exp_res.json()
            bud_data = bud_res.json() if bud_res.status_code == 200 else []
            
            if not exp_data:
                st.info("No data found. Start by adding some expenses! 💸")
                return
            
            # --- DATA PREPARATION ---
            df = pd.DataFrame(exp_data)
            df.columns = [c.lower() for c in df.columns]
            df = df.rename(columns={'description': 'note', 'category_name': 'category name'})
            df['date'] = pd.to_datetime(df['date']).dt.date

            # Filter by Date
            if isinstance(date_input, tuple) and len(date_input) == 2:
                start_date, end_date = date_input
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

            budget_map = {b['category_id']: b['amount'] for b in bud_data}

            # --- HEADER & SUMMARY ---
            st.title("🏆 Financial Intelligence")
            
            total_spent = df['amount'].sum()
            total_budget = sum(budget_map.values())
            
            analysis_df = df.groupby(['category_id', 'category name'])['amount'].sum().reset_index()
            total_overspent = sum(max(0, row['amount'] - budget_map.get(row['category_id'], 0)) for _, row in analysis_df.iterrows())
            
            s1, s2, s3 = st.columns(3)
            s1.metric("Total Spent", f"${total_spent:,.2f}")
            s2.metric("Total Budget", f"${total_budget:,.2f}")
            s3.metric("Overspent", f"${total_overspent:,.2f}", 
                      delta=f"-${total_overspent:,.2f}" if total_overspent > 0 else None, 
                      delta_color="inverse")

            # --- BUDGET TRACKING ---
            st.divider()
            st.subheader("🎯 Budget Tracking")
            for _, row in analysis_df.iterrows():
                limit = budget_map.get(row['category_id'], 0)
                spent = row['amount']
                col_m, col_p = st.columns([0.3, 0.7])
                
                with col_m:
                    if limit > 0:
                        remaining = limit - spent
                        st.metric(row['category name'], f"${spent:,.2f}", 
                                  delta=f"${remaining:,.2f} left", 
                                  delta_color="normal" if remaining >= 0 else "inverse")
                    else:
                        # FIXED THE SYNTAX ERROR HERE
                        st.metric(row['category name'], f"${spent:,.2f}", delta="No budget")

                with col_p:
                    if limit > 0:
                        percent = spent / limit
                        st.progress(min(percent, 1.0))
                        if percent > 1.0:
                            st.warning(f"⚠️ {((percent-1)*100):,.0f}% Over Limit!")

            # --- VISUALS ---
            st.divider()
            c1, c2 = st.columns(2)
            
            # --- BLUE & GREEN PALETTE ---
            finance_colors = ['#008080', '#2E8B57', '#4682B4', '#3CB371', '#00ced1']

            with c1:
                fig_pie = px.pie(df, values='amount', names='category name', hole=0.5, 
                                 title="Spending Distribution",
                                 color_discrete_sequence=finance_colors)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with c2:
                st.subheader("📈 Spending Momentum")
                df_trend = df.groupby(['date', 'category name'])['amount'].sum().reset_index()
                
                fig_bar = px.bar(
                    df_trend, 
                    x='date', 
                    y='amount', 
                    color='category name',
                    title="Daily Spending Flow",
                    barmode='stack',
                    color_discrete_sequence=finance_colors
                )
                
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Date",
                    yaxis_title="Spent ($)",
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # --- DATA TABLE & CSV EXPORT ---
            st.divider()
            col_t, col_btn = st.columns([0.8, 0.2])
            with col_t:
                st.subheader("📊 Transaction Log")
            
            with col_btn:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Save CSV",
                    data=csv,
                    file_name=f"finance_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )

            st.dataframe(df.sort_values('date', ascending=False), hide_index=True, use_container_width=True)

            # --- MANAGE ---
            st.divider()
            st.subheader("⚙️ Manage")
            for _, row in df.sort_values('date', ascending=False).iterrows():
                c_info, c_del = st.columns([0.85, 0.15])
                with c_info:
                    st.write(f"**{row['date']}** | {row.get('category name', 'N/A')} | **${row['amount']:.2f}**")
                with c_del:
                    if st.button("Delete", key=f"del_exp_{row['id']}"):
                        requests.delete(f"{API_BASE_URL}/expenses/{row['id']}?user_id={user_id}")
                        st.rerun()

        else:
            st.error(f"Backend Error: {exp_res.status_code}")
    except Exception as e:
        st.error(f"UI Error: {e}")