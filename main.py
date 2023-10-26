import os
import hashlib
from pymongo import MongoClient

# MongoDB Atlas connection details
cluster1_uri = "mongodb+srv://amritalodh:Amritosanto0@amrito.sbi230b.mongodb.net/?retryWrites=true&w=majority"
client1 = MongoClient(cluster1_uri)
db1 = client1['blockchain_db']
collection1 = db1['blocks']
certificate_db = client1['certificate_db']
certificate_collection = certificate_db['certificates']

class Block:
    def __init__(self, previous_hash, data_hash, current_hash):
        self.previous_hash = previous_hash
        self.data_hash = data_hash
        self.current_hash = current_hash

def create_genesis_block():
    # Genesis block has a previous hash of 0
    return Block("0", calculate_hash("Genesis Block"), calculate_hash("0" + calculate_hash("Genesis Block")))

def get_last_document(collection):
    try:
        # Find the last document without sorting
        last_document = collection.find_one(sort=[("_id", -1)])

        if last_document:
            return last_document  # Return the last document
        else:
            return None  # No documents found in the collection
    except Exception as e:
        print(f"Error: {str(e)}")
    return None

def calculate_hash(data):
    if isinstance(data, str):
        # If the data is a text string, encode it as bytes before hashing
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def create_new_block(previous_block, file_path):
    previous_hash = previous_block.current_hash

    # Read the file content and calculate its hash
    with open(file_path, 'rb') as file:
        file_data = file.read()
        data_hash = calculate_hash(file_data)

    # Combine the previous data hash and file hash to create the new block's data hash
    current_hash = calculate_hash(previous_block.current_hash + data_hash)

    # Create a new block
    new_block = Block(previous_hash, data_hash, current_hash)

    return new_block

def add_block_to_chain(new_block, collection, index):
    result = collection.insert_one({
        "index": index,
        "previous_hash": new_block.previous_hash,
        "current_hash": new_block.current_hash,
        "data_hash": new_block.data_hash
    })
    return result.inserted_id

def main():
    last_document = get_last_document(collection1)

    if last_document and "data_hash" in last_document:
        previous_block = Block(last_document["previous_hash"], last_document["data_hash"], last_document["current_hash"])
        index = last_document["index"] + 1
    else:
        # If there are no documents in the collection or if 'data_hash' is not present, create a genesis block
        previous_block = create_genesis_block()
        index = 0

    # Specify the folder where files are located (e.g., "temp_uploads")
    folder_path = "temp_uploads"

    # Loop through files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Create a new block with the file
        new_block = create_new_block(previous_block, file_path)

        # Store the new block in MongoDB
        inserted_id = add_block_to_chain(new_block, collection1, index)

        # Update the previous block with the new block
        previous_block = new_block
        index += 1

if __name__ == "__main__":
    main()
