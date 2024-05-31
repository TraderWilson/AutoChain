#################################### Import Packages ##################################

import os
import json
import streamlit as st
import time
import pandas as pd
import pytz
import requests
import html
from datetime import datetime, timedelta
from web3 import Web3
from dotenv import load_dotenv
from web3.exceptions import ContractLogicError

#################################### Set Up Pinata ##################################

load_dotenv()

pinata_api_key = os.getenv("API_Key")
pinata_secret_api_key = os.getenv("API_Secret")

PINATA_BASE_URL = 'https://api.pinata.cloud'
UPLOAD_ENDPOINT = '/pinning/pinFileToIPFS'
HEADERS = {
    'pinata_api_key': pinata_api_key,
    'pinata_secret_api_key': pinata_secret_api_key,
}

def upload_image_to_pinata(image_file):
    if image_file is not None:
        files = {
            'file': (image_file.name, image_file.getvalue())
        }
        try:
            response = requests.post(
                PINATA_BASE_URL + UPLOAD_ENDPOINT,
                files = files,
                headers = HEADERS
            )
            if response.status_code == 200:
                st.success("Image uploaded to IPFS successfully")
                return response.json().get('IpfsHash')
            else:
                st.error(f"Failed to upload image to IPFS: {response.text}")
                return None
        except Exception as e:
            st.error(f"An error occurred while uploading the image: {str(e)}")
            return None
    else:
        st.error("No image file provided")
        return None

#################################### Set Up The Connection Between Python And Solidity ##################################

# Initialize Web3 with Ganache endpoint
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Load the contract ABI
with open('RegisterCar.json') as f:
    car_registry_abi = json.load(f)

with open('TitleTransfer.json') as t:
    title_transfer_abi = json.load(t)

# Set the contract address (this is the address of the deployed contract)
car_registry_address = '0x5B9A32Ed753604434aA86EA36934fC3350c0Ff79'
title_transfer_address = '0x2e6E7e54B265CD88b370773541c5302501D6A404'

# Contract instances
car_registry = w3.eth.contract(address = car_registry_address, abi = car_registry_abi)
title_transfer = w3.eth.contract(address = title_transfer_address, abi = title_transfer_abi)

# Initialize DataFrames in session state
# if 'owners_history_df' not in st.session_state:
#     st.session_state.owners_history_df = pd.DataFrame(columns=['VIN', 'Old Owner', 'New Owner', 'Timestamp'])

if 'registration_history_df' not in st.session_state:
    st.session_state.registration_history_df = pd.DataFrame(columns=['VIN', 'Owner', 'Make', 'Model', 'Year', 'Plate Number', 'Timestamp'])

#################################### Set Up Streamlit Interface ##################################

# Custom CSS to change the button color
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: green;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html = True
)


# Sidebar navigation
st.sidebar.title("AutoChain Project")

options = [
    "🏠 Home",
    "🚗 Register Car",
    "📜 Car Ownership History",
    "🔄 Title Transfer",
    "🔍 Get Car Details",
    "📊 Export Registration History"
]

page = st.sidebar.radio(" Navigation", options)


# Streamlit UI

# # Define the CSS for the labels
# label_css = """
# <style>
# .label {
#     font-size: 20px;
#     color: #6E69D5;
# }
# </style>
# """

# # Insert the CSS into the Streamlit app
# st.markdown(label_css, unsafe_allow_html = True)

if page == options[0]:
    st.header('''**:rainbow[Welcome to AutoChain Project.]**''')
    st.header('''**:rainbow[Use the sidebar to navigate between pages.]**''')

    # st.markdown("""
    # <p class = "big-font">Welcome to AutoChain Project.</p>
    # <p class = "big-font">Use the sidebar to navigate between pages.</p>
    # """, unsafe_allow_html = True)
    
    # st.markdown(
    #     """
    #     <style>
    #     .big-font {
    #         font-size:30px;
    #         text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.5);
    #         font-weight: bold;
    #     }
    #     .stApp {
    #     background-image: url("https://img.freepik.com/free-vector/abstract-soft-colorful-watercolor-texture-background-design-vector_1055-12127.jpg?w=1480&t=st=1716867542~exp=1716868142~hmac=56f252b2cd571fc056fe787f1b78ef0601ae5f1962521cb375da55dcc2b23d27");
    #     background-size: cover;
    #     background-repeat: no-repeat;
    #     background-position: ;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.markdown(
        """
        <style>
        .stApp{
        background-image: url("https://img.freepik.com/free-vector/abstract-soft-colorful-watercolor-texture-background-design-vector_1055-12127.jpg?w=1480&t=st=1716867542~exp=1716868142~hmac=56f252b2cd571fc056fe787f1b78ef0601ae5f1962521cb375da55dcc2b23d27");
        background-size: cover;
        background-repeat: no-repeat;}
        </style>
        """,
        unsafe_allow_html = True

    )


elif page == options[1]:
 
    st.header('''**:rainbow[Register a Car]**''')
    accounts = w3.eth.accounts
    # st.markdown('<p class="label">Select Owner</p>', unsafe_allow_html = True)
    # owner = st.selectbox("Select Owner", options = accounts, label_visibility = "collapsed")
    owner = st.selectbox("Select Owner", options = accounts)
    # st.markdown('<p class="label">Enter Your VIN</p>', unsafe_allow_html = True)
    # vin = st.text_input('Enter Your VIN', label_visibility = "collapsed")
    vin = st.text_input('Enter Your VIN')
    # st.markdown('<p class="label">Enter Your Maker</p>', unsafe_allow_html = True)
    # make = st.text_input("Enter Your Maker", label_visibility = "collapsed")
    make = st.text_input("Enter Your Maker")
    # st.markdown('<p class="label">Enter Your Model</p>', unsafe_allow_html = True)
    # model = st.text_input("Enter Your Model", label_visibility = "collapsed")
    model = st.text_input("Enter Your Model")
    # st.markdown('<p class="label">Enter Car Year</p>', unsafe_allow_html = True)
    # year = st.number_input("Enter Car's Year", min_value = 1900, max_value = datetime.now().year, step = 1, label_visibility = "collapsed")
    year = st.number_input("Enter Car's Year", min_value = 1900, max_value = datetime.now().year, step = 1)
    # st.markdown('<p class="label">Enter Plate Number</p>', unsafe_allow_html = True)
    # plate_number = st.text_input("Enter Plate Number", label_visibility = "collapsed")
    plate_number = st.text_input("Enter Plate Number")
    # st.markdown('<p class="label">Upload Car Image</p>', unsafe_allow_html = True)
    # image_file = st.file_uploader("Upload Car Image", type = ["png", "jpg", "jpeg"], label_visibility = "collapsed")
    image_file = st.file_uploader("Upload Car Image", type = ["png", "jpg", "jpeg"])
    image_hash = upload_image_to_pinata(image_file)
    
    if st.button("Register Car"):
        if image_hash is not None:
            try:
                tx_hash = car_registry.functions.registerCar(vin, make, model, year, plate_number, image_hash).transact({'from': owner})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                if receipt.status == 1:
                    st.success("Registration Successful")
                    st.write(f"Transaction Hash: {tx_hash.hex()}")
                    st.write(f"Owner Address: {owner}")
                
                    new_registration = pd.DataFrame({
                        'VIN': [vin],
                        'Owner': [owner],
                        'Make': [make],
                        'Model': [model],
                        'Year': [year],
                        'Plate Number': [plate_number],
                        'Timestamp': [datetime.now(pytz.UTC)]
                    })
                    
                    st.session_state.registration_history_df = pd.concat([st.session_state.registration_history_df, new_registration], ignore_index=True)
                    st.write("Registration History Updated")
                
                else:
                    st.error("Registration Failed")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Image upload failed, cannot register car without image hash.")

elif page == options[2]:
    st.header('''**:rainbow[Car Ownership History]**''')
    # st.markdown('<p class="label">Enter VIN</p>', unsafe_allow_html = True)
    # vin = st.text_input('Enter VIN:', label_visibility = "collapsed")
    vin = st.text_input('Enter VIN:')
    
    if st.button('Get Ownership History'):
        history = car_registry.functions.getCarOwnershipHistory(vin).call()
        if history:
            df = pd.DataFrame(history, columns = ['owner', 'timestamp'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 's')
            st.write('Ownership History for VIN:', vin)
            st.dataframe(df)
        else:
            st.write('No ownership history found for the given VIN.')

elif page == options[3]:
    st.header('''**:rainbow[Initiate Title Transfer]**''')
    # st.markdown('<p class="label">VIN for Transer</p>', unsafe_allow_html = True)
    # vin_transfer = st.text_input("VIN for Transfer", label_visibility = "collapsed")
    vin_transfer = st.text_input("VIN for Transfer")
    # st.markdown('<p class="label">Seller Address</p>', unsafe_allow_html = True)
    # seller_address = st.text_input("Seller Address", label_visibility = "collapsed")
    seller_address = st.text_input("Seller Address")
    # st.markdown('<p class="label">Buyer Address</p>', unsafe_allow_html = True)
    # buyer_address = st.text_input("Buyer Address", label_visibility = "collapsed")
    buyer_address = st.text_input("Buyer Address")
    # st.markdown('<p class="label">Price (ETH)</p>', unsafe_allow_html = True)
    # price = st.number_input("Price (ETH)", min_value = 0.0, format = "%.6f", label_visibility = "collapsed")
    price = st.number_input("Price (ETH)", min_value = 0.0, format = "%.6f")
    # st.markdown('<p class="label">Transfer Timestamp</p>', unsafe_allow_html = True)
    # transfer_timestamp = st.number_input("Transfer Timestamp", value = int(time.mktime(datetime.now().timetuple())), label_visibility = "collapsed")
    transfer_timestamp = st.number_input("Transfer Timestamp", value = int(time.mktime(datetime.now().timetuple())))
    # st.markdown('<p class="label">Car Registry Contract Address</p>', unsafe_allow_html = True)
    # registry_address = st.text_input("Car Registry Contract Address", value = car_registry_address, label_visibility = "collapsed")
    registry_address = st.text_input("Car Registry Contract Address", value = car_registry_address)
    
    if st.button("Initiate Transfer"):
        try:
            tx_hash = title_transfer.functions.initiateTransfer(
                vin_transfer,
                w3.toChecksumAddress(seller_address),
                w3.toChecksumAddress(buyer_address),
                w3.toWei(price, 'ether'),
                int(datetime.now().timestamp()),
                w3.toChecksumAddress(registry_address)
            ).transact({'from': w3.toChecksumAddress(seller_address)})
    
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
            if receipt.status == 1:
                st.success("Title Transfer Successful")
                st.write(f"Transaction Hash: {tx_hash.hex()}")
                st.write(f"New Owner Address: {buyer_address}")
                st.balloons()
            else:
                st.error("Transfer Failed")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif page == options[4]:
    st.header('''**:rainbow[Get Car Details]**''')
    # st.markdown('<p class="label">Enter VIN</p>', unsafe_allow_html = True)
    # vin = st.text_input('Enter VIN', label_visibility = "collapsed")
    vin = st.text_input('Enter VIN')
    
    if st.button('Get Car Details'):
        try:
            car_details = car_registry.functions.getCar(vin).call()
            st.write(f"Owner: {car_details[0]}")
            st.write(f"Make: {car_details[1]}")
            st.write(f"Model: {car_details[2]}")
            st.write(f"Year: {car_details[3]}")
            st.write(f"Plate Number: {car_details[4]}")
            
            image_hash = car_details[5]
            if image_hash:
                ipfs_url = f"https://ipfs.io/ipfs/{image_hash}"
                st.image(ipfs_url, caption = 'Car Image', use_column_width = True)
            else:
                st.warning("No image available for this car.")
                
        except Exception as e:
            st.error(f"Error fetching car details: {e}")

elif page == options[5]:
    st.header('''**:rainbow[Export Registration History]**''')
    st.markdown('''**:rainbow[Select the time period to export registration history.]**''')

    # This calculates a date that is 30 days before the current date and time.
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days = 30)) 
    start_time = st.time_input("Start Time", datetime.min.time())
    end_date = st.date_input("End Date", datetime.now())
    end_time = st.time_input("End Time", datetime.now().time())
    
    start_datetime = datetime.combine(start_date, start_time).replace(tzinfo = pytz.UTC)
    end_datetime = datetime.combine(end_date, end_time).replace(tzinfo = pytz.UTC)

    start_datetime = pd.Timestamp(start_datetime)
    end_datetime = pd.Timestamp(end_datetime)

    if pd.api.types.is_datetime64_any_dtype(st.session_state.registration_history_df['Timestamp']):
        if st.session_state.registration_history_df['Timestamp'].dt.tz is None:
            st.session_state.registration_history_df['Timestamp'] = st.session_state.registration_history_df['Timestamp'].dt.tz_localize(pytz.UTC)
    else:
        st.session_state.registration_history_df['Timestamp'] = pd.to_datetime(st.session_state.registration_history_df['Timestamp']).dt.tz_localize(pytz.UTC)
    
    if st.button("Export Data"):
        filtered_df = st.session_state.registration_history_df[
            (st.session_state.registration_history_df['Timestamp'] >= start_datetime) &
            (st.session_state.registration_history_df['Timestamp'] <= end_datetime)
        ]
        
        if not filtered_df.empty:
            st.write(filtered_df)
            # csv = filtered_df.to_csv(index = False).encode('utf-8')
            # st.download_button(
            #     label = "Download CSV",
            #     data = csv,
            #     file_name = 'registration_history.csv',
            #     mime = 'text/csv',
            # )
        else:
            st.write("No records found in the specified period.")
