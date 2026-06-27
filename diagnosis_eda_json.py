import json
import pandas as pd

data = []
with open('math_logic_samples.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data, columns=['id', 'instruction', 'response'])
df.to_excel('dataset.xlsx', index=False)

def full_eda(df):
    df['response_length'] = df['response'].str.len()
    df['word_count'] = df['response'].str.split().str.len()
    
    print("=== 1. SHAPE ===")
    print(df.shape)
    
    print("\n=== 2. MISSING VALUES ===")
    print(df.isnull().sum())
    
    print("\n=== 3. DUPLICATES ===")
    print("Duplicate rows:", df.duplicated(subset=['instruction']).sum())
    print("Unique instructions:", df['instruction'].nunique())
    
    print("\n=== 4. RESPONSE LENGTH ===")
    print(df['response_length'].describe())
    
    print("\n=== 5. WORD COUNT ===")
    print(df['word_count'].describe())
    
    print("\n=== 6. LENGTH BY INSTRUCTION ===")
    print(df.groupby('instruction')['response_length'].agg(['min', 'max', 'mean', 'std']))
    
    print("\n=== 7. THEATRICAL SELF CORRECTION ===")
    for phrase in ['i made an error', 'i was wrong', 'let me correct', 'wait that is wrong']:
        count = df['response'].str.lower().str.contains(phrase).sum()
        print(f"   '{phrase}': {count}")
    
    print("\n=== 8. OVERCLAIMING ===")
    for phrase in ['we have proved', 'we proved', 'this proves', 'qed']:
        count = df['response'].str.lower().str.contains(phrase).sum()
        print(f"   '{phrase}': {count}")
    
    print("\n=== 9. PROVE TYPE INSTRUCTIONS ===")
    df['is_prove_type'] = df['instruction'].str.lower().str.contains('prove')
    print(df[df['is_prove_type']][['id', 'instruction', 'response_length']])
    
    print("\n=== 10. MARKDOWN USAGE ===")
    df['has_markdown'] = df['response'].str.contains('##')
    print(df['has_markdown'].value_counts())
    
    print("\n=== 11. UNIQUE WORDS PER RESPONSE ===")
    df['unique_words'] = df['response'].apply(lambda x: len(set(x.lower().split())))
    print(df['unique_words'].describe())
    
    print("\n=== 12. RESPONSE START PATTERNS ===")
    df['response_start'] = df['response'].str[:80]
    print(df['response_start'].value_counts())
full_eda(df)


