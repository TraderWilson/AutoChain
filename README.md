# AutoChain Project

<img src='https://github.com/TraderWilson/AutoChain/blob/main/Image/blockchain_title.jpeg' width="1000" height="400">

## Background
The integration of blockchain technology is revolutionizing the vehicle registration process, shifting the primary method from traditional paperwork and centralized databases to digital platforms. Blockchain uses a decentralized ledger to record and store car registration data, ensuring that all records are transparent, tamper-proof, and easily accessible to authorized parties. Smart contracts automate the registration process by verifying and transferring ownership instantly upon fulfillment of pre-defined conditions, reducing the need for intermediaries and speeding up the process. Car registrations are issued as digital certificates on the blockchain, which are cryptographically secured, making them resistant to forgery and fraud. The immutable nature of blockchain ensures that once a registration record is added, it cannot be altered or deleted, maintaining the integrity and accuracy of vehicle ownership history. This technology also reduces costs by eliminating intermediaries and administrative overhead, streamlines the registration process, and enhances security. Blockchain facilitates interoperability between different jurisdictions, making it easier to manage car registrations across borders.

At a high level, the system consists of three main components: `CarRegister.sol`, `TitleTransfer.sol`, and `AutoChain.py`. `CarRegister.sol` defines a smart contract for managing car registrations, including events for registering cars, transferring titles, updating ownership, and looking up car information. TitleTransfer.sol handles the initiation and completion of title transfers. `AutoChain.py` integrates with the Pinata cloud API for IPFS file hosting, connects Python with Solidity, and sets up the user interface using Streamlit. Together, these components form a cohesive system for secure, transparent, and efficient car registration and title management on the blockchain.

## Objective
Create and demonstrate a car registration system that utilizes blockchain technology.

## Hypothesis
Creating a car registration system on the blockchain forms a cohesive system for secure, transparent, and efficient car registration and title management.

## How to Run the Project

**1. [CarRegister.sol](CarRegister.sol)**

   - Car Class: Defines the structure and properties of a car, including `VIN`, `make`, `model`, and owner details.
      ```solidity
    struct Car {
        address payable owner;
        string make;
        string model;
        uint16 year;
        string plate_number;
        string vin;
        string imageHash; // Added field for image IPFS hash
    }

    struct OwnershipHistory {
        address owner;
        uint256 timestamp;
    }
   - Events: Emits `events` for car registration and title transfer, ensuring transparency and traceability.
     ```solidity
    event CarRegistered(
        string indexed vin,
        address indexed owner, 
        string make, 
        string model, 
        uint16 year, 
        string plate_number,
        string imageHash // Added imageHash to the event
    );

    event UpdateCarOwner(
        string indexed vin,
        address indexed old_owner,
        address indexed new_owner
    );
   - Car Lookup: Provides functions to retrieve car details using the `VIN`.
    
**2. [TitleTransfer.sol](TitleTransfer.sol)**

   - Initiate Transfer: Starts the title transfer process by inputting the car's `VIN` and the new owner's details.
     ```solidity
    function initiateTransfer (
        string memory _vin, 
        address payable _seller, 
        address payable _buyer, 
        uint256 _price, 
        uint256 _transferTimestamp,
        address carRegistryAddress
    ) public onlyCarOwner(_vin, carRegistryAddress) {

        totalTransferRequests++;

        transferRequests[totalTransferRequests] = TransferRequest(
            _vin, 
            _seller, 
            _buyer, 
            _price, 
            _transferTimestamp, 
            false
        );

        CarRegistry carRegistry = CarRegistry(payable(carRegistryAddress));

        carRegistry.updateCarOwner(_vin, _buyer);

        emit TransferInitiated(totalTransferRequests, _vin, _seller, _buyer, _price, _transferTimestamp);
    }   

**3. [AutoChain.py](AutoChain.py)**

   - IPFS File Hosting: Sets up Pinata cloud API to store car registration documents on IPFS.
     ```python
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
   - Blockchain Connection: Uses `web3.py` to interact with deployed Solidity contracts from Python.
     ```python
    from web3 import Web3
    # Initialize Web3 with Ganache endpoint
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
   - User Interface: Implements a Streamlit interface for easy interaction with the blockchain, allowing users to register cars, initiate and complete title transfers, and look up car information.

## Conclusion

Overall, blockchain brings transparency, fraud prevention, streamlined transfers, cost savings, global standardization, and improved record-keeping to the vehicle registration process, modernizing it for the digital age.

## Credits
https://ethereum.org/en/developers/docs/
https://remix-ide.readthedocs.io/en/latest/
https://docs.soliditylang.org/en/v0.8.26/
https://docs.ipfs.tech/
https://docs.streamlit.io/develop
