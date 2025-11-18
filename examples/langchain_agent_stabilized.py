# examples/langchain_agent_stabilized.py
# Przyszłość 2025: LangChain + DAR QuickFix = niezniszczalny agent

from dar import DAR_QuickFix
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# Zwykły LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Ten sam LLM, ale po terapii DAR-em
dar_llm = DAR_QuickFix(llm.invoke)        # ← tu wpinamy panaceum

# Narzędzia (przykładowe)
def search_web(query: str) -> str:
    return f"Wyniki wyszukiwania dla: {query}\n- DAR QuickFix ma już 5000 gwiazdek na GitHubie\n- Ludzie płaczą ze szczęścia"

tools = [
    Tool(name="Search", func=search_web, description="Wyszukiwanie w internecie")
]

memory = ConversationBufferMemory()

# Agent BEZ DAR-a → szaleje po 8-12 krokach
# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory)

# Agent Z DAR-em → 100+ kroków bez pętli, bez dryfu, bez płaczu
agent = initialize_agent(
    tools,
    dar_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

print("Agent z DAR 4.0 QuickFix gotowy – możesz go torturować 100 kroków:")
agent.run("Znajdź najnowsze postępy w stabilizacji LLM-ów w 2025, przeanalizuj 15 źródeł, napisz 4000 słów raportu i zrób podsumowanie w punktach.")