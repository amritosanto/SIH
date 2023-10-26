from pymongo import MongoClient

# MongoDB Atlas connection details
cluster_uri = "mongodb+srv://amritalodh:Amritosanto0@amrito.sbi230b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster_uri)
db = client['blockchain_db']
collection = db['blocks']

def check_hash(index, provided_hash):
    # Search for the document with the given index
    document = collection.find_one({"index": index})

    if document:
        stored_hash = document.get("data_hash")
        # Compare the provided hash with the stored hash
        if provided_hash == stored_hash:
            return True
        else:
            return False
    else:
        print(f"No document found with index {index}")
        return False

def main():
    try:
        # Input index and hash
        index = int(input("Enter the index: "))
        provided_hash = input("Enter the hash to compare: ")

        result = check_hash(index, provided_hash)

        if result:
            print("Hashes match: True")
        else:
            print("Hashes do not match: False")
    except ValueError:
        print("Invalid input. Please enter a valid index as an integer.")

if __name__ == "__main__":
    main()
