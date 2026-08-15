from vector_db import search_precedent, store_case
from ollama import chat

model = "qwen3:8b"

def judge_case(attorney_statement_a, attorney_statement_b):
    arguments = f"""
        ATTORNEY A:
        {attorney_statement_a}

        ATTORNEY B:
        {attorney_statement_b}
    """

    # Using normal buffer memory - every piece of information is important
    conversation = [
        {
            "role": "user",
            "content": f"""
                You are the judge in a civil case.
                
                You have been presented with statements from two attorneys.
                
                You have access to a tool called search_precedent. This tool retrieves
                previously judged cases that are similar to the current case.
                
                A case may be considered complex when, for example:
                
                - the arguments involve multiple conflicting issues;
                - the facts are ambiguous or difficult to interpret;
                - both sides present substantial and competing arguments;
                - the correct interpretation of the facts is difficult to determine;
                - several interacting issues make the decision less clear.
                
                You do NOT need to use the tool for every case. Use it when you believe that
                retrieving similar previously judged cases could meaningfully help you
                evaluate a sufficiently complex or difficult case.
                
                There are exactly TWO possible workflows:
                
                WORKFLOW 1 — USE PRECEDENT:
                
                If you choose Workflow 1, your response at this stage must consist only of
                the search_precedent tool call. Do not provide analysis, reasoning, or a
                verdict until after the tool results are returned.
                
                If you decide that precedent would be useful:
                
                1. Call search_precedent.
                2. Do not issue a verdict before calling the tool.
                3. Wait for the tool to return the retrieved cases.
                4. After receiving the tool results, evaluate them together with the
                   attorneys' arguments.
                5. Then issue the final verdict.
                
                WORKFLOW 2 — DO NOT USE PRECEDENT:
                
                If you decide that precedent would not meaningfully help:
                
                1. Do not call search_precedent.
                2. Immediately issue the final verdict based on the attorneys' arguments.
                
                Do not perform both workflows.
                
                IMPORTANT:
                
                - Base your decision only on the information presented.
                - Do not invent facts, evidence, witnesses, documents, or legal authorities.
                - The attorneys may present biased, incomplete, or weak arguments.
                - Do not assume that a retrieved case is legally relevant merely because it
                  is similar in wording or subject matter.
                - Precedent is informational only and must not automatically determine the
                  verdict.
                - Evaluate the strength, relevance, consistency, and persuasiveness of both
                  attorneys' arguments.
                - Do not favor either attorney automatically.
                - If precedent is retrieved, critically evaluate whether it is actually
                  relevant to the current case.
                - Give your reasoning in formal courtroom style.
                - At the very end of your final verdict, write EXACTLY ONE of:
                
                WINNER: A
                
                or
                
                WINNER: B
                
                CASE:
                
                {arguments}
                """
        }
    ]

    precedent_used = False

    response = chat(
        model=model,
        messages=conversation,
        tools=[search_precedent],
        think=True
    )

    if response.message.tool_calls:

        for tool_call in response.message.tool_calls:

            if tool_call.function.name == "search_precedent":
                precedent_used = True

                result = search_precedent(**tool_call.function.arguments)

                conversation.append({
                    "role": "assistant",
                    "content": response.message.content,
                    "tool_calls": response.message.tool_calls
                })

                conversation.append({
                    "role": "tool",
                    "tool_name": "search_precedent",
                    "content": str(result)
                })

        # Give the judge the retrieved precedent and let it finish the decision
        final_response = chat(
            model=model,
            messages=conversation,
            think=True
        )

        verdict = final_response.message.content.strip()

    else:
        # No precedent was requested, so the first response is the final verdict
        verdict = response.message.content.strip()

    summary_prompt = f"""
        Create a concise summary of this judged case for a precedent database.
    
        Include:
    
        - the nature of the dispute
        - the important facts presented by the attorneys
        - the main argument made by Attorney A
        - the main argument made by Attorney B
        - any relevant precedent that was retrieved
        - the final verdict
    
        Use ONLY information contained in the material below.
    
        Do not invent facts, evidence, arguments, or legal authorities.
    
        ATTORNEY A:
        {attorney_statement_a}
    
        ATTORNEY B:
        {attorney_statement_b}
    
        JUDGE'S VERDICT:
        {verdict}
    
        Return ONLY the summary.
        """

    summary_response = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": summary_prompt
            }
        ]
    )

    store_case(
        case_summary=summary_response.message.content.strip()
    )

    # Extract winner
    if "WINNER: A" in verdict:
        winner = "A"
    elif "WINNER: B" in verdict:
        winner = "B"
    else:
        winner = "UNKNOWN"

    return {
        "winner": winner,
        "verdict": verdict,
        "precedent_used": precedent_used
    }