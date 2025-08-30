from transform import transform  

def validate(df):
    # 1) Tem linhas?
    assert len(df) > 0, "DataFrame vazio"

    # 2) Tem as colunas essenciais?
    for c in ['id','title','author','score','time']:
        assert c in df.columns, f"Coluna em falta: {c}"

    # 3) Os scores são >= 0?
    assert df['score'].ge(0).all(), "Score negativo encontrado"

    # 4) Percentagem de títulos vazios
    null_titles = df['title'].isna().mean()
    assert null_titles < 0.10, f"Demasiados títulos nulos: {null_titles:.1%}"

if __name__ == "__main__":
    df = transform()
    validate(df)
    print("Qualidade: OK ✅")