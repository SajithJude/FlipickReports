import streamlit as st 
import openai
import os

openai.api_key = os.getenv("API_KEY")




# typeques= st.selectbox("Select the type of questions you want to generate",['essay','mcq'])
source = st.text_input("Input the source URL of the content")
number = st.slider('Number of questions', 0, 5, 1)
total_marks = st.number_input('Marks per question')
essay = st.button("Generate Essay Questions")
# grade = st.button("Grade essay")


if essay:
    inut = "Generate " + str(number) + " essay questions with answers,  the marks per question should be " + str(total_marks) + " and the answers should contain the marking criteria divided accordingly, Use the content in the following url as a knowledge base to generate the questions : " + str(source) 
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inut,
        temperature=0.56,
        max_tokens=2100,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    questions = response.choices[0].text.strip()
    st.code(questions, language=None)


# typeques= st.selectbox("Select the type of questions you want to generate",['essay','mcq'])
scheme = st.text_area("Paste the marking scheme here")
answers = st.text_area("Paste the answers given by student here")
result = st.button("Grade the student")
# grade = st.button("Grade result")


if result:
    promp = "Use the criteria in the given marking scheme, and grade the answers given by the student according to the scheme, list down the areas the student is weak based on the grades .\n Marking scheme : " + str(scheme) +"\n" + "Student answers :" +"\n"+  str(answers)
    outs = openai.Completion.create(
        model="text-davinci-003",
        prompt=promp,
        temperature=0.56,
        max_tokens=2100,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    grading = outs.choices[0].text.strip()
    st.write(grading)



