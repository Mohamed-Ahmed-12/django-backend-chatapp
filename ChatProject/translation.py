import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def translate(text, src="eng_Latn", tgt="arb_Arab"):
    tokenizer.src_lang = src
    inputs = tokenizer(text, return_tensors="pt").to(device)
    translated = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt)
    )
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# print(translate("How are you?", src="eng_Latn", tgt="arb_Arab"))