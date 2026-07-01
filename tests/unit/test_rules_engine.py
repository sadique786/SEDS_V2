from decision.rules_engine import (RulesEngine)

engine = RulesEngine()

print(engine.validate_detection(0.92))

print(engine.validate_detection(0.40))
