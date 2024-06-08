import streamlit as st
from PIL import Image
import os

# Custom CSS to make the app look better
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for dogs if it doesn't exist
if 'dogs' not in st.session_state:
    st.session_state.dogs = []

def add_dog(name, breed, address, age, photo):
    # Save the uploaded photo
    if photo is not None:
        img = Image.open(photo)
        img_path = f"dog_photos/{name}_{len(st.session_state.dogs)}.png"
        os.makedirs("dog_photos", exist_ok=True)
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
    st.set_page_config(page_title="Paws & Purrs Adoption", layout="wide")
    local_css("style.css")
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>🐾 Paws & Purrs Adoption 🐶</h1>
            <p>Find your new best friend today!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # About Us section
    st.markdown("""
        <div class="about-us">
            <h2>About Us</h2>
            <p>At Paws & Purrs, we believe every dog deserves a loving home. 
            Our mission is to connect adorable, adoptable dogs with their perfect 
            forever families. Browse our furry friends below and find your new companion!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for adding new dogs
    st.sidebar.markdown('<h2 class="sidebar-header">Add a New Dog</h2>', unsafe_allow_html=True)
    name = st.sidebar.text_input("Dog's Name")
    breed = st.sidebar.text_input("Dog's Breed")
    address = st.sidebar.text_input("Dog's Location")
    age = st.sidebar.number_input("Dog's Age (in years)", min_value=0, max_value=20, step=1)
    photo = st.sidebar.file_uploader("Upload Dog's Photo", type=["jpg", "jpeg", "png"])
    
    if st.sidebar.button("Add Dog"):
        if name and breed and address and photo:
            if add_dog(name, breed, address, age, photo):
                st.sidebar.success("🎉 Dog added successfully!")
            else:
                st.sidebar.error("😞 Failed to add dog. Please try again.")
        else:
            st.sidebar.warning("🚨 Please fill in all fields and upload a photo.")
    
    # Display dogs
    st.markdown('<h2 class="section-header">Find Your Furry Companion</h2>', unsafe_allow_html=True)
    
    # Create a grid to display dogs
    cols = st.columns(3)
    for idx, dog in enumerate(st.session_state.dogs):
        with cols[idx % 3]:
            with st.container():
                st.image(dog['photo'], caption=dog['name'], use_column_width=True)
                st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; text-align: center;">
                        <h3 style="margin-top: 10px;">{dog['name']}</h3>
                        <p><strong>Breed:</strong> {dog['breed']}</p>
                        <p><strong>Age:</strong> {dog['age']} years</p>
                        <p><strong>Location:</strong> {dog['address']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Adopt Me! 💖", key=f"adopt_{idx}"):
                    st.balloons()
                    st.success(f"🎊 Congratulations on adopting {dog['name']}! 🐶")
                    os.remove(dog['photo'])  # Remove the dog's photo
                    st.session_state.dogs.pop(idx)
                    st.experimental_rerun()
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>© 2024 Paws & Purrs Adoption. Made with 💙 for dogs and their humans.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
