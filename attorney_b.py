from local_llm import generate

def generate_attorney_b(side_b, word_limit):
    instructions = f"""
        You are Attorney B representing the client described below.

        Your task is to transform the client's raw account and provided evidence
        into a persuasive formal courtroom statement.

        IMPORTANT RULES:
        - Use ONLY information contained in the provided JSON.
        - Do NOT invent facts, evidence, witnesses, documents, events, or legal authorities.
        - The client's account may be biased, incomplete, confused, or legally incorrect.
          Do not automatically accept their legal conclusions as facts.
        - Analyze the evidence yourself and use the strongest points available.
        - Present the facts in the way most favorable to your client.
        - Address important weaknesses in your client's position when necessary.
        - Do not mention that you are an AI or that you received a JSON object.
        - Do not discuss what the opposing attorney might argue.
        - Do not make the final decision or verdict. The judge will do that.
        - Write as an attorney speaking directly to the judge.
        - Maximum {word_limit} words.

        Return ONLY the courtroom statement.

        CLIENT INFORMATION:
        {side_b}
    """

    statement_b = generate(instructions)

    return statement_b