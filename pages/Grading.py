import streamlit as st 
import openai
import os

openai.api_key = os.getenv("API_KEY")




# typeques= st.selectbox("Select the type of questions you want to generate",['essay','mcq'])
scheme = st.text_area("Paste the marking scheme here")
answers = st.text_area("Paste the answers given by student here")
result = st.button("Grade the student")
# grade = st.button("Grade result")


if result:
    inut = "Use the criteria in the given marking scheme, and grade the answers given by the student according to the scheme, list down the areas the student is weak based on the grades .\n Marking scheme : " + str(scheme) +"\n" + "Student answers :" +"\n"+  str(answers)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inut,
        temperature=0.56,
        max_tokens=2100,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    grading = response.choices[0].text.strip()
    st.write(grading)


