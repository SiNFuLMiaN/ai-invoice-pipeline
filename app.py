import streamlit as st
import os
from main import ai_invoice_pipeline, prompt
import shutil
import pandas as pd
import json


def reset_memory():
    st.session_state.is_processed = False


st.set_page_config(page_title="AI Invoice Pipeline", page_icon="🤑")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display:none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if "is_processed" not in st.session_state:
    st.session_state.is_processed = False

st.title(" 🧾 AI Invoice Pipeline 🤑", anchor=False)
st.markdown(
    "UPLOAD A PDF, DOCX OR A IMAGE AND GET CLEAN EXCEL OR JSON FILE IN THE OUTPUT"
)

uploaded_files = st.file_uploader(
    "CLICK HERE TO UPLOAD YOUR FILES",
    accept_multiple_files=True,
    on_change=reset_memory,
    type=["pdf", "docx", "png", "jpg", "jpeg", "webp"],
)


if uploaded_files:
    st.info(
        f"You have Uploaded the {len(uploaded_files)} files. These files are ready to be processed"
    )

    st.divider()
    if st.button("Process Invoices", key="1"):

        temp_folder = "temp_files"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        for upload in uploaded_files:
            filepath = os.path.join(temp_folder, upload.name)

            with open(filepath, "wb") as file:
                file.write(upload.getbuffer())

        basedir = os.path.dirname(os.path.abspath(__file__))

        results_folder = os.path.join(basedir, "streamlit Results")

        # If the folder doesn't exist, tell the Operating System to build it
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        Excel_File_path = os.path.join(
            basedir, "streamlit Results", "Invoice_Report.xlsx"
        )

        Json_File_path = os.path.join(
            basedir, "streamlit Results", "Invoice_Report.json"
        )

        with st.spinner(
            "Please Wait Patiently. Longer Files May Take Longer Periods of Time"
        ):

            # json_data, excel_data = ai_invoice_pipeline(
            #     temp_folder, prompt, Json_File_path, Excel_File_path
            # )

            # If the old files from yesterday are still there, delete them so we start fresh!
            if os.path.exists(Json_File_path):
                os.remove(Json_File_path)
            if os.path.exists(Excel_File_path):
                os.remove(Excel_File_path)

            try:
                ai_invoice_pipeline(
                    temp_folder, prompt, Json_File_path, Excel_File_path
                )
                shutil.rmtree(temp_folder)
            except Exception as e:
                st.error(
                    f"Fatal error has occurred. Please Try again. The error is {e} "
                )
                shutil.rmtree(temp_folder)
                st.stop()
        # shutil.rmtree(temp_folder)
        st.session_state.is_processed = True

        # is_processed = True
    if st.session_state.is_processed:

        st.success(
            "Your files have been processed successfully. A json file and an excel file has been saved in the streamlit Results folder. Please check the folder for the results."
        )

        basedir = os.path.dirname(os.path.abspath(__file__))
        Excel_File_path = os.path.join(
            basedir, "streamlit Results", "Invoice_Report.xlsx"
        )

        Json_File_path = os.path.join(
            basedir, "streamlit Results", "Invoice_Report.json"
        )

        st.divider()
        st.subheader("📊 Extracted Financial Data")

        with open(Json_File_path, "r", encoding="utf-8") as file:
            raw_text = json.load(file)

        dataframe = pd.DataFrame(raw_text)

        # st.dataframe(dataframe, hide_index=True, use_container_width=True)

        tab1, tab2 = st.tabs(["📊 Table View", "🗂️ Raw JSON"])

        with tab1:
            st.dataframe(dataframe, hide_index=True, use_container_width=True)

        with tab2:
            st.json(raw_text)

        st.divider()

        with open(Json_File_path, "rb") as jf:
            st.download_button(
                label="📥 Download JSON File",
                data=jf,
                key="download1",
                file_name="output_data.json",
                mime="application/json",
            )

        with open(Excel_File_path, "rb") as ef:
            st.download_button(
                label="📥 Download Excel File",
                data=ef,
                key="download2",
                file_name="output_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


else:
    if st.button("Process Invoices", key="2"):
        st.error("Please Upload a file first")
