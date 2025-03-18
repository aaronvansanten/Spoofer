import SpooferAPI as sp

def main():
    spoofer = sp.Spoofer()
    spoofer.write_collection_API_Call(file_name="test", write_as_csv=True, items_per_page=25)
    
if __name__ == "__main__":
    main()