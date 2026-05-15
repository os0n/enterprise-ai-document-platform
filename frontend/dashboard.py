import streamlit as st
import pandas as pd
import json

from auth import (
    login_user,
    register_user
)

from api_client import (
    load_documents,
    analyze_document
)


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Enterprise AI Platform",
    page_icon="📄",
    layout="wide"
)


# =========================
# SESSION STATE
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None


# =========================
# AUTH PAGE
# =========================
if not st.session_state.authenticated:

    st.markdown(
        """
        <h1 style='text-align: center;'>
        Enterprise AI Platform
        </h1>

        <p style='text-align: center;'>
        AI-powered document processing and workflow automation system.
        </p>
        """,
        unsafe_allow_html=True
    )

    login_tab, register_tab = st.tabs(
        [
            "Login",
            "Register"
        ]
    )

    # =========================
    # LOGIN TAB
    # =========================
    with login_tab:

        st.subheader("Login")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            try:

                response = login_user(
                    login_email,
                    login_password
                )

                if response.status_code == 200:

                    token = response.json()[
                        "access_token"
                    ]

                    st.session_state.access_token = token

                    st.session_state.authenticated = True

                    st.session_state.user_email = login_email

                    st.success(
                        "Login successful."
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Login failed. Status Code: {response.status_code}"
                    )

                    try:
                        st.json(response.json())

                    except Exception:
                        st.text(response.text)

            except Exception as e:

                st.error(
                    f"Connection Error: {str(e)}"
                )

    # =========================
    # REGISTER TAB
    # =========================
    with register_tab:

        st.subheader("Create Account")

        register_name = st.text_input(
            "Full Name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            try:

                response = register_user(
                    register_email,
                    register_name,
                    register_password
                )

                if response.status_code == 200:

                    st.success(
                        "Account created successfully."
                    )

                else:

                    st.error(
                        f"Registration failed. Status Code: {response.status_code}"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        st.text(
                            response.text
                        )

            except Exception as e:

                st.error(
                    f"Connection Error: {str(e)}"
                )

# =========================
# MAIN APP
# =========================
else:

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.title(
        "Enterprise AI Platform"
    )

    st.sidebar.success(
        f"Logged in as:\n{st.session_state.user_email}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Invoice",
            "Documents"
        ]
    )

    # =========================
    # LOGOUT
    # =========================
    if st.sidebar.button("Logout"):

        st.session_state.authenticated = False

        st.session_state.access_token = None

        st.session_state.user_email = None

        st.rerun()

    # =========================
    # LOAD DOCUMENTS
    # =========================
    documents = []

    try:

        response = load_documents(
            st.session_state.access_token
        )

        if response.status_code == 200:

            documents = response.json().get(
                "documents",
                []
            )

    except Exception as e:

        st.error(
            f"Failed to load documents: {str(e)}"
        )

    # =========================
    # DASHBOARD
    # =========================
    if page == "Dashboard":

        st.title("Dashboard")

        total_documents = len(documents)

        approved_count = len([
            doc for doc in documents
            if doc.get("workflow_status") == "approved"
        ])

        pending_count = len([
            doc for doc in documents
            if doc.get("workflow_status") == "pending_review"
        ])

        rejected_count = len([
            doc for doc in documents
            if doc.get("workflow_status") == "rejected"
        ])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Documents",
            total_documents
        )

        col2.metric(
            "Approved",
            approved_count
        )

        col3.metric(
            "Pending Review",
            pending_count
        )

        col4.metric(
            "Rejected",
            rejected_count
        )

        st.divider()

        st.subheader("Recent Documents")

        if documents:

            table_data = []

            for doc in documents:

                table_data.append({
                    "ID": doc["id"],
                    "Filename": doc["filename"],
                    "Workflow": doc["workflow_status"],
                    "Reason": doc["workflow_reason"],
                    "Created At": doc["created_at"]
                })

            df = pd.DataFrame(
                table_data
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info("No documents found.")

    # =========================
    # UPLOAD PAGE
    # =========================
    elif page == "Upload Invoice":

        st.title("Upload Invoice")

        uploaded_file = st.file_uploader(
            "Upload Invoice",
            type=["pdf", "png", "jpg", "jpeg"]
        )

        if uploaded_file is not None:

            st.success(
                "File uploaded successfully."
            )

            if st.button(
                "Analyze Invoice",
                use_container_width=True
            ):

                with st.spinner(
                    "Processing invoice with AI..."
                ):

                    try:

                        response = analyze_document(
                            st.session_state.access_token,
                            uploaded_file
                        )

                        if response.status_code == 200:

                            data = response.json()

                            st.success(
                                "Invoice processed successfully."
                            )

                            workflow = data.get(
                                "workflow",
                                {}
                            )

                            st.subheader(
                                "Workflow Decision"
                            )

                            st.json(workflow)

                            extracted_data = data.get(
                                "extracted_data",
                                {}
                            )

                            st.subheader(
                                "Extracted Data"
                            )

                            extracted_table = []

                            for key, value in extracted_data.items():

                                extracted_table.append({
                                    "Field": key,
                                    "Value": str(value)
                                })

                            df = pd.DataFrame(
                                extracted_table
                            )

                            st.dataframe(
                                df,
                                use_container_width=True
                            )

                        else:

                            st.error(
                                f"Failed to process invoice. Status Code: {response.status_code}"
                            )

                            try:

                                st.json(
                                    response.json()
                                )

                            except Exception:

                                st.text(
                                    response.text
                                )

                    except Exception as e:

                        st.error(
                            f"Connection Error: {str(e)}"
                        )

    # =========================
    # DOCUMENTS
    # =========================
    elif page == "Documents":

        st.title("Documents")

        if documents:

            table_data = []

            for doc in documents:

                extracted_data = {}

                try:

                    extracted_data = json.loads(
                        doc["extracted_data"]
                    )

                except Exception:
                    pass

                vendor = extracted_data.get(
                    "vendor_name"
                )

                invoice_id = extracted_data.get(
                    "invoice_id"
                )

                invoice_date = extracted_data.get(
                    "invoice_date"
                )

                workflow = doc.get(
                    "workflow_status",
                    "pending"
                )

                if workflow == "approved":

                    workflow_badge = (
                        "🟢 Approved"
                    )

                elif workflow == "pending_review":

                    workflow_badge = (
                        "🟡 Pending Review"
                    )

                elif workflow == "rejected":

                    workflow_badge = (
                        "🔴 Rejected"
                    )

                else:

                    workflow_badge = workflow

                table_data.append({

                    "Vendor": vendor,

                    "Invoice ID": invoice_id,

                    "Date": invoice_date,

                    "Workflow": workflow_badge,

                    "Reason": doc.get(
                        "workflow_reason",
                        "-"
                    )
                })

            df = pd.DataFrame(
                table_data
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No documents found.")