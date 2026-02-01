import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Storage vs Demurrage Cost Comparison", layout="wide")

# Title
st.title("📦 Storage vs Demurrage Cost Comparison")
st.markdown("Compare warehouse storage charges and demurrage charges based on key dates")

# ==================== PRICING DATA ====================
pricing_data = {
    'France': {
        'storage_rate': 50.0,  # EUR per container per day
        'delivery_to_storage': 325.0,  # EUR per container
        'fuel_percentage': 7,  # % of delivery
        'handling_in_out': 200.0,  # EUR per container
        'demurrage': {
            '20\'dc': {
                'Day 1-7': 0,
                'Day 8-10': 83,
                'Day 11-20': 138,
                'Day 21+': 159
            },
            '40\'dc': {
                'Day 1-7': 0,
                'Day 8-10': 135,
                'Day 11-20': 200,
                'Day 21+': 260
            },
            '40\'hc': {
                'Day 1-7': 0,
                'Day 8-10': 135,
                'Day 11-20': 200,
                'Day 21+': 260
            }
        },
        'detention': {
            '20\'dc': {
                'Day 1-10': 0,
                'Day 11-14': 72,
                'Day 15-24': 108,
                'Day 25+': 126
            },
            '40\'dc': {
                'Day 1-10': 0,
                'Day 11-14': 118,
                'Day 15-24': 180,
                'Day 25+': 243
            },
            '40\'hc': {
                'Day 1-10': 0,
                'Day 11-14': 118,
                'Day 15-24': 180,
                'Day 25+': 243
            }
        }
    },
    'United Kingdom': {
        'storage_rate': 30.0,  # GBP per container per day
        'delivery_to_storage': 175.0,  # GBP per container
        'fuel_percentage': 0,  # No fuel percentage for UK
        'handling_in_out': 70.0,  # GBP per container and move
        'demurrage': {
            '20\'dc': {
                'Day 1-6': 0,
                'Day 7-12': 69,
                'Day 13-22': 110,
                'Day 23+': 166
            },
            '40\'dc': {
                'Day 1-6': 0,
                'Day 7-12': 138,
                'Day 13-22': 221,
                'Day 23+': 304
            },
            '40\'hc': {
                'Day 1-6': 0,
                'Day 7-12': 138,
                'Day 13-22': 221,
                'Day 23+': 304
            }
        },
        'detention': {
            '20\'dc': {
                'Day 1-6': 0,
                'Day 7-12': 76,
                'Day 13-22': 83,
                'Day 23+': 110
            },
            '40\'dc': {
                'Day 1-6': 0,
                'Day 7-12': 90,
                'Day 13-22': 97,
                'Day 23+': 124
            },
            '40\'hc': {
                'Day 1-6': 0,
                'Day 7-12': 90,
                'Day 13-22': 97,
                'Day 23+': 124
            }
        }
    }
}

# Sidebar for inputs
st.sidebar.header("⚙️ Configuration")

# Client selection
client = st.sidebar.selectbox("Select Client", ["Emma Matratzen Gmbh"])

# Destination country
destination_country = st.sidebar.selectbox("Destination Country", list(pricing_data.keys()))

# Container type
container_type = st.sidebar.selectbox("Container Type", ["20'dc", "40'dc", "40'hc"])

# Get date inputs
discharge_date = st.sidebar.date_input("Discharge Date", value=datetime.today())
demurrage_pickup_date = st.sidebar.date_input("Estimated Pickup (Demurrage)", value=datetime.today() + timedelta(days=5))
storage_pickup_date = st.sidebar.date_input("Estimated Pickup (Storage)", value=datetime.today() + timedelta(days=10))
storage_end_date = st.sidebar.date_input("Scheduled Storage End Date", value=datetime.today() + timedelta(days=35))

# Validate dates
if demurrage_pickup_date <= discharge_date:
    st.sidebar.error("❌ Estimated Pickup (Demurrage) must be after Discharge Date")
    st.stop()

if storage_end_date <= storage_pickup_date:
    st.sidebar.error("❌ Scheduled Storage End Date must be after Estimated Pickup (Storage)")
    st.stop()

# ==================== CALCULATIONS ====================
pricing = pricing_data[destination_country]

# Calculate days
demurrage_days = (demurrage_pickup_date - discharge_date).days  # Discharge to Estimated Pickup (Demurrage)
detention_storage_days = (storage_end_date - storage_pickup_date).days  # Estimated Pickup (Storage) to Scheduled Storage End

# Get costs based on day ranges
def get_demurrage_cost(days, container_type, pricing, destination):
    """Calculate demurrage cost based on day ranges"""
    demurrage_rates = pricing['demurrage'][container_type]
    
    if destination == 'France':
        # France: Days 1-7 free, 8-10, 11-20, 21+
        if days <= 7:
            return days * demurrage_rates['Day 1-7']
        elif days <= 10:
            return (days - 7) * demurrage_rates['Day 8-10']
        elif days <= 20:
            cost = 3 * demurrage_rates['Day 8-10']
            cost += (days - 10) * demurrage_rates['Day 11-20']
            return cost
        else:
            cost = 3 * demurrage_rates['Day 8-10']
            cost += 10 * demurrage_rates['Day 11-20']
            cost += (days - 20) * demurrage_rates['Day 21+']
            return cost
    else:  # United Kingdom
        # UK: Days 1-6 free, 7-12, 13-22, 23+
        if days <= 6:
            return days * demurrage_rates['Day 1-6']
        elif days <= 12:
            return (days - 6) * demurrage_rates['Day 7-12']
        elif days <= 22:
            cost = 6 * demurrage_rates['Day 7-12']
            cost += (days - 12) * demurrage_rates['Day 13-22']
            return cost
        else:
            cost = 6 * demurrage_rates['Day 7-12']
            cost += 10 * demurrage_rates['Day 13-22']
            cost += (days - 22) * demurrage_rates['Day 23+']
            return cost

# Calculate total demurrage cost
total_demurrage = get_demurrage_cost(demurrage_days, container_type, pricing, destination_country)

# Function to calculate detention cost based on day ranges
def get_detention_cost(days, container_type, pricing, destination):
    """Calculate detention cost based on day ranges"""
    detention_rates = pricing['detention'][container_type]
    
    if destination == 'France':
        # France: Days 1-10 free, 11-14, 15-24, 25+
        if days <= 10:
            return days * detention_rates['Day 1-10']  # All days free (0)
        elif days <= 14:
            # Days 1-10 free, days 11-14 charged
            cost = 10 * detention_rates['Day 1-10']  # Days 1-10 (free)
            cost += (days - 10) * detention_rates['Day 11-14']  # Days 11-14+
            return cost
        elif days <= 24:
            # Days 1-10 free, days 11-14 at one rate, 15-24 at another
            cost = 10 * detention_rates['Day 1-10']  # Days 1-10 (free)
            cost += 4 * detention_rates['Day 11-14']  # Days 11-14 (4 days)
            cost += (days - 14) * detention_rates['Day 15-24']  # Days 15-24+
            return cost
        else:  # days > 24
            # Days 1-10 free, days 11-14, 15-24, 25+ at different rates
            cost = 10 * detention_rates['Day 1-10']  # Days 1-10 (free)
            cost += 4 * detention_rates['Day 11-14']  # Days 11-14 (4 days)
            cost += 10 * detention_rates['Day 15-24']  # Days 15-24 (10 days)
            cost += (days - 24) * detention_rates['Day 25+']  # Days 25+
            return cost
    else:  # United Kingdom
        # UK: Days 1-6 free, 7-12, 13-22, 23+
        if days <= 6:
            return days * detention_rates['Day 1-6']  # All days free (0)
        elif days <= 12:
            # Days 1-6 free, days 7-12 charged
            cost = 6 * detention_rates['Day 1-6']  # Days 1-6 (free)
            cost += (days - 6) * detention_rates['Day 7-12']  # Days 7-12+
            return cost
        elif days <= 22:
            # Days 1-6 free, days 7-12, 13-22
            cost = 6 * detention_rates['Day 1-6']  # Days 1-6 (free)
            cost += 6 * detention_rates['Day 7-12']  # Days 7-12 (6 days)
            cost += (days - 12) * detention_rates['Day 13-22']  # Days 13-22+
            return cost
        else:  # days > 22
            # Days 1-6 free, days 7-12, 13-22, 23+ at different rates
            cost = 6 * detention_rates['Day 1-6']  # Days 1-6 (free)
            cost += 6 * detention_rates['Day 7-12']  # Days 7-12 (6 days)
            cost += 10 * detention_rates['Day 13-22']  # Days 13-22 (10 days)
            cost += (days - 22) * detention_rates['Day 23+']  # Days 23+
            return cost

# Calculate storage costs (includes detention + daily storage rate)
fuel_cost = (pricing['delivery_to_storage'] * pricing['fuel_percentage']) / 100
storage_base_cost = pricing['delivery_to_storage'] + fuel_cost + pricing['handling_in_out']

# Calculate detention cost based on storage days
detention_cost = get_detention_cost(detention_storage_days, container_type, pricing, destination_country)

# Add daily storage cost from pickup to storage end
daily_storage_cost = detention_storage_days * pricing['storage_rate']

# Total storage + detention cost
total_storage_detention = storage_base_cost + detention_cost + daily_storage_cost

# Get currency symbol
currency_symbol = "€" if destination_country == "France" else "£"

# ==================== DISPLAY ====================
tab1 = st.tabs(["Summary"])[0]

# ==================== TAB 1: COMPARISON ====================
with tab1:
    st.subheader("Cost Comparison Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Demurrage Cost", f"{currency_symbol}{total_demurrage:,.2f}", f"{demurrage_days} days")
    
    with col2:
        st.metric("Total Storage + Detention Cost", f"{currency_symbol}{total_storage_detention:,.2f}", f"{detention_storage_days} days")
    
# ==================== SUMMARY SECTION ====================
st.markdown("---")

# General Information & Timeline
col1, col2 = st.columns(2)

with col1:
    st.markdown("### General Information")
    st.markdown(f"""
    - **Client**: {client}
    - **Destination Country**: {destination_country}
    - **Container Type**: {container_type}
    """)

with col2:
    st.markdown("### Timeline")
    st.markdown(f"""
    - **Discharge Date**: {discharge_date.strftime('%B %d, %Y')}
    - **Estimated Pickup (Demurrage)**: {demurrage_pickup_date.strftime('%B %d, %Y')}
    - **Estimated Pickup (Storage)**: {storage_pickup_date.strftime('%B %d, %Y')}
    - **Scheduled Storage End Date**: {storage_end_date.strftime('%B %d, %Y')}
    - **Demurrage Days**: {demurrage_days} days
    - **Storage + Detention Days**: {detention_storage_days} days
    """)

st.markdown("---")

# Cost summary
st.markdown("### Cost Summary")
col1, col2 = st.columns(2)

if destination_country == 'France':
    with col1:
        st.markdown(f"""
        **Storage Charges (One-time)**
        - Delivery to Storage: {currency_symbol}{pricing['delivery_to_storage']:.2f}
        - Fuel Surcharge (7%): {currency_symbol}{fuel_cost:.2f}
        - Handling In/Out: {currency_symbol}{pricing['handling_in_out']:.2f}
        - Base Storage Cost: {currency_symbol}{storage_base_cost:.2f}
        
        **Daily Storage** (from Pickup to Storage End)
        - Days: {detention_storage_days}
        - Daily Rate: {currency_symbol}{pricing['storage_rate']:.2f}
        - Storage Cost: {currency_symbol}{daily_storage_cost:.2f}
        
        **Detention Charges** (Tiered by days)
        - Days 1-10: Free
        - Days 11-14: {currency_symbol}{pricing['detention'][container_type]['Day 11-14']}
        - Days 15-24: {currency_symbol}{pricing['detention'][container_type]['Day 15-24']}
        - Days 25+: {currency_symbol}{pricing['detention'][container_type]['Day 25+']}
        - Detention Cost: {currency_symbol}{detention_cost:.2f}
        
        - **Total Storage + Detention: {currency_symbol}{total_storage_detention:.2f}**
        """)

    with col2:
        st.markdown(f"""
        **Demurrage Charges**
        - Days: {demurrage_days}
        - Container Type: {container_type}
        - Applicable Rates:
          - Days 1-7: Free
          - Days 8-10: {currency_symbol}{pricing['demurrage'][container_type]['Day 8-10']}
          - Days 11-20: {currency_symbol}{pricing['demurrage'][container_type]['Day 11-20']}
          - Days 21+: {currency_symbol}{pricing['demurrage'][container_type]['Day 21+']}
        - **Total: {currency_symbol}{total_demurrage:.2f}**
        """)
else:  # United Kingdom
    with col1:
        st.markdown(f"""
        **Storage Charges (One-time)**
        - Delivery to Storage: {currency_symbol}{pricing['delivery_to_storage']:.2f}
        - Handling In/Out: {currency_symbol}{pricing['handling_in_out']:.2f}
        - Base Storage Cost: {currency_symbol}{storage_base_cost:.2f}
        
        **Daily Storage** (from Pickup to Storage End)
        - Days: {detention_storage_days}
        - Daily Rate: {currency_symbol}{pricing['storage_rate']:.2f}
        - Storage Cost: {currency_symbol}{daily_storage_cost:.2f}
        
        **Detention Charges** (Tiered by days)
        - Days 1-6: Free
        - Days 7-12: {currency_symbol}{pricing['detention'][container_type]['Day 7-12']}
        - Days 13-22: {currency_symbol}{pricing['detention'][container_type]['Day 13-22']}
        - Days 23+: {currency_symbol}{pricing['detention'][container_type]['Day 23+']}
        - Detention Cost: {currency_symbol}{detention_cost:.2f}
        
        - **Total Storage + Detention: {currency_symbol}{total_storage_detention:.2f}**
        """)

    with col2:
        st.markdown(f"""
        **Demurrage Charges**
        - Days: {demurrage_days}
        - Container Type: {container_type}
        - Applicable Rates:
          - Days 1-6: Free
          - Days 7-12: {currency_symbol}{pricing['demurrage'][container_type]['Day 7-12']}
          - Days 13-22: {currency_symbol}{pricing['demurrage'][container_type]['Day 13-22']}
          - Days 23+: {currency_symbol}{pricing['demurrage'][container_type]['Day 23+']}
        - **Total: {currency_symbol}{total_demurrage:.2f}**
        """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Storage vs Demurrage Cost Comparison Tool | Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)
