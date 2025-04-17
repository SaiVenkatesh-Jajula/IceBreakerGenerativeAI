import streamlit as st
from icebreaker import ice_break

st.set_page_config(page_title="Ice Breaker", layout="centered")

st.title("LinkedIn IceBreaker GenAI. Agent 🤖")

name = st.text_input("Name", placeholder="Enter Full Name")

if st.button("Check") and name:
    with st.spinner("Generating Icebreaker..."):
        summary, image_url = ice_break(name)

    if summary is None:
        st.error("❌ Sorry, unable to find the profile.\nPlease search with another full name of the person.")

    else:
        st.markdown(f"## Picture of {name}:", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <img src="{image_url}" width="150">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("## About :")
        st.write(summary.summary)

        st.markdown("## Key Facts :")
        for fact in summary.facts:
            st.markdown(f" • {fact}")




