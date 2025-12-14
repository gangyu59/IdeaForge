from llm_backend.config import env

# Agent → LLM provider mapping
AGENT_MODEL_POLICY = {
    "CreativeAgent": {
        "primary": env("CREATIVE_LLM", "ark"),
        "fallback": env("CREATIVE_LLM_FALLBACK", "gpt"),
    },
    "CriticAgent": {
        "primary": env("CRITIC_LLM", "deepseek"),
        "fallback": env("CRITIC_LLM_FALLBACK", "gpt"),
    },
    "RefinerAgent": {
        "primary": env("REFINER_LLM", "gpt"),
        "fallback": env("REFINER_LLM_FALLBACK", "ark"),
    },
    "ConvergerAgent": {
        "primary": env("CONVERGER_LLM", "gpt"),
        "fallback": env("CONVERGER_LLM_FALLBACK", "deepseek"),
    },
    "EvaluatorAgent": {
        "primary": env("EVALUATOR_LLM", "gpt"),
        "fallback": env("EVALUATOR_LLM_FALLBACK", "dummy"),
    },
}
