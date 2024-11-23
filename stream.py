import streamlit as st
import io
import os
import zipfile
from fillFile import getFieldsandLines, fillAll, fillMultiple
import pandas as pd

temp_dir = "tempDir"
st.set_page_config(layout="wide", page_title="Automatic Form Filling System")
os.makedirs(temp_dir, exist_ok=True)

def create_image_zip(image_files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, image_file in enumerate(image_files):
            image_name = f"image_{idx + 1}.png"
            img_byte_arr = io.BytesIO()
            image_file.save(img_byte_arr, format="PNG")
            zip_file.writestr(image_name, img_byte_arr.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

if "page" not in st.session_state:
    st.session_state.page = "upload"

def go_to_page(page_name):
    st.session_state.page = page_name

if st.session_state.page == "upload":
    st.title("Upload Image of Form")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        save_path = os.path.join(temp_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.save_path = save_path
        st.session_state.dict1 = getFieldsandLines(save_path)
        print(st.session_state.dict1)
        if 'Error' in st.session_state.dict1:
            st.error("Template Not Supported")
        if 'Error' not in st.session_state.dict1:
            st.image(uploaded_file, caption="Form Chosen", width=600)
            if st.button("Submit"):
                st.session_state.page = "fill_page"

elif st.session_state.page == "fill_page":
    st.title("Fill Out the Form Details")

    if st.session_state.save_path:
        tab1, tab2, tab3 = st.tabs(["Fill Form", "Preview","Multiple Copies"])
        with tab1:
            user_inputs = {}
            dict1 = st.session_state.dict1
            for field in dict1.keys():
                user_input = st.text_input(f"Enter the {field}", key=field)
                if user_input:
                    user_inputs[user_input] = dict1[field]
            
            if st.button("Submit", key="submit_fill"):
                img = fillAll(st.session_state.save_path, user_inputs)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format="PNG")
                img_byte_arr.seek(0)
                st.session_state.filled_image = img_byte_arr


        with tab2:
            if "filled_image" in st.session_state:
                st.image(st.session_state.filled_image, caption="Filled Form Preview", width=600)
                st.download_button(
                    label="Download Processed Image",
                    data=st.session_state.filled_image,
                    file_name="filled_form.png",
                    mime="image/png"
                )
            else:
                st.write("No form has been filled yet. Please fill out the form first.")
        
        with tab3:
            dict1 = st.session_state.dict1
            if dict1:
                df = pd.DataFrame(columns=dict1.keys())
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()
                st.download_button(
                    label="Download CSV Template",
                    data=csv_data,
                    file_name="form_template.csv",
                    mime="text/csv"
                )
                uploaded_csv = st.file_uploader("Upload the filled CSV file", type=["csv"])
                if uploaded_csv is not None:
                    try:
                        uploaded_df = pd.read_csv(uploaded_csv)
                        st.write("Uploaded CSV Preview:")
                        st.dataframe(uploaded_df)
                        images = fillMultiple(st.session_state.save_path,uploaded_df,dict1)
                        zip_file= create_image_zip(images)
                        st.download_button(
                        label="Download ZIP",
                        data=zip_file,
                        file_name="images.zip",
                        mime="application/zip"
                    )
                    except Exception as e:
                        st.error(f"Error reading the uploaded CSV file: {e}")
            else:
                st.write("No fields available to create an Excel file.")

    else:
        st.write("No file was uploaded.")
 
    if st.button("Go Back"):
        st.session_state.page = "upload"