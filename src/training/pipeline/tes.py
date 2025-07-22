from shared.utils.preprocessing import normalize_text
from feature_engineering import score_of_the_match_between_two_texts


# Teste com seu exemplo
job = normalize_text("Job description*:\n\n- Prospecção de sellers para Hapvida\n- Negociação de condições comerciais (comissão) e contrato\n- Gestão de entrada do seller nos sistemas Hapvida (Vtex, SAP, Pagarme)\n- Analise concorrente e definição de condições comerciais (promoções, descontos, cupons)\n- Configuração da Vtex (marcas, categorias, condições comerciais)\n- Acompanhamento de performance (funil, vendas, serviço de entrega do seller, atendimento)\n- Acompanhamento do resultado financeiro (receita, despesas e resultados)\n\n*Pré-Requisitos*:\n\n- Nível superior completo,\n- Experiência de ao menos 5 anos com plataforma de ecommerce, em especial VTEX,\n\n*Perfil comportamental*:\n\n- Criativo\n- Proativo\n- Empático\n- Auto-organizado\n- Resiliente\n- Colaborativo")
cv = normalize_text("commerce consultant problem solverecommerce consultant problem solver "
      "ecossistemas ecommerce mkt digitalecossistemas ecommerce mkt digital 2018 momento 4 anos 5 meses")

score = score_of_the_match_between_two_texts(job, cv)
print(f"Score de similaridade: {score:.2f}")