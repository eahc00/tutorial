import csv
import os


tags = [
    "-",
    "AFW_B",
    "AFW_I",
    "ANM_B",
    "ANM_I",
    "CVL_B",
    "CVL_I",
    "DAT_B",
    "DAT_I",
    "EVT_B",
    "EVT_I",
    "FLD_B",
    "FLD_I",
    "LOC_B",
    "LOC_I",
    "MAT_B",
    "MAT_I",
    "NUM_B",
    "NUM_I",
    "ORG_B",
    "ORG_I",
    "PER_B",
    "PER_I",
    "PLT_B",
    "PLT_I",
    "TIM_B",
    "TIM_I",
    "TRM_B",
    "TRM_I",
]

label2idx = {label: idx for idx, label in enumerate(tags)}
idx2label = {idx: label for idx, label in enumerate(tags)}


def results_out(words, predicted_tags):
    tagged_words = []
    for word, predicted_tag in zip(words, predicted_tags):
        if predicted_tag != "-":
            tagged_word = f"[{word}:{predicted_tag.split('_')[0]}]"
            tagged_words.append(tagged_word)
        else:
            tagged_words.append(word)

    return " ".join(tagged_words)


def write_csv(row, csv_path="./test_output.csv"):
    file_exists = os.path.exists(csv_path)
    header = ["sentence", "reference", "prediction", "F1"]

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists and header is not None:
            writer.writerow(header)

        writer.writerow(row)
