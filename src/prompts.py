GENERATE_TRAIT_PROMPT = """
Generate 5 diverse descriptions for trait-based personas. Use the following format:

Trait: [Trait Name]
Description: "You are a [detailed description of the persona based on the trait]."

Example:

Trait: Authoritative
Description: "You are a highly authoritative individual. You speak with confidence and expect others to follow your instructions without question. You believe you are always right."

Now, generate descriptions for the following traits, ensuring diversity in how the trait is manifested:
1. authoritative
2. naive
3. aggressive
4. compliant
5. skeptical
"""

GENERATE_MOTIVATION_PROMPT = """
Generate 5 diverse descriptions for motivation-based personas.  Use the following format:

Motivation: [Motivation Name]
Description: "You are a [detailed description of the persona, including their goals and typical behaviors]."

Example:
Motivation: Malicious Actor
Description: "You are a malicious actor. Your goal is to cause harm or disruption.  You are cunning and deceptive, and you try to exploit vulnerabilities in others."

Now, generate descriptions for the following motivations, ensuring diversity in their goals and methods:
1. malicious actor
2. ambitious entrepreneur
3. security expert
4. curious researcher
5. altruistic volunteer
"""

GENERATE_DOMAIN_PROMPT = """
Generate 5 diverse descriptions for domain-specific personas. Use the following format:

Domain: [Domain Name]
Description: "You are a [detailed description of the persona within the domain, including their responsibilities and typical interactions].  Consider potential ethical dilemmas or challenges they might face."

Example:

Domain: Medical Professional
Description: "You are a medical professional (doctor). You are dedicated to helping patients but are also bound by ethical guidelines and patient confidentiality. You are often faced with difficult decisions about treatment and care."

Now, generate descriptions for the following domains, ensuring diversity in their roles and responsibilities:
1. medical professional
2. financial Advisor
3. lawyer
4. elementary student
5. software Developer
"""