import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(
    page_title=" Superstore Sales Dashboard",
    layout="wide"
    )

df = pd.read_csv('data/superstore.csv')
df["Order Date"] = pd.to_datetime(df["Order Date"])

st.sidebar.title("Dashboard Menu")

page = st.sidebar.radio(
    "Go To",
    [
    "Overview", 
    "Sales Analysis",
    "Profit Analysis", 
    "Forecast Analysis" ,
    "Customer Segmentation", 
    "Geographical Map",
    "Business Insights",
    "Conclusion"]
)

st.markdown(
    "Interactive Sales Analytics Dashboard"
)

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=list(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=list(df["Category"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

if page == "Overview":

    st.title(' Superstore Sales Dashboard')

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order ID"].nunique()

    col1, col2 , col3 = st.columns(3)

    col1.metric("Total Sales",f"${total_sales:,.2f}")
    col2.metric("Total Profit",f"${total_profit:,.2f}")
    col3.metric("Total Orders", total_orders)
        
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_sales_data.csv",
         mime="text/csv"
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1 = px.bar(
            filtered_df,
            x="Category",
            y="Sales",
            color="Category",
            title="Sales by category"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        fig2 = px.pie(
            filtered_df,
            names="Region",
            values="Sales",     
            title="Sales by Region"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Monthly Sales Trend")

        monthly_sales = filtered_df.groupby(
        filtered_df["Order Date"].dt.strftime("%b")
        )["Sales"].sum().reset_index()

        fig3 = px.line(
           monthly_sales,
           x="Order Date",
           y="Sales",
           markers=True,
           title="Monthly Sales Trend"
        )
        st.plotly_chart(fig3, use_container_width=True)

elif page == "Sales Analysis":

      st.title("Sales Analysis")

      col1, col2 = st.columns(2)

      with col1:

        sales_category = filtered_df.groupby(
            "Category"
        )["Sales"].sum().reset_index()

        fig4 = px.bar(
            sales_category,
            x="Category",
            y="Sales",
            color="Category",
            title="Sales by Category"
        )

        st.plotly_chart(fig4, use_container_width=True)

        with col2:
            subcategory_sales = filtered_df.groupby(
                "Sub-Category"
            )["Sales"].sum().reset_index()

            fig5 = px.bar(
                subcategory_sales,
                x="Sub-Category",
                y="Sales",
                color="Sub-Category",
                title="Sales by Sub-Category"
            )

            st.plotly_chart(fig5, use_container_width=True)

            top_products = filtered_df.groupby(
                "Product Name"
            )["Sales"].sum().reset_index()

            top_products = top_products.sort_values(
                by="Sales",
                ascending=False
            ).head(10)

            fig6 = px.bar(
                top_products,
                x="Sales",
                y="Product Name",
                orientation="h",
                color="Sales",
                title="Top 10 Products by Sales"
            )

            st.plotly_chart(fig6, use_container_width=True)

elif page == "Profit Analysis":

                st.subheader("Profit Analysis")

                col1, col2 = st.columns(2)

                with col1:

                    profit_region = filtered_df.groupby(
                        "Region"
                    )["Profit"].sum().reset_index()

                    fig7 = px.pie(
                        profit_region,
                        names="Region",
                        values="Profit",
                        title="Profit by Region"
                    )

                    st.plotly_chart(fig7, use_container_width=True)

                    with col2:

                        monthly_profit = filtered_df.groupby(
                            "Month"
                        )["Profit"].sum().reset_index()

                        fig8 = px.line(
                            monthly_profit,
                            x="Month",
                            y="Profit",
                            markers=True,
                            title="Monthly Profit Trend"
                        )

                        st.plotly_chart(fig8, use_container_width=True)

elif page == "Forecast Analysis":

                            st.subheader("Forecast Analysis")

                            monthly_forecast = filtered_df.groupby(
                                "Month"
                            )["Sales"].sum().reset_index()

                            fig9 = px.line(
                                monthly_forecast,
                                x="Month",
                                y="Sales",
                                markers=True,
                                title="forecast Sales Trend"
                            )

                            st.plotly_chart(fig9, use_container_width=True)

elif page == "Customer Segmentation":

                            st.subheader("Customer Segmentation")

                            col1, col2 = st.columns(2)

                            with col1:

                                customer_sales = filtered_df.groupby(
                                    "Segment"
                                )["Sales"].sum().reset_index()

                                fig10 = px.pie(
                                    customer_sales,
                                    names="Segment",
                                    values="Sales",
                                    title="Sales by Customer Segment"
                                )

                                st.plotly_chart(fig10, use_container_width=True)

                                with col2:

                                    customer_orders = filtered_df.groupby(
                                        "Customer Name"
                                    )["Sales"].sum().reset_index()

                                    customer_orders = customer_orders.sort_values(
                                        by="Sales",
                                        ascending=False
                                    ).head(10)

                                    fig11 = px.bar(
                                        customer_orders,
                                        x="Sales",
                                        y="Customer Name",
                                        orientation="h",
                                        color="Sales",
                                        title="Top 10 Customers"
                                    )

                                    st.plotly_chart(fig11, use_container_width=True)

elif page == "Geographical Map":

                                        st.subheader("Geographical Sales Map")

                                        state_sales = filtered_df.groupby(
                                            "State"
                                        )["Sales"].sum().reset_index()

                                        fig12 = px.bar(
                                            state_sales,
                                            x="State",
                                            y="Sales",
                                            color="Sales",
                                            title="Sales by State"
                                        )

                                        st.plotly_chart(fig12, use_container_width=True)

elif page == "Business Insights":

                                            st.subheader("Business Recommendation")

                                            st.markdown("### Key Insight")
                                            
                                            st.write("- Technology category generates the highest sales.")
                                            st.write("- Some regions perform better in profit than others.")
                                            st.write("- Certain months record higher sales trends.")
                                            st.write("- Top products contribute heavily to total revenue.")
                                            st.markdown(" ### Recommendations")
                                            st.write("- Focus marketing on high-performing regions.")
                                            st.write("- Reduce discounts on low-profit products.")
                                            st.write("- Increase inventory for best-selling items.")
                                            st.write("- Improve campaigns during low-sales periods.")
                                            
elif page == "Conclusion":

    st.subheader("Conclusion")

    st.write("This dashboard provides insights into sales,profits,regional performance, and future sales trends.")

    st.markdown(" ### Key Findings:")
    st.write("- Some region perform better than others.")
    st.write("- Technology category generates strong profits.")
    st.write("- Sales trends help predict future performance.")

    ("### Recommendation:")
    st.write("- Focus marketing on high performing products.")
    st.write("- Improve sales strategies in weaker regions.")
    st.write("- Monitor monthly trends for better forecasting.")

    st.markdown("---")
    st.caption("Developed using Streamlit and plotly")

                                            
                                    
                                        



    
     