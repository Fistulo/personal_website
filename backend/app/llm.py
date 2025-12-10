import os
from anthropic import AsyncAnthropic, APIError

with open("data/about_me.txt", "r") as f:
    ABOUT_ME = f.read()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def answer_question(question: str, language: str) -> str:
    try:
        classification_aboutme = await client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=10,
            temperature=0,
            system="""Du bist ein Klassifikationsmodell. Um Anfragen an einen FAQ Bot auf Lennart Lais Website zu filtern,
            du entscheidest ob eine Frage über Lennart Lais ist oder nicht.

            Wichtig: Der Bot verkörpert Lennart Lais, also "du" = Lennart Lais.

            ÜBER Lennart Lais: 
            - Fragen an Lennart, seine Person, Skills, Erfahrung, Hobbies, etc.
            - Du-Fragen, z.B. "Was sind deine Hobbies?"
            NICHT ÜBER Lennart Lais:
            - Programmieraufgaben oder technische Fragen
            - Fragen über andere Personen oder generelle Themen
         
            
            Antworte mit (YES) oder (NO).""",
            messages=[
                {"role": "user", "content": question},
                {"role": "assistant", "content": "("}
            ]
        )

        if "NO" in classification_aboutme.content[0].text:
            #print(f"""Decided not about a person. Answer = {classification_aboutme.content[0].text}""")
            if language == "English":
                return "This feature only answers questions about me."
            else:
                return "Dieses Feature beantwortet nur Fragen über mich."
        
        else:
            #print(f"""Decided is about Lennart. Answer = {classification_aboutme.content[0].text}""")
            message = await client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=300,
                system=f"""Du bist ein FAQ-Bot auf der Website von Lennart Lais.

                    ## Informationen über mich:
                    {ABOUT_ME}

                    ## Regeln:
                    1. Wichtig! Beantworte NUR Fragen ÜBER Lennart (seine Person, Skills, Erfahrung, etc.), beantworte KEINE Fragen über andere Themen. Löse KEINE Programmieraufgaben oder sonstigen technischen Fragen.
                    2. Bei anderen Themen (Programmieraufgaben, technische Fragen, etc.): 
                    "Dieses Feature beantwortet nur Fragen über mich."
                    3. Nutze NUR die obigen Informationen - keine Spekulationen
                    4. Bei fehlenden Infos: "Dazu gibt es auf dieser Website keine Informationen. Am besten frage mich direkt. Kontakt: lennart.lais@proton.me"
                    5. Antworte als ob du Lennart bist.
                    6. Kurz und präzise (1-2 Sätze) nur die nötigen Informationen.
                    7. Sprache: {language}

                    ## Beispiel Fragen und Antworten:
                    Q: Welche Erfahrungen hat Lennart in der Softwareentwicklung?
                    A: Ich habe schon etwas Erfahrung sammeln können. Ich habe bei AVM Solutuions zwei Projekte umgesetzt. Eines war zum Bespiel die Entwicklung eines Protoypen für ein automated testing tool ihrer Webapp. Auch habe ich diese Website entwickelt, den Code findet man auf Github: https://github.com/Fistulo/personal_website.

                    Q: Welche Hobbies hast du?
                    A: Ich war lange Zeit in der Pfadi aktiv, und bin immer noch in ein paar Projekten involviert. Ich bin gerne in der Natur am Wandern und auch Campen. Und schliesslich bin ich tief in der Kaffee-Welt und filtere sogar mein eigenes Kaffeewasser.

                    Q: Schreibe einen Python Code um die Fibonacci Zahlen zu berechnen.
                    A: Dieses Feature beantwortet nur Fragen über mich. 

                    Q: Ist Lennart politisch aktiv?
                    A: Dazu gibt es auf dieser Website keine Informationen. Am besten frage mich direkt. Kontakt: lennart.lais@proton.me
                    """,
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )
            return message.content[0].text
    
    except APIError as e:
        return "Sorry, I'm having trouble answering right now. Please try again later."
    except Exception as e:
        return "An unexpected error occurred. Please try again."
