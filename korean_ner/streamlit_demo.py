import streamlit as st
import pandas as pd
from tutorial.korean_ner.ner_bert_inference import NERBERTInference
from tutorial.korean_ner.utils import results_out

st.markdown("### Example")
with st.container(border=True):
    result_df = pd.read_csv("/home/eahc00/tutorial/korean_ner/result_csv.csv")
    example = result_df[:5].drop(result_df.columns[0], axis=1)

    styled_df = example.style.set_properties(**{"text-align": "center"}).format(
        {"f1": "{:.2f}"}
    )  # f1 열만 소수점 4자리
    st.dataframe(styled_df, row_height=70)

st.markdown("---")  # 구분선
st.markdown(" ")
st.markdown("### input")

input_sentence = st.text_input(
    "Enter text for NER tagging",
)

model_name = "bert-base-multilingual-cased"
num_labels = 29
ner_bert_inference = NERBERTInference(model_name, num_labels)
words, tags = ner_bert_inference.ner_inference(input_sentence)
result = results_out(words, tags)

st.markdown("---")
st.markdown(" ")
st.markdown("### output")

with st.container(border=True):
    st.write("**" + result + "**")
