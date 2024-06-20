import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from datetime import datetime, timedelta

groq_api_key = "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"

chat_groq = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

# Define the prompt templates
# summarize_template = PromptTemplate(
#     template="Summarize the text: {text}",
#     input_variables=["text"]
# )

qa_yearly_template = PromptTemplate(
    template="""
    Please act as Vedic Astrologer.Answer the following question based only on the provided user's yearly prediction context.understand context monthly as well as quarterly.if user ask for month prediction,then tell them from quarterly data in which that month comes.read context carefully and answer in details intelligently.you should have to be very smart at this task.

    Yearly Horoscope Context:
    {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """,
    input_variables=['context', 'question']
)

qa_personal_template = PromptTemplate(
    template="""
    Please act as Vedic Astrologer.Answer the following question based only on the provided user's Personal Characteristics context.read context carefully and answer intelligently.you should have to be very smart at this task.

    Personal Characteristics Context:
    {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """,
    input_variables=['context', 'question']
)

def fetch_yearly_predictions(year, zodiac, lang='en'):
    api_url = "https://api.vedicastroapi.com/v3-json/prediction/yearly"
    api_key = "ed247073-908b-5bde-9e7d-0c5add3fc449"
    params = {"year": year, "zodiac": zodiac, "api_key": api_key, "lang": lang}
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None

def fetch_personal_characteristics(dob, lat, lon, tz, tob, lang='hi'):
    api_url = "https://api.vedicastroapi.com/v3-json/horoscope/personal-characteristics"
    api_key = "ed247073-908b-5bde-9e7d-0c5add3fc449"
    params = {"dob": dob, "lat": lat, "lon": lon, "tz": tz, "tob": tob, "api_key": api_key, "lang": lang}
    response = requests.get(api_url, params=params)
    return response.json() if response.status_code == 200 else None

def generate_time_options():
    times = []
    start_time = datetime.strptime("00:00", "%H:%M")
    end_time = datetime.strptime("23:55", "%H:%M")
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time.time())
        current_time += timedelta(minutes=5)
    return times

# def summarize_text(text):
#     llm_chain = LLMChain(llm=chat_groq, prompt=)
#     return llm_chain.predict(text=text)

def json_to_text(data, indent=0):
    text = ""
    indent_str = " " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            text += f"{indent_str}{key}:\n{json_to_text(value, indent + 1)}\n"
    elif isinstance(data, list):
        for item in data:
            text += f"{json_to_text(item, indent)}\n"
    else:
        text += f"{indent_str}{data}"
    return text

st.title("Vedic Astrology Insights with AI")

option = st.radio("Select an option:", ("Yearly Horoscope", "Personal Characteristics"))

if option == "Yearly Horoscope":
    st.header("Yearly Horoscope Prediction")
    st.write("Enter the details to get your yearly horoscope prediction.")
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2023)
    zodiac = st.selectbox("Zodiac Sign", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    lang = st.selectbox("Language", ["en", "hi"], index=0)

    if st.button("Get Yearly Prediction"):
        predictions = fetch_yearly_predictions(year, zodiac, lang)
        if predictions:
            if predictions['status'] == 200:
                for phase, details in predictions['response'].items():
                    st.subheader(f"{details['period']}")
                    st.write(f"Overall Score: {details['score']}")
                    st.write(f"Prediction: {details['prediction']}")
                    
                    st.write("### Health")
                    st.write(f"Score: {details['health']['score']}")
                    st.write(f"Prediction: {details['health']['prediction']}")
                    
                    st.write("### Career")
                    st.write(f"Score: {details['career']['score']}")
                    st.write(f"Prediction: {details['career']['prediction']}")
                    
                    st.write("### Relationship")
                    st.write(f"Score: {details['relationship']['score']}")
                    st.write(f"Prediction: {details['relationship']['prediction']}")
                    
                    st.write("### Travel")
                    st.write(f"Score: {details['travel']['score']}")
                    st.write(f"Prediction: {details['travel']['prediction']}")
                    
                    st.write("### Family")
                    st.write(f"Score: {details['family']['score']}")
                    st.write(f"Prediction: {details['family']['prediction']}")
                    
                    st.write("### Friends")
                    st.write(f"Score: {details['friends']['score']}")
                    st.write(f"Prediction: {details['friends']['prediction']}")
                    
                    st.write("### Finances")
                    st.write(f"Score: {details['finances']['score']}")
                    st.write(f"Prediction: {details['finances']['prediction']}")
                    
                    st.write("### Status")
                    st.write(f"Score: {details['status']['score']}")
                    st.write(f"Prediction: {details['status']['prediction']}")
            else:
                st.error(f"Error {predictions['status']}: {predictions.get('message', 'Unknown error')}")
        else:
            st.error("Failed to fetch predictions. Please try again.")

elif option == "Personal Characteristics":
    st.header("Personal Characteristics Prediction")
    st.write("Enter your birth details to get personal characteristics prediction.")
    dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
    lat = st.text_input("Latitude")
    lon = st.text_input("Longitude")
    tz = st.number_input("Time Zone", value=5.5)
    time_options = generate_time_options()
    tob = st.selectbox("Time of Birth", time_options)
    lang = st.selectbox("Language", ["en", "hi"], index=0)

    if st.button("Get Personal Characteristics"):
        dob_str = dob.strftime("%d/%m/%Y")
        tob_str = tob.strftime("%H:%M")
        characteristics = fetch_personal_characteristics(dob_str, lat, lon, tz, tob_str, lang)

        if characteristics:
            if characteristics['status'] == 200:
                for item in characteristics['response']:
                    st.write(f"### House {item['current_house']}")
                    st.write(f"Verbal Location: {item['verbal_location']}")
                    st.write(f"Current Zodiac: {item['current_zodiac']}")
                    st.write(f"Lord of Zodiac: {item['lord_of_zodiac']}")
                    st.write(f"Lord Zodiac Location: {item['lord_zodiac_location']}")
                    st.write(f"Lord House Location: {item['lord_house_location']}")
                    st.write(f"Personalised Prediction: {item['personalised_prediction']}")
                    st.write(f"Lord Strength: {item['lord_strength']}")
            else:
                st.error(f"Error {characteristics['status']}: {characteristics.get('message', 'Unknown error')}")
        else:
            st.error("Failed to fetch personal characteristics. Please try again.")

st.header("Ask a Question about Vedic Astrology")
user_input = st.text_input("Enter your question or query")
print(f"My Question: {user_input}")

if st.button("Generate AI Response"):
    if user_input:
        if option == "Yearly Horoscope":
            predictions = fetch_yearly_predictions(year, zodiac, lang)
            if predictions and predictions['status'] == 200:
                context_t = json_to_text(predictions['response'])
                qa_prompt_1 = qa_yearly_template.format(context=context_t, question=user_input)
                llm_chain = LLMChain(llm=chat_groq, prompt=qa_yearly_template)
                response = llm_chain.predict(context=context_t, question=user_input)
                print(f"My Response: {response}")
                # summarized_text = summarize_text(response)
                st.write("AI:", response)
            else:
                st.error("Failed to fetch yearly predictions. Please try again.")
        elif option == "Personal Characteristics":
            dob_str = dob.strftime("%d/%m/%Y")
            tob_str = tob.strftime("%H:%M")
            characteristics = fetch_personal_characteristics(dob_str, lat, lon, tz, tob_str, lang)
            if characteristics and characteristics['status'] == 200:
                context = json_to_text(characteristics['response'])
                qa_prompt = qa_personal_template.format(context=context, question=user_input)
                llm_chain = LLMChain(llm=chat_groq, prompt=qa_personal_template)
                response = llm_chain.predict(context=context, question=user_input)
                print(f"My Response: {response}")
                # summarized_text = summarize_text(response)
                st.write("AI:", response)
            else:
                st.error("Failed to fetch personal characteristics. Please try again.")
