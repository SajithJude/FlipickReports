import streamlit 
import openai
import os

openai.api_key = os.getenv("API_KEY")




# typeques= st.selectbox("Select the type of questions you want to generate",['essay','mcq'])
source = st.text_input("Input the source URL of the content")
number = st.slider('Number of questions', 0, 5, 1)
total_marks = st.number_input('Marks per question')
essay = st.button("Generate Essay")
grade = st.button("Grade essay")


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
    st.write(questions)


