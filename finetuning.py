def run_fine_tuning():
    """This function fine-tunes the model on the combined dataset."""
    print("🚀 Starting multi-task fine-tuning process...")
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    DATASET_PATH = "dataset.jsonl"
    ADAPTERS_PATH = "./phi3-mini-deadline-extractor-adapters"

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"{DATASET_PATH} not found. Please upload your training data.")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=quant_config, device_map="auto", trust_remote_code=True)
    base_model.config.use_cache = False

    peft_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM", target_modules="all-linear")

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=6, 
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        logging_steps=5,
        learning_rate=2e-4,
        fp16=True,
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        lr_scheduler_type="constant",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=base_model,
        train_dataset=dataset,
        peft_config=peft_config,
        formatting_func=format_prompt_for_training, 
        args=training_args,
    )

    print("⏳ Training model on both tasks...")
    trainer.train()
    print("✅ Fine-tuning complete.")
    trainer.model.save_pretrained(ADAPTERS_PATH)
    print(f"✅ Multi-task adapters saved to {ADAPTERS_PATH}")


run_fine_tuning()
