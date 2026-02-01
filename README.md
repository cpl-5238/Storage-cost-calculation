# 📦 Storage vs Demurrage Cost Comparison Tool

An interactive **Streamlit** application that compares warehouse storage charges and demurrage charges based on container type, destination country, and key dates.

## 🎯 Features

- **Multi-country support**: France and United Kingdom pricing
- **Container types**: 20'dc, 40'dc, 40'hc
- **Tiered pricing**: Automatic cost calculation based on day ranges
- **Interactive UI**: Date selection and real-time cost updates
- **Currency support**: Automatic EUR (€) and GBP (£) display
- **Detailed breakdown**: Storage, detention, and demurrage cost summary

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cpl-5238/Storage-cost-calculation.git
cd Storage-cost-calculation
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install streamlit pandas numpy
```

### Run the Application

```bash
streamlit run compare_storage_vs_demurrage.py
```

The app will open at `http://localhost:8501` in your browser.

## 📊 How It Works

### Inputs (Sidebar)
- **Client**: Select client (currently Emma Matratzen Gmbh)
- **Destination Country**: Choose France or United Kingdom
- **Container Type**: Select 20'dc, 40'dc, or 40'hc
- **Dates**:
  - Discharge Date
  - Estimated Pickup (Demurrage)
  - Estimated Pickup (Storage)
  - Scheduled Storage End Date

### Outputs (Main Page)
- **Cost Metrics**: Total demurrage and storage+detention costs
- **Timeline**: Summary of all key dates and calculated days
- **Cost Breakdown**: Itemized costs by category

### Pricing Tiers

#### France
- **Demurrage**: Days 1-7 free, then tiered rates for 8-10, 11-20, 21+
- **Detention**: Days 1-10 free, then tiered rates for 11-14, 15-24, 25+
- **Storage**: €50/day per container
- **Base**: €325 delivery + 7% fuel + €200 handling

#### United Kingdom
- **Demurrage**: Days 1-6 free, then tiered rates for 7-12, 13-22, 23+
- **Detention**: Days 1-6 free, then tiered rates for 7-12, 13-22, 23+
- **Storage**: £30/day per container
- **Base**: £175 delivery + £70 handling

## 📝 Example Usage

1. Select **France** as destination
2. Choose **40'dc** container
3. Set dates:
   - Discharge: Feb 1
   - Demurrage Pickup: Feb 10
   - Storage Pickup: Feb 15
   - Storage End: Mar 15
4. View calculated costs instantly

## 🔧 Customization

To add new countries or modify pricing, edit the `pricing_data` dictionary in the script:

```python
pricing_data = {
    'New Country': {
        'storage_rate': 50.0,
        'delivery_to_storage': 325.0,
        'fuel_percentage': 7,
        'handling_in_out': 200.0,
        'demurrage': {...},
        'detention': {...}
    }
}
```

## 📦 Dependencies

- **streamlit** - Web UI framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing

## 📄 License

This project is open source. Feel free to use and modify.

## 👤 Author

Created for Emma Matratzen Gmbh

---

**Questions?** Open an issue or contact the repository owner.
```bash
python3 matlab_like_app.py
```

### Run General Streamlit App
```bash
streamlit run streamlit_app.py
```

## 📦 Dependencies

- `streamlit` - Web framework for data applications
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing library

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created by C. Ahossain

## 📧 Contact

For questions or suggestions, please reach out.

