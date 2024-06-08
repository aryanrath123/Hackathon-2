import streamlit as st
from PIL import Image
import os

# Initialize session state for dogs if it doesn't exist
if 'dogs' not in st.session_state:
    st.session_state.dogs = []

def add_dog(name, breed, address, age, photo):
    # Save the uploaded photo
    if photo is not None:
        img = Image.open(photo)
        img_path = f"dog_photos/{name}_{len(st.session_state.dogs)}.png"
        img.save(img_path)
        
        st.session_state.dogs.append({
            'name': name,
            'breed': breed,
            'address': address,
            'age': age,
            'photo': img_path
        })
        return True
    return False

def main():
    st.set_page_config(page_title="Dog Adoption Website", layout="wide")
    
    # Create a directory to store dog photos if it doesn't exist
    os.makedirs("dog_photos", exist_ok=True)
    
    st.title("Dog Adoption Website")
    
    # Sidebar for adding new dogs
    st.sidebar.header("Add a New Dog")
    name = st.sidebar.text_input("Dog's Name")
    breed = st.sidebar.text_input("Dog's Breed")
    address = st.sidebar.text_input("Dog's Address")
    age = st.sidebar.number_input("Dog's Age (in years)", min_value=0, max_value=20, step=1)
    photo = st.sidebar.file_uploader("Upload Dog's Photo", type=["jpg", "jpeg", "png"])
    
    if st.sidebar.button("Add Dog"):
        if name and breed and address and photo:
            if add_dog(name, breed, address, age, photo):
                st.sidebar.success("Dog added successfully!")
            else:
                st.sidebar.error("Failed to add dog. Please try again.")
        else:
            st.sidebar.error("Please fill in all fields and upload a photo.")
    
    # Display dogs
    st.header("Dogs Available for Adoption")
    
    # Create a grid to display dogs
    cols = st.columns(3)
    for idx, dog in enumerate(st.session_state.dogs):
        with cols[idx % 3]:
            st.subheader(dog['name'])
            image = Image.open(dog['photo'])
            st.image(image, use_column_width=True)
            st.write(f"Breed: {dog['breed']}")
            st.write(f"Age: {dog['age']} years")
            st.write(f"Address: {dog['address']}")
            if st.button("Adopt", key=f"adopt_{idx}"):
                st.success(f"Thank you for adopting {dog['name']}!")
                os.remove(dog['photo'])  # Remove the dog's photo
                st.session_state.dogs.pop(idx)
                st.experimental_rerun()

if __name__ == "__main__":
    main()