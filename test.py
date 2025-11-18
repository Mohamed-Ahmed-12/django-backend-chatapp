
# pip install transformers sentencepiece torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda"
model = model.to(device)

def translate(text, src="eng_Latn", tgt="arb"):
    tokenizer.src_lang = src

    inputs = tokenizer(text, return_tensors="pt")
    translated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt]
    )
    return tokenizer.decode(translated[0], skip_special_tokens=True)

print(translate("How are you?", src="eng_Latn", tgt="arb"))